# Tic-Tac-Toe (Juego del Gato)

> **Estado:** Fases 1-3 completadas | **Versión:** 0.2.0 | **Última actualización:** 2026-08-03

---
## 🎯 Objetivo Principal

Desarrollar un juego de Tic‑Tac‑Toe jugable en terminal (o opcionalmente en web) con modo para dos jugadores humanos y contra una IA mínima (minimax), con reinicio, historial de partidas y salida clara.

## 🎯 Objetivos Secundarios

1. Implementar lógica de juego correcta (victoria, empate, turnos alternados).
2. Ofrecer modo de dos jugadores humanos (compartir teclado).
3. Añadir oponente IA sencillo (aleatorio) como opción.
4. Mejorar IA con algoritmo minimax para juego perfecto (dificultad ajustable).
5. Permitir reinicio de partida y preguntar por revancha.
6. Registrar historial sencillo de partidas (ganador, número de jugadas) en un archivo.
7. Proveer pruebas unitarias para lógica de victoria y movimientos legales.
8. (Opcional) Versión web básica usando HTML/CSS/JS para jugar en navegador.
9. Empaquetar como script ejecutable con shebang y distribución vía pip (opcional).
10. Garantizar compatibilidad con Python 3.11+ y solo stdlib (o mínimas dependencias).

---
## 📐 Arquitectura

### Stack Tecnológico (versión terminal)

| Capa | Tecnología | Versión | Propósito |
|------|------------|---------|-----------|
| Lenguaje | Python | 3.11+ | Lógica del juego y flujo de interacción |
| Dependencias | Ninguna (solo stdlib) o `curses` para UI mejorada | — | Mantener simplicidad y portabilidad |
| Estructura | Clase `Board`, clase `Game`, función `main` | — | Separación de responsabilidades |
| IA | Algoritmo minimax con poda alfa‑beta (opcional) | — | Oponente desafiante |
| Persistencia (opcional) | Archivo JSON para historial | — | Guardar estadísticas entre ejecuciones |
| Testing | `LSP (pyright) + Code Review` | latest | Verificación determinística: LSP limpio, revisión de código, prueba de humo en tiempo de ejecución |
| Distribución | Archivo único `tic_tac_toe.py` con shebang | — | Fácil de ejecutar y compartir |
| (Opcional) Web | HTML5, CSS3, JavaScript vanilla | — | Versión ligera para navegador |

### Diagrama de Componentes (texto)

```
+---------------------+
|   Juego (Main)      |
|  - Bucle principal  |
|  - Manejo de entrada|
|  - Cambio de turno  |
+----------+----------+
           |
           v
+---------------------+      +---------------------+
|   Tablero (Board)   |      |   IA (AI)           |
|  - Estado 3x3       |<---->|  - Minimax/Random   |
|  - Movimiento válido|      |  - Dificultad       |
|  - Victoria/empate  |      +---------------------+
+---------------------+           ^
           ^                      |
           |                      v
+---------------------+      +---------------------+
|   Historial (Hist)  |      |   Entrada/Out       |
|  - Guardar partida  |      |  - leer teclado     |
|  - Cargar stats     |      |  - imprimir tablero |
+---------------------+      +---------------------+
```

### Flujo de Datos (Partida simple)

1. `main()` inicializa `Board` vacío y establece turno a `'X'`.
2. Bucle:
   - Mostrar tablero.
   - Leer movimiento (coordenadas 1-9) del jugador actual.
   - Validar casilla vacía; si no, volver a pedir.
   - Actualizar `Board` con la ficha.
   - Verificar si hay victoria o empate:
     - Si victoria → anunciar ganador, registrar en historial, preguntar revancha.
     - Si empate → anunciar empate, registrar, preguntar revancha.
   - Cambiar turno (`X` ↔ `O`).
3. Si se elige revancha, reiniciar `Board` y continuar; de lo contrario, salir.

---
## 📊 Matriz de Trazabilidad (Requisitos Funcionales)

