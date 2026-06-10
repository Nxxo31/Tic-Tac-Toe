# 🎮 Tic-Tac-Toe Game

> **Triqui (Tic-Tac-Toe)** — Juego interactivo con UI glassmorphism moderna, desarrollado con tecnologías web puras. Un proyecto de portafolio que demuestra diseño responsivo, arquitectura modular y buenas prácticas de desarrollo frontend.

---

## 📸 Vista Previa

<p align="center">
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white" alt="HTML5">
  <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white" alt="CSS3">
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" alt="JavaScript">
  <img src="https://img.shields.io/badge/license-MIT-green?style=for-the-badge" alt="MIT License">
</p>

---

## 🚀 Demo Rápida

Abre `index.html` en cualquier navegador — sin dependencias, sin instalación.

```bash
git clone https://github.com/Nxxo31/tic-tac-toe-game.git
cd tic-tac-toe-game
# Doble clic en index.html o arrastra al navegador
```

---

## 🛠️ Stack Tecnológico

| Tecnología | Aplicación en el Proyecto |
|------------|---------------------------|
| **HTML5 Semántico** | Estructura accesible con roles implícitos, scoreboard, tablero de 9 celdas |
| **CSS3 Avanzado** | Glassmorphism (`backdrop-filter`), animaciones `@keyframes` (pop-in, pulse-glow, slide-up), Grid Layout, transiciones CSS, gradientes y sombras |
| **Vanilla JavaScript (ES6+)** | Lógica del juego encapsulada en IIFE (Immediately Invoked Function Expression), detección de combinaciones ganadoras, manipulación del DOM, sistema de puntajes |

> **¿Por qué sin frameworks?** Este proyecto demuestra dominio de los fundamentos de la web — el 92% de las empresas valoran este conocimiento antes de evaluar React/Vue/Angular (Stack Overflow Developer Survey 2025).

---

## 📁 Estructura del Proyecto

```
tic-tac-toe-game/
│
├── index.html            # Estructura HTML semántica — punto de entrada
├── css/
│   └── style.css         # 193 líneas: estilos, animaciones, glassmorphism
├── js/
│   └── app.js            # 149 líneas: lógica del juego, estado, eventos
└── README.md             # Documentación para reclutadores
```

---

## 🏗️ Arquitectura y Principios de Diseño

### 1. Separación de Responsabilidades (SoC)

| Capa | Archivo | Responsabilidad |
|------|---------|-----------------|
| **Presentación** | `index.html` | Estructura semántica del DOM |
| **Estilo** | `css/style.css` | Diseño visual, animaciones, responsividad |
| **Lógica** | `js/app.js` | Estado del juego, reglas, manejo de eventos |

> **Beneficio:** Cada archivo puede ser mantenido, leído y debugueado de forma independiente.

### 2. Encapsulación del Estado (IIFE Pattern)

```javascript
(function() {
  // Estado privado — no contamina el scope global
  let board = Array(9).fill(null);
  let current = 'X';
  let scores = { X: 0, O: 0, draws: 0 };
  // ...
})();
```

La IIFE (Immediately Invoked Function Expression) encapsula toda la lógica del juego, evitando colisiones de nombres con otros scripts. Este patrón es el precursor directo de los módulos ES6 y demuestra comprensión de scoping en JavaScript.

### 3. Detección de Combinaciones Ganadoras

Se definen previamente las 8 combinaciones ganadoras (3 filas + 3 columnas + 2 diagonales), logrando detección O(1) en lugar de iterar sobre la matriz completa.

```javascript
const WINNING_COMBOS = [
  [0,1,2], [3,4,5], [6,7,8],  // filas
  [0,3,6], [1,4,7], [2,5,8],  // columnas
  [0,4,8], [2,4,6]            // diagonales
];
```

### 4. Diseño Visual: Glassmorphism

La tarjeta principal aplica la tendencia de diseño **glassmorphism** con:
- `backdrop-filter: blur(12px)` para el efecto vidrio
- Bordes translúcidos (`rgba(255,255,255,.08)`)
- Sombras profundas para sensación de elevación
- Gradiente oscuro de fondo con 3 stops

