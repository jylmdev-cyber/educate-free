import { useState } from 'react'
import { ArrowDown, ArrowUp, ArrowUpRight, Check, CirclePlus, Flag, ListOrdered, Plus, Trash2 } from 'lucide-react'
import { catalog, courseById, courses, durationHours } from '@/lib/catalog'
import { usePersonal } from '@/lib/store'
import { Button } from '@/components/ui/button'
import { SelectField } from '@/components/ui/select-field'
export default function RoutesView({ onOpen, notify }: { onOpen: (id: string) => void; notify: (text: string) => void }) {
  const personal = usePersonal()
  const [selectedId, setSelected] = useState('route-1')
  const [newName, setNewName] = useState('')
  const [showNew, setShowNew] = useState(false)
  const [addId, setAddId] = useState('')
  const route = personal.routes.find(r => r.id === selectedId) ?? personal.routes[0]
  const done = route?.courseIds.filter(id => personal.completed.includes(id)).length ?? 0
  const total = route?.courseIds.length ?? 0
  const progress = total ? Math.round(done / total * 100) : 0
  const knownHours = route?.courseIds.reduce((sum, id) => sum + (durationHours(courseById.get(id)!.duration) ?? 0), 0) ?? 0
  const unknown = route?.courseIds.filter(id => durationHours(courseById.get(id)!.duration) === null).length ?? 0
  const originalIndex = Number(route?.id.replace('route-', '')) - 1
  const original = catalog.routes[originalIndex]
  return <div className="routes-layout"><aside className="route-picker"><span className="eyebrow">ELIGE TU DIRECCIÓN</span>{personal.routes.map((r, i) => <button key={r.id} onClick={() => setSelected(r.id)} className={r.id === route?.id ? 'route-choice selected' : 'route-choice'} aria-pressed={r.id === route?.id}><span className="route-choice-number">{String(i + 1).padStart(2, '0')}</span><span><strong>{r.name}</strong><small>{r.courseIds.length} cursos · {r.courseIds.filter(id => personal.completed.includes(id)).length} completados</small></span></button>)}<Button variant="secondary" onClick={() => setShowNew(!showNew)}><Plus size={16} />Crear una ruta</Button>{showNew && <form className="new-route" onSubmit={e => { e.preventDefault(); if (newName.trim() && personal.routes.length < 50) { setSelected(personal.createRoute(newName)); setNewName(''); setShowNew(false); notify('Tu nueva ruta está lista.') } }}><label>Nombre de la nueva ruta<input required maxLength={100} value={newName} onChange={e => setNewName(e.target.value)} placeholder="Mi próximo objetivo" /></label><Button type="submit">Crear ruta</Button></form>}<div className="local-note"><Flag size={21} /><strong>A tu propio ritmo</strong><p>Tu progreso se guarda en este navegador. Exporta un respaldo para llevarlo contigo.</p></div></aside>
    <section className="route-workspace" aria-label="Ruta seleccionada">{route ? <>
      <div className="route-heading"><div><span className="eyebrow">TU PLAN, PASO A PASO</span><h2>{route.name}</h2></div><span className="progress-number">{progress}<small>%</small></span></div>
      <div className="progress-track" role="progressbar" aria-label="Progreso de la ruta" aria-valuenow={progress} aria-valuemin={0} aria-valuemax={100}><span style={{ width: `${progress}%` }} /></div><p className="route-progress-meta">{done} de {total} cursos completados · {Math.round(knownHours)} h publicadas{unknown > 0 ? ` + ${unknown} duraciones no comparables` : ''}</p>
      <div className="route-step-list">{route.courseIds.map((id, index) => { const c = courseById.get(id)!; const checked = personal.completed.includes(id); return <article className={`route-step ${checked ? 'done' : ''}`} key={id}><label className="step-check"><input type="checkbox" checked={checked} onChange={() => personal.toggleComplete(id)} aria-label={`Completar ${c.title}`} /><span aria-hidden="true">{checked ? <Check size={16} /> : String(index + 1).padStart(2, '0')}</span></label><div className="step-body"><small>{c.area}</small><button onClick={() => onOpen(id)}>{c.title}<ArrowUpRight size={15} /></button><p>{c.institution.split(' / ')[0]} · {c.duration}</p></div><div className="step-controls"><Button variant="ghost" size="icon" disabled={index === 0} aria-label={`Subir ${c.title}`} onClick={() => personal.moveCourse(route.id, index, -1)}><ArrowUp size={16} /></Button><Button variant="ghost" size="icon" disabled={index === total - 1} aria-label={`Bajar ${c.title}`} onClick={() => personal.moveCourse(route.id, index, 1)}><ArrowDown size={16} /></Button><Button variant="ghost" size="icon" aria-label={`Quitar ${c.title} de esta ruta`} onClick={() => { personal.removeCourse(route.id, id); notify('Curso quitado de esta ruta. Su progreso personal se conserva.') }}><Trash2 size={15} /></Button></div></article> })}</div>
      {total === 0 && <div className="empty-state"><ListOrdered size={28} /><h3>El primer paso lo eliges tú</h3><p>Agrega cursos desde aquí o desde cualquier ficha del catálogo.</p></div>}
      <form className="add-route" onSubmit={e => { e.preventDefault(); if (addId) { personal.addCourse(route.id, addId); setAddId(''); notify('Curso agregado a tu ruta.') } }}><div className="form-field"><span className="select-label">Agregar un curso</span><SelectField label="Agregar un curso" value={addId} disabled={route.courseIds.length === courses.length} onValueChange={setAddId} options={[{ value: '', label: 'Selecciona una oportunidad' }, ...courses.filter(c => !route.courseIds.includes(c.id)).map(c => ({ value: c.id, label: `${c.title} — ${c.institution.split(' / ')[0]}` }))]} /></div><Button disabled={!addId}><CirclePlus size={16} />Agregar</Button></form>
      {original && <details className="source-details"><summary>Ver orientación y etapas de esta ruta</summary><ol>{original.steps.map(s => <li key={s.order}>{s.topic}</li>)}</ol><p>{original.note}</p></details>}
    </> : <div className="empty-state"><h2>Crea tu primera ruta</h2><p>Usa el botón Crear una ruta para empezar.</p></div>}</section></div>
}
