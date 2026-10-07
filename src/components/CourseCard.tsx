import { ArrowUpRight, Bookmark, Check, Clock3, Globe2, MapPin } from 'lucide-react'
import type { Course } from '@/lib/catalog'
import { effectiveRegistration, groups, topics, UNKNOWN } from '@/lib/catalog'
import { usePersonal } from '@/lib/store'
import { Button } from './ui/button'
export function Status({ course }: { course: Course }) {
  const status = effectiveRegistration(course)
  const text: Record<string, string> = { PERMANENTE: 'A tu ritmo', ABIERTA: 'Inscripción abierta', PRÓXIMAMENTE: 'Próximamente', CERRADA: 'Plazo cerrado' }
  return <span className={`status status-${status.toLowerCase()}`}><span />{text[status]}</span>
}
export default function CourseCard({ course, onOpen, rank }: { course: Course; onOpen: (id: string) => void; rank?: number }) {
  const saved = usePersonal(s => s.favorites.includes(course.id))
  const complete = usePersonal(s => s.completed.includes(course.id))
  const toggle = usePersonal(s => s.toggleFavorite)
  const provider = course.institution.split(' / ')[0]
  return <article className={`course-card group-${course.group}`}>
    <div className="card-top"><span className="provider-symbol" aria-hidden="true">{provider === 'Fundación Romero' ? 'FR' : provider.slice(0, 2).toUpperCase()}</span><span className="provider-name">{provider}</span><Button variant="ghost" size="icon" aria-label={`${saved ? 'Quitar de guardados' : 'Guardar'} ${course.title}`} aria-pressed={saved} onClick={() => toggle(course.id)}><Bookmark size={18} fill={saved ? 'currentColor' : 'none'} /></Button></div>
    <div className="card-tags">{rank && <span className="rank-tag">TOP {String(rank).padStart(2, '0')}</span>}<span className="topic-tag">{topics(course)[0]}</span>{complete && <span className="complete-tag"><Check size={12} />Completado</span>}</div>
    <button className="card-title" onClick={() => onOpen(course.id)}><h3>{course.title}</h3></button>
    <div className="card-meta"><span><Clock3 size={15} />{course.duration.includes(UNKNOWN) ? 'Duración por confirmar' : course.duration}</span><span>{course.group === 'C' ? <Globe2 size={15} /> : <MapPin size={15} />}{groups[course.group]} · Virtual</span></div>
    <div className="card-credential"><span className={course.certificate_price === 'GRATIS' ? 'credential-free' : ''}><span className="credential-dot" />{course.certificate_price === 'GRATIS' ? 'Curso y credencial gratis' : course.certificate_price === 'S/50' ? 'Curso gratis · credencial S/50' : 'Curso gratis · revisar credencial'}</span></div>
    <div className="card-bottom"><Status course={course} /><Button variant="ghost" size="sm" onClick={() => onOpen(course.id)}>Ver detalles<ArrowUpRight size={16} /></Button></div>
  </article>
}
