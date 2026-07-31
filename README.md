# 🎮 Triqui · Tic-Tac-Toe

[![CI](https://github.com/Nxxo31/Tic-Tac-Toe/actions/workflows/ci.yml/badge.svg)](https://github.com/Nxxo31/Tic-Tac-Toe/actions/workflows/ci.yml)
[![Vercel](https://img.shields.io/badge/Deployed%20on-Vercel-black?logo=vercel)](https://triqui-coral.vercel.app)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Minimax](https://img.shields.io/badge/AI-Minimax%20%2B%20Alpha--Beta-purple)](https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning)
[![PWA](https://img.shields.io/badge/PWA-Offline%20Ready-5A0EBF?logo=pwa&logoColor=white)](manifest.json)
[![Zero Deps](https://img.shields.io/badge/Dependencies-Zero-brightgreen)](https://triqui-coral.vercel.app)
[![HTML5](https://img.shields.io/badge/HTML5-Vanilla%20JS-orange?logo=javascript&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)

> Juego de Tic-Tac-Toe (Triqui) con IA invencible, diseño glassmorphism y animaciones fluidas.
> **🔗 Juega ahora:** [triqui-coral.vercel.app](https://triqui-coral.vercel.app)

---

## ✨ Características

### 🎮 Modos de Juego

- **PvP** (2 jugadores locales) — turnos alternados en el mismo dispositivo
- **vs IA** — dos niveles de dificultad:
  - 🟢 **Fácil**: Movimientos aleatorios (posible ganar)
  - 🔴 **Imposible**: Minimax + Alpha-Beta pruning (IA invencible — mejor resultado = empate)

### 🤖 IA Minimax con Alpha-Beta Pruning

La IA explora exhaustivamente el árbol de juego (3×3 = hasta 9! estados) y elige el movimiento óptimo garantizando que nunca pierde:

```
          Estado actual
         /      |      \
      X en 0  X en 1  X en 2  ... (9 ramas)
         |              |
     O responde    O responde
    /    |    \   /    |    \
  eval  eval  eval eval eval eval
```

- **Complejidad temporal**: O(b^d) reducida por poda Alpha-Beta
- **Resultado garantizado**: IA invencible (mejor resultado para humano = empate)
- **Latencia**: < 1ms por movimiento (3×3 es finito y pequeño)

### 🎨 Tema Claro/Oscuro (Theme Toggle)

- Toggle persistente vía `localStorage` (`triqui_theme`)
- Dark mode con glassmorphism neon (default)
- Light mode con gradientes suaves
- CSS Custom Properties para transiciones instantáneas

```javascript
// Persistencia del tema
let currentTheme = localStorage.getItem('triqui_theme') || 'dark';
applyTheme(currentTheme); // Aplica inmediatamente al cargar
```

### 🔊 Sonidos Web Audio API

Efectos de sonido generados con osciladores (sin assets externos):

| Evento | Sonido | Frecuencia |
|--------|--------|------------|
| Movimiento | Tono corto | 440 Hz |
| Victoria | Acuerdo ascendente | 523 → 784 Hz |
| Empate | Tono grave | 220 Hz |

No se cargan archivos de audio — todo se sintetiza con `Web Audio API` osciladores.

### 💾 Scoreboard y Leaderboard Persistentes

- Puntajes acumulados guardados en `localStorage`
- Leaderboard con historial de partidas (modo, dificultad, resultado, fecha)
- Modal de leaderboard con botón de limpiar historial

### 📱 PWA Offline-First

- `manifest.json` con iconos 192px y 512px
- `sw.js` con estrategia:
  - **Cache-first** para assets (CSS, JS, iconos)
  - **Network-first** para HTML
- `CACHE_VERSION` controla invalidación del cache
- Juega offline después de la primera visita

### 🎭 Animaciones

| Animación | Tecnología | Trigger |
|-----------|-----------|---------|
| Línea ganadora | SVG con gradiente animado | 3 en línea detectado |
| Confetti | JS DOM elemental | Victoria |
| Shake | CSS keyframes | Empate |
| Hover/Tap | CSS transitions | Interacción de celda |

---

## 🛠 Stack Tecnológico

| Tecnología | Uso |
|------------|-----|
| **HTML5** | Estructura semántica |
| **CSS3** | Glassmorphism, Grid, Animations, Custom Properties, backdrop-filter |
| **Vanilla JS (ES6+)** | Lógica del juego, IA Minimax, State Machine, PWA |
| **SVG** | Línea ganadora animada |
| **Web Audio API** | SFX move/win/draw (osciladores, sin assets) |
| **localStorage** | Scoreboard, leaderboard, theme persistence |
| **Service Worker** | PWA offline-first (cache-first assets, network-first HTML) |
| **Vercel** | Hosting + CI/CD |

**Cero dependencias npm.** No hay `node_modules`, no hay build step. Vanilla puro.

---

## 📁 Estructura del Proyecto

```
triqui/
├── index.html          # Entry point HTML semántico
├── css/
│   └── style.css       # Glassmorphism, animaciones, responsive
├── js/
│   └── app.js          # Lógica del juego + IA Minimax + State Machine
├── manifest.json        # PWA manifest (iconos, theme, display)
├── sw.js               # Service Worker (cache-first, network-first)
├── icon-192.png        # PWA icon (192×192)
├── icon-512.png        # PWA icon (512×512)
├── vercel.json         # Configuración Vercel + headers de seguridad
├── docs/
│   └── ARCHITECTURE.md  # Documentación técnica
├── playwright-package.json  # Tests E2E (pendiente Issue #1)
├── triqui.spec.js           # Playwright spec (pendiente integración CI)
└── README.md           # Este archivo
```

---

## 🧠 Arquitectura

El proyecto sigue un patrón **IIFE (Immediately Invoked Function Expression)** para encapsular el estado del juego sin variables globales.

Para detalles técnicos completos, véase [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

### Flujo del juego

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Usuario    │────▶│  makeMove()  │────▶│ checkWinner()│
│  hace click │     └──────────────┘     └──────┬──────┘
└─────────────┘                                  │
                                                  ▼
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Reset /    │◀────│  updateTurn()│◀────│   Ganador?  │
│  Nueva ronda│     └──────────────┘     └─────────────┘
└─────────────┘
```

```
[Click celda] → [State Machine] → [validar movimiento] → [actualizar tablero]
  → (si vs IA) → [Minimax + Alpha-Beta] → [mejorMove] → [actualizar]
  → [detectar fin: win/draw?] → [animación SVG + sonidos + confetti/shake]
  → [actualizar localStorage scoreboard/leaderboard] → [render]
```

---

## 🎮 Cómo jugar

1. Abre [triqui-coral.vercel.app](https://triqui-coral.vercel.app)
2. Selecciona modo: **PvP** o **vs IA**
3. Si vs IA, elige dificultad: **Fácil** o **Imposible**
4. Haz click en una celda para jugar
5. ¡Gana quien complete 3 en línea!

> 💡 **Tip**: Contra la IA en modo Imposible, el mejor resultado posible es empate. Intenta bloquear siempre.

---

## 🛡️ Seguridad

Headers de seguridad configurados en `vercel.json`:

| Header | Valor |
|--------|-------|
| `Content-Security-Policy` | default-src 'self' |
| `X-Content-Type-Options` | nosniff |
| `X-Frame-Options` | DENY |
| `X-XSS-Protection` | 1; mode=block |
| `Referrer-Policy` | strict-origin-when-cross-origin |

Sin backend, sin formularios, sin superficie de ataque de servidor. localStorage solo persiste puntajes y preferencias (sin PII).

---

## 📊 Estado del Proyecto

| Componente | Estado | Verificación |
|------------|--------|--------------|
| PvP (2 jugadores) | ✅ Completo | Prueba manual |
| IA Minimax + Alpha-Beta | ✅ Completo | IA invencible verificada |
| Dificultad Fácil/Imposible | ✅ Completo | Toggle funcional |
| Animación SVG ganadora | ✅ Completo | Inspección visual |
| Confetti + Shake | ✅ Completo | Inspección visual |
| Scoreboard persistente | ✅ Completo | Reload conserva datos |
| Leaderboard | ✅ Completo | Modal con historial |
| Theme toggle | ✅ Completo | Persistente en reload |
| Sonidos Web Audio API | ✅ Completo | SFX reproducidos |
| PWA offline-first | ✅ Completo | Lighthouse PWA checklist |
| Tests E2E Playwright | ⏳ Pendiente | Issue #1 |

---

## 📄 Licencia

MIT © [Nxxo31](https://github.com/Nxxo31)

---

<p align="center">Hecho con ❤️ para portafolio profesional</p>
