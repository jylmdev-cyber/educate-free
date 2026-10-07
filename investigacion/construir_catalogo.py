"""Construye el catálogo curado; no matricula, no instala paquetes, no consulta APIs privadas."""
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'investigacion'
UNKNOWN = 'No confirmado en la fuente oficial'
DATE = '2026-10-07'
FREE = 'Curso y certificado GRATIS'
PAID_CERT = 'Curso GRATIS / certificado de pago'
CALL = 'Convocatoria gratuita'
FREEMIUM = 'Freemium'
FAQ = 'https://capacitacionlaboral.trabajo.gob.pe/preguntas-frecuentes/'
MTPE = 'https://capacitacionlaboral.trabajo.gob.pe/cursos/'
courses = []


def add(group, title, area, institution, country, url, duration=UNKNOWN,
        certificate=UNKNOWN, certificate_price=UNKNOWN, category=CALL,
        status='PERMANENTE', start=UNKNOWN, requirements='Cuenta gratuita; conexión a Internet.',
        notes='', sources=(), closing=None, evidence='Ficha pública y política del proveedor',
        level='Básico', peru_basis='Oferta virtual global; acceso desde Perú inferido de su alcance público, sin matrícula individual probada.'):
    row = dict(id=f'{group}{sum(c["group"] == group for c in courses) + 1:02}',
               group=group, title=title, area=area, institution=institution,
               location=country, modality='Virtual, a tu ritmo', duration=duration,
               course_price='GRATIS', certificate=certificate,
               certificate_price=certificate_price, registration=status,
               start=start, url=url, category=category, requirements=requirements,
               notes=notes, sources=list(dict.fromkeys([url, *sources])),
               closing=closing, consulted_on=DATE, evidence=evidence,
               level=level, peru_access_basis=peru_basis)
    courses.append(row)
    return row


mtpe = json.loads((ROOT / '.pallaquino/evidence/EDU-001/mtpe_catalogo.json').read_text(encoding='utf-8'))['courses']


def local(group, title, area):
    matches = [r for r in mtpe if r['title'] == title]
    if not matches:
        raise ValueError(f'No existe el título exacto en catálogo MTPE: {title}')
    # Dos versiones de Excel con mismo título: conservar la de mayor duración, sin sumar ambas.
    card = max(matches, key=lambda r: int(re.search(r'\d+', r['duration'])[0]))
    issuer = card['certifier']
    if group == 'A':
        assert issuer == 'Fundación Romero'
    row = add(group, card['title'], area,
              f'{issuer} / CAPACÍTA-T (MTPE)',
              'Lima, Perú' if group == 'A' else 'Perú, alcance nacional (MTPE sede Lima)',
              card['url'], card['duration'], 'Certificado de curso', 'GRATIS', FREE,
              requirements='Ingresar desde CAPACÍTA-T y crear cuenta en la plataforma aliada según su formulario.',
              sources=(MTPE, FAQ), evidence='Tarjeta del catálogo oficial + ficha individual + FAQ MTPE',
              peru_basis='Programa nacional del MTPE: cursos virtuales para participantes en Perú.')
    if issuer in ('Cisco', 'Huawei del Perú'):
        row['notes'] = 'Certificado de formación según oferta MTPE; no acredita que el examen profesional Cisco/Huawei sea gratis.'
    if title == 'Fundamentos de IA con IBM SkillsBuild':
        row['certificate'] = 'Certificado anunciado; emisor ' + UNKNOWN
        row['notes'] = 'El título menciona IBM, pero la tarjeta MTPE dice «Certifica: Cisco». Discrepancia conservada; confirmar emisor al matricularse.'
    return row


A = [
    ('Introducción al Power BI', 'BI / Power BI'),
    ('Análisis de datos con Power BI', 'Análisis de datos / BI'),
    ('Excel intermedio', 'Excel'),
    ('Excel básico', 'Excel / ofimática'),
    ('Plan de negocios', 'Emprendimiento / gestión'),
    ('Finanzas para emprender', 'Finanzas'),
    ('Logística 360°. Claves para una gestión moderna y eficiente', 'Logística'),
    ('Cómo gestionar tu equipo de trabajo', 'Gestión / liderazgo'),
    ('Comunicación asertiva', 'Habilidades blandas'),
    ('Agile mindset', 'Agile'),
    ('Estrategias ágiles para empresas', 'Agile / gestión'),
    ('Recursos humanos en épocas de transformación digital', 'RR. HH. / transformación digital'),
    ('Gestión del cambio', 'Transformación digital / gestión'),
    ('Dirección de personal', 'Liderazgo / RR. HH.'),
    ('Modelo Canvas', 'Gestión empresarial'),
    ('Plan de marketing para emprender', 'Marketing / emprendimiento'),
    ('Contabilidad de costos', 'Finanzas / costos'),
    ('Estrategias de motivación del personal', 'Liderazgo'),
    ('El rol del líder en la transformación digital', 'Liderazgo / transformación digital'),
    ('Gestión de la innovación', 'Innovación'),
]
for title, area in A:
    local('A', title, area)

UNI = 'https://cursosgratuitos.uni.edu.pe/programapit/pit-uni-2026.php'
add('A', 'Programa de Iniciación Tecnológica (PIT UNI 2026)', 'Tecnología / ofimática',
    'Universidad Nacional de Ingeniería', 'Lima, Perú', UNI,
    certificate='Certificado con nota mínima 12; constancia con 75 % de asistencia',
    certificate_price='S/50', category=PAID_CERT, status='PRÓXIMAMENTE',
    requirements='Prerregistro 12–14 oct.; matrícula 15–26 oct. 2026. Externos: correo institucional activo de universidad/instituto.',
    notes='Se contabiliza el programa una sola vez. No se inventan los títulos de sus más de 80 cursos; fecha de clases no publicada en la ficha consultada.',
    closing='2026-10-26', peru_basis='Convocatoria virtual UNI para alumnos UNI y participantes externos con correo institucional.')

