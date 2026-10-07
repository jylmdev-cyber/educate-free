import { readFileSync } from 'node:fs'
import assert from 'node:assert/strict'
const data = JSON.parse(readFileSync('investigacion/catalogo.json', 'utf8'))
assert.equal(new Set(data.courses.map(c => c.id)).size, data.courses.length)
for (const c of data.courses) {
  assert.ok(c.title && c.institution && c.consulted_on)
  for (const u of c.sources) assert.equal(new URL(u).protocol, 'https:')
}
const ids = new Set(data.courses.map(c => c.id))
assert.equal(data.top15.length, 15)
assert.equal(data.routes.length, 4)
for (const r of data.top15) assert.ok(ids.has(r.course_id))
for (const r of data.routes) for (const s of r.steps) for (const id of s.course_ids) assert.ok(ids.has(id))
console.log(`Data contract OK: ${data.courses.length} offers, 15 recommendations, 4 routes, ${data.watchlist.length} institutions.`)