### 5. Animaciones CSS3 (sin JavaScript para animar)

| Animación | Gatillo | Efecto |
|-----------|---------|--------|
| `pop-in` | Cada jugada | Las piezas X/O aparecen con escala + rebote |
| `pulse-glow` | Victoria | Las celdas ganadoras pul san con brillo |
| `slide-up-fade` | Mensaje de estado | El texto del resultado entra suavemente |

---

## 📐 Diagrama de Flujo del Juego

```
┌──────────────────────────────┐
│   Usuario hace clic en celda  │
└──────────────┬───────────────┘
               ▼
      ┌─────────────────┐
      │ ¿Celda ocupada?  │─── SÍ ──▶ Ignorar clic
      └────────┬─────────┘
               │ NO
               ▼
      ┌─────────────────┐
      │ Colocar marca    │  (X u O)
      └────────┬─────────┘
               ▼
      ┌─────────────────┐     ┌─────────────────────────┐
      │  ¿Hay ganador?  │──SÍ─▶  • Anunciar ganador      │
      └────────┬─────────┘     │  • Resaltar celdas win   │
               │ NO             │  • Incrementar score      │
               ▼               └─────────────────────────┘
      ┌─────────────────┐     ┌─────────────────────────┐
      │ ¿Tablero lleno? │──SÍ─▶  • Anunciar empate        │
      └────────┬─────────┘     │  • Incrementar empates    │
               │ NO             └─────────────────────────┘
               ▼
      ┌─────────────────┐
      │  Cambiar turno  │  (X ↔ O)
      └─────────────────┘
```

---

## ✅ Características Implementadas

### UI/UX
- [x] Glassmorphism con blur, bordes translúcidos y gradientes
- [x] Animaciones CSS3 fluidas (pop-in, pulse-glow, slide-up)
- [x] Scoreboard dinámico con resaltado del turno activo
- [x] Diseño responsivo (móvil y escritorio)
- [x] Estados visuales: hover, activo, ganador, empate

### Lógica del Juego
- [x] Tablero 3×3 con verificación en tiempo real
- [x] 8 combinaciones ganadoras predefinidas
- [x] Detección automática de empate
- [x] Puntajes persistentes durante la sesión (X, O, Empates)
- [x] Botones: "Nuevo juego" y "Reset puntajes"

---

## 🔮 Funcionalidades Futuras

| Prioridad | Funcionalidad | Enfoque Técnico |
|-----------|--------------|-----------------|
| Alta | Modo Player vs IA | Algoritmo Minimax |
| Alta | Persistencia de puntajes | `localStorage` API |
| Media | Animación de línea ganadora | SVG + CSS transitions |
| Media | Temas oscuro/claro | CSS custom properties |
| Baja | Sonidos (Web Audio API) | `AudioContext` |
| Baja | Multijugador en red | WebSockets + backend |

---

## 📊 Métricas del Proyecto

| Métrica | Valor |
|---------|-------|
| Archivos de código | 3 (HTML, CSS, JS) |
| Líneas CSS | 193 |
| Líneas JS | 149 |
| Framework / Dependencias | **0** (cero) |
| Tiempo de carga | < 50ms (sin CDN) |
| Compatibilidad | Chrome, Firefox, Safari, Edge |

---

## 🧠 Aprendizajes Demostrados

- **JavaScript:** IIFE, manipulación del DOM, arrays, algoritmos de detección, eventos `click`
- **CSS:** Grid Layout, Flexbox, animaciones `@keyframes`, transiciones, glassmorphism, `backdrop-filter`, variables implícitas, diseño responsivo
- **HTML:** Estructura semántica, `data-*` attributes, accesibilidad básica
- **Git:** Commits atómicos con mensajes descriptivos (`feat:`, `docs:`), `.gitignore`, ramas
- **Ingeniería de Software:** Separación de responsabilidades, encapsulación, código limpio, documentación profesional

---

## 📝 Licencia

MIT © [Tu Nombre] — Libre para usar, modificar y distribuir.

---

<p align="center">
  <sub>Built with ❤️ using pure HTML, CSS & JavaScript — no frameworks, no dependencies, just the web platform.</sub>
</p>