B = [
    ('Fundamentos de Python 1', 'Python'),
    ('Fundamentos de Python 2', 'Python'),
    ('Desarrollo Back-End (Nivel básico)', 'Backend'),
    ('Desarrollo Front-End (Nivel básico)', 'Frontend'),
    ('Fundamentos de IA con IBM SkillsBuild', 'IA'),
    ('Introducción a la ciencia de datos', 'Ciencia de datos'),
    ('Introduction to Modern AI', 'IA'),
    ('Seguridad de terminales', 'Ciberseguridad'),
    ('Administración de amenazas cibernéticas', 'Ciberseguridad'),
    ('Defensa de la red', 'Ciberseguridad / redes'),
    ('Introducción a ciberseguridad', 'Ciberseguridad'),
    ('Conceptos básicos de redes', 'Redes'),
    ('Dispositivos de red y configuración inicial', 'Redes'),
    ('Direccionamiento de red y solución de problemas básicos', 'Redes'),
    ('Soporte y seguridad de red', 'Redes / soporte'),
    ('English for IT 1', 'Inglés para tecnología'),
    ('English for IT 2', 'Inglés para tecnología'),
    ('Curso HCIA-Datacom V1.0', 'Redes'),
    ('Curso HCIA-Cloud Computing V5.5', 'Cloud'),
    ('Comunicación de datos y tecnología de redes', 'Redes'),
    ('Búsqueda e IA', 'IA'),
    ('Gestión y análisis de datos', 'Datos'),
    ('Representación de la información y organización de los datos', 'Datos'),
    ('Conceptos básicos de la nube: desarrollo y conceptos básicos', 'Cloud'),
    ('Descripción General de la IA', 'IA'),
    ('Cloud Advanced: Arquitectura y Tecnologías', 'Cloud'),
    ('Gestión efectiva del tiempo', 'Gestión / habilidades blandas'),
    ('Inglés básico para el trabajo (nivel A1)', 'Inglés laboral'),
    ('Desarrolla tu pensamiento crítico', 'Habilidades blandas'),
    ('Competencias socioemocionales para la empleabilidad', 'Empleabilidad'),
]
for title, area in B:
    local('B', title, area)


def international(title, area, provider, url, duration=UNKNOWN, cert=UNKNOWN,
                  cert_price=UNKNOWN, category=CALL, notes='', policy=(), **kw):
    return add('C', title, area, provider, 'Internacional, virtual', url,
               duration, cert, cert_price, category, notes=notes, sources=policy, **kw)


KAGGLE = 'https://www.kaggle.com/learn/'
for title, slug, area, duration in [
    ('Python', 'python', 'Python', '5 h estimadas'),
    ('Intro to SQL', 'intro-to-sql', 'SQL', '3 h estimadas'),
    ('Pandas', 'pandas', 'Python / datos', UNKNOWN),
    ('Advanced SQL', 'advanced-sql', 'SQL', UNKNOWN),
    ('Intro to Machine Learning', 'intro-to-machine-learning', 'Machine Learning', UNKNOWN),
    ('Intermediate Machine Learning', 'intermediate-machine-learning', 'Machine Learning', UNKNOWN),
    ('Data Visualization', 'data-visualization', 'Visualización de datos', UNKNOWN),
    ('Data Cleaning', 'data-cleaning', 'Calidad de datos', UNKNOWN),
]:
    international(title, area, 'Kaggle Learn', f'https://www.kaggle.com/learn/{slug}',
                  duration, 'Certificado de finalización', 'GRATIS', FREE,
                  policy=(KAGGLE,), notes='La política del catálogo ofrece certificados gratuitos; algunas fichas renderizan mediante JavaScript.')

for title, base, weeks in [
    ('CS50x: Introduction to Computer Science', 'https://cs50.harvard.edu/x/', '11 semanas de contenido; ritmo propio'),
    ('CS50P: Introduction to Programming with Python', 'https://cs50.harvard.edu/python/', '10 semanas de contenido; ritmo propio'),
    ('CS50 SQL: Introduction to Databases with SQL', 'https://cs50.harvard.edu/sql/', '7 semanas de contenido; ritmo propio'),
]:
    international(title, 'Software / Python / bases de datos', 'Harvard — CS50', base,
                  weeks, 'Certificado CS50 (no verificado por edX)', 'GRATIS', FREE,
                  policy=(base + 'certificate/',),
                  requirements='Entregar ejercicios y proyecto final con al menos 70 % según las reglas del curso.',
                  notes='Certificado CS50 gratuito separado del certificado verificado de edX, que es de pago.')

international('Data Analytics Essentials', 'Data Analytics / Excel / SQL', 'Cisco Networking Academy',
              'https://www.netacad.com/courses/data-analytics-essentials', '30 h',
              'Badge de formación', 'GRATIS', FREE,
              notes='Curso distinto a Introducción a la ciencia de datos del grupo B; no equivale a un examen profesional Cisco.')
international('Introduction to Linux (LFS101)', 'Linux', 'Linux Foundation',
              'https://training.linuxfoundation.org/training/introduction-to-linux/', '60 h',
              'Badge incluido', 'GRATIS', FREE,
              notes='La ficha ofrece el curso a $0 con acceso por 90 días. Es un curso gratuito completo con plazo de acceso; no es una prueba de suscripción ni el examen LFCS.')

AWS = 'https://aws.amazon.com/education/awseducate/'
for title, area in [('Getting Started with Storage', 'AWS / almacenamiento'),
                    ('Getting Started with Compute', 'AWS / cómputo'),
                    ('Getting Started with Networking', 'AWS / redes'),
                    ('Getting Started with Databases', 'AWS / bases de datos'),
                    ('Getting Started with Cloud Operations', 'AWS / operaciones cloud')]:
    international(title, area, 'AWS Educate', AWS,
                  notes='Cursos nombrados en el catálogo público. Inscripción desde el portal AWS Educate; no hay enlace público individual confirmado. Badges en cursos elegibles; asignación y costo de credencial individual: ' + UNKNOWN + '. No es certificación profesional AWS.',
                  requirements='Registro AWS Educate; 13 años o más; el programa no exige tarjeta de crédito.',
                  peru_basis='Programa abierto a cualquier persona según AWS; acceso individual desde Perú no probado.')

