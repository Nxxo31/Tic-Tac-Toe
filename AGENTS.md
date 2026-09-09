## PROJECT.md — Fuente de Verdad (OBLIGATORIO)
PROJECT.md es la **unica fuente de verdad** del estado, desarrollo y documentacion de este proyecto.
- Leer PROJECT.md ANTES de cualquier accion.
- Actualizar PROJECT.md DESPUES de cada desarrollo significativo.
- No crear .md separados para specs, docs o arquitectura — todo va en PROJECT.md.

# AGENTS.md — Tic-Tac-Toe (Juego del Gato)

**Versión:** 0.1.0 | **Generado:** 2026-08-01
**Proyecto:** `/home/sebas/proyectos/Tic-Tac-Toe/`
**Estado:** Inicio — Fase 0 completada (repo + estructura base), Fase 1 pendiente (MVP jugabilidad)

> **PROJECT.md es la fuente de verdad del estado del proyecto.** Este archivo describe CÓMO trabajar (reglas, arquitectura, patrones, verificación). PROJECT.md describe QUÉ (avance, métricas, decisiones). No duplicar datos de progreso aquí.

---

## Rol del Agente

Este archivo rige las reglas operacionales para cualquier agente (dev, orchestrator, research) que trabaje en este proyecto. Define:

- **Stack y arquitectura** — qué tecnologías, cómo se organiza el código
- **Fases de desarrollo** — lifecycle obligatorio, gate por gate
- **Verificación** — los 3 layers que deben pasar antes de commit
- **Reglas críticas** — constraints no negociables del proyecto

**Precedencia:** Instrucciones explícitas del usuario > global AGENTS.md > este archivo.

---

## Stack Tecnológico

| Capa | Tecnología | Versión | Propósito |
|------|-----------|---------|-----------|
| Lenguaje | Python | 3.11+ | Lógica del juego y flujo de interacción |
| Dependencias | Solo stdlib (cero deps) o `curses` opcional | — | Portabilidad máxima |
| IA | Algoritmo minimax con poda alfa-beta (opcional) | — | Oponente desafiante |
| Persistencia | JSON plano (`history.json`) | — | Historial ligero de partidas |
| Testing | `LSP (pyright) + Code Review` | latest | Verificación determinística: LSP limpio, revisión de código, prueba de humo en tiempo de ejecución |
| Distribución | Archivo único `tic_tac_toe.py` con shebang | — | Ejecución directa sin instalación |
| (Opcional) Web | HTML5 + CSS3 + JavaScript vanilla | — | Demo en navegador, cero deps |

**Regla hard:** Zero dependencias externas para el MVP. Solo se permite `curses` si se mejora la UI de terminal. Cualquier adición de dependencia requiere aprobación explícita.

---

## Arquitectura

### Estructura de Archivos (objetivo)

```
Tic-Tac-Toe/
├── tic_tac_toe.py          ← Script principal ( runnable: ./tic_tac_toe.py )
│     ├── class Board        ← Estado 3x3, validación, victoria/empate
│     ├── class Game         ← Bucle principal, turnos, modos (PvP/PvE)
│     ├── class AI           ← random_move() y minimax_move() con alfa-beta
│     ├── class History      ← Guardar/cargar partidas en JSON
│     └── def main()         ← Entry point, manejo de entrada, bloques try/except
├── tests/
│   └── test_board.py        ← Pruebas unitarias de Board (verificación determinística)
├── web/                     ← (Opcional, Fase 6)
│   ├── index.html
│   ├── style.css
│   └── script.js
├── pyproject.toml           ← (Opcional, Fase 7 — distribución vía pip)
├── history.json             ← Generado en runtime, NO se commitea
├── PROJECT.md
├── AGENTS.md
├── README.md
└── .gitignore
```

### Representación del Tablero

- Lista de 9 elementos (índices 0-8), cada uno `' '` (vacío), `'X'` o `'O'`.
- Input del usuario: coordenadas 1-9; conversión interna a índice 0-8 (`position - 1`).
- Ninguna representación alternativa (matrices 2D, dicts) — la lista plana es canónica.

