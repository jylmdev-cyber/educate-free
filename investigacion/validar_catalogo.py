"""Controles reproducibles de estructura, coherencia y trazabilidad; no valida matrícula."""
import json
import re
from collections import Counter
from datetime import date, datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'investigacion'
EVIDENCE=ROOT/'.pallaquino/evidence/EDU-001'
data=json.loads((OUT/'catalogo.json').read_text(encoding='utf-8'))
rows=data['courses']
markdown=(OUT/'catalogo.md').read_text(encoding='utf-8')
http=json.loads((EVIDENCE/'fichas_http.json').read_text(encoding='utf-8'))['records']
audit=json.loads((OUT/'fuentes.json').read_text(encoding='utf-8'))
UNKNOWN='No confirmado en la fuente oficial'
errors=[]
checks=[]


def check(name, condition, detail=''):
    checks.append(dict(check=name,result='PASS' if condition else 'FAIL',detail=detail))
    if not condition:
        errors.append(name+': '+detail)


check('Fecha de corte explícita', data['as_of']=='2026-10-07' and data['timezone']=='America/Lima')
counts=Counter(r['group'] for r in rows)
check('Objetivos cuantitativos según alcance declarado',counts['A']>=20 and counts['B']>=30 and counts['C']>=30,str(dict(counts)))
check('IDs únicos',len({r['id'] for r in rows})==len(rows))
check('Cursos no duplicados por proveedor y título',len({(r['institution'].casefold(),r['title'].casefold()) for r in rows})==len(rows))
check('Definición honesta del grupo B','no significa 30' in data['group_definitions']['B'])
fields=['id','title','area','institution','location','modality','duration','course_price','certificate','certificate_price','registration','start','url','category','requirements','sources','peru_access_basis']
check('Campos requeridos completos',all(all(r.get(f) for f in fields) for r in rows))
allowed_categories={'Curso y certificado GRATIS','Curso GRATIS / certificado de pago','Becado','Convocatoria gratuita','Auditoría gratuita','Freemium','Pago'}
check('Categorías válidas',all(r['category'] in allowed_categories for r in rows))
check('Estados válidos',all(r['registration'] in {'ABIERTA','PRÓXIMAMENTE','PERMANENTE','CERRADA'} for r in rows))
check('Todos los cursos incluidos son virtuales',all(r['modality'].startswith('Virtual') for r in rows))
check('Sin plazo cerrado presentado activo',all(not r['closing'] or date.fromisoformat(r['closing'])>=date.fromisoformat(data['as_of']) or r['registration']=='CERRADA' for r in rows))
check('Gratuidad de credencial consistente',all(r['certificate_price']=='GRATIS' and r['certificate']!=UNKNOWN for r in rows if r['category']=='Curso y certificado GRATIS'))
check('Curso gratuito con credencial pagada explícita',all(r['certificate_price'] not in {'GRATIS',UNKNOWN} for r in rows if r['category']=='Curso GRATIS / certificado de pago'))
check('No hay sustitutos vagos para desconocidos',not any(str(r[f]).strip().lower() in {'n/a','por confirmar','desconocido','no informado','sin información','-','?'} for r in rows for f in fields if f!='sources'))
trusted={'capacitacionlaboral.trabajo.gob.pe','cursosgratuitos.uni.edu.pe','www.kaggle.com','cs50.harvard.edu','www.netacad.com','training.linuxfoundation.org','aws.amazon.com','www.databricks.com','learn.oracle.com','blogs.oracle.com','www.life-global.org','www.freecodecamp.org','opensource.freecodecamp.org','skillshop.withgoogle.com','support.google.com','learn.microsoft.com','www.linkedin.com','github.com','learn.github.com','www.redhat.com','training.fortinet.com','helpdesk.training.fortinet.com','knowledge.iadb.org','app.santanderopenacademy.com','www.santanderopenacademy.com','www3.congreso.gob.pe','learning.sap.com','trailhead.salesforce.com','skillsbuild.org'}
check('Enlaces y políticas de dominios oficiales permitidos',all(urlsplit(u).scheme=='https' and urlsplit(u).hostname in trusted for r in rows for u in r['sources']))
http_by_url={r['url']:r for r in http}
check('Cada enlace principal respondió HTTP 200',all(http_by_url.get(r['url'],{}).get('status')==200 for r in rows),'HTTP 200 no demuestra matrícula; se informa separadamente contenido dinámico.')
check('Cada fuente tiene registro de lectura HTTP',all(u in http_by_url for r in rows for u in r['sources']))
check('Lecturas en fecha de corte',all(r['consulted_at'].startswith(data['as_of']) for r in http))
check('Respuestas exitosas con SHA256',all(re.fullmatch('[0-9a-f]{64}',r.get('sha256','')) for r in http if r['status']==200))
mtpe_urls={r['url'] for r in rows if r['group'] in 'AB' and 'capacitacionlaboral' in r['url']}
check('50 fichas MTPE con botón de curso',len(mtpe_urls)==50 and all(any(x['label']=='Empezar curso' for x in http_by_url[u].get('enrollment_links',[])) for u in mtpe_urls))
ids={r['id'] for r in rows}
check('TOP contiene 15 IDs distintos y existentes',len(data['top15'])==15 and len({r['course_id'] for r in data['top15']})==15 and all(r['course_id'] in ids for r in data['top15']))
check('TOP incluye justificación, aprendizaje, CV y nivel',all(all(r.get(f) for f in ['why','learn','cv','level']) for r in data['top15']))
check('Cuatro rutas con cursos existentes',len(data['routes'])==4 and all(cid in ids for route in data['routes'] for step in route['steps'] for cid in step['course_ids']))
check('Rutas ordenadas',all([s['order'] for s in r['steps']]==list(range(1,len(r['steps'])+1)) for r in data['routes']))
table_rows=[l for l in markdown.splitlines() if re.match(r'\| [ABC]\d\d \|',l)]
check('Tablas con 13 columnas y totalidad de registros',len(table_rows)==len(rows) and all(len(l.split('|'))-2==13 for l in table_rows))
check('Orden de categorías dentro de cada tabla',all([next(i for i,r in enumerate(table_rows) if r.startswith('| '+row['id']+' |')) for row in sorted((r for r in rows if r['group']==g),key=lambda r:({'Curso y certificado GRATIS':0,'Curso GRATIS / certificado de pago':1,'Convocatoria gratuita':3,'Freemium':5}[r['category']],r['id']))]==sorted(next(i for i,r in enumerate(table_rows) if r.startswith('| '+row['id']+' |')) for row in rows if row['group']==g) for g in 'ABC'))
check('Secciones solicitadas y límites visibles',all(t in markdown for t in ['TOP 15 CURSOS QUE MÁS RECOMIENDO','OPORTUNIDADES QUE CONVIENE VIGILAR','RUTA 1','RUTA 2','RUTA 3','RUTA 4','No se realizó matrícula','exhaustividad total no demostrada']))
check('Búsqueda social documentada',all(any(any(domain in json.dumps(c['args']) for domain in domains) for c in audit['calls']) for domains in [('linkedin.com',),('facebook.com',),('instagram.com',),('twitter.com','x.com')]))
check('Registro de búsquedas no vacío',len(audit['calls'])>=50)
warnings=dict(unknown_duration=sum(UNKNOWN in r['duration'] for r in rows),
              unknown_certificate=sum(UNKNOWN in r['certificate'] for r in rows),
              unknown_certificate_price=sum(UNKNOWN in r['certificate_price'] for r in rows),
              sparse_public_pages=[r['url'] for r in http if r.get('visible_chars',0)<100],
              http_failures=[dict(url=r['url'],status=r['status'],error=r.get('error')) for r in http if r['status']!=200],
              enrollment_tested=False,all_requested_institutions_individually_verified=False,
              note='Estos límites no se convierten en comprobaciones de matrícula o costo desconocido. La revisión informativa requiere lectura humana de las fuentes.')
result=dict(task='EDU-001',command='python investigacion/validar_catalogo.py',
            timestamp=datetime.now(timezone.utc).isoformat(),agent='codex-root',
            exit_code=1 if errors else 0,result='FAIL' if errors else 'PASS',
            courses=len(rows),groups=dict(counts),checks=checks,errors=errors,warnings=warnings)
(EVIDENCE/'validacion_catalogo.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(result=result['result'],checks=len(checks),errors=errors,courses=len(rows),groups=dict(counts),warnings={k:v for k,v in warnings.items() if not isinstance(v,list)}),ensure_ascii=False))
raise SystemExit(result['exit_code'])