for title, url, duration in [
    ('Databricks Fundamentals', 'https://www.databricks.com/resources/learn/training/databricks-fundamentals', '1 h de videos; catálogo general indica 1 h 30 min'),
    ('Generative AI Fundamentals', 'https://www.databricks.com/resources/learn/training/generative-ai-fundamentals', '60 min'),
    ('AI Agent Fundamentals', 'https://www.databricks.com/resources/training/level-your-ai-agent-skills', '90 min'),
]:
    international(title, 'Datos / IA', 'Databricks', url, duration,
                  'Badge tras evaluación', 'GRATIS', FREE,
                  policy=('https://www.databricks.com/learn/training/home',),
                  notes='Cursos breves con badge; separados de las certificaciones profesionales Databricks.')

international('Oracle Agentic AI Foundations Associate (2026)', 'IA agéntica / automatización', 'Oracle University',
              'https://learn.oracle.com/ols/learning-path/become-an-oracle-agentic-ai-foundations-associate/146553/163239',
              '6 h 28 min de curso; preparación y examen adicionales',
              'Certificación al aprobar examen', 'GRATIS', FREE,
              policy=('https://blogs.oracle.com/oracleuniversity/oracle-agentic-ai-foundations-training-certification-now-available',),
              requirements='Cuenta Oracle; familiaridad con LLM y programación recomendada; aprobar examen.',
              notes='Gratuidad explícita del examen en fuente Oracle de junio de 2026; detalles de identidad y acceso se revisan en MyLearn.')

HP = 'https://www.life-global.org/?lang=en'
for title, url, area in [
    ('Agile Project Management', 'https://www.life-global.org/course/380-agile-project-management', 'Agile / proyectos'),
    ('AI for Business Professionals', 'https://www.life-global.org/course/423-ai-for-business-professionals', 'IA / gestión empresarial'),
    ('Introduction to Cybersecurity Awareness', 'https://www.life-global.org/course/346-introduction-to-cybersecurity-awareness', 'Ciberseguridad')]:
    international(title, area, 'HP LIFE / HP Foundation', url,
                  cert='Certificado de finalización', cert_price='GRATIS', category=FREE,
                  policy=(HP, *(['https://www.life-global.org/news/agile-project-management'] if title == 'Agile Project Management' else [])), notes='Formación introductoria; certificado de finalización, sin afirmar acreditación profesional Scrum o ciberseguridad.')

for title, slug in [('Relational Database', 'relational-database'), ('Responsive Web Design', 'responsive-web-design')]:
    international(title, 'Bases de datos / desarrollo web', 'freeCodeCamp',
                  'https://www.freecodecamp.org/learn/' + slug,
                  cert='Certificación curricular por proyectos', cert_price='GRATIS', category=FREE,
                  policy=('https://opensource.freecodecamp.org/about/',),
                  notes='La gratuidad incluye certificaciones; no se trasladan estimaciones antiguas de 300 h al currículo actual.')

for title, area in [('Google Ads Search — formación y certificación foundational', 'Marketing digital'),
                    ('Google Ads Measurement — formación y certificación foundational', 'Marketing / analítica')]:
    international(title, area, 'Google Skillshop',
                  'https://skillshop.withgoogle.com/intl/es-419_ALL/googleads/',
                  cert='Certificación foundational al aprobar evaluación', cert_price='GRATIS', category=FREE,
                  policy=('https://support.google.com/google-ads/answer/7539883?hl=en',
                          'https://support.google.com/skillshop/answer/14746215?hl=en'),
                  notes='Buscar la especialidad indicada en Skillshop. No confundir con las certificaciones Professional supervisadas y sujetas a tarifas.')

MS = 'https://learn.microsoft.com/en-us/training/support/faq'
for title, url in [
    ('Get started with Microsoft data analytics', 'https://learn.microsoft.com/en-us/training/paths/data-analytics-microsoft/'),
    ('Prepare data for analysis with Power BI', 'https://learn.microsoft.com/en-us/training/paths/prepare-data-power-bi/')]:
    international(title, 'Power BI / datos', 'Microsoft Learn', url,
                  cert='Logros del perfil Learn; certificación profesional requiere trámite aparte',
                  policy=(MS,), level='Intermedio',
                  notes='Formación gratuita. Duración no confirmada en la ficha actual (hay diferencias entre versiones). No se ofrece PL-300 gratis.')
international('Career Essentials in Generative AI by Microsoft and LinkedIn', 'IA Generativa / productividad',
              'Microsoft / LinkedIn Learning',
              'https://www.linkedin.com/learning/paths/career-essentials-in-generative-ai-by-microsoft-and-linkedin',
              '4 h de contenido; 5 cursos', 'Professional Certificate del programa', 'GRATIS', FREE,
              policy=('https://learn.microsoft.com/en-us/credentials/support/microsoft-essentials-professional-certificate-frequently-asked-questions',),
              notes='Ruta actualizada el 25 sep. 2026. Acceso gratuito del programa Essentials, separado de una prueba general de LinkedIn Learning.',
              requirements='Cuenta LinkedIn; completar ruta y evaluación.')

for title, slug, duration in [
    ('Introduction to GitHub', 'introduction-to-github', 'Menos de 1 h'),
    ('Introduction to Git', 'introduction-to-git', UNKNOWN),
    ('Hello GitHub Actions', 'hello-github-actions', 'Menos de 30 min')]:
    international(title, 'Git / DevOps', 'GitHub Skills', 'https://github.com/skills/' + slug,
                  duration, policy=('https://learn.github.com/skills',),
                  notes='Ejercicio público gratuito. Usar repositorio público y recursos locales para evitar consumo facturable de Actions/Codespaces; certificado no anunciado.')