### Separación de Responsabilidades

| Clase | Responsabilidad | No debe hacer |
|-------|----------------|----------------|
| `Board` | Estado del tablero, validación de movimientos, detección victoria/empate | Manejar turnos, entrada/salida, persistencia |
| `Game` | Bucle principal, alternar turnos, seleccionar modo (PvP/PvE), preguntar revancha | Conocer algoritmo de IA, escribir/leer historial directamente |
| `AI` | Elegir movimiento (aleatorio o minimax con poda alfa-beta) | Modificar Board directamente — debe retornar la posición elegida |
| `History` | Guardar/cargar partidas en `history.json` | Conocer lógica del juego o estado del tablero |
| `main()` | Entry point, manejo de `KeyboardInterrupt`, flujo general | Contener lógica de juego (delegar a Game/Board) |

### Algoritmo Minimax

- Explora recursivamente todas las jugadas hasta estado terminal (victoria/derrota/empate).
- Puntajes: `+10` victoria IA, `-10` victoria humano, `0` empate.
- Poda alfa-beta obligatoria para la dificultad "Experto".
- Dificultades: "Fácil" (aleatorio puro), "Medio" (minimax profundidad limitada), "Experto" (minimax completo con alfa-beta).
- **Invariante:** La IA en dificultad "Experto" NUNCA pierde contra juego óptimo. Verificación: jugar 100 partidas con movimientos óptimos contra IA — debe resultar en empate 100% de las veces.

---

## Reglas Críticas

1. **Solo stdlib.** Cero dependencias externas para el MVP. `curses` solo si se mejora UI de terminal y requiere decisión explícita.
2. **Python 3.11+.** Usar features modernas (match/case, type hints con `|`, `tomllib`) cuando aplique.
3. **OOP obligatorio.** Clases `Board`, `Game`, `AI`, `History` — no código procedural suelto.
4. **Manejo de `KeyboardInterrupt`.** Toda entrada de usuario debe estar envuelta en `try/except KeyboardInterrupt` para salida limpia sin traceback (R-15).
5. **Validación de entrada.** Input fuera de rango (no 1-9) o casilla ocupada debe volver a pedir — nunca lanzar excepción al usuario.
6. **`history.json` no se commitea.** Es un artefacto de runtime. Debe estar en `.gitignore`.
7. **Branch workflow.** `main` siempre verde, solo PRs. Features en `feature/<name>`, fixes en `fix/<name>`.
8. **Commits atómicos en español.** Formato: `feat: descripción`, `fix: descripción`, `docs:`, `refactor:`, `test:`, `chore:`.

---

## Fases de Desarrollo — Lifecycle Obligatorio

> **No es opcional.** Cada fase debe pasar antes de avanzar. Adaptado del global AGENTS.md lifecycle.

```
SPEC → IMPLEMENT → REVIEW (independiente) → SELF-REVIEW → VALIDATION → COMMIT
```

### Fase 1 — Spec

Antes de escribir código, definir dentro de PROJECT.md (Sprint Activo):
- Qué problema se resuelve
- Qué archivos se ven afectados
- Criterios de aceptación verificables

**No spec = no código.** No plan = no ejecución.

### Fase 2 — Implement

- Escribir código siguiendo las convenciones de este AGENTS.md.
- Tocar solo lo necesario para la tarea.
- Type hints en todas las firmas de funciones y métodos públicos.
- Docstrings en todas las clases y métodos públicos (Google style).

### Fase 3 — Review (independiente)

- Un subagente con contexto fresco revisa el diff adversarialmente.
- El agente que escribió el código NUNCA lo revisa.
- Retorna: PASS / FAIL (con issues) / NOTES (observaciones <80% confianza).
- Hallazgos críticos deben state un escenario de fallo concreto.

### Fase 4 — Self-Review

