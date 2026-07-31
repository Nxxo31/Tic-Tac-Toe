# PROJECT.md — Triqui (Tic-Tac-Toe)

> **Estado:** Activo | **Versión:** 2.0.0 | **Última actualización:** 2026-07-31
> **Repositorio:** https://github.com/Nxxo31/triqui
> **Deploy:** https://triqui-coral.vercel.app

---

## 🎯 Objetivo Principal

Tic-Tac-Toe web con IA invencible (Minimax + Alpha-Beta pruning), estética glassmorphism responsive, theme toggle persistente, sonidos Web Audio API y capacidad PWA offline-first — cero dependencias npm, vanilla puro.

## 🎯 Objetivos Secundarios

1. Modo PvP (2 jugadores locales) y modo vs IA con dificultad Fácil (aleatorio) / Imposible (Minimax)
2. Scoreboard y leaderboard persistentes en localStorage
3. PWA con service worker (cache-first assets, network-first HTML) para offline
4. Animaciones SVG de línea ganadora, confetti en victoria, shake en empate
5. Theme toggle (dark/light) persistente + sonidos move/win/draw via Web Audio API

---

## 📐 Arquitectura

### Stack Tecnológico

| Capa | Tecnología | Versión | Propósito |
|------|-----------|---------|-----------|
| UI | HTML5 semántico | — | Estructura accesible |
| Estilos | CSS3 | — | Grid, Glassmorphism, Animations, Custom Properties |
| Lógica | Vanilla JavaScript | ES6+ | IIFE, State Machine, IA |
| IA | Minimax + Alpha-Beta Pruning | — | Búsqueda exhaustiva del árbol de juego (3x3 → 9! ≈ finito) |
| Persistencia | localStorage | — | Scoreboard, leaderboard, theme |
| Audio | Web Audio API | — | SFX move/win/draw (sin assets externos) |
| PWA | Service Worker | v1 | cache-first assets, network-first HTML |
| Deploy | Vercel | — | Sin build step, static hosting |

### Diagrama de Arquitectura

```
┌─────────────────────────────────────────────────────┐
│               Capa CLIENTE (Browser)                 │
│  [index.html] → [js/app.js (IIFE, State Machine)]    │
│  → [css/style.css (glassmorphism + neon)]            │
│  → [SVG ganador animado + Confetti + Shake]           │
│  → [Web Audio SFX] + [theme toggle persistente]       │
├─────────────────────────────────────────────────────┤
│               Capa IA                                │
│  [Minimax + Alpha-Beta] → evaluación de heurística    │
│  (Fácil: random · Imposible: Minimax óptimo)         │
├─────────────────────────────────────────────────────┤
│               Capa DATOS / PWA                       │
│  [localStorage: scoreboard/leaderboard/theme]        │
│  [sw.js (CACHE_VERSION: v1) — PWA offline-first]     │
└─────────────────────────────────────────────────────┘
```

### Flujo de Datos

```
[Click celda] → [app.js State Machine] → [validar movimiento] → [actualizar tablero]
  → (si vs IA) → [Minimax + Alpha-Beta] → [mejorMove] → [actualizar]
  → [detectar fin: win/draw?] → [animación SVG línea + sonidos + confetti/shake]
  → [actualizar localStorage scoreboard/leaderboard] → [render]
```

---

## 📊 Matriz de Trazabilidad

| Req ID | Descripción | Componente | Estado | Verificación |
|--------|-------------|------------|--------|--------------|
| R-01 | Modo PvP (2 jugadores locales) | js/app.js | ✅ | Prueba manual + E2E pendiente |
| R-02 | Modo vs IA con Minimax + Alpha-Beta | js/app.js | ✅ | IA invencible verificada (no pierde) |
| R-03 | Dificultad Fácil (aleatorio) / Imposible (Minimax) | js/app.js | ✅ | Toggle de dificultad |
| R-04 | Animación SVG de línea ganadora con gradiente animado | js/app.js + css/style.css | ✅ | Inspección visual |
| R-05 | Confetti en victoria | js/app.js | ✅ | Inspección visual |
| R-06 | Efecto shake en empate | js/app.js + css/style.css | ✅ | Inspección visual |
| R-07 | Scoreboard persistente (localStorage) | js/app.js | ✅ | Reload → scoreboard conserva datos |
| R-08 | Leaderboard con historial de partidas (localStorage) | js/app.js | ✅ | Reload → leaderboard conserva |
| R-09 | PWA: manifest.json + service worker | manifest.json + sw.js | ✅ | Lighthouse PWA checklist |
| R-10 | Diseño glassmorphism responsive | css/style.css | ✅ | Prueba en mobile |
| R-11 | Headers de seguridad en vercel.json | vercel.json | ✅ | `/` responde con headers CSP |
| R-12 | Theme claro/oscuro persistente | js/app.js | ✅ | Toggle + reload conserva preferencia |
| R-13 | Sonidos move/win/draw (Web Audio API) | js/app.js | ✅ | Eventos de audio reproducidos |
| R-14 | Tests E2E con Playwright | playwright-package.json + triqui.spec.js | ⏳ | Pendiente — Issue #1 |