international('Containers, Kubernetes and Red Hat OpenShift Technical Overview (DO080)',
              'Contenedores / Kubernetes', 'Red Hat',
              'https://www.redhat.com/en/services/training/do080-deploying-containerized-applications-technical-overview',
              policy=('https://www.redhat.com/en/services/training-and-certification',),
              notes='Videos gratuitos de introducción, no la prueba de Red Hat Learning Subscription ni una certificación profesional.')
international('Cybersecurity and Cloud Fundamentals', 'Ciberseguridad / cloud', 'Fortinet Training Institute',
              'https://training.fortinet.com/local/staticpage/view.php?page=library_cybersecurity-and-cloud-fundamentals',
              duration='11 h estimadas', cert='Exam badge al aprobar el curso',
              category=FREEMIUM,
              policy=('https://helpdesk.training.fortinet.com/support/solutions/articles/73000524102-how-do-i-register-for-the-free-online-self-paced-training-',
                      'https://helpdesk.training.fortinet.com/support/solutions/articles/73000665752-how-will-the-cybersecurity-fundamentals-training-be-organized-'),
              notes='Lecciones autoguiadas gratuitas; laboratorios bajo demanda pueden ser de pago. Reemplaza cursos retirados el 15 jul. 2026.')
international('Gestión de proyectos de desarrollo', 'Gestión de proyectos', 'BID Academy',
              'https://knowledge.iadb.org/es/curso/gestion-de-proyectos-de-desarrollo', '30 h',
              'Credencial digital verificable BID', category=CALL, status='ABIERTA',
              notes='La ficha anuncia formación gratis y credencial. No explicita por separado la tarifa de la credencial: se deja sin confirmar; no confundir con alternativas Coursera de pago.',
              requirements='Dirigido a sector público, privado, emprendedores y organizaciones civiles; cuenta en plataforma.',
              peru_basis='Orientado a América Latina y el Caribe; Perú comprendido en ese alcance. No se probó matriculación personal.')

SANT = 'https://www.santanderopenacademy.com/es/sites/courses/tools.html'
for title, slug in [('Excel: de intermedio a avanzado', 'excel-course-intermediate-to-advanced'),
                    ('Power BI: análisis y modelado de datos intermedio', 'power-bi-intermediate-data-analysis-and-modeling')]:
    international(title, 'Excel / Power BI', 'Santander Open Academy',
                  'https://app.santanderopenacademy.com/es/course/' + slug, '8 h (directorio oficial del Congreso)',
                  'Certificado de finalización', 'GRATIS', FREE,
                  policy=(SANT, 'https://www.santanderopenacademy.com/es/faq.html',
                          'https://www3.congreso.gob.pe/OCI/capacitaciones/cursos/'),
                  notes='Directorio oficial indica disponible 2026; ficha de inscripción usa JavaScript. No se confirmó cupo individual ni cierre del curso; modalidad abierta según política de cursos de acceso directo.',
                  requirements='Cuenta Santander Open Academy; revisar términos de edad y acceso en la ficha al ingresar.')

SAP = 'https://learning.sap.com/helpcenter/learning-site'
for title, slug, duration, cert in [
    ('Discovering SAP Business Technology Platform', 'discovering-sap-business-technology-platform-1', '1 h 5 min', 'Achievement de finalización'),
    ('Exploring DevOps with SAP BTP', 'exploring-devops-with-sap-btp', '3 h 46 min', UNKNOWN)]:
    international(title, 'SAP / cloud / DevOps', 'SAP Learning', 'https://learning.sap.com/courses/' + slug,
                  duration, cert, policy=(SAP,),
                  notes='Contenido autoguiado gratuito. Entornos de práctica y certificación profesional pueden requerir pago; costo separado del achievement no confirmado.')
international('Get Started with Artificial Intelligence', 'IA', 'Salesforce Trailhead',
              'https://trailhead.salesforce.com/content/learn/trails/get-started-with-ai-data', '3 h 15 min aprox.',
              'Badges de módulos / puntos Trailhead', 'GRATIS', FREE,
              policy=('https://trailhead.salesforce.com/',),
              notes='Ruta de ocho pasos; no se cuentan por separado sus módulos. Badges de aprendizaje separados de la certificación profesional Salesforce.')
international('Data Fundamentals', 'Datos / ciencia de datos', 'IBM SkillsBuild',
              'https://skillsbuild.org/cs/learning-catalog?topic=data', 'Banda de catálogo 3–10 h; duración exacta ' + UNKNOWN,
              'Credencial digital anunciada', category=CALL,
              policy=('https://skillsbuild.org/adult-learners',),
              notes='Catálogo oficial consultado en versión checa; buscar Data Fundamentals en SkillsBuild. Idioma español de este curso y costo separado de credencial no confirmados.')


def by_title(title):
    matches = [r for r in courses if r['title'] == title]
    if len(matches) != 1:
        raise ValueError(f'Título ambiguo o ausente: {title}')
    return matches[0]['id']


