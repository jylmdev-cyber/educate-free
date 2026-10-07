import { describe, expect, it } from 'vitest'
import { courseById, courses, defaultFilters, durationHours, effectiveRegistration, filterCourses, peruToday, safeUrl } from '../src/lib/catalog'
import { freshData, makeBackup, parseBackup, reorder } from '../src/lib/progress'

describe('Catálogo y controles temporales', () => {
  it('conserva las 95 fichas originales y fuentes HTTPS', () => { expect(courses).toHaveLength(95); expect(courseById.size).toBe(95); expect(courses.every(c => safeUrl(c.url))).toBe(true) })
  it('combina búsqueda, geografía, área y duración sin ampliar los resultados', () => {
    const rows = filterCourses({ ...defaultFilters, query: 'pythn', group: 'B', area: 'Python', duration: '20' })
    expect(rows.map(c => c.id).sort()).toEqual(['B01', 'B02'])
  })
  it('filtra credencial pagada sin presentarla como gratis', () => { const rows = filterCourses({ ...defaultFilters, category: 'Curso GRATIS / certificado de pago' }, [], '2026-10-07'); expect(rows.map(c => c.id)).toEqual(['A21']); expect(rows[0].certificate_price).toBe('S/50') })
  it('separa desconocidos y duraciones ambiguas de horas numéricas', () => { expect(durationHours('No confirmado en la fuente oficial')).toBeNull(); expect(durationHours('11 semanas de contenido')).toBeNull(); expect(durationHours('1 h de videos; catálogo general indica 1 h 30 min')).toBeNull(); expect(durationHours('Banda 3–10 h')).toBeNull(); expect(durationHours('1 hora y 30 minutos')).toBe(1.5); expect(durationHours('90 min')).toBe(1.5) })
  it('calcula Perú sin depender de la zona del navegador', () => { expect(peruToday(new Date('2026-10-12T02:00:00Z'))).toBe('2026-10-11') })
  it('no mantiene próxima una convocatoria con plazo vencido', () => { const uni = courseById.get('A21')!; expect(effectiveRegistration(uni, '2026-10-07')).toBe('PRÓXIMAMENTE'); expect(effectiveRegistration(uni, '2026-10-12')).toBe('ABIERTA'); expect(effectiveRegistration(uni, '2026-10-26')).toBe('ABIERTA'); expect(effectiveRegistration(uni, '2026-10-27')).toBe('CERRADA') })
  it('respeta favoritos y ordena duraciones desconocidas al final', () => { expect(filterCourses({ ...defaultFilters, savedOnly: true }, ['B02']).map(c => c.id)).toEqual(['B02']); const sorted = filterCourses({ ...defaultFilters, sort: 'duration' }); expect(durationHours(sorted.at(-1)!.duration)).toBeNull(); expect(durationHours(sorted[0].duration)).toBeGreaterThanOrEqual(60) })
  it('bloquea esquemas ejecutables y enlaces con credenciales', () => { expect(safeUrl('javascript:alert(1)')).toBeNull(); expect(safeUrl('https://user:pass@example.com')).toBeNull(); expect(safeUrl('http://example.com')).toBeNull() })
})
describe('Respaldos y rutas personales', () => {
  it('restaura el progreso completo tras exportar', () => { const data = freshData(); data.completed = ['B01']; data.favorites = ['C11']; data.followed = ['watch-1']; data.reviewed['watch-1'] = '2026-10-07'; expect(parseBackup(JSON.stringify(makeBackup(data)))).toEqual(data) })
  it('rechaza JSON corrupto y formatos ajenos', () => { expect(() => parseBackup('{')).toThrow('JSON'); expect(() => parseBackup('{}')).toThrow('EducaLibre'); expect(() => parseBackup(' '.repeat(1_000_001))).toThrow('1 MB') })
  it('rechaza IDs desconocidos sin aceptar parcialmente un respaldo', () => { const backup = makeBackup(freshData()); backup.data.completed = ['unknown-id']; expect(() => parseBackup(JSON.stringify(backup))).toThrow('catálogo') })
  it('detecta reasignación de IDs aunque exista el nuevo ID', () => { const backup = makeBackup(freshData()); backup.signatures.A04 = 'otro proveedor::otro curso'; expect(() => parseBackup(JSON.stringify(backup))).toThrow('identificadores') })
  it('rechaza rutas duplicadas y seguimiento no válido', () => { const backup = makeBackup(freshData()); backup.data.routes.push(backup.data.routes[0]); expect(() => parseBackup(JSON.stringify(backup))).toThrow('inválidas'); const bad = makeBackup(freshData()); bad.data.followed = ['outsider']; expect(() => parseBackup(JSON.stringify(bad))).toThrow('inválidas') })
  it('deduplica cursos y respeta límite/nombre de rutas', () => { const backup = makeBackup(freshData()); backup.data.completed = ['A01', 'A01']; expect(parseBackup(JSON.stringify(backup)).completed).toEqual(['A01']); backup.data.routes[0].name = ' '.repeat(5); expect(() => parseBackup(JSON.stringify(backup))).toThrow('ruta inválida') })
  it('reordena sin perder ni duplicar cursos; protege límites', () => { expect(reorder(['A01', 'B01', 'C01'], 0, 1)).toEqual(['B01', 'A01', 'C01']); expect(reorder(['A01'], 0, -1)).toEqual(['A01']) })
})