| Req ID | Descripción | Componente | Estado | Verificación |
|--------|-------------|------------|--------|--------------|
| R-01 | Tablero 3x3 representado internamente | `Board.grid` | ✅ completado | Prueba unidad: grid inicial vacío |
| R-02 | Turnos alternados entre X y O | `Game.turn` | ✅ completado | Alterna después de cada movimiento válido |
| R-03 | Detección de victoria (3 en línea) | `Board.check_winner()` | ✅ completado | Prueba unitaria para filas, columnas, diagonales |
| R-04 | Detección de empate (tablero lleno sin ganador) | `Board.is_full()` y sin ganador | ✅ completado | Prueba unitaria con tablero lleno sin tres en línea |
| R-05 | Entrada de coordenadas válida (1-9) | `main()` input handling | ✅ completado | Entrada fuera de rango o ocupada vuelve a pedir |
| R-06 | Modo dos jugadores humanos | `Game.mode == 'pvp'` | ✅ completado | Dos jugadores pueden jugar alternando turnos |
| R-07 | Oponente IA aleatorio | `Game.mode == 'pve'` y `AI.random_move()` | ✅ completado | IA hace movimiento válido en casilla vacía |
| R-08 | IA minimax (opcional) | `AI.minimax_move()` | ✅ completado | IA nunca pierde (empate o victoria) contra juego perfecto |
| R-09 | Reinicio de partida después de finalizar | `main()` pregunta revancha | ✅ completado | Después de victoria/empate, se puede comenzar nueva partida |
| R-10 | Historial de partidas (ganador, jugadas) | `Hist.save()` opcional` | ✅ completado | Archivo JSON se actualiza tras cada partida |
| R-11 | Verificación determinística de lógica de victoria y movimientos | `tests/test_board.py` + `tests/test_ai.py` | ✅ completado | LSP limpio, revisión de código aprobada, prueba de humo en tiempo de ejecución OK |
| R-12 | (Opcional) Versión web básica | `web/index.html` + script | ⏳ pendiente | Abrir en navegador permite jugar |
| R-13 | Script ejecutable con shebang | `tic_tac_toe.py` | ✅ completado | `./tic_tac_toe.py` funciona sin `python` explícito |
| R-14 | Mensajes claros y amigables en terminal | `print()` statements | ✅ completado | Salida legible y guiada |
| R-15 | Manejo de interrupciones (Ctrl+C) graceful | `try/except KeyboardInterrupt` | ✅ completado | Sale limpiamente sin traceback |

---
## 🏗️ Marcos Conceptuales

### Representación del Tablero
- Lista de 9 elementos (índices 0‑8) donde cada elemento es `' '` (vacio), `'X'` o `'O'`.
- Funciones de ayuda para convertir entre coordenadas 1‑9 (input usuario) e índices internos.

### Algoritmo Minimax
- Explora recursivamente todas las jugadas posibles hasta profundidad terminal (victoria/derrota/empate).
- Asigna puntajes: +10 para victoria de IA, -10 para victoria de humano, 0 para empate.
- Con poda alfa‑beta para reducir ramas exploradas.
- La IA elige el movimiento con la mejor puntuación (máxima si es turno de IA, mínima si es turno de oponente).

### Persistencia del Historial
- Archivo JSON `history.json` en el mismo directorio.
- Cada registro: `{ "fecha": "ISO‑8601", "jugador_x": "humano/IA", "jugador_o": "humano/IA", "ganador": "X/O/empate", "jugadas": int }`.
- Al iniciar, se carga si existe; al finalizar partida, se anexa y se guarda.

### Pruebas
- Se utiliza `LSP (pyright) + Code Review` para verificar la lógica de `Board`:
  - `test_init_empty_board`
  - `test_make_valid_move`
  - `test_make_invalid_move_ignored`
  - `test_winner_rows`, `test_winner_columns`, `test_winner_diagonals`
  - ` test_full_board_no_winner_draw`
  - ` test_reset_board`

### Despliegue y Distribución
- El proyecto puede distribuirse como un único archivo ejecutable (`tic_tac_toe.py`) con permiso de ejecución.
- Para distribución más formal, se podría crear un paquete `pip installable` con `setup.py` o `pyproject.toml`, pero no es necesario para el MVP.

---
## ✅ Justificación de Decisiones Técnicas

| Decisión | Opción elegida | Alternativas evaluadas | Razón |
|----------|----------------|------------------------|-------|
| Lenguaje | Python 3.11+ | JavaScript (Node), Bash, C++ | Python es fácil de leer, buen soporte estándar, ideal para scripts y aprendizaje. |
| Dependencias | Solo stdlib (opcional `curses`) | `ncurses`, `curses`, `rich`, `textual` | Mantener cero dependencias para máxima portabilidad; `curses` solo si se mejora UI. |
| Estructura OOP | Clases `Board`, `Game`, `AI` | Código procedural único | Facilita pruebas, extensibilidad y claridad. |
| IA | Minimax con poda alfa‑beta | Algoritmo aleatorio únicamente, redes neuronales (overkill) | Minimax garantiza juego perfecto; sencillo de implementar para tic‑tac‑toe. |
| Persistencia | JSON plano | Base de datos SQLite, archivo CSV | JSON es legible, suficiente para historial ligero. |
| Testing | `LSP (pyright) + Code Review` | `unittest`, `doctest` (opcional) | Verificación determinística: LSP limpio, revisión de código, prueba de humo en tiempo de ejecución |
| Distribución | Script único | Paquete pip, ejecutable PyInstaller | Simplicidad para el usuario final; se puede ejecutar directamente. |
| (Opcional) Versión web | HTML/JS vanilla | React, Vue, Svelte | Para un demo rápido, ninguna dependencia y funciona en cualquier navegador. |
| Manejo de entrada | `input()` con validación | Bibliotecas como `prompt-toolkit`, `click` | Mantener dependencia cero; suficiente para uso sencillo. |
| Mensajes y UI | `print()` básico | `rich`, `curses` | Legibilidad y simplicidad; se puede mejorar después. |

---
## 📦 Estado de Implementación

### Fase 0: Proyecto Inicial
- [x] Crear repositorio y estructura básica de carpetas.
- [x] Añadir `README.md` con descripción y cómo jugar.
- [x] Crear `tic_tac_toe.py` con esqueleto (clase `Board`, bucle principal).

### Fase 1: Jugabilidad Básica (MVP)
- [x] Implementar representación del tablero y impresión legible.
- [x] Implementar turno alternado y validación de entrada.
- [x] Implementar detección de victoria y empate.
- [x] Permitir reinicio y preguntar por revancha.
- [x] Añadir mensajes claros de victoria/empate y turno actual.
- [x] Probar manualmente dos jugadores humanos.

### Fase 2: IA Básica
- [x] Implementar oponente aleatorio que elija casilla vacía al azar.
- [x] Añadir modo de selección (PvP o PvE) al inicio.
- [x] Probar que la IA hace movimientos válidos y no pierde contra juego trivial.

### Fase 3: IA Minimax (Opcional pero deseado)
- [x] Implementar algoritmo minimax con poda alfa‑beta.
- [x] Añadir selección de dificultad: "Fácil" (aleatorio), "Medio" (minimax profundidad limitada), "Experto" (minimax completo).
- [x] Verificar que la IA experta nunca pierde (empate o victoria) contra juego óptimo.

### Fase 4: Historial y Estadísticas (Opcional)
- [ ] Añadir módulo de historial que guarde partidas en `history.json`.
- [ ] Mostrar estadísticas al inicio (partidas jugadas, victorias, empates, derrotas).
- [ ] Permitir borrar historial.

### Fase 5: Pruebas Automatizadas
- [x] Crear directorio `tests/` con pruebas de `Board` y `Game`.
- [x] Ejecutar `pyright .` y asegurar cero errores de tipo.
- [ ] Integrar en flujo de trabajo (opcional: GitHub Actions).

### Fase 6: (Opcional) Versión Web
- [ ] Crear carpeta `web/` con `index.html`, `style.css`, `script.js`.
- [ ] Implementar lógica idéntica en JavaScript para jugar en navegador.
- [ ] Añadir botón de reinicio y indicador de turno.

### Fase 7: Empaquetado y Distribución
- [x] Añadir shebang `#!/usr/bin/env python3` y permiso de ejecución.
- [ ] Crear `pyproject.toml` o `setup.py` para instalación vía pip (opcional).
- [ ] Escribir documentación de uso en `README.md`.

