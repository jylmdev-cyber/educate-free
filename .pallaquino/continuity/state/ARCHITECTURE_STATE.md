# ARCHITECTURE_STATE

Arquitectura estática React/HashRouter/Zustand/Radix intacta. Se centralizan tokens CSS de color y tipografía; SVG y Recharts consumen variables compartidas. Font WOFF2 local procesada por Vite, sin CDN en ejecución ni cambios funcionales.

Updated 2026-10-07T21:31:55.676495+00:00.

## Historical snapshot (superseded where noted)

# ARCHITECTURE_STATE

EDU-007 no cambia arquitectura React/Radix ni persistencia. Agrega documentación y scanner de candidatos Git. E2E escribe .artifacts/e2e; CI adjunta resultados sin mezclar continuidad local. Src, catálogo runtime y PROMPT intactos.

Updated 2026-10-07T18:38:13.352347+00:00. codex-root.

## Historical snapshot (superseded where noted)

# ARCHITECTURE_STATE

Estado vigente EDU-006: SelectField reemplaza NativeSelect; React controlado y Radix portal/keyboard/foco. Variantes field/capsule; valor vacío mapeado a sentinel; botón quitar separado. Filtros, sort, rutas/fichas usan el componente. Datos/store/progress intactos. Las notas históricas de NativeSelect están superadas.

Updated 2026-10-07T17:39:13.733364+00:00. codex-root.

## Historical snapshot (superseded where noted)

# Architecture State

Frontend estático React + TypeScript + Vite. HashRouter evita 404 al recargar rutas en Pages. JSON original importado directamente. Fuse para búsqueda, Recharts diferido para oferta educativa, Zustand/localStorage para estado personal con firmas de IDs y exportación/importación revisable. Sin backend ni secretos. Python HTTP público propone cambios del radar mediante PR borrador; catálogo nunca actualizado automáticamente.

Updated: 2026-10-07T15:58:41.213865+00:00. Agent: codex-root.

## EDU-004

EDU-004 agrega NativeSelect, envoltorio nativo sin estado; CSS centraliza tokens y estados. Container query en .page permite reflow de rutas según ancho disponible. Dependencias, store y modelo de datos intactos.

Updated 2026-10-07T16:41:25.482577+00:00. codex-root.