- ¿El diff matchea el spec?
- ¿Código muerto?
- ¿Error handling cubierto?
- ¿Nuevas dependencias? (Prohibido sin aprobación)

### Fase 5 — Validation (3 layers, todos obligatorios)

Ver sección "Verification Gates" abajo.

### Fase 6 — Commit

- Solo después de que todas las gates pasan.
- `git status --porcelain` debe estar limpio (excepto `.gitignore` y `PROJECT.md`).
- Commit atómico, mensaje descriptivo en español.
- `Closes #N` si hay issue asociado.

---

## Verification Gates — Compilar NO es funcionar

> **Principio: "Don't imagine — execute."** Un build que pasa solo prueba que el código compila. NO prueba que funcione.

### Layer 1 — Deterministic Gates (compila + estilo)

| Gate | Command | Qué valida |
|------|---------|------------|
| Syntax check | `python3 -m py_compile tic_tac_toe.py` | Compila sin errores |
| Lint | `python3 -m pyflakes tic_tac_toe.py` (si disponible) o `ruff check .` | Estilo + bugs comunes |
| Type check | `python3 -m mypy tic_tac_toe.py --ignore-missing-imports` (si disponible) | Types correctos |
| LSP Diagnostics (pyright) | `pyright .` | 0 errores de tipo |

Necesarios pero NO suficientes. Un syntax check exitoso no significa que el juego funcione.

### Layer 2 — Runtime Verification (el juego FUNCIONA)

Después de Layer 1, ejecutar el juego real y verificar comportamiento observable:

```bash
# Verificar imports reales (no solo syntax)
python3 -c "from tic_tac_toe import Board, Game, AI, main; print('imports OK')"

# Smoke test: crear tablero, hacer movimientos, verificar victoria
python3 -c "
from tic_tac_toe import Board
b = Board()
assert all(c == ' ' for c in b.grid), 'tablero no vacío'
b.make_move(0, 'X')
assert b.grid[0] == 'X', 'movimiento no aplicado'
assert b.check_winner() is None, 'no debería haber ganador aún'
print('Board OK')
"

# Ejecutar el script directamente (verificar shebang + runnable)
./tic_tac_toe.py <<< $'1\n5\n2\n4\n3\n'  # Simular entrada: X juega 1-5-2, O juega 4-3 (victoria diagonal X)

# Si hay IA: jugar contra ella y verificar que hace movimientos válidos
python3 -c "
from tic_tac_toe import Board, AI
b = Board()
ai = AI()
move = ai.random_move(b.grid)
assert 0 <= move <= 8 and b.grid[move] == ' ', f'movimiento IA inválido: {move}'
print(f'AI move OK: position {move}')
"
```

### Layer 3 — Adversarial Probes (intentar romperlo)

Después del happy path, probar casos edge:

- **Entrada inválida:** Input fuera de rango (0, 10, -1, letras), verificar que vuelve a pedir sin crash
- **Casilla ocupada:** Mover dos veces al mismo lugar, verificar que se rechaza
- **Tablero lleno sin ganador:** Llenar las 9 casillas sin 3 en línea, verificar detección de empate
- **Ctrl+C:** Enviar SIGINT durante `input()`, verificar salida limpia sin traceback
- **IA minimax invencible:** Jugar 100 partidas con movimientos óptimos contra IA "Experto" — debe ser 100% empates

**Reportar al menos UN adversarial probe ejecutado y su resultado.**

### Reglas de Verificación (NO NEGOCIABLES)

1. **No claims de completion sin runtime evidence.** Syntax OK ≠ funciona. Required: comando ejecutado + output observado.
2. **No asumir que algo funciona porque compila.** Un cascarón compila perfectamente.
3. **No confiar en self-reporting del subagente.** "Passes" sin output real = no verificado.
4. **Adversarial probe mandatory.** Al menos un caso edge probado, no solo happy path.
5. **Formato de evidence:** Para cada claim:
   - **Command run:** comando exacto ejecutado
   - **Output observed:** output real del terminal
   - **Result:** PASS o FAIL con Expected vs Actual