TOP = [
    ('Excel intermedio', 'Es una base útil para puestos administrativos y de datos.', 'Trabajo intermedio con hojas de cálculo; contrastar temario al entrar.', 'Formación de 20 h; reforzar con un archivo propio de análisis.', 'Intermedio'),
    ('Introducción al Power BI', 'Introduce BI con una oferta local accesible.', 'Primeros pasos en Power BI.', 'Certificado de curso de 15 h y dashboard como portafolio.', 'Básico'),
    ('Fundamentos de Python 1', 'Da una entrada estructurada a programación.', 'Fundamentos de Python.', '30 h de formación Cisco; no equivale a aprobar un examen externo.', 'Básico'),
    ('Fundamentos de Python 2', 'Profundiza después de la primera parte.', 'Programación en Python de continuación.', '40 h adicionales y ejercicios para documentar en GitHub.', 'Intermedio'),
    ('CS50 SQL: Introduction to Databases with SQL', 'Combina fundamentos y ejercicios exigentes.', 'Consultas, relaciones y bases de datos.', 'Certificado CS50 gratuito si apruebas; proyecto SQL demostrable.', 'Básico'),
    ('CS50P: Introduction to Programming with Python', 'Favorece práctica sostenida en lugar de solo videos.', 'Programación y resolución de problemas con Python.', 'Proyecto final y certificado CS50 de aprobación.', 'Básico'),
    ('Data Analytics Essentials', 'Ordena competencias de entrada a análisis.', 'Proceso analítico con Excel, SQL y visualización.', '30 h y badge Cisco, acompañados de un caso práctico.', 'Básico'),
    ('Introduction to Linux (LFS101)', 'Linux sirve como base para cloud y DevOps.', 'Uso y conceptos fundamentales de Linux.', '60 h y badge; no es la certificación LFCS.', 'Básico'),
    ('English for IT 1', 'Permite trabajar vocabulario técnico de forma sostenida.', 'Inglés orientado a tecnología.', '50 h de formación; no acredita un nivel mediante examen internacional.', 'Básico'),
    ('Curso HCIA-Datacom V1.0', 'Aporta una base extensa de redes.', 'Conceptos de comunicación de datos.', '64 h de curso; no afirmar HCIA aprobado sin examen profesional.', 'Básico'),
    ('Relational Database', 'Permite construir evidencia práctica de bases de datos.', 'SQL y trabajo con bases relacionales mediante proyectos.', 'Certificación curricular freeCodeCamp y repositorio de proyectos.', 'Básico'),
    ('Oracle Agentic AI Foundations Associate (2026)', 'Tiene examen gratuito explícito y contenido actual.', 'Fundamentos y construcción de agentes de IA.', 'Certificación Oracle al aprobar; familiaridad previa con LLM recomendada.', 'Intermedio'),
    ('Career Essentials in Generative AI by Microsoft and LinkedIn', 'Conecta IA con productividad laboral.', 'IA generativa, Copilot y uso responsable.', 'Professional Certificate del programa; 4 h de contenido actualizado.', 'Básico'),
    ('Gestión de proyectos de desarrollo', 'Cubre una necesidad común del sector público y privado.', 'Herramientas y prácticas de gestión de proyectos.', '30 h y credencial BID anunciada; confirmar costo específico de credencial.', 'Básico'),
    ('Logística 360°. Claves para una gestión moderna y eficiente', 'Es pertinente para ingeniería industrial y operaciones.', 'Panorama de gestión logística.', 'Certificado de curso de 20 h; útil con un caso de mejora de procesos.', 'Básico'),
]
top = [dict(rank=i, course_id=by_title(t), why=w, learn=l, cv=cv, level=lev)
       for i, (t, w, l, cv, lev) in enumerate(TOP, 1)]

routes = [
    ('RUTA 1 — ANALISTA DE DATOS', [
        ('Excel', ['Excel básico', 'Excel intermedio']),
        ('SQL', ['Intro to SQL', 'CS50 SQL: Introduction to Databases with SQL']),
        ('Power BI', ['Introducción al Power BI', 'Análisis de datos con Power BI']),
        ('Python', ['Fundamentos de Python 1', 'Pandas']),
        ('Fundamentos analíticos y estadísticos', ['Data Analytics Essentials']),
        ('BI y calidad de datos', ['Prepare data for analysis with Power BI', 'Data Cleaning']),
        ('IA aplicada a datos', ['Intro to Machine Learning', 'Intermediate Machine Learning'])],
     'No se verificó aquí un curso completo de estadística inferencial gratuito con certificado; la etapa analítica necesita práctica adicional. Cerrar con un dashboard y un análisis reproducible.'),
    ('RUTA 2 — INGENIERÍA / TECNOLOGÍA', [
        ('Linux', ['Introduction to Linux (LFS101)']),
        ('Git', ['Introduction to Git', 'Introduction to GitHub']),
        ('Python', ['Fundamentos de Python 1', 'Fundamentos de Python 2']),
        ('Bases de datos', ['Relational Database']),
        ('Contenedores', ['Containers, Kubernetes and Red Hat OpenShift Technical Overview (DO080)']),
        ('Cloud', ['Getting Started with Compute', 'Getting Started with Storage', 'Getting Started with Networking']),
        ('DevOps', ['Hello GitHub Actions', 'Exploring DevOps with SAP BTP']),
        ('Ciberseguridad', ['Introducción a ciberseguridad', 'Defensa de la red'])],
     'DO080 ofrece una visión de contenedores/Kubernetes, no un programa completo de Docker. DevOps requiere práctica local y un pipeline; SAP BTP es una aplicación específica de CI/CD.'),
    ('RUTA 3 — GESTIÓN', [
        ('Gestión empresarial', ['Plan de negocios', 'Modelo Canvas']),
        ('Gestión de proyectos', ['Gestión de proyectos de desarrollo']),
        ('Fundamentos de Scrum y Kanban', ['Agile Project Management']),
        ('Agile', ['Agile mindset', 'Estrategias ágiles para empresas']),
        ('Liderazgo', ['Cómo gestionar tu equipo de trabajo', 'Dirección de personal']),
        ('Finanzas', ['Finanzas para emprender', 'Contabilidad de costos']),
        ('Transformación digital', ['Gestión del cambio', 'El rol del líder en la transformación digital'])],
     'HP LIFE confirma fundamentos de Scrum y Kanban en el temario. No se verificó una certificación profesional Scrum gratuita. Elaborar un plan de negocio, cronograma y tablero de seguimiento.'),
    ('RUTA 4 — INTELIGENCIA ARTIFICIAL', [
        ('Fundamentos', ['Introduction to Modern AI', 'Get Started with Artificial Intelligence']),
        ('IA generativa', ['Generative AI Fundamentals', 'Career Essentials in Generative AI by Microsoft and LinkedIn']),
        ('Uso de prompts en contexto laboral', ['AI for Business Professionals']),
        ('Python', ['Fundamentos de Python 1', 'CS50P: Introduction to Programming with Python']),
        ('Machine Learning', ['Intro to Machine Learning', 'Intermediate Machine Learning']),
        ('Base cloud para IA', ['Getting Started with Compute', 'Getting Started with Databases']),
        ('Agentes y automatización', ['AI Agent Fundamentals', 'Oracle Agentic AI Foundations Associate (2026)'])],
     'La ruta ofrece aproximaciones a prompts y cloud: no se verificó aquí un curso independiente completo de Prompt Engineering o Cloud AI. Construir un caso con evaluación de resultados; desplegar servicios cloud puede generar costos.'),
]
route_data = [dict(title=t, steps=[dict(order=i, topic=topic, course_ids=[by_title(x) for x in titles])
                                  for i, (topic, titles) in enumerate(steps, 1)], note=note)
              for t, steps, note in routes]

