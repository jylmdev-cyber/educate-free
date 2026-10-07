# Validación y alcance

La evidencia local de ingeniería se conserva en `.pallaquino/evidence/`, los checkpoints en `.pallaquino/continuity/checkpoints/` y el handoff en `.pallaquino/continuity/HANDOFF.json`; se excluyen de Git por contener resultados, baselines y referencias de la máquina. Las políticas, herramientas y notas de continuidad permanecen versionadas. CI adjunta su propia evidencia como artefacto de Actions.

## Suite disponible

| Control | Cobertura |
| --- | --- |
| `npm run data:check` | Contrato de 95 ofertas, 15 recomendaciones, cuatro rutas y 20 instituciones. |
| TypeScript / ESLint | Tipos y análisis estático. |
| Vitest: 15 pruebas | Búsqueda, filtros y contratos/progreso/respaldo. |
| Python: cuatro pruebas | Baseline/cambios, fallo de acceso, desafíos de acceso y URL insegura. |
| Playwright: 20 casos | Diez escenarios en escritorio y móvil emulado. |
| axe en E2E | Cinco vistas, fichas y menús dentro de los escenarios ejecutados. |
| Build / audit | Producción estática y vulnerabilidades reportadas del árbol de producción. |
| `npm run repo:check` | Candidatos de Git, exclusiones, tamaños y patrones conocidos de secretos. |

## Escenarios de navegador

- Filtros combinados, quitar uno sin perder otros y reiniciar todos.
- Ordenamiento, favoritos y fichas de cursos.
- Teclado Home/End/typeahead, foco, Escape y modales anidados.
- Rutas sin opciones disponibles; creación, edición, reordenamiento y progreso persistente.
- Exportación/importación con resumen y rechazo de datos ajenos.
- Cinco vistas, gráficos, radar y navegación por subruta.
- Anchos 320/393/768/1440, valores largos y colores forzados.

La última validación de controles anterior a la preparación GitHub fue EDU-006, el **7 de octubre de 2026**: 15 Vitest, cuatro Python, 20 E2E, types/lint/build/data/audit aprobaron; el audit de producción reportó cero vulnerabilidades. El componente fue comparado contra el diseño elegido con capturas IAB de escritorio/móvil y revisión visual documentada. Estos resultados locales no sustituyen un run de Actions.

EDU-007 verifica adicionalmente documentación, higiene Git, autoría y salidas CI; sus comandos/fechas/códigos de salida se registran localmente, sin inventar estado remoto.

## Límites de las afirmaciones

- Móvil emulado no equivale a dispositivos físicos.
- No se ha validado Safari, un lector de pantalla real ni zoom mediante la UI del navegador para esta entrega.
- axe y revisión propia son controles acotados, no una certificación completa ni una auditoría independiente.
- El scanner de repositorio busca patrones conocidos; un resultado sin hallazgos no garantiza ausencia universal de secretos.
- El audit npm depende de vulnerabilidades conocidas y no sustituye revisión del código.
- No se ha ejecutado GitHub Actions ni publicado un sitio remoto durante la preparación local.
- El radar detecta contenido público, no matrícula autenticada ni convocatorias confirmadas.

Para comprobar una publicación, registra su URL real, SHA del commit y enlace al run de Actions siguiendo [DEPLOYMENT.md](DEPLOYMENT.md).
