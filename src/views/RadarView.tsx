import { useEffect, useState } from 'react'
import { ArrowUpRight, Bell, CheckCheck, Radar, Search } from 'lucide-react'
import { institutions } from '@/lib/progress'
import { normalize, peruToday, safeUrl } from '@/lib/catalog'
import { usePersonal } from '@/lib/store'
import { Button } from '@/components/ui/button'
import { parseRadarReport, type RadarReport } from '@/lib/radar'
export default function RadarView({ notify }: { notify: (text: string) => void }) {
  const personal = usePersonal()
  const [query, setQuery] = useState('')
  const [followedOnly, setFollowedOnly] = useState(false)
  const [report, setReport] = useState<RadarReport | null>(null)
  useEffect(() => {
    const controller = new AbortController()
    fetch(`${import.meta.env.BASE_URL}radar-checks.json`, { signal: controller.signal }).then(response => { if (!response.ok) throw new Error('Informe no disponible'); return response.json() as Promise<unknown> }).then(value => setReport(parseRadarReport(value))).catch(() => { /* Manual source review remains available. */ })
    return () => controller.abort()
  }, [])
  const today = peruToday()
  const visible = institutions.filter(i => normalize(`${i.institution} ${i.note}`).includes(normalize(query)) && (!followedOnly || personal.followed.includes(i.id)))
  const uniExpired = today > '2026-10-26'
  return <div className="radar-view"><section className="radar-feature"><div className="radar-orbit" aria-hidden="true"><Radar size={72} /><i /><i /></div><div><span className="eyebrow">UNA OPORTUNIDAD EN EL HORIZONTE</span><h2>{uniExpired ? 'PIT UNI: revisar la siguiente edición' : 'PIT UNI: prepara tu próximo paso'}</h2><p>Prerregistro del 12 al 14 de octubre de 2026. Matrícula del 15 al 26. Curso gratuito, credencial opcional S/50; externos requieren correo institucional.</p><Button asChild variant="secondary"><a href={institutions[0].url} target="_blank" rel="noopener noreferrer">Revisar convocatoria<ArrowUpRight size={16} /></a></Button></div><span className="radar-date"><strong>12–14</strong><span>OCT 2026</span><small>{uniExpired ? 'Plazo publicado vencido' : today < '2026-10-12' ? 'Prerregistro próximo' : today <= '2026-10-14' ? 'Periodo de prerregistro' : 'Consultar matrícula'}</small></span></section>
    <div className="radar-toolbar"><label className="search-box"><Search size={19} /><span className="sr-only">Buscar instituciones</span><input value={query} onChange={e => setQuery(e.target.value)} placeholder="Buscar una institución o convocatoria" /></label><label className="check-label"><input type="checkbox" checked={followedOnly} onChange={e => setFollowedOnly(e.target.checked)} />Solo las que sigo ({personal.followed.length})</label></div>
    <p className="context-note"><Bell size={18} />Seguir guarda la institución en tu radar personal. Las revisiones se marcan manualmente; no se envían notificaciones. El monitoreo programado requiere activar el workflow del repositorio.</p>
    <p className="context-note">{report?.checked_at ? `Último chequeo publicado: ${new Date(report.checked_at).toLocaleString('es-PE', { timeZone: 'America/Lima' })}. ${report.checks.filter(c => c.state === 'changed').length} fuentes con cambios; ${report.checks.filter(c => c.state === 'access_failure').length} consultas fallidas. Un cambio de página requiere revisión de la convocatoria.` : 'Aún no hay un chequeo automático publicado. Consulta las fuentes oficiales para verificar nuevas convocatorias.'}</p>
    <div className="radar-grid">{visible.map(i => { const followed = personal.followed.includes(i.id); return <article className="radar-card" key={i.id}><div className="radar-card-top"><span className="institution-icon" aria-hidden="true">{i.institution.slice(0, 2).toUpperCase()}</span><Button variant={followed ? 'secondary' : 'ghost'} size="sm" aria-pressed={followed} onClick={() => personal.toggleFollow(i.id)}><Bell size={15} fill={followed ? 'currentColor' : 'none'} />{followed ? 'Siguiendo' : 'Seguir'}</Button></div><h3>{i.institution}</h3><p>{i.note}</p><div className="radar-card-footer"><a href={safeUrl(i.url) ?? undefined} target="_blank" rel="noopener noreferrer">Fuente oficial<ArrowUpRight size={15} /></a><Button variant="ghost" size="sm" onClick={() => { personal.review(i.id, today); notify(`${i.institution}: revisión personal registrada.`) }}><CheckCheck size={15} />Marcar revisado</Button></div><small>Revisión personal: {personal.reviewed[i.id] ?? 'Pendiente'} · Fuente del informe: 07 oct. 2026</small></article> })}</div>
    {!visible.length && <div className="empty-state"><Radar size={30} /><h3>No hay instituciones en esta selección</h3><p>Busca otro nombre o desactiva el filtro de seguimiento.</p></div>}
  </div>
}
