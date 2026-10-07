# Subir EducaLibre a GitHub y publicar en Pages

Esta guía prepara la publicación del código y del sitio estático. El destino es [jylmdev-cyber/educate-free](https://github.com/jylmdev-cyber/educate-free). Los ejemplos reutilizables usan `OWNER` y `REPO`: sustitúyelos por tu cuenta/organización y el nombre real del repositorio.

Subir código a `main` inicia la validación de CI. Para publicar el sitio se necesita habilitar Pages y establecer explícitamente `ENABLE_PAGES_DEPLOY=true`.

## 1. Revisar la entrega local

La preparación inicializa Git en `main` y conserva el lockfile. Antes de subir:

```sh
git status
git log -1 --oneline
npm run repo:check
```

`.gitignore` excluye dependencias, builds, pruebas y evidencia local. El contenido del sitio se genera en `dist/`; esa carpeta se publica mediante Actions, no se añade al historial.

Si partes de una copia de carpeta sin `.git`, usa `git init -b main`, revisa los candidatos y crea tu primer commit con tu identidad Git local. No uses `git add --force` para introducir archivos excluidos.

## 2. Crear y conectar el repositorio

Crea un **repositorio vacío** en GitHub, sin README/LICENSE/.gitignore iniciales, para evitar historias independientes. Decide su visibilidad según tu proyecto. La disponibilidad de Pages en repositorios privados depende del plan, según [GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).

Con la URL real del repositorio:

```sh
git remote add origin https://github.com/OWNER/REPO.git
git remote -v
git push -u origin main
```

Si ya existe `origin`, inspecciónalo antes de cambiarlo. Si el remoto contiene commits, integra su historial deliberadamente; no fuerces el push. GitHub requiere un método de autenticación compatible con Git/CLI; no pongas credenciales en la URL ni en archivos del proyecto.

Alternativamente, si tienes GitHub CLI autenticado y quieres crear un repositorio público nuevo:

```sh
gh repo create OWNER/REPO --public --source=. --remote=origin --push
```

Ese comando **crea un repositorio público y sube código**; úsalo solo después de decidir el destino y visibilidad. Para privado, cambia `--public` por `--private`. Ningún remoto se crea automáticamente al ejecutar la app.

## 3. Activar Pages

1. Abre **Settings → Pages → Build and deployment**.
2. En **Source**, selecciona **GitHub Actions**.
3. En **Settings → Secrets and variables → Actions → Variables**, crea la variable **ENABLE_PAGES_DEPLOY** con valor **true**.
4. Abre **Actions → Validate and deploy EducaLibre**.
5. Ejecuta **Run workflow** sobre `main` si el primer push ocurrió antes de activar Pages.
6. Espera que `validate` y `deploy` terminen correctamente.
7. Abre la URL de salida del job `deploy` / entorno `github-pages`.

Si la variable está ausente o tiene otro valor, CI valida el código y omite el despliegue.

El [workflow](../.github/workflows/deploy.yml) tiene lectura de contenido por defecto. Solo el job de despliegue recibe `pages: write` e `id-token: write`. Publica únicamente `dist/` después de los controles cuando se habilita la variable; los pull requests validan sin desplegar. Configuración según la [guía oficial de workflows de Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).

## 4. Configurar la base del sitio

El workflow usa `vars.PAGES_BASE` cuando existe; de lo contrario calcula `/REPO/` a partir del nombre real del repositorio.

| Destino | PAGES_BASE | Ejemplo de URL, no una publicación existente |
| --- | --- | --- |
| Sitio de proyecto | `/REPO/` (automático) | `https://OWNER.github.io/REPO/#/` |
| Repositorio `OWNER.github.io` | `/` (configurar variable) | `https://OWNER.github.io/#/` |
| Dominio propio en la raíz | `/` (configurar variable) | `https://tu-dominio.example/#/` |

Define variables en **Settings → Secrets and variables → Actions → Variables → New repository variable**. `PAGES_BASE` es una ruta pública, no un secreto; debe empezar y terminar con `/`.

Para dominio propio, configura el dominio y DNS siguiendo [la documentación oficial](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site). Si usas un archivo `CNAME`, colócalo en `public/` con el dominio real y comprueba que llegue a `dist/`. No se incluye un dominio ficticio en el proyecto.

HashRouter permite recargar `#/analisis`, `#/rutas` y las demás vistas sin reglas de servidor. Una base incorrecta impide cargar los assets antes de que el router se ejecute.

## 5. Verificación posterior al despliegue

- Abrir el catálogo desde la URL real y comprobar carga de CSS/JS.
- Buscar y combinar filtros; abrir/cerrar fichas con teclado.
- Navegar a las cinco vistas y recargar una ruta con `#/`.
- Comprobar gráficos, rutas, progreso tras recarga y respaldo JSON.
- Revisar el radar y su fecha publicada; ausencia de chequeos es un estado válido inicial.
- Probar móvil y revisar consola/Network ante fallos.

La ejecución local no prueba el entorno remoto. Registra el enlace al run de Actions, su commit y URL antes de afirmar que la publicación fue validada.

## Radar automático opcional

El [workflow de radar](../.github/workflows/radar.yml) propone cambios los lunes a las 13:00 UTC / **08:00 Lima**, y también admite ejecución manual. Usa el `GITHUB_TOKEN` del repositorio; no necesita un token personal en el código.

1. Si quieres usarlo, habilita **Settings → Actions → General → Workflow permissions → Allow GitHub Actions to create and approve pull requests**. Las políticas de organización pueden limitar esa opción. El workflow crea un borrador; no aprueba ni fusiona PRs.
2. Ejecuta el radar manualmente para obtener una primera línea base.
3. Revisa fuentes con señal `changed` y consultas fallidas antes de fusionar.
4. Comprueba la validación del PR. GitHub puede pedir **Approve workflows to run** para PRs creados con `GITHUB_TOKEN`; sigue esa indicación o ejecuta manualmente la validación sobre la rama propuesta. Véase [la documentación de eventos generados por tokens](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow).
5. Tras fusionar, si no se inicia un despliegue por un cambio generado con el token, ejecuta **Validate and deploy EducaLibre** sobre `main`.

El artefacto `public-radar-proposal` queda disponible incluso si la creación del PR falla después de subir el artefacto. La app recibe señales nuevas cuando `radar-checks.json` forma parte de un build publicado.

El monitor no confirma matrícula, costos ni cupos y no modifica el informe. Mantén estable el orden del watchlist.

## Badges de CI y demo

El README incluye badges estáticos de versiones/configuración y un badge dinámico del workflow con el destino real. Para reutilizarlo en otro repositorio:

```markdown
[![Validación](https://github.com/OWNER/REPO/actions/workflows/deploy.yml/badge.svg?branch=main)](https://github.com/OWNER/REPO/actions/workflows/deploy.yml)
```

Reemplaza ambos `OWNER/REPO` antes de usarlo. Añade un enlace **Demo** usando la URL que entrega el job `deploy`. No publiques un badge de éxito o una URL de ejemplo como si fueran resultados reales.

## Problemas frecuentes

| Síntoma | Comprobar |
| --- | --- |
| Página sin estilos o assets 404 | Base de build, `PAGES_BASE`, nombre real del repo y barra final. |
| `deploy` falla al configurar Pages | Source = GitHub Actions, entorno `github-pages`, permisos Pages/OIDC y políticas de organización. |
| No hay deploy en un PR | Es intencional: publica únicamente `main` fuera de eventos pull_request. |
| No empieza CI del PR del radar | Buscar solicitud de aprobación o ejecutar validación manual sobre su rama. |
| Falta el navegador de Playwright local | `npx playwright install chromium`, o `PLAYWRIGHT_CHANNEL=chrome` si Chrome está instalado. |
| Radar sin señales nuevas en la web | Revisar PR, merge y build publicado; no basta con ejecutar el chequeo. |
| Progreso distinto después de cambiar URL | localStorage depende del origen; exportar/importar respaldo antes de migrar. |

## Volver a una versión anterior

Revierte el cambio mediante un nuevo commit/PR y permite que `main` publique la versión corregida. Conserva el historial y evita `push --force`. Un rollback de código no elimina localStorage; revisa compatibilidad de datos antes de retroceder cambios de persistencia.
