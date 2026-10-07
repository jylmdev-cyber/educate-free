# Identidad visual de EducaLibre

La interfaz usa azul tinta, turquesa y fondos de hielo para distinguir contenido, acciones y estados. La paleta se define en las variables de `:root` de [src/index.css](../src/index.css); los menús de Radix, gráficos y la ilustración comparten esos tokens.

| Rol | Token | Color |
| --- | --- | --- |
| Texto y marca | `--ink` | `#163B4C` |
| Acciones y selecciones | `--primary` | `#0B6E75` |
| Hover de acción | `--primary-hover` | `#07575D` |
| Texto secundario | `--muted` | `#526578` |
| Fondo general | `--canvas` | `#F3F7FB` |
| Tarjetas y menús | `--surface` | `#FFFFFF` |
| Selección y contexto | `--primary-soft` | `#E7F4F4` |
| Avisos | `--warning` | `#8A4B17` |
| Éxito | `--success` | `#176E57` |
| Estado cerrado | `--danger` | `#A63D44` |
| Foco de teclado | `--focus` | `#2463C7` |

Los gráficos combinan turquesa, azul y ámbar. Incluyen leyendas, valores y tablas complementarias; los estados conservan texto e iconos además del color.

## Tipografía

**Plus Jakarta Sans** es la familia de la interfaz, títulos, cifras y menús. La fuente variable admite pesos de 200 a 800; se usan pesos mayores en títulos y selecciones para crear jerarquía. Los títulos principales tienen un tamaño fluido y menor espaciado entre letras; el hero adapta su escala en móvil.

Se incluyen dos archivos WOFF2 en [src/assets/fonts](../src/assets/fonts): Latin y Latin-ext, que suman **49.076 bytes** (aproximadamente 48 KiB). La variante Latin cubre las letras acentuadas y la ñ del español. Las fuentes se sirven desde el mismo sitio, sin solicitudes a Google Fonts en tiempo de ejecución. Vite genera los nombres con hash y respeta la base de GitHub Pages.

`font-display: swap` permite mostrar texto durante la carga. El fallback es `system-ui`, `-apple-system`, Segoe UI y `sans-serif`. No se introduce una dependencia npm.

La distribución mantiene la [licencia SIL Open Font License 1.1](../src/assets/fonts/OFL.txt). Los archivos proceden de [Google Fonts](https://fonts.google.com/specimen/Plus+Jakarta+Sans), con licencia disponible en su [repositorio oficial](https://github.com/google/fonts/tree/main/ofl/plusjakartasans). Esta licencia corresponde a la fuente; la licencia principal de la aplicación continúa pendiente.

## Legibilidad y mantenimiento

- Contraste objetivo de texto normal: al menos **4,5:1**; controles y foco: al menos **3:1**. Referencia: [WCAG 2.2, contraste mínimo](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html).
- Los select conservan una altura mínima de 44 px, estados deshabilitados y soporte para colores forzados. En móvil se compacta el espacio interno de las cápsulas para acomodar las nuevas métricas de fuente.
- Modifica los tokens compartidos al cambiar colores. Conserva el significado de los estados y revisa su contraste en el fondo real.
- Al sustituir la fuente, conserva su licencia, comprueba acentos y ñ, rutas de assets, pesos, ajuste en móvil y funcionamiento sin fuentes remotas.
- La revisión automática y la emulación móvil no equivalen a una certificación completa ni a pruebas con dispositivos físicos o lectores de pantalla.