watch = [
    ('UNI PIT', UNI, 'Prerregistro 12–14 oct.; matrícula 15–26 oct. 2026. Correo institucional externo; credencial S/50. Confirmar títulos y calendario de clases.'),
    ('MTPE CAPACÍTA-T', MTPE, 'Catálogo público de 214 cursos observado. Revisar las vigencias de aliados. Las rutas agrupadas no otorgan certificado propio; sí sus cursos según FAQ.'),
    ('PCM / Talento Digital', 'https://www.gob.pe/institucion/pcm/noticias/1423146-pcm-lanza-cursos-virtuales-gratuitos-de-inteligencia-artificial-programacion-web-y-ciberseguridad-con-certificacion-internacional', 'Anuncio del 26 jul. 2026 con 15 cursos Cisco. No sumar de nuevo los mismos cursos de CAPACÍTA-T; página Talento Digital dio error de acceso en la herramienta.'),
    ('SERVIR / ENAP', 'https://www.gob.pe/institucion/servir/campa%C3%B1as/23775-cursos-mooc-2026-de-la-enap-servir-libres-gratuitos-y-certificados', 'Convocatoria MOOC consultada cerró 12 jul. 2026. Revisar nuevas ediciones; no está abierta al corte de este catálogo.'),
    ('SERVIR municipalidades', 'https://sites.google.com/servir.gob.pe/mimunimecapacita/inicio', 'Transformación digital municipal 12–26 oct., pero plazo de inscripción 5 oct. 09:00: CERRADA al 7 oct., aunque el sitio conserva una etiqueta de inscripción.'),
    ('Municipalidad de Lima', 'https://www.gob.pe/institucion/munilima/noticias/1427868-capacitate-gratis-y-potencia-tu-emprendimiento-municipalidad-de-lima-ofrece-mas-de-280-cursos-tecnico-productivos', 'Anuncio 10 ago. 2026 con opciones virtuales para mayores de 18 residentes de Lima; inicio ya pasado. Vacantes actuales y certificado: ' + UNKNOWN + '.'),
    ('Fundación Romero / becas', 'https://www.becasgruporomero.pe/', 'Convocatorias mediante convenios y padrón de beneficiarios; no toda la oferta comercial de Campus Romero es gratis. Entrar a los cursos A desde el programa MTPE.'),
    ('Fundación Telefónica / Conecta Empleo', 'https://www.fundaciontelefonica.com.pe/conecta-empleo/', 'El catálogo específico Perú discontinuó su oferta; el sitio remite a edición global. No reutilizar fechas de cohortes antiguas.'),
    ('SENATI empresas', 'https://empresas.senati.edu.pe/', 'Cursos gratuitos para empresas aportantes: elegibilidad restringida. Bolsa de trabajo/webinars pueden limitarse a estudiantes de último semestre y egresados.'),
    ('TECSUP', 'https://www.tecsup.edu.pe/buscador-y-biblioteca/?tipo_programa=33', 'Usar filtro de programas gratuitos. IA generativa aplicada encontrada con precio S/1780 fue excluida. Un curso regalo por matrícula pagada no es formación independiente gratuita.'),
    ('PRONABEC — India / ITEC', 'https://www.pronabec.gob.pe/beca-india/', 'e-ITEC depende de cursos convocados; requisitos publicados de edad 25–45 y cinco años de experiencia. No se confirmó una cohorte virtual concreta abierta.'),
    ('PRONABEC convocatorias', 'https://www.pronabec.gob.pe/category/vigente/', 'Beca Perú de junio-julio y beneficios Club Estrella vigentes hasta marzo no se presentan como abiertos en octubre.'),
    ('SBS', 'https://www.sbs.gob.pe/prevencion-de-lavado-activos/Semana-de-Prevencion-del-Lavado-de-Activos', 'Semana 26–30 oct. 2026 con actividad de IA; verificar registro y alcance. Precio y certificado de cada evento no confirmados.'),
    ('Congreso — cursos virtuales', 'https://www3.congreso.gob.pe/participacion/cursos/cursos-vigentes/', 'Edición octubre inició 5 oct.; portal dice inscripción abierta. Formación cívica fuera del foco técnico principal; confirmar cierre y certificado.'),
    ('Google Career Certificates / Coursera', 'https://grow.google/certificates', 'No hay beca completa Google/Coursera verificada en esta investigación. No asumir que preview, ayuda financiera o primer módulo equivalen a curso completo gratis. Revisar precio y ayuda financiera en la inscripción específica.'),
    ('edX', 'https://support.edx.org/hc/en-us/articles/1500003964681-What-is-the-audit-track', 'Auditoría gratuita depende del curso, tiene plazo de acceso y no incluye credencial ni evaluaciones calificadas. Certificados verificados aparte.'),
    ('NVIDIA', 'https://www.nvidia.com/en-us/training/self-paced-courses/?section=free-courses', 'Revisar filtro de cursos gratuitos; la interfaz dinámica no permitió cerrar aquí una ficha individual con precio/certificado actual.'),
    ('Palo Alto Networks', 'https://www.paloaltonetworks.com/services/education', 'Biblioteca de módulos digitales gratuitos confirmada. Verificar curso específico, duración y credencial; exámenes profesionales separados.'),
    ('SAP Learning', SAP, 'Formación autoguiada libre, con recursos premium y certificación profesional separados.'),
    ('AWS Educate', AWS, 'Revisar badge y condiciones de cada curso. AWS Skill Builder y certificaciones profesionales tienen productos de pago distintos.'),
]

