# EDU-003 — Plan de mejora de todos los select

Estado: PLAN ENTREGADO; implementación pendiente. Modo MAINTENANCE / autonomía STANDARD, inferidos del alcance de presentación solicitado. Riesgo LOW para la propuesta nativa. Responsable: codex-root; sin agentes adicionales. Skill: frontend_accessibility_expert.

## Objetivo y alcance

Dar a todos los select una apariencia uniforme, legible y coherente con EducaLibre: blanco cálido, verde bosque, bordes suaves y foco visible. El entregable actual es este plan. La implementación futura cubre todos los select existentes y conserva valores, eventos, etiquetas, filtrado, ordenamiento y progreso.

## Inventario confirmado por lectura del repositorio

| Contexto | Controles | Archivo | Situación actual |
|---|---|---|---|
| Catálogo y análisis | Ubicación, área, institución, gratuidad, inscripción, duración | src/components/Filters.tsx:12 | Seis controles compartidos; fuente 10 px, altura mínima 36 px, radio 7 px |
| Ordenamiento del catálogo | Recomendados / nombre / duración | src/App.tsx:47 | Fuente 10 px, 9 px en móvil; sin borde; ancho limitado |
| Ruta de aprendizaje | Agregar un curso | src/views/RoutesView.tsx:26 | Fuente 10 px, radio 5 px; lista larga con título e institución |
| Modal de ficha | Agregar a mi ruta | src/components/CourseDetail.tsx:24 | Comparte las reglas add-route; lista depende de rutas personales |

Nueve controles lógicos, cuatro sitios de definición JSX y quince usos entre vistas (6 + 6 + 1 + 1 + 1). TOP 15 no tiene un select propio; sus fichas usan el mismo modal. Radar no contiene select. Las reglas están repartidas en src/index.css:6, 12, 14, 72, 75, 94 y 101.

La lectura confirma estilos dispares y tamaños pequeños; no se declara una nueva auditoría visual o de accesibilidad aprobada. Las capturas/pruebas de EDU-002 constituyen evidencia histórica de la versión existente.

## Decisión de diseño

Crear un componente compartido `NativeSelect` en `src/components/ui/native-select.tsx`, envolviendo un `<select>` real. Usar clases y tokens propios con dos variantes: formulario y barra de herramientas. Ambas comparten tipografía, altura, radio, flecha y estados. Las diferencias se limitan al ancho y la ubicación.

No requiere dependencias nuevas. Conserva la selección nativa en móvil y los tests actuales basados en `selectOption`. El componente admite props estándar de select, className, ref, variante y una marca visual opcional `active` para filtros aplicados. No contiene lógica del catálogo ni del store.

