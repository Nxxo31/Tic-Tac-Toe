# Triqui — Project State

> **Repositorio:** https://github.com/Nxxo31/triqui
> **Deploy:** https://triqui-coral.vercel.app
> **Stack:** HTML + CSS + JS vanilla · PWA · Vercel

---

## Current Status (V2 — Activa)

### ✅ Completado
- Modo PvP (2 jugadores locales)
- Modo vs IA con Minimax + Alpha-Beta pruning
- Dificultad: Fácil (aleatorio) / Imposible (Minimax)
- Animación SVG de línea ganadora con gradiente animado
- Confetti en victoria
- Efecto shake en empate
- Scoreboard persistente (localStorage)
- Leaderboard con historial de partidas (localStorage)
- PWA: manifest.json + service worker (offline-first para assets)
- Diseño glassmorphism responsive
- Seguridad: headers en vercel.json

### 🔜 Próximos features (Roadmap)
- [ ] Tema claro / oscuro
- [ ] Soporte multijugador online (WebSocket)
- [ ] Sonidos al jugar / ganar

### 🧪 Testing pendiente
- `playwright-package.json` y `triqui.spec.js` (untracked) — setup de tests E2E sin integrar

---

## Stack

| Capa | Tecnología |
|------|-----------|
| UI | HTML5 semántico |
| Estilos | CSS3 (Grid, Glassmorphism, Animations, Custom Properties) |
| Lógica | Vanilla JS (IIFE, State Machine) |
| IA | Minimax con Alpha-Beta Pruning |
| Persistencia | localStorage |
| PWA | Service Worker (cache-first assets, network-first HTML) |
| Deploy | Vercel (sin build step) |

## Archivos clave

```
triqui/
├── index.html              # Entry point — estructura UI
├── css/style.css           # Estilos + animaciones
├── js/app.js               # Lógica del juego + IA (IIFE)
├── sw.js                   # Service Worker (CACHE_VERSION: v1)
├── manifest.json           # PWA manifest
├── vercel.json             # Config Vercel + headers seguridad
├── AGENTS.md               # Contexto para agentes IA
├── PROJECT.md              # Este archivo
├── README.md               # Documentación general
├── docs/ARCHITECTURE.md    # Documentación técnica
└── .gitignore
```

## Commits recientes

```
84c5d41 chore: add AGENTS.md for triqui
a95b22d feat(V2): difficulty modes, PWA, leaderboard, animations
0995844 feat: project architecture upgrade
...
```

## Reglas de desarrollo

- **Zero dependencias npm** — vanilla puro
- Cambios en `sw.js` → incrementar `CACHE_VERSION`
- Commits atómicos en español
- Probar en browser antes de commitear