---

## Verificación Determinística

### Gates (NO tests unitarios)

| Gate | Herramienta | Qué valida |
|------|------------|------------|
| LSP | `pyright .` | 0 errores de tipo |
| Build | `python3 -m py_compile tic_tac_toe.py` | Compila sin errores |
| Code Review | `delegate_task` con skill `code-review-and-quality` | Revisión adversarial del diff |
| Runtime | `python3 -c "from tic_tac_toe import Board; ..."` | Smoke test: imports + comportamiento básico |

NO vitest, NO pytest, NO jest. Los gates son determinísticos: LSP clean + build exit 0 + code review + runtime verification.

---

## Persistencia del Historial

- Archivo: `history.json` en el directorio del proyecto (mismo directorio que `tic_tac_toe.py`).
- Schema por registro:
  ```json
  {
    "fecha": "2026-08-01T14:30:00",
    "jugador_x": "humano",
    "jugador_o": "IA",
    "ganador": "X",
    "jugadas": 5
  }
  ```
- Al iniciar: cargar historial existente si el archivo existe.
- Al finalizar partida: anexar registro y guardar.
- **`history.json` NO se commitea** — es un artefacto de runtime.

---

## Distribución y Empaquetado

### MVP (Fase 0-5)

- Archivo único `tic_tac_toe.py` con shebang `#!/usr/bin/env python3`.
- Permisos de ejecución: `chmod +x tic_tac_toe.py`.
- Ejecución: `./tic_tac_toe.py` o `python3 tic_tac_toe.py`.

### Formal (Fase 7, opcional)

- `pyproject.toml` para instalación vía `pip install .`
- No requerido para el MVP — decidir solo si hay necesidad real de distribución formal.

---

## Directory Hygiene

**Prohibido commitear:**

| Tipo | Ejemplos | Alternativa |
|------|---------|-------------|
| Runtime data | `history.json` | `.gitignore` (es de runtime) |
| Build artifacts | `dist/`, `build/`, `*.egg-info` | `.gitignore` |
| OS artifacts | `.DS_Store`, `Thumbs.db` | `.gitignore` |
| Temp | `*.tmp`, `*.bak`, `*.swp`, `*~` | Git |

**Pre-commit verification:**
```bash
git status --porcelain | grep "^??"
```
Si hay untracked files (excepto `.gitignore`, `PROJECT.md`, `AGENTS.md`, `README.md`):
- **Borrar** si es trash (cache, temp, log)
- **Añadir a .gitignore** si es un patrón recurrente
- **Commitear** solo si es un source file legítimo

**`.gitignore` mínimo:**
```
__pycache__/
*.pyc
history.json
*.egg-info/
dist/
build/
.env
.DS_Store
*.tmp
*.bak
```

---

## AGENTS.md ↔ PROJECT.md Sincronización (obligatoria)

- **AGENTS.md** describe CÓMO: reglas, arquitectura, patrones, file structure, stack, security.
- **PROJECT.md** describe QUÉ: estado, progreso, métricas, commit hashes, test counts.

**No duplicar datos de progreso aquí.** Cuando PROJECT.md cambie estructuralmente (archivos, componentes, stack, arquitectura), este AGENTS.md debe actualizarse en la misma sesión.

---

## Quick Reference — Comandos

| Acción | Comando |
|--------|---------|
| Ejecutar el juego | `./tic_tac_toe.py` |
| Ejecutar verificaciones | `pyright .` |
| Syntax check | `python3 -m py_compile tic_tac_toe.py` |
| Ver imports | `python3 -c "from tic_tac_toe import Board, Game, AI, main; print('OK')"` |
| Pre-commit check | `git status --porcelain \| grep "^??"` |
| Crear feature branch | `git checkout -b feature/<name> main` |

---
*Generado por SophIA — Sebastian Velasco's autonomous operating system*
