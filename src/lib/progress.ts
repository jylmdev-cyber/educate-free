import { catalog, courseById, courseSignature, courses } from './catalog'

export type LearningRoute = { id: string; name: string; courseIds: string[] }
export type PersonalData = { favorites: string[]; completed: string[]; routes: LearningRoute[]; followed: string[]; reviewed: Record<string, string> }
export const institutions = catalog.watchlist.map((item, index) => ({ ...item, id: `watch-${index + 1}` }))
export const institutionIds = new Set(institutions.map(i => i.id))
export const initialRoutes: LearningRoute[] = catalog.routes.map((route, index) => ({ id: `route-${index + 1}`, name: route.title.replace(/^RUTA \d+ — /, ''), courseIds: [...new Set(route.steps.flatMap(step => step.course_ids))] }))
export const freshData = (): PersonalData => ({ favorites: [], completed: [], routes: initialRoutes.map(r => ({ ...r, courseIds: [...r.courseIds] })), followed: [], reviewed: {} })
const isObject = (value: unknown): value is Record<string, unknown> => !!value && typeof value === 'object' && !Array.isArray(value)
const isStringList = (value: unknown): value is string[] => Array.isArray(value) && value.every(v => typeof v === 'string')
const unique = (value: string[]) => [...new Set(value)]
function validateCourseIds(value: unknown): string[] {
  if (!isStringList(value) || value.some(id => !courseById.has(id))) throw new Error('El respaldo contiene cursos que no pertenecen a este catálogo.')
  return unique(value)
}
export function validatePersonalData(value: unknown): PersonalData {
  if (!isObject(value) || !Array.isArray(value.routes) || !isStringList(value.followed) || !isObject(value.reviewed)) throw new Error('El archivo no tiene la estructura de un respaldo EducaLibre.')
  const routes = value.routes.map((route): LearningRoute => {
    if (!isObject(route) || typeof route.id !== 'string' || !/^[a-zA-Z0-9-]{1,80}$/.test(route.id) || typeof route.name !== 'string' || !route.name.trim() || route.name.length > 100) throw new Error('Hay una ruta inválida en el respaldo.')
    return { id: route.id, name: route.name.trim(), courseIds: validateCourseIds(route.courseIds) }
  })
  if (routes.length > 50 || new Set(routes.map(r => r.id)).size !== routes.length || value.followed.some(id => !institutionIds.has(id))) throw new Error('El respaldo contiene rutas o instituciones inválidas.')
  const reviewed: Record<string, string> = {}
  for (const [id, at] of Object.entries(value.reviewed)) {
    if (!institutionIds.has(id) || typeof at !== 'string' || !/^\d{4}-\d{2}-\d{2}$/.test(at) || Number.isNaN(Date.parse(at))) throw new Error('Fecha de revisión inválida en el respaldo.')
    reviewed[id] = at
  }
  return { favorites: validateCourseIds(value.favorites), completed: validateCourseIds(value.completed), routes, followed: unique(value.followed), reviewed }
}

export function makeBackup(data: PersonalData) {
  return { app: 'educalibre', version: 1, catalogDate: catalog.as_of, exportedAt: new Date().toISOString(), signatures: Object.fromEntries(courses.map(c => [c.id, courseSignature(c)])), data: validatePersonalData(data) }
}
export function parseBackup(text: string): PersonalData {
  if (text.length > 1_000_000) throw new Error('El respaldo supera el límite de 1 MB.')
  let value: unknown
  try { value = JSON.parse(text) } catch { throw new Error('El archivo no es JSON válido.') }
  if (!isObject(value) || value.app !== 'educalibre' || value.version !== 1 || !isObject(value.signatures)) throw new Error('Selecciona un respaldo exportado desde EducaLibre.')
  const data = validatePersonalData(value.data)
  const used = new Set([...data.favorites, ...data.completed, ...data.routes.flatMap(r => r.courseIds)])
  for (const id of used) if (value.signatures[id] !== courseSignature(courseById.get(id)!)) throw new Error('El catálogo cambió de identificadores. Conserva tu respaldo y revisa su compatibilidad antes de importarlo.')
  return data
}
export function reorder(ids: string[], index: number, direction: -1 | 1) {
  const next = [...ids], target = index + direction
  if (target < 0 || target >= ids.length) return next
  ;[next[index], next[target]] = [next[target], next[index]]
  return next
}
