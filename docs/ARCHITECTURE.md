## Estructura del Proyecto

```
triqui/
├── index.html          # Entry point - UI structure
├── css/
│   └── style.css       # Estilos glassmorphism + animaciones
├── js/
│   └── app.js          # Lógica del juego (IIFE)
├── vercel.json         # Configuración de Vercel + headers de seguridad
├── README.md           # Documentación del proyecto
└── docs/
    └── ARCHITECTURE.md # Decisiones técnicas y arquitectura
```

## Patrones Aplicados

- **IIFE**: Encapsulamiento del estado del juego sin exponer variables globales
- **State Machine**: El estado del juego (`active`, `current`, `board[]`) se modifica solo a través de funciones controladas
- **Minimax con Alpha-Beta Pruning**: IA óptima para Tic-Tac-Toe con complejidad O(b^d) reducida
- **localStorage API**: Persistencia de puntajes entre sesiones con validación de datos
- **SVG dinámico**: Línea ganadora calculada con coordenadas absolutas del DOM

## Decisiones Técnicas

| Aspecto | Decisión | Razón |
|---------|----------|-------|
| Sin framework | Vanilla JS | Cero dependencias, carga instantánea, demo de portafolio clean |
| Sin bundler | Archivos nativos | Deploy directo a Vercel sin build step |
| CSS Grid | Tablero 3x3 | Semántico, responsive sin media queries complejas |
| backdrop-filter | Glassmorphism | Tendencia visual 2024-2025, atractiva para portafolio |
| Minimax vs ML | Algoritmo clásico | Para Tic-Tac-Toe es óptimo y determinístico |

## Roadmap

- [x] Modo PvP
- [x] Modo vs IA (Minimax)
- [x] Animación SVG de línea ganadora
- [x] localStorage para puntajes
- [ ] Modo dificultad (Random / Medio / Imposible)
- [ ] Soporte multijugador online (WebSocket)
- [ ] Tema claro / oscuro