data = dict(schema_version=1,task='EDU-001',as_of=DATE,timezone='America/Lima',
            scope='Investigación de fuentes públicas; no se crea cuenta ni se prueba matrícula personal.',
            group_definitions={'A':'Proveedor situado en Lima; formación virtual local mediante convenio MTPE y un programa UNI.',
                               'B':'30 cursos diferentes de la oferta nacional MTPE; no significa 30 cursos de universidades fuera de Lima.',
                               'C':'Oferta global virtual. Acceso desde Perú inferido del alcance global/latinoamericano; ver restricciones por ficha.'},
            courses=courses,top15=top,routes=route_data,
            watchlist=[dict(institution=i,url=u,note=n) for i,u,n in watch],
            limitations=[
                'Se consultaron fichas, políticas y catálogos oficiales. La disponibilidad pública permanente no garantiza cupos ni recepción de certificados.',
                'Sin sesión autenticada: no se verificó matrícula individual, elegibilidad final ni emisión de credenciales.',
                'La oferta peruana se concentra en CAPACÍTA-T: no es una muestra independiente de treinta regiones.',
                'Búsquedas regionales y de varias instituciones no encontraron una convocatoria verificable o devolvieron información parcial; no demuestra ausencia de oferta.',
                'LinkedIn, Facebook, Instagram y X se buscaron mediante índices públicos. No se revisaron feeds completos ni publicaciones privadas.',
                'No todas las empresas, universidades o dependencias enumeradas en PROMPT.MD tuvieron revisión individual. Cobertura amplia, exhaustividad total no demostrada.',
                'Campos desconocidos conservan el texto literal exigido; fechas de matrícula no se convierten en fechas de inicio.',
            ])
