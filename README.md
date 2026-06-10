# ✦ Triqui - Tic-Tac-Toe

> Un juego moderno de **Triqui** (Tic-Tac-Toe / Tres en Raya) diseñado con una interfaz glassmorphism y experiencia de usuario interactiva. Construido completamente en un solo archivo HTML independiente con tecnologías web puras — sin frameworks, sin dependencias externas.

---

## 🎮 Demo / Uso

Simplemente abre `index.html` en cualquier navegador moderno:

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/triqui.git
cd triqui

# Abrir en el navegador (Linux/macOS)
open index.html

# O simplemente doble clic en el archivo
```

---

## 🛠️ Stack Tecnologico

| Tecnologia | Uso |
|------------|-----|
| **HTML5** | Estructura semantica del juego |
| **CSS3** | Estilos modernos, animaciones, glassmorphism, responsive design |
| **Vanilla JavaScript (ES6+)** | Logica del juego, manipulacion del DOM, eventos |

**Sin dependencias externas.** No se requiere npm, Webpack, ni ningun framework.

---

## 🏗️ Arquitectura del Proyecto

```
triqui/
├── index.html          # Punto de entrada (UI + estructura)
├── css/
│   └── style.css       # Estilos, animaciones y diseño responsivo
├── js/
│   └── app.js          # Logica del juego, estado y manejo de eventos
└── README.md           # Documentacion
```

### Principios de Diseno Aplicados

- **Modularidad**: Separacion de responsabilidades — HTML estructura, CSS presentacion, JS comportamiento.
- **Encapsulacion**: Codigo JavaScript envuelto en IIFE (Immediately Invoked Function Expression) para evitar contaminacion del scope global.
- **Estado centralizado**: Un solo objecto `board[]` y variables controlan todo el flujo del juego.
- **DOM eficiente**: Re-renderizado selectivo sin librerias externas.

---

## ⚙️ Caracteristicas Implementadas

### 🎨 UI/UX
- **Glassmorphism**: Tarjeta principal con `backdrop-filter: blur` y bordes translucidos sobre un gradiente oscuro.
- **Animaciones fluidas**: Entrada de piezas (`pop-in`), pulso de celdas ganadoras (`pulse-glow`), transiciones de estado.
- **Scoreboard dinamico**: Marcador en tiempo real con resaltado del jugador activo.
- **Responsive**: Se adapta a moviles y escritorio.
- **Interaccion visual**: Hover effects, cambios de escala, sombras gradiente.

### 🧠 Logica del Juego
- Tablero 3x3 con verificacion de combinaciones ganadoras.
- Detecta victorias por filas, columnas y diagonales.
- Detecta empates automaticamente.
- Sistema de puntos persistente durante la sesion (X, O y Empates).
- Reset de tablero y reset completo de puntajes.

---

## 📊 Diagrama del Flujo del Juego

```
Usuario hace clic en celda
        |
        v
+-------------------+
|  Celda ocupada?  +--SI--> Ignorar
+-------------------+
        | NO
        v
+-------------------+
|  Colocar marca   |(X u O)
+-------------------+
        |
        v
+-------------------+    +------SI------> Anunciar ganador
|  Hay ganador?     |    |                Resaltar celdas
+-------------------+    |                Actualizar score
        |                |
        | NO             |
        v                |
+-------------------+    |
|  Tablero lleno?   +---SI------> Anunciar empate
+-------------------+           Actualizar score
        |
        | NO
        v
+-------------------+
|  Cambiar turno    |
+-------------------+
```

---

## 🚀 Mejoras Futuras

- [ ] Modo Player vs IA (Minimax)
- [ ] Modulo de sonidos (Web Audio API)
- [ ] Animacion de linea ganadora
- [ ] Temas oscuro/claro
- [ ] Persistencia de puntajes en localStorage
- [ ] Multijugador en red (WebSockets)

---

## 📝 Licencia

MIT — Libre para usar, modificar y distribuir.

---

<p align="center"><i>Construido con pureza web — HTML, CSS y JS sin adornos.</i></p>
