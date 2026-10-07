# Contribuir a EducaLibre

Gracias por ayudar a mejorar el acceso a formación. Este repositorio combina una SPA, un catálogo documentado y herramientas de monitoreo; cada cambio debe conservar su trazabilidad.

## Preparación

1. Usa Node.js 24+ y ejecuta `npm ci`.
2. Inicia la app con `npm run dev`.
3. Instala Python 3.11+ para las pruebas del radar.
4. Lee [README.md](README.md) y [.pallaquino/AI_ENTRYPOINT.md](.pallaquino/AI_ENTRYPOINT.md). Los agentes deben recuperar continuidad y declarar/reservar archivos antes de editar.

## Flujo de trabajo

- Parte de `main` y crea una rama con nombre descriptivo, por ejemplo `feat/filtro-modalidad` o `docs/instalacion`.
- Explica el problema y el resultado esperado antes de cambiar contratos.
- Mantén el cambio acotado; añade capturas cuando afecte la interfaz.
- Usa mensajes Conventional Commits: `feat: ...`, `fix: ...`, `docs: ...`, `ci: ...` o `chore: ...`.
- Abre un PR utilizando la plantilla incluida y registra comandos realmente ejecutados. No marques una comprobación pendiente como aprobada.

La preparación local del titular sigue la política de autoría de PALLAQUINO. Quienes contribuyan deben usar su identidad real conforme a las reglas del proyecto; no copies la identidad del titular ni cambies configuración Git global mediante herramientas automatizadas.

## Calidad proporcional al cambio

| Cambio | Comprobaciones relevantes |
| --- | --- |
| Documentación | Enlaces relativos, comandos, versiones y afirmaciones; `npm run repo:check`. |
| Datos del catálogo | Fuentes oficiales, `npm run data:check`, Vitest y flujos afectados. |
| Lógica o persistencia | Types, lint, Vitest, compatibilidad de respaldos y E2E afectados. |
| Interfaz | Types, lint, build, E2E, teclado/foco y capturas de escritorio/móvil. |
| Radar | Cuatro pruebas Python; muestras controladas y semántica de señales. |
| Workflows | YAML, permisos, condiciones de deploy, rutas de artefactos y gates ejecutables localmente. |

El workflow de GitHub ejecuta la suite completa antes de publicar. Configura `PAGES_BASE` de la misma manera para build y E2E; los ejemplos están en el README.

## Contratos que deben preservarse

- No cambies IDs de cursos o rutas como parte de una corrección de texto.
- Los IDs de instituciones dependen del orden del watchlist; modificarlo requiere una migración del estado personal.
- Distingue costo de curso y credencial; no presentes lo desconocido como gratuito.
- Describe el análisis como oferta educativa, salvo que se incorpore otra base validada.
- Conserva el formato de respaldo y el resumen previo al reemplazo de datos.
- El radar genera señales; no convierte cambios de una página en convocatorias confirmadas.

## Dependencias

Usa `npm ci` para instalar. Si cambias dependencias, justifica la necesidad, revisa compatibilidad/licencia y conserva el lockfile. Dependabot crea propuestas; no se fusionan automáticamente. Ejecuta `npm audit --omit=dev` y los gates afectados.

## Archivos locales

No incluyas `node_modules/`, `dist/`, `.artifacts/`, evidencia local de PALLAQUINO, archivos `.env`, claves ni respaldos personales. `npm run repo:check` revisa candidatos e informa rutas/reglas sin imprimir valores de secretos. Su análisis es acotado y no sustituye una revisión del diff.

Para reportar un problema de datos, incluye el ID del curso y un enlace institucional público. Para fallos de UI, incluye navegador, tamaño de pantalla y pasos de reproducción.