(OUT / 'catalogo.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

EMOJI = {'ABIERTA':'🟢 ABIERTA','PRÓXIMAMENTE':'🟡 PRÓXIMAMENTE','PERMANENTE':'🔵 PERMANENTE','CERRADA':'🔴 CERRADA'}
ORDER = {FREE:0,PAID_CERT:1,'Becado':2,CALL:3,'Auditoría gratuita':4,FREEMIUM:5,'Pago':6}
HEADERS = ['N.º','Curso','Área','Institución','Ciudad/País','Modalidad','Duración','Precio del curso','Certificado','Precio del certificado','Inscripción','Inicio','Enlace oficial']
def cell(value):
    return str(value).replace('|','/').replace('\n',' ')

counts = Counter(r['group'] for r in courses)
lines = ['# Catálogo de capacitación gratuita para residentes de Lima', '',
         f'**Corte: 7 de octubre de 2026 · America/Lima. {len(courses)} oportunidades: {counts["A"]} Lima, {counts["B"]} adicionales de alcance nacional y {counts["C"]} internacionales.**', '',
         'Los números son ofertas distintas, no inscripciones garantizadas. En A se agrupan cursos de Fundación Romero mediante CAPACÍTA-T y el programa UNI; B reúne cursos nacionales MTPE de otros proveedores y del propio ministerio. Ambos grupos pueden estudiarse desde Lima. No se hallaron treinta ofertas verificadas de universidades regionales y no se atribuyen a regiones que no las ofrecen.', '',
         '🔵 PERMANENTE significa catálogo autoguiado público sin cierre anunciado; 🟢 ABIERTA requiere una ficha que declare inscripciones abiertas; 🟡 PRÓXIMAMENTE indica un próximo plazo; 🔴 CERRADA queda en vigilancia. No se realizó matrícula con una cuenta personal. El alcance global se interpreta como acceso desde Perú, salvo restricciones expresas. Ver requisitos debajo de cada tabla.', '',
         'Las categorías figuran junto al nombre del curso. **Curso y certificado GRATIS** incluye badges cuando la fuente lo indica. Un badge o certificado de finalización no equivale automáticamente a una certificación profesional. Los precios desconocidos se muestran como «'+UNKNOWN+'». No se incluyen pruebas gratuitas de suscripciones como cursos gratuitos completos.', '',
         '## Fuentes y política de gratuidad', '',
         f'CAPACÍTA-T confirma formación virtual gratuita y certificado gratuito en su [FAQ oficial]({FAQ}); también aclara que las rutas completas no tienen certificado propio. Las duraciones y emisores provienen de tarjetas públicas, contrastadas con fichas individuales.', '',
         f'La [convocatoria UNI]({UNI}) separa curso sin costo y credencial S/50. [AWS Educate]({AWS}) publica cursos y laboratorios gratuitos; no se promete examen AWS. [HP LIFE]({HP}) confirma curso y certificado gratuitos. [Microsoft Learn]({MS}) ofrece formación sin costo y distingue logros de credenciales profesionales.', '',
         'El certificado gratuito de [CS50](https://cs50.harvard.edu/x/certificate/) exige aprobación; edX cobra por su modalidad verificada. [Google Skillshop](https://support.google.com/skillshop/answer/14746215?hl=en) mantiene gratuitas las certificaciones foundational, separadas de las Professional. [Oracle](https://blogs.oracle.com/oracleuniversity/oracle-agentic-ai-foundations-training-certification-now-available) anuncia expresamente gratis el examen Agentic AI Foundations.', '']

for group, heading in [('A','A. LIMA'),('B','B. TODO EL PERÚ'),('C','C. INTERNACIONALES DISPONIBLES PARA PERÚ')]:
    rows = sorted((r for r in courses if r['group']==group),key=lambda r:(ORDER[r['category']],r['id']))
    lines += ['## '+heading,'',f'{len(rows)} oportunidades. Referencias {group}xx estables para enlazar recomendaciones y rutas.','',
              '| '+' | '.join(HEADERS)+' |','| '+' | '.join(['---']*13)+' |']
    for r in rows:
        vals=[r['id'],f'**{r["title"]}** — {r["category"]}',r['area'],r['institution'],r['location'],r['modality'],r['duration'],r['course_price'],r['certificate'],r['certificate_price'],EMOJI[r['registration']],r['start'],f'[Ficha oficial]({r["url"]})']
        lines.append('| '+' | '.join(cell(v) for v in vals)+' |')
    lines += ['', '### Requisitos, alcance y observaciones del grupo '+group, '']
    if group in ('A','B'):
        lines += ['Los cursos CAPACÍTA-T se realizan desde su ficha oficial, luego de crear cuenta en el aula correspondiente. Los aliados pueden imponer vigencias o condiciones de acceso; la gratuidad se refiere a la vía MTPE, no a una membresía comercial del proveedor. **No se comprobó el alta de una cuenta ni la entrega del certificado.**', '']
        if group == 'A':
            lines += ['Se eligió la versión de 20 h de Excel intermedio y la de 10 h de Excel básico. Versiones cortas con el mismo título y traducciones no se suman como oportunidades nuevas. Fundación Romero es proveedor local; modalidad virtual no implica exclusividad para residentes de Lima.', '']
            r = next(x for x in rows if x['id']=='A21')
            lines += [f'- **A21:** {r["requirements"]} {r["notes"]}', '']
        else:
            lines += ['- Cisco/Huawei: certificados de formación anunciados por el programa; no se ha verificado gratuidad de exámenes profesionales CCNA, HCIA u otros.',
                      '- B05: ficha «Fundamentos de IA con IBM SkillsBuild», pero tarjeta «Certifica: Cisco». Emisor definitivo: '+UNKNOWN+'.',
                      '- Las 50 h de English for IT corresponden a cada ficha individual. No se usa la duración de una ruta agregada como duración de curso.', '']
    else:
        for r in rows:
            refs='; '.join(f'[Fuente {i}]({u})' for i,u in enumerate(r['sources'][1:],1))
            lines += [f'- **{r["id"]} — {r["title"]}:** {r["requirements"]} {r["notes"]} '+refs]
        lines += ['']

lines += ['## TOP 15 CURSOS QUE MÁS RECOMIENDO', '',
          'Selección editorial para empleabilidad, práctica, trayectoria del proveedor y costo. No promete contratación. Las rutas extensas se priorizan; las introducciones breves sirven como complemento. Niveles son orientación editorial si la ficha no los define.', '']
for rec in top:
    r=next(x for x in courses if x['id']==rec['course_id'])
    lines += [f'{rec["rank"]}. **{r["id"]} — [{r["title"]}]({r["url"]})**. Por qué: {rec["why"]} Aprenderás: {rec["learn"]} CV: {rec["cv"]} Nivel: **{rec["level"]}**.','']
lines += ['## Rutas de aprendizaje', '',
          'El orden es una propuesta de estudio, no un prerrequisito institucional. Los cursos repetidos entre rutas se cursan una sola vez y no incrementan los totales del catálogo.', '']
for route in route_data:
    lines += ['### '+route['title'],'']
    for step in route['steps']:
        refs=[]
        for cid in step['course_ids']:
            r=next(x for x in courses if x['id']==cid)
            refs.append(f'{cid} [{r["title"]}]({r["url"]})')
        lines.append(f'{step["order"]}. **{step["topic"]}:** '+' → '.join(refs)+'.')
    lines += ['',route['note'],'']
lines += ['## OPORTUNIDADES QUE CONVIENE VIGILAR','',
          'Vigilancia sugerida: revisar estos enlaces semanalmente y nuevamente antes de inscribirse. Es una lista de revisión; no se creó una automatización ni se enviaron notificaciones.', '',
          '| Institución / programa | Situación observada y qué revisar | Fuente oficial |',
          '| --- | --- | --- |']
for row in data['watchlist']:
    lines.append('| '+cell(row['institution'])+' | '+cell(row['note'])+' | [Revisar]('+row['url']+') |')
lines += ['', '## Cobertura, exclusiones y límites de verificación', '']
for note in data['limitations']:
    lines.append('- '+note)
lines += ['', 'Se investigaron con combinaciones de búsqueda tecnología, gestión, universidades de Lima, institutos y fuentes públicas peruanas; también regiones del Perú y proveedores internacionales. Los registros de consulta se conservan en [fuentes.json](fuentes.json). La extracción del catálogo MTPE y las lecturas HTTP se guardan como evidencia técnica PALLAQUINO.', '',
          'No se verificaron ofertas independientes actuales para todos los temas solicitados — por ejemplo R, Product Management, una certificación Scrum gratuita, un programa completo Docker o Prompt Engineering — ni una beca integral vigente de Google Career Certificates. Tampoco se atribuyen a cada universidad o región resultados encontrados en otra entidad. La lista del PROMPT es una guía de cobertura, no una garantía de que cada institución publique una convocatoria vigente.', '',
          '**Antes de inscribirte:** abrir la ficha oficial, confirmar plazo y requisitos, elegir la vía gratuita indicada y comprobar por separado si la credencial es incluida, opcional o de pago. Una publicación vieja o un curso que inicia pronto puede tener matrícula ya cerrada.', '',
          '## Evidencia y reproducción', '',
          '- Datos: [catalogo.json](catalogo.json). Fuentes consultadas: [fuentes.json](fuentes.json).',
          '- Generación: `python investigacion/construir_catalogo.py` (usa la extracción MTPE ya registrada; no actualiza automáticamente la investigación).',
          '- Control estructural: `python investigacion/validar_catalogo.py`.',
          '- Los controles estructurales no prueban aceptación de matrícula, entrega de certificados ni gratuidad de servicios cloud fuera del curso.', '']
(OUT / 'catalogo.md').write_text('\n'.join(lines),encoding='utf-8')
print(json.dumps({'courses':len(courses),'groups':counts,'top':len(top),'routes':len(route_data)},ensure_ascii=False))