El menú desplegado de un select tradicional sigue dependiendo del navegador/sistema operativo: CSS no garantiza opciones, scrollbars o estados hover idénticos en todas las plataformas. Mejorar su fuente/colores donde haya soporte sin comprometer la legibilidad. Si se requiere personalizar completamente ese menú, planificar una segunda tarea con una primitiva accesible y pruebas de teclado/portales dentro del modal. No mezclar ese cambio de interacción con esta primera mejora. [Referencia MDN: select y estilos](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/select#styling_with_css).

## Especificación visual propuesta

| Elemento | Objetivo |
|---|---|
| Altura | Mínimo 44 px en ambas variantes y en móvil |
| Texto del control | 14 px escritorio; 16 px móvil; line-height 1.4 |
| Etiqueta | 12 px, peso 600, separación de 6–8 px |
| Fondo y texto | Fondo blanco; texto de la paleta actual `--ink` |
| Borde | 1 px; color propuesto #7c8d7b, sujeto a medición de contraste |
| Radio | 10 px, coherente con controles y tarjetas |
| Espaciado | 12 px horizontal; reservar 36–40 px a la derecha para flecha |
| Flecha | ChevronDown de lucide ya instalado; decorativo, aria-hidden y pointer-events:none |
| Hover | Borde verde bosque, sin saltos de tamaño |
| Foco por teclado | Outline de 3 px con separación de 2–3 px, compatible con el foco azul existente |
| Filtro aplicado | Borde verde y fondo verde muy tenue; solo cuando difiere del valor de reset |
| Disabled | Fondo suave, texto legible y cursor adecuado; atributo disabled real |
| Error, cuando exista | aria-invalid y mensaje asociado; no introducir errores artificiales en filtros |

Estas medidas son objetivos de implementación, no resultados ya verificados. No depender únicamente del color para comunicar estados. En forced-colors mantener bordes/foco del sistema; ocultar flecha decorativa y restaurar appearance:auto si es necesario. Evitar animaciones de tamaño y respetar reduced-motion.

## Plan de ejecución

1. **Base compartida.** Definir tokens CSS para select y construir NativeSelect con flecha y props nativas. Mantener un único origen de estilos para ambas variantes.
2. **Filtros.** Migrar el helper Select de Filters.tsx. Conservar los seis aria-label y sus valores. Las opciones “Todas…” siguen siendo elecciones válidas de reset; no convertirlas en placeholders deshabilitados. Ajustar grid/espaciado con controles más altos.
3. **Ordenamiento.** Migrar App.tsx a la variante toolbar. Darle contorno y flecha consistentes, etiqueta accesible explícita, ancho suficiente para el valor elegido y disposición que pueda apilarse en móvil.
4. **Rutas y fichas.** Migrar RoutesView y CourseDetail. Alinear altura con el botón Agregar, contener nombres largos con min-width:0/width:100% y evitar que la flecha tape texto. Mantener nombre completo en el menú nativo. Definir presentación del estado vacío sin alterar IDs ni persistencia.
5. **Limpieza y adaptación.** Retirar propiedades duplicadas de `.filter-label select`, `.catalog-tools select`, `.add-route select` y sus overrides móviles. Asegurar que clases del wrapper no hereden reglas dirigidas a todos los span de etiquetas. Revisar a 320, 393, 768 y 1440 px y con zoom 200%.
6. **Validación y entrega.** Ejecutar gates indicados abajo, guardar capturas antes/después, registrar resultados reales, actualizar mapa/continuidad, liberar reservas y crear checkpoint/handoff.

Grafo de ejecución: base → filtros/ordenamiento/rutas/modal → limpieza responsive → validación → entrega. Un único agente ejecutará las migraciones de manera secuencial para evitar conflictos en index.css.

## Archivos de implementación previstos

- Nuevo: `src/components/ui/native-select.tsx`.
- Modificar: `src/index.css`, `src/components/Filters.tsx`, `src/App.tsx`, `src/views/RoutesView.tsx`, `src/components/CourseDetail.tsx`.
- Si se detecta cobertura funcional faltante: `tests/e2e/app.spec.ts`, con pruebas de selección, nombres accesibles y comportamiento real; no tests que reproduzcan valores CSS.
- Metadatos/evidencia PALLAQUINO de la tarea de implementación.

Estos archivos de aplicación están declarados como trabajo futuro: no se modificaron ni quedaron reservados durante la planificación. Reservarlos al iniciar la implementación. Informe original, catálogo, store, lockfile y workflows quedan fuera del cambio visual.

## Impacto, riesgos y mitigación

- Aumentar fuente/altura puede comprimir la fila del sorter y Agregar: permitir wrap/apilado y medir overflow.
- `appearance:none` puede ocultar affordance/foco del sistema: añadir flecha decorativa y comprobar forced-colors.
- Un wrapper mal ubicado puede romper labels o foco: mantener `<label>` y nombres accesibles; comprobar teclado dentro/fuera del modal.
- Opciones largas pueden ampliar el menú o recortar el valor cerrado: controlar ancho del campo, mantener contenido completo al seleccionar y revisar fuentes/duraciones largas.
- Reglas CSS heredadas pueden anular tokens: eliminar duplicados y revisar estilos computados en cada contexto.
- Menú nativo depende del navegador: documentar la variación y verificar plataformas; no prometer pixel-perfect entre sistemas.

Rollback de la implementación: restaurar solo los seis archivos modificados y retirar NativeSelect; sin migración de datos ni cambios de localStorage. Guardar copia previa si sigue sin existir Git. Restauración documental de esta planificación: `evidence/EDU-003/baseline/`.

## Criterios de aceptación

1. Los nueve controles lógicos usan el componente compartido; ninguna vista retiene estilos especiales de fuente/borde/altura.
2. Altura mínima 44 px y texto legible; texto/fondo cumple objetivo 4.5:1 y límites/foco pertinentes 3:1, comprobados en estados implementados.
3. Flecha visible y coherente; no tapa el valor ni intercepta interacción.
4. Tab/flechas/selección nativa funcionan; Escape/cierre de ficha y retorno de foco conservados. Sin cambios en valores, filtros, reset, ordenamiento o adición a rutas.
5. Nombres accesibles correctos y estado disabled real; el filtro por institución y la selección de curso siguen siendo utilizables con etiquetas largas.
6. Sin overflow horizontal a los anchos establecidos, zoom 200% ni recortes del modal. Menú del sistema puede variar entre plataformas.
7. Capturas de catálogo, análisis, rutas y modal, desktop/móvil, más evidencia de gates y limitaciones.

## Gates futuros, proporcionales a presentación

```text
npm run typecheck
npm run lint
npm test
PAGES_BASE=/educate-free/ npm run build
PLAYWRIGHT_CHANNEL=chrome PAGES_BASE=/educate-free/ npm run test:e2e
```

En PowerShell configurar variables con `$env:PAGES_BASE='/educate-free/'` y `$env:PLAYWRIGHT_CHANNEL='chrome'` antes de los comandos. Ejecutar las pruebas de navegador después de confirmar que el build terminó.

Reutilizar pruebas de filtros combinados, rutas, modal y teclado. Añadir solo escenarios reales que falten: ordenamiento, label del select en modal y selección por teclado. Axe y capturas de contraste/overflow complementan las pruebas funcionales. Revisar Chrome y Edge disponibles; Safari/Firefox/teléfono físico se registran como no verificados si no están disponibles. No se ejecutaron estos gates para estilos nuevos durante la planificación.

## Handoff

Solicitado y entregado: plan completo de estilos. Pendiente: implementación y su validación. Próxima acción: aplicar el plan cuando la tarea pase a implementación, reservar archivos previstos y mantener las funciones actuales. La publicación GitHub continúa pendiente del destino y no forma parte de este plan.
