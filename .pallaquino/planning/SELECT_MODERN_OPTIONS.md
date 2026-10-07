# EDU-005 — Opciones modernas para los select

Estado: tres conceptos visuales entregados; selección pendiente. La aplicación conserva EDU-004.

Objetivo: comparar una estética más moderna y distintas formas de filtrar, manteniendo identidad verde, contenido del catálogo y seis dimensiones de filtrado. Son imágenes de concepto, sin implementación ni validación funcional nueva.

La numeración corresponde al orden real en que las imágenes se mostraron en esta conversación.

| Opción | Dirección | Diferencia | Impacto de una futura implementación |
| --- | --- | --- | --- |
| 1 | Campos suaves | Superficies tintadas, iconos discretos y etiqueta integrada dentro del campo | Puede conservar el select nativo; ajustes de componente/CSS y pruebas de reflow |
| 2 | Filtros en cápsulas | Barra compacta, filtros activos removibles y menú anclado | Cambia la estructura de filtros; requiere revisar interacción, foco y selección única |
| 3 | Menús con búsqueda | Selector con búsqueda interna para listas largas | Requiere combobox y controles de teclado, lectura accesible, estado vacío y posicionamiento |

Referencias: captura del navegador integrado, estilos y NativeSelect actuales. Paleta bosque #254e40, tinta #23352f, salvia y fondo claro. Generadas con Image Gen, cada dirección en una llamada independiente.

Imágenes durables y correspondencia exacta: `evidence/EDU-005/concepts.json`.

Observación de revisión: el menú abierto de la tercera imagen cubre parte de la segunda fila de filtros. En código deberán conservarse los seis controles, comprobar el posicionamiento y permitir cerrar el menú por Escape, clic exterior y navegación por teclado. Los mockups no demuestran contraste medido, foco real ni comportamiento móvil.

Criterios cumplidos: tres imágenes independientes, diferencias de estructura/interacción, contexto del producto conservado, aplicación intacta por SHA256, evidencia y continuidad actualizadas.

Siguiente paso: el usuario elige una imagen o solicita refinamientos. Luego se declara y reserva el alcance de implementación, se conserva el catálogo/progreso y se verifican accesibilidad, filtros, rutas, fichas y pantallas pequeñas. No se inicia una reconstrucción completa de la SPA.
