import { create } from 'zustand'
import { createJSONStorage, persist } from 'zustand/middleware'
import { freshData, makeBackup, parseBackup, reorder, validatePersonalData } from './progress'
import type { PersonalData } from './progress'
import { courseById } from './catalog'

export let storageProblem = ''
const storage = {
  getItem: (key: string) => { try { return localStorage.getItem(key) } catch { storageProblem = 'El navegador bloqueó el almacenamiento. Exporta un respaldo para conservar tu progreso.'; return null } },
  setItem: (key: string, value: string) => { try { localStorage.setItem(key, value) } catch { storageProblem = 'No se pudo guardar el progreso en el navegador. Exporta un respaldo.' } },
  removeItem: (key: string) => { try { localStorage.removeItem(key) } catch { storageProblem = 'No se pudo acceder al almacenamiento local.' } },
}
type Store = PersonalData & {
  toggleFavorite: (id: string) => void; toggleComplete: (id: string) => void;
  addCourse: (routeId: string, courseId: string) => void; removeCourse: (routeId: string, courseId: string) => void;
  moveCourse: (routeId: string, index: number, direction: -1 | 1) => void;
  createRoute: (name: string) => string; toggleFollow: (id: string) => void; review: (id: string, date: string) => void;
  replaceData: (data: PersonalData) => void;
}
const toggle = (ids: string[], id: string) => ids.includes(id) ? ids.filter(x => x !== id) : [...ids, id]
export const usePersonal = create<Store>()(persist((set) => ({
  ...freshData(),
  toggleFavorite: id => { if (courseById.has(id)) set(s => ({ favorites: toggle(s.favorites, id) })) },
  toggleComplete: id => { if (courseById.has(id)) set(s => ({ completed: toggle(s.completed, id) })) },
  addCourse: (routeId, courseId) => { if (courseById.has(courseId)) set(s => ({ routes: s.routes.map(r => r.id === routeId ? { ...r, courseIds: [...new Set([...r.courseIds, courseId])] } : r) })) },
  removeCourse: (routeId, courseId) => set(s => ({ routes: s.routes.map(r => r.id === routeId ? { ...r, courseIds: r.courseIds.filter(id => id !== courseId) } : r) })),
  moveCourse: (routeId, index, direction) => set(s => ({ routes: s.routes.map(r => r.id === routeId ? { ...r, courseIds: reorder(r.courseIds, index, direction) } : r) })),
  createRoute: name => { const id = `custom-${crypto.randomUUID()}`; set(s => ({ routes: [...s.routes, { id, name: name.trim().slice(0, 100), courseIds: [] }] })); return id },
  toggleFollow: id => set(s => ({ followed: toggle(s.followed, id) })),
  review: (id, date) => set(s => ({ reviewed: { ...s.reviewed, [id]: date } })),
  replaceData: data => set(validatePersonalData(data)),
}), {
  name: 'educalibre-progress-v1', version: 1, storage: createJSONStorage(() => storage),
  partialize: s => makeBackup(s),
  merge: (persisted, current) => { if (!persisted) return current; try { return { ...current, ...parseBackup(JSON.stringify(persisted)) } } catch { storageProblem = 'El progreso guardado no es compatible. Se cargaron rutas iniciales; conserva tu respaldo para revisar los datos.'; return current } },
}))