---

## 🏗️ Marcos Conceptuales

### Teoría de juegos — Minimax
Tic-Tac-Toe es un juego de suma cero determinista con information perfecta. El árbol de búsqueda es finito (3x3 = hasta 9 movimientos), así que Minimax explora exhaustivamente evaluando TERMINAL states (+1 win, 0 draw, -1 loss) y backpropaga el valor óptimo asumiendo que el oponente juga perfecto. Con Alpha-Beta Pruning se poda ramas que no afectan la decisión, reduciendo nodos explorados.

### State Machine explícita con IIFE
El patrón IIFE (Immediately Invoked Function Expression) encapsula todo el estado en closure, exponiendo solo handlers de UI. La máquina de estados simple (idle → playing → win/draw) evita bugs de race condition en eventos rápidos.

### PWA offline-first
Service worker con estrategia cache-first para assets (CSS, JS, iconos) y network-first para HTML — permite jugar offline después de la primera visita. `CACHE_VERSION` en sw.js controla invalidación: cambiarlo hace al browser descartar el cache anterior.

---

## ✅ Justificación de Decisiones Técnicas

| Decisión | Opción elegida | Alternativas evaluadas | Razón |
|----------|---------------|----------------------|-------|
| Stack | Vanilla JS puro (sin npm) | React, Vue, Svelte | Cero build step, binario descargable de un solo archivo; maximiza performance y portabilidad; demostración de dominio del DOM sin capas |
| IA | Minimax + Alpha-Beta | Red neuronal, tabla pre-computada | 3x3 es manso: Minimax exhaustivo es invencible en <1ms; Alpha-Beta poda para optimizar. Una tabla sería más rápido pero opaca y estática. |
| Persistencia | localStorage | IndexedDB, Cookies | 3 keys pequeñas (scoreboard, leaderboard, theme); localStorage es síncrono y suficiente; IndexedDB sería overkill |
| Audio | Web Audio API | `<audio>` con archivos mp3 | Sin assets externos (manifest requirement); osciladores generan tonos move/win/draw sin assets pesados |
| Animación ganador | SVG con gradiente animado | Canvas, GIF | SVG es vectorial escalable + accesible + CSS-animatable; GIF pierde calidad y Canvas sería overkill para una línea |
| PWA | Service Worker cache-first | No PWA | Offline-first.addon value; el SW se invalida con CACHE_VERSION bump |
| Deploy | Vercel (sin build step) | GitHub Pages, Netlify | Static hosting gratis; Vercel ya estaba configurado; GitHub Pages fue evaluado pero Vercel da mejor DX para PWA |

---

## 📦 Estado de Implementación

### Fases Completadas

| Fase | Descripción | Commit | Verificación |
|------|-------------|--------|--------------|
| V1 | Arquitectura inicial + PvP + vanilla JS | 0995844 | Prueba manual |
| V2 | Difficulty modes, PWA, leaderboard, animaciones SVG, confetti/shake | a95b22d | Deploy https://triqui-coral.vercel.app |
| V2.1 | AGENTS.md para contexto de agentes IA | 84c5d41 | — |
| V2.2 | GitHub templates CI 3-layer gates | e548eef | CI workflow |

### Próximos Pasos (Backlog)

| ID | Descripción | Prioridad | Issue |
|----|-------------|-----------|-------|
| B-1 | Tests E2E con Playwright | Alta | #1 |
| B-2 | Soporte multijugador online (WebSocket) | Media | — |
| B-3 | Sonidos avanzados (música + efectos espaciales) | Baja | — |
| B-4 | IA con dificultad Intermedia (Minimax limitado a profundidad N) | Baja | — |
| B-5 | Internacionalización (i18n ES/EN) | Baja | — |
| B-6 | Modo torneo con múltiples partidas | Baja | — |

---

## ⚠️ Limitaciones Conocidas

1. Sin tests automatizados — `playwright-package.json` y `triqui.spec.js` existen sin integrar al CI (Issue #1)
2. Solo PvP local — multijugador online requiere WebSocket backend (pendiente)
3. Dificultad "Intermedia" no existe — solo Fácil o Imposible (sin grado intermedio)
4. El cache del service worker requiere bump manual de `CACHE_VERSION` en sw.js al cambiar assets
5. Sin i18n — solo español

---

## 🔐 Seguridad

- Headers de seguridad en `vercel.json` (CSP, X-Frame-Options, X-Content-Type-Options)
- Sin backend ni formularios → sin superficie de ataque de servidor
- Sin dependencias externas → sin riesgo de supply chain
- localStorage solo persiste puntajes y preferencias (sin PII)

---

## 📚 Referencias

- [Minimax con Alpha-Beta Pruning — Wikipedia](https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning)
- [Service Workers — MDN](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API)
- [Web Audio API — MDN](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API)
- [PWA — web.dev](https://web.dev/learn/pwa/)

---

*Generado por SophIA — Sebastian Velasco's autonomous operating system*