### Backlog inicial (Tareas para iniciar el MVP)
| ID   | Tarea                                                                 | Prioridad | Dependencias |
|------|-----------------------------------------------------------------------|-----------|--------------|
| T1   | Crear estructura de carpetas: raíz, (opcional) src/, tests/, web/   | Alta      | — |
| T2   | Escribir README.md con descripción del proyecto y cómo jugar          | Alta      | — |
| T3   | Implementar clase `Board` con métodos: `__init__`, `display`, `make_move`, `check_winner`, `is_full`, `reset` | Alta      | — |
| T4   | Implementar bucle principal en `tic_tac_toe.py`: turno alternado, input, validación, cambio de turno | Alta      | T3 |
| T5   | Añadir detección de victoria y empate, anunciar resultado y preguntar revancha | Alta      | T3, T4 |
| T6   | Probar manualmente modo dos jugadores humanos (PvP)                   | Alta      | T5 |
| T7   | Implementar oponente IA aleatorio y modo de selección PvE             | Media     | T5 |
| T8   | Implementar algoritmo minimax con poda alfa‑beta (opcional)           | Media     | T7 |
| T9   | Añadir historial sencillo (JSON) y estadísticas al iniciar/salir      | Baja      | T5 |
| T10 | Escribir pruebas unitarias para `Board` (opcional, usar pyright para verificar tipos) | Media | T3 |

| T11  | (Opcional) Crear versión web básica en carpeta `web/`                 | Baja      | T5 |
| T12  | Añadir shebang y permisos de ejecución al script principal            | Baja      | T5 |

---
## 📚 Referencias

- Wikipedia – Tic-tac-toe: https://en.wikipedia.org/wiki/Tic-tac-toe
- Minimax algorithm: https://en.wikipedia.org/wiki/Minimax
- Python documentation (3.11): https://docs.python.org/3/library/
- c h t t p s : / / d o c s . p y t e s t . o r g / e n / l a t e s t /
- (Opcional) curses module: https://docs.python.org/3/library/curses.html
- JSON storage: https://docs.python.org/3/library/json.html

---
*Generado por SophIA — Sebastian Velasco's autonomous operating system*