import source from '../../investigacion/catalogo.json'
import Fuse from 'fuse.js'

export type Course = typeof source.courses[number]
export type Registration = 'ABIERTA' | 'PRÓXIMAMENTE' | 'PERMANENTE' | 'CERRADA'
export const catalog = source
export const courses = source.courses
export const courseById = new Map(courses.map(course => [course.id, course]))
export const UNKNOWN = 'No confirmado en la fuente oficial'
export const groups: Record<string, string> = { A: 'Lima', B: 'Todo el Perú', C: 'Internacional' }
export const normalize = (value: string) => value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().trim()
export const topics = (course: Course) => course.area.split('/').map(s => s.trim())
export const allTopics = [...new Set(courses.flatMap(topics))].sort((a, b) => a.localeCompare(b, 'es'))
export const allInstitutions = [...new Set(courses.map(c => c.institution))].sort((a, b) => a.localeCompare(b, 'es'))
export const categories = [...new Set(courses.map(c => c.category))]

export function durationHours(text: string): number | null {
  const value = normalize(text)
  if (/no confirmado|semanas|banda|catalogo|–|\d\s*-\s*\d/.test(value)) return null
  const hours = value.match(/(\d+(?:[.,]\d+)?)\s*(?:horas?\b|h\b|hrs?\b)/)
  const minutes = value.match(/(\d+(?:[.,]\d+)?)\s*(?:minutos?\b|min\b)/)
  if (!hours && !minutes) return null
  return (hours ? Number(hours[1].replace(',', '.')) : 0) + (minutes ? Number(minutes[1].replace(',', '.')) / 60 : 0)
}

export function peruToday(now = new Date()): string {
  const parts = new Intl.DateTimeFormat('en-CA', { timeZone: 'America/Lima', year: 'numeric', month: '2-digit', day: '2-digit' }).formatToParts(now)
  return ['year', 'month', 'day'].map(name => parts.find(p => p.type === name)?.value).join('-')
}

export function effectiveRegistration(course: Course, today = peruToday()): Registration {
  if (course.closing && today > course.closing) return 'CERRADA'
  if (course.id === 'A21' && today >= '2026-10-12' && today <= '2026-10-26') return 'ABIERTA'
  return course.registration as Registration
}

export function safeUrl(value: string): string | null {
  try { const url = new URL(value); return url.protocol === 'https:' && !url.username && !url.password ? url.href : null } catch { return null }
}

export type Filters = { query: string; group: string; area: string; institution: string; category: string; registration: string; duration: string; savedOnly: boolean; sort: string }
export const defaultFilters: Filters = { query: '', group: '', area: '', institution: '', category: '', registration: '', duration: '', savedOnly: false, sort: 'recommended' }
const index = new Fuse(courses, { keys: ['title', 'area', 'institution', 'location'], threshold: 0.32, ignoreLocation: true, getFn: (obj, path) => normalize(String(obj[path as keyof Course])) })
const rank = new Map(source.top15.map(r => [r.course_id, r.rank]))

export function filterCourses(filters: Filters, favorites: string[] = [], today = peruToday()): Course[] {
  let results = filters.query.trim() ? index.search(normalize(filters.query)).map(result => result.item) : [...courses]
  results = results.filter(c => (!filters.group || c.group === filters.group)
    && (!filters.area || topics(c).includes(filters.area))
    && (!filters.institution || c.institution === filters.institution)
    && (!filters.category || c.category === filters.category)
    && (!filters.registration || effectiveRegistration(c, today) === filters.registration)
    && (!filters.savedOnly || favorites.includes(c.id))
    && (!filters.duration || (filters.duration === 'unknown' ? durationHours(c.duration) === null
      : durationHours(c.duration) !== null && durationHours(c.duration)! >= Number(filters.duration))))
  if (filters.sort === 'name') results.sort((a, b) => a.title.localeCompare(b.title, 'es'))
  if (filters.sort === 'duration') results.sort((a, b) => (durationHours(b.duration) ?? -1) - (durationHours(a.duration) ?? -1))
  if (filters.sort === 'recommended' && !filters.query.trim()) results.sort((a, b) => (rank.get(a.id) ?? 100) - (rank.get(b.id) ?? 100))
  return results
}

export function distribution(items: Course[], getLabel: (course: Course) => string) {
  const counts = new Map<string, number>()
  items.forEach(c => { const label = getLabel(c); counts.set(label, (counts.get(label) ?? 0) + 1) })
  return [...counts].map(([name, value]) => ({ name, value })).sort((a, b) => b.value - a.value)
}

export function courseSignature(course: Course): string { return `${normalize(course.institution)}::${normalize(course.title)}` }
