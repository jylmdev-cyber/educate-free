import { Building2, Clock3, FileText, LayoutGrid, MapPin, Search, BadgeCheck, Code2, FileSpreadsheet, ChartColumn, ShieldCheck } from 'lucide-react'
import type { LucideIcon } from 'lucide-react'
import { allInstitutions, allTopics, categories, defaultFilters, groups } from '@/lib/catalog'
import type { Filters as FilterState } from '@/lib/catalog'
import { SelectField } from './ui/select-field'
type Props = { value: FilterState; onChange: (filters: FilterState) => void; count: number }
export default function Filters({ value, onChange, count }: Props) {
  const set = (key: keyof FilterState, next: string | boolean) => onChange({ ...value, [key]: next })
  const active = Object.entries(value).filter(([key, v]) => key !== 'sort' && Boolean(v)).length
  const featuredAreas = ['Excel', 'Power BI', 'Python', 'Ciberseguridad']
  const orderedAreas = [...featuredAreas.filter(topic => allTopics.includes(topic)), ...allTopics.filter(topic => !featuredAreas.includes(topic))]
  return <section className="filter-panel" aria-label="Buscar y filtrar oportunidades">
    <div className="search-row"><label className="search-box"><Search size={21} aria-hidden="true" /><span className="sr-only">Buscar cursos</span><input value={value.query} onChange={e => set('query', e.target.value)} placeholder="¿Qué quieres aprender? Python, Power BI, gestión…" /><kbd aria-hidden="true">Buscar</kbd></label></div>
    <div className="filter-grid">
      <FilterSelect icon={MapPin} label="Ubicación" value={value.group} onChange={v => set('group', v)} options={Object.entries(groups)} empty="Todas las ubicaciones" />
      <FilterSelect icon={LayoutGrid} label="Área" value={value.area} onChange={v => set('area', v)} options={orderedAreas.map(x => [x, x])} empty="Todas las áreas" />
      <FilterSelect icon={Building2} label="Institución" value={value.institution} onChange={v => set('institution', v)} options={allInstitutions.map(x => [x, x])} empty="Todas las instituciones" />
      <FilterSelect icon={BadgeCheck} label="Gratuidad" value={value.category} onChange={v => set('category', v)} options={categories.map(x => [x, x])} empty="Todos los tipos" />
      <FilterSelect icon={FileText} label="Inscripción" value={value.registration} onChange={v => set('registration', v)} options={['ABIERTA', 'PERMANENTE', 'PRÓXIMAMENTE', 'CERRADA'].map(x => [x, x.charAt(0) + x.slice(1).toLowerCase()])} empty="Todos los estados" />
      <FilterSelect icon={Clock3} label="Duración" value={value.duration} onChange={v => set('duration', v)} options={ [['10','10 horas o más'],['20','20 horas o más'],['40','40 horas o más'],['unknown','Sin duración confirmada']] } empty="Cualquier duración" />
    </div>
    <div className="filter-bottom"><span aria-live="polite"><strong>{count}</strong> oportunidades encontradas</span><div className="filter-bottom-actions"><button type="button" className="clear-filters" onClick={() => onChange({ ...defaultFilters })} disabled={!active}>Limpiar filtros</button><label className="check-label"><input type="checkbox" checked={value.savedOnly} onChange={e => set('savedOnly', e.target.checked)} />Solo mis guardados</label></div></div>
  </section>
}
function FilterSelect({ label, icon, value, onChange, options, empty }: { label: string; icon: LucideIcon; value: string; onChange: (value: string) => void; options: string[][]; empty: string }) {
  const areaIcons: Record<string, LucideIcon> = { Python: Code2, Excel: FileSpreadsheet, 'Power BI': ChartColumn, Ciberseguridad: ShieldCheck }
  return <SelectField label={label} icon={icon} variant="capsule" removable value={value} onValueChange={onChange} options={[{ value: '', label: empty }, ...options.map(([key, text]) => ({ value: key, label: text, icon: label === 'Área' ? areaIcons[text] : undefined }))]} />
}
