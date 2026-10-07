import { ArrowUpRight, Bookmark, Check, CirclePlus, Clock3, Info } from 'lucide-react'
import { courseById, catalog, groups, safeUrl } from '@/lib/catalog'
import { usePersonal } from '@/lib/store'
import { Dialog, DialogContent, DialogDescription, DialogTitle } from './ui/dialog'
import { Button } from './ui/button'
import { SelectField } from './ui/select-field'
import { Status } from './CourseCard'
import { useState } from 'react'
export default function CourseDetail({ id, onClose, notify }: { id: string | null; onClose: () => void; notify: (text: string) => void }) {
  const course = id ? courseById.get(id) : undefined
  const personal = usePersonal()
  const [chosenRoute, setRoute] = useState('route-1')
  const recommendation = catalog.top15.find(r => r.course_id === id)
  if (!course) return null
  const selected = personal.routes.find(r => r.id === chosenRoute) ?? personal.routes[0]
  const isAdded = selected?.courseIds.includes(course.id)
  return <Dialog open={!!course} onOpenChange={open => { if (!open) onClose() }}><DialogContent>
    <div className="detail-kicker"><span className="eyebrow">{course.id} / {groups[course.group]}</span><Status course={course} /></div>
    <DialogTitle className="detail-title">{course.title}</DialogTitle><DialogDescription className="detail-provider">{course.institution}</DialogDescription>
    <div className="detail-summary"><span><Clock3 size={18} />{course.duration}</span><span>{course.modality}</span></div>
    <div className="detail-prices"><div><span>Formación</span><strong>{course.course_price}</strong></div><div><span>Precio de la credencial</span><strong>{course.certificate_price}</strong></div></div>
    <dl className="detail-fields"><div><dt>Credencial</dt><dd>{course.certificate}</dd></div><div><dt>Requisitos de acceso</dt><dd>{course.requirements}</dd></div><div><dt>Inicio de clases</dt><dd>{course.start}</dd></div>{course.closing && <div><dt>Cierre publicado</dt><dd>{course.closing}</dd></div>}<div><dt>Acceso desde Perú</dt><dd>{course.peru_access_basis}</dd></div></dl>
    {recommendation && <section className="recommendation-detail"><span className="eyebrow">Nuestra selección · TOP {recommendation.rank}</span><h3>Una habilidad que suma a tu perfil</h3><p><strong>Por qué:</strong> {recommendation.why}</p><p><strong>Aprenderás:</strong> {recommendation.learn}</p><p><strong>En tu CV:</strong> {recommendation.cv}</p><p><strong>Nivel orientativo:</strong> {recommendation.level}</p></section>}
    {course.notes && <p className="detail-note"><Info size={18} />{course.notes}</p>}
    <div className="add-route"><div className="form-field"><span className="select-label">Agregar a mi ruta</span><SelectField label="Agregar a mi ruta" disabled={!selected} value={selected?.id ?? ''} onValueChange={setRoute} options={personal.routes.length ? personal.routes.map(r => ({ value: r.id, label: r.name })) : [{ value: '', label: 'Crea una ruta primero' }]} /></div><Button disabled={!!isAdded || !selected} onClick={() => { if (selected) { personal.addCourse(selected.id, course.id); notify(`Curso agregado a ${selected.name}.`) } }}><CirclePlus size={16} />{isAdded ? 'Ya está en la ruta' : 'Agregar'}</Button></div>
    <div className="detail-actions"><Button asChild><a href={safeUrl(course.url) ?? undefined} target="_blank" rel="noopener noreferrer">Ir a la fuente oficial<ArrowUpRight size={17} /></a></Button><Button variant="secondary" aria-pressed={personal.favorites.includes(course.id)} onClick={() => personal.toggleFavorite(course.id)}><Bookmark size={16} />{personal.favorites.includes(course.id) ? 'Guardado' : 'Guardar'}</Button><Button variant="secondary" aria-pressed={personal.completed.includes(course.id)} onClick={() => personal.toggleComplete(course.id)}><Check size={16} />{personal.completed.includes(course.id) ? 'Completado' : 'Marcar completado'}</Button></div>
    <details className="source-details"><summary>Fuentes y límites de verificación</summary><p>Consulta del informe: {course.consulted_on}. {course.evidence}. La disponibilidad pública no garantiza aceptación de matrícula. Revisa fechas y condiciones en la plataforma.</p><ul>{course.sources.map((url, i) => <li key={url}><a href={safeUrl(url) ?? undefined} target="_blank" rel="noopener noreferrer">Fuente oficial {i + 1}<ArrowUpRight size={13} /></a></li>)}</ul></details>
  </DialogContent></Dialog>
}
