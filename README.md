# 🎮 Triqui · Tic-Tac-Toe

[![Vercel](https://img.shields.io/badge/Deployed%20on-Vercel-black?logo=vercel)](https://triqui-coral.vercel.app)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

> Juego de Tic-Tac-Toe (Triqui) con IA invencible, diseño glassmorphism y animaciones fluidas.
> **🔗 Juega ahora:** [triqui-coral.vercel.app](https://triqui-coral.vercel.app)

---

## ✨ Características

- 🎯 **Dos modos de juego**: PvP (2 jugadores) y vs IA (Minimax)
- 🤖 **IA invencible**: Algoritmo Minimax con Alpha-Beta pruning
- 💾 **Persistencia**: Puntajes guardados en localStorage
- 🎨 **Diseño moderno**: Glassmorphism, gradientes y animaciones SVG
- 📱 **Responsive**: Funciona en móvil y desktop
- ⚡ **Zero dependencies**: Vanilla JS, sin frameworks ni builds

---

## 🛠 Stack Tecnológico

| Tecnología | Uso |
|------------|-----|
| **HTML5** | Estructura semántica |
| **CSS3** | Glassmorphism, Grid, Animaciones, backdrop-filter |
| **Vanilla JS** | Lógica del juego, IA Minimax, DOM manipulation |
| **SVG** | Línea ganadora animada |
| **Vercel** | Hosting + CI/CD |

---

## 🚀 Deploy

Deploy automático a Vercel en cada push a `main`:

```bash
vercel --prod
```

**URL de producción:** [triqui-coral.vercel.app](https://triqui-coral.vercel.app)

---

## 📁 Estructura del Proyecto

```
triqui/
├── index.html        # Entry point
├── css/
│   └── style.css     # Estilos glassmorphism
├── js/
│   └── app.js        # Lógica del juego + IA Minimax
├── vercel.json       # Configuración Vercel + headers de seguridad
├── docs/
│   └── ARCHITECTURE.md  # Documentación técnica
└── README.md         # Este archivo
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

### Algoritmo Minimax

La IA explora el árbol de posibilidades y elige el movimiento óptimo:

```
          Estado actual
         /      |      \
      X en 0  X en 1  X en 2  ... (9 ramas)
         |              |
     O responde    O responde
    /    |    \   /    |    \
  eval  eval  eval eval eval eval
```

- **Complejidad**: O(b^d) con poda Alpha-Beta
- **Resultado**: IA invencible (mejor resultado para humano = empate)

---

## 🎮 Cómo jugar

1. Abre [triqui-coral.vercel.app](https://triqui-coral.vercel.app)
2. Selecciona modo: **PvP** o **vs IA**
3. Haz click en una celda para jugar
4. ¡Gana quien complete 3 en línea!

> 💡 **Tip**: Contra la IA, el mejor resultado posible es empate. Intenta bloquear siempre.

---

## 🛡️ Seguridad

Headers de seguridad configurados en `vercel.json`:

| Header | Valor |
|--------|-------|
| X-Content-Type-Options | nosniff |
| X-Frame-Options | DENY |
| X-XSS-Protection | 1; mode=block |
| Referrer-Policy | strict-origin-when-cross-origin |

---

## 📄 Licencia

MIT © [Nxxo31](https://github.com/Nxxo31)

---

<p align="center">Hecho con ❤️ para portafolio profesional</p>
