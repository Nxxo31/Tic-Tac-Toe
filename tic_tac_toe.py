#!/usr/bin/env python3
"""Tic-Tac-Toe (Juego del Gato) — jugabilidad en terminal.

Fases 1-3 del PROJECT.md:
  - Fase 1: Jugabilidad básica MVP (tablero, turnos, victoria, reinicio)
  - Fase 2: IA básica (oponente aleatorio, modo PvP/PvE)
  - Fase 3: IA Minimax con poda alfa-beta (dificultad ajustable)

Stack: Python 3.11+ stdlib ONLY — cero dependencias externas.

Uso:
    ./tic_tac_toe.py
    python3 tic_tac_toe.py
"""

from __future__ import annotations

import json
import random
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------

EMPTY: str = " "
PLAYER_X: str = "X"
PLAYER_O: str = "O"
BOARD_SIZE: int = 9

# Combinaciones ganadoras (índices 0-8 en lista plana de 9)
WIN_LINES: tuple[tuple[int, int, int], ...] = (
    (0, 1, 2),  # fila 1
    (3, 4, 5),  # fila 2
    (6, 7, 8),  # fila 3
    (0, 3, 6),  # columna 1
    (1, 4, 7),  # columna 2
    (2, 5, 8),  # columna 3
    (0, 4, 8),  # diagonal principal
    (2, 4, 6),  # diagonal secundaria
)

Dificultad = Literal["facil", "medio", "experto", "expert+"]
Modo = Literal["pvp", "pve"]

# Profundidad máxima de minimax por dificultad
# None = sin límite (árbol completo, tic-tac-toe es pequeño)
PROFUNDIDAD_DIFICULTAD: dict[str, int | None] = {
    "facil": 0,  # facil = aleatorio puro, no se usa minimax
    "medio": 3,  # profundidad limitada — a veces comete errores
    "experto": None,  # árbol completo — invencible
    "expert+": 10,  # profundidad alta para juego experto+
}


# ---------------------------------------------------------------------------
# Board — estado del tablero, validación, victoria/empate
# ---------------------------------------------------------------------------


class Board:
    """Representa el tablero 3x3 como lista plana de 9 elementos.

    Índices internos: 0-8. El usuario introduce 1-9; la conversión
    es ``position - 1``.

    Atributos:
        grid: Lista de 9 elementos, cada uno ``' '`` (vacío), ``'X'`` o ``'O'``.
    """

    def __init__(self) -> None:
        """Inicializa un tablero vacío de 9 casillas."""
        self.grid: list[str] = [EMPTY] * BOARD_SIZE

    # -- Representación --------------------------------------------------

    def display(self) -> str:
        """Retorna una representación legible del tablero como string."""
        g = self.grid
        sep = "---+---+---"
        lines: list[str] = []
        for i in range(0, 9, 3):
            row = f" {g[i] if g[i] != EMPTY else i + 1} | {g[i + 1] if g[i + 1] != EMPTY else i + 2} | {g[i + 2] if g[i + 2] != EMPTY else i + 3}"
            lines.append(row)
            if i < 6:
                lines.append(sep)
        return "\n".join(lines)

    def __str__(self) -> str:
        """Alias de ``display()`` para ``print(board)``."""
        return self.display()

    # -- Movimientos -----------------------------------------------------

    def make_move(self, position: int, player: str) -> bool:
        """Intenta colocar ``player`` en la posición ``position`` (0-8).

        Args:
            position: Índice interno 0-8.
            player: Símbolo del jugador (``'X'`` o ``'O'``).

        Returns:
            ``True`` si el movimiento fue aplicado, ``False`` si la casilla
            estaba ocupada o la posición era inválida.
        """
        if not self.is_valid_position(position):
            return False
        if self.grid[position] != EMPTY:
            return False
        self.grid[position] = player
        return True

    @staticmethod
    def is_valid_position(position: int) -> bool:
        """Verifica que ``position`` esté en el rango válido 0-8."""
        return isinstance(position, int) and 0 <= position < BOARD_SIZE

    def available_moves(self) -> list[int]:
        """Retorna lista de índices vacíos disponibles."""
        return [i for i in range(BOARD_SIZE) if self.grid[i] == EMPTY]

    # -- Detección de fin de partida -------------------------------------

    def check_winner(self) -> str | None:
        """Verifica si hay un ganador.

        Returns:
            ``'X'`` o ``'O'`` si hay tres en línea, ``None`` si no.
        """
        for a, b, c in WIN_LINES:
            if self.grid[a] != EMPTY and self.grid[a] == self.grid[b] == self.grid[c]:
                return self.grid[a]
        return None

    def is_full(self) -> bool:
        """Retorna ``True`` si el tablero está completamente lleno."""
        return EMPTY not in self.grid

    def is_draw(self) -> bool:
        """Retorna ``True`` si hay empate (tablero lleno sin ganador)."""
        return self.is_full() and self.check_winner() is None

    def is_game_over(self) -> bool:
        """Retorna ``True`` si la partida terminó (victoria o empate)."""
        return self.check_winner() is not None or self.is_full()

    # -- Reinicio --------------------------------------------------------

    def reset(self) -> None:
        """Reinicia el tablero a 9 casillas vacías."""
        self.grid = [EMPTY] * BOARD_SIZE

    def copy(self) -> Board:
        """Retorna una copia profunda del tablero (para simulación minimax)."""
        new = Board()
        new.grid = list(self.grid)
        return new


# ---------------------------------------------------------------------------
# AI — oponente aleatorio y Minimax con poda alfa-beta
# ---------------------------------------------------------------------------


class AI:
    """Inteligencia artificial para modo PvE.

    Soporta tres dificultades:
        - ``facil``: movimiento aleatorio puro.
        - ``medio``: minimax con profundidad limitada (puede cometer errores).
        - ``experto``: minimax completo con poda alfa-beta (invencible).
        - ``expert+": minimax con profundidad alta (equivalente a experto para tic-tac-toe).

    La IA siempre juega como ``'O'`` por convención del proyecto.
    """

    SCORE_WIN: int = 10  # victoria de la IA
    SCORE_LOSS: int = -10  # victoria del humano
    SCORE_DRAW: int = 0  # empate

    def __init__(self, dificultad: Dificultad = "experto") -> None:
        """Inicializa la IA con la dificultad especificada."""
        self.dificultad: Dificultad = dificultad
        self.ai_symbol: str = PLAYER_O
        self.human_symbol: str = PLAYER_X

    # -- Movimiento público ----------------------------------------------

    def get_move(self, board: Board) -> int:
        """Elige el siguiente movimiento de la IA.

        Args:
            board: Estado actual del tablero.

        Returns:
            Índice 0-8 de la casilla seleccionada.
        """
        # Fácil: siempre aleatorio
        if self.dificultad == "facil":
            return self.random_move(board.grid)
        # Medio/Experto: minimax con profundidad según dificultad
        profundidad = PROFUNDIDAD_DIFICULTAD.get(self.dificultad, None)
        return self.minimax_move(board, profundidad)

    @staticmethod
    def random_move(grid: list[str]) -> int:
        """Selecciona una casilla vacía al azar.

        Args:
            grid: Estado actual del tablero.

        Returns:
            Índice 0-8 de una casilla vacía.
        """
        available = [i for i in range(BOARD_SIZE) if grid[i] == EMPTY]
        return random.choice(available) if available else -1

    # -- Minimax con poda alfa-beta ------------------------------------

    def minimax_move(self, board: Board, profundidad_max: int | None) -> int:
        """Ejecuta minimax con poda alfa-beta para elegir el mejor movimiento.

        Args:
            board: Estado actual del tablero.
            profundidad_max: Profundidad máxima de búsqueda.
                ``None`` = sin límite (árbol completo).

        Returns:
            Índice 0-8 del mejor movimiento encontrado.
        """
        best_score = float("-inf")
        best_move = -1
        alpha = float("-inf")
        beta = float("inf")
        for move in board.available_moves():
            board.grid[move] = self.ai_symbol
            score = self._minimax(board, 0, False, alpha, beta, profundidad_max)
            board.grid[move] = EMPTY  # deshacer movimiento
            if score > best_score:
                best_score = score
                best_move = move
            alpha = max(alpha, best_score)
        return best_move if best_move != -1 else self.random_move(board.grid)

    def _minimax(
        self,
        board: Board,
        depth: int,
        is_maximizing: bool,
        alpha: float,
        beta: float,
        profundidad_max: int | None,
    ) -> int:
        """Recursión minimax con poda alfa-beta.

        Args:
            board: Tablero en estado simulado.
            depth: Profundidad actual de recursión.
            is_maximizing: ``True`` si es el turno de la IA (maximizar).
            alpha: Mejor valor encontrado para el maximizador.
            beta: Mejor valor encontrado para el minimizador.
            profundidad_max: Profundidad máxima permitida.

        Returns:
            Puntuación del estado terminal o mejor encontrado.
        """
        winner = board.check_winner()
        if winner == self.ai_symbol:
            return self.SCORE_WIN - depth  # prefiero ganar rápido
        if winner == self.human_symbol:
            return self.SCORE_LOSS + depth  # prefiero perder tarde
        if board.is_full():
            return self.SCORE_DRAW
        # Cortar por profundidad (modo Medio)
        if profundidad_max is not None and depth >= profundidad_max:
            return self.SCORE_DRAW  # evaluación estática: empate heurístico
        available = board.available_moves()
        if is_maximizing:
            max_eval = float("-inf")
            for move in available:
                board.grid[move] = self.ai_symbol
                eval_score = self._minimax(
                    board, depth + 1, False, alpha, beta, profundidad_max
                )
                board.grid[move] = EMPTY
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  # poda beta
            return int(max_eval)
        else:
            min_eval = float("inf")
            for move in available:
                board.grid[move] = self.human_symbol
                eval_score = self._minimax(
                    board, depth + 1, True, alpha, beta, profundidad_max
                )
                board.grid[move] = EMPTY
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break  # poda alfa
            return int(min_eval)


# ---------------------------------------------------------------------------
# History — guardar/cargar partidas en JSON
# ---------------------------------------------------------------------------


class History:
    """Persistencia ligera del historial de partidas en ``history.json``.

    Cada registro: ``{"fecha", "modo", "jugador_x", "jugador_o",
    "ganador", "jugadas"}``.
    """

    def __init__(self, filepath: str | Path = "history.json") -> None:
        """Inicializa el historial con la ruta del archivo JSON."""
        self.filepath: Path = Path(filepath)
        self.records: list[dict[str, object]] = []
        self._load()

    def _load(self) -> None:
        """Carga el historial existente si el archivo existe."""
        if self.filepath.exists():
            try:
                data = json.loads(self.filepath.read_text(encoding="utf-8"))
                if isinstance(data, list):
                    self.records = data
            except (json.JSONDecodeError, OSError):
                self.records = []

    def save(self) -> None:
        """Guarda todos los registros en el archivo JSON."""
        self.filepath.write_text(
            json.dumps(self.records, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def add_record(
        self,
        modo: str,
        jugador_x: str,
        jugador_o: str,
        ganador: str,
        jugadas: int,
    ) -> None:
        """Añade un registro de partida al historial.

        Args:
            modo: ``"pvp"`` o ``"pve"``.
            jugador_x: ``"humano"`` o ``"IA"``.
            jugador_o: ``"humano"`` o ``"IA"``.
            ganador: ``"X"``, ``"O"`` o ``"empate"``.
            jugadas: Número total de jugadas en la partida.
        """
        record: dict[str, object] = {
            "fecha": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "modo": modo,
            "jugador_x": jugador_x,
            "jugador_o": jugador_o,
            "ganador": ganador,
            "jugadas": jugadas,
        }
        self.records.append(record)
        self.save()

    def stats(self) -> dict[str, int]:
        """Retorna estadísticas básicas: total, victorias X, victorias O, empates."""
        total = len(self.records)
        wins_x = sum(1 for r in self.records if r.get("ganador") == PLAYER_X)
        wins_o = sum(1 for r in self.records if r.get("ganador") == PLAYER_O)
        draws = sum(1 for r in self.records if r.get("ganador") == "empate")
        return {
            "total": total,
            "victorias_x": wins_x,
            "victorias_o": wins_o,
            "empates": draws,
        }


# ---------------------------------------------------------------------------
# Game — bucle principal, turnos, modos, revancha
# ---------------------------------------------------------------------------


class Game:
    """Orquesta la partida: turnos, modos (PvP/PvE), revancha.

    Atributos:
        board: Instancia de ``Board``.
        current_player: ``'X'`` o ``'O'`` — jugador con el turno actual.
        mode: ``"pvp"`` o ``"pve"``.
        ai: Instancia de ``AI`` (solo en modo PvE, sino ``None``).
        history: Instancia de ``History`` para registro de partidas.
        move_count: Contador de jugadas en la partida actual.
    """

    def __init__(self, mode: Modo = "pvp", dificultad: Dificultad = "experto") -> None:
        """Inicializa la partida con modo y dificultad de IA.

        Args:
            mode: ``"pvp"`` (dos humanos) o ``"pve"`` (humano vs IA).
            dificultad: Nivel de la IA — ``"facil"``, ``"medio"`` o ``"experto"``.
        """
        self.board: Board = Board()
        self.current_player: str = PLAYER_X
        self.mode: Modo = mode
        self.ai: AI | None = AI(dificultad) if mode == "pve" else None
        self.history: History = History()
        self.move_count: int = 0

    # -- Lógica de turnos ----------------------------------------------

    def switch_player(self) -> None:
        """Cambia el turno al jugador opuesto."""
        self.current_player = PLAYER_O if self.current_player == PLAYER_X else PLAYER_X

    def play_move(self, position: int) -> bool:
        """Aplica un movimiento del jugador humano en ``position`` (1-9).

        Args:
            position: Coordenada del usuario (1-9).

        Returns:
            ``True`` si el movimiento fue exitoso, ``False`` si inválido.
        """
        index = position - 1  # convertir 1-9 → 0-8
        if self.board.make_move(index, self.current_player):
            self.move_count += 1
            return True
        return False

    def play_ai_move(self) -> int:
        """La IA elige y ejecuta su movimiento.

        Returns:
            Índice 0-8 de la casilla jugada, o ``-1`` si no hay movimientos.
        """
        if self.ai is None:
            return -1
        move = self.ai.get_move(self.board)
        if move >= 0:
            self.board.make_move(move, self.current_player)
            self.move_count += 1
        return move

    # -- Estado ----------------------------------------------------------

    def get_status(self) -> str | None:
        """Retorna el resultado de la partida o ``None`` si continúa.

        Returns:
            ``'X'``, ``'O'``, ``'empate'`` o ``None``.
        """
        winner = self.board.check_winner()
        if winner is not None:
            return winner
        if self.board.is_full():
            return "empate"
        return None

    def is_over(self) -> bool:
        """Retorna ``True`` si la partida ha terminado."""
        return self.board.is_game_over()

    def reset(self) -> None:
        """Reinicia la partida a estado inicial."""
        self.board.reset()
        self.current_player = PLAYER_X
        self.move_count = 0

    # -- Registro en historial -------------------------------------------

    def record_game(self, result: str) -> None:
        """Registra la partida finalizada en el historial.

        Args:
            result: ``'X'``, ``'O'`` o ``'empate'``.
        """
        if self.mode == "pvp":
            jug_x, jug_o = "humano", "humano"
        else:
            jug_x, jug_o = "humano", "IA"
        self.history.add_record(
            modo=self.mode,
            jugador_x=jug_x,
            jugador_o=jug_o,
            ganador=result,
            jugadas=self.move_count,
        )

    def save_game(self) -> dict:
        """Guarda la partida actual en el historial.

        Captura el estado actual del tablero, modo, jugador actual,
        contador de jugadas y resultado, y lo persiste usando el
        historial existente.

        Returns:
            dict con los datos guardados para referencia.
        """
        result = self.get_status()
        if self.mode == "pvp":
            jug_x, jug_o = "humano", "humano"
        else:
            jug_x, jug_o = "humano", "IA"
        self.history.add_record(
            modo=self.mode,
            jugador_x=jug_x,
            jugador_o=jug_o,
            ganador=result if result else "empate",
            jugadas=self.move_count,
        )
        return self.history.records[-1]


# ---------------------------------------------------------------------------
# main() — entry point, UI de terminal, manejo de entrada
# ---------------------------------------------------------------------------


def select_mode() -> Modo:
    """Pregunta al usuario el modo de juego (PvP o PvE).

    Returns:
        ``"pvp"`` o ``"pve"``.
    """
    while True:
        print("\n--- Selección de modo ---")
        print("  1) PvP  — dos jugadores humanos")
        print("  2) PvE  — humano vs IA")
        choice = input("Elige (1/2): ").strip()
        if choice == "1":
            return "pvp"
        if choice == "2":
            return "pve"
        print("❌ Opción inválida. Introduce 1 o 2.")


def select_difficulty() -> Dificultad:
    """Pregunta al usuario la dificultad de la IA.

    Returns:
        ``"facil"``, ``"medio"`` o ``"experto"``.
    """
    while True:
        print("\n--- Dificultad IA ---")
        print("  1) Fácil    — IA aleatoria")
        print("  2) Medio    — Minimax profundidad limitada")
        print("  3) Experto  — Minimax completo (invencible)")
        choice = input("Elige (1/2/3): ").strip()
        if choice == "1":
            return "facil"
        if choice == "2":
            return "medio"
        if choice == "3":
            return "experto"
        print("❌ Opción inválida. Introduce 1, 2 o 3.")


def get_human_move(board: Board, player: str) -> int:
    """Lee y valida el movimiento del jugador humano.

    Args:
        board: Estado actual del tablero.
        player: Símbolo del jugador actual (``'X'`` o ``'O'``).

    Returns:
        Posición 1-9 válida elegida por el usuario.
    """
    while True:
        raw = input(f"Jugador {player} — elige casilla (1-9): ").strip()
        # Validar que sea un número entero
        if not raw.isdigit():
            print("❌ Introduce un número del 1 al 9.")
            continue
        pos = int(raw)
        if pos < 1 or pos > 9:
            print("❌ Número fuera de rango. Debe ser 1-9.")
            continue
        index = pos - 1
        if board.grid[index] != EMPTY:
            print("❌ Esa casilla ya está ocupada. Elige otra.")
            continue
        return pos


def play_turn(game: Game) -> None:
    """Ejecuta un turno (humano o IA) y muestra el resultado."""
    board = game.board
    player = game.current_player
    # Si es turno de IA en modo PvE
    if game.mode == "pve" and game.ai is not None and player == game.ai.ai_symbol:
        print(f"\n🤖 IA ({player}) pensando...")
        move = game.play_ai_move()
        if move >= 0:
            print(f"   IA juega en la casilla {move + 1}")
        return
    # Turno humano
    pos = get_human_move(board, player)
    game.play_move(pos)


def play_game(game: Game) -> str:
    """Ejecuta el bucle principal de una partida.

    Args:
        game: Instancia de ``Game`` configurada.

    Returns:
        Resultado de la partida: ``'X'``, ``'O'`` o ``'empate'``.
    """
    board = game.board
    while not game.is_over():
        print(f"\n{'=' * 20}")
        print(f"Turno: Jugador {game.current_player}")
        print(board.display())
        print(f"{'=' * 20}")
        play_turn(game)
        # Verificar fin de partida antes de cambiar turno
        status = game.get_status()
        if status is not None:
            break
        game.switch_player()
    # Mostrar tablero final
    print(f"\n{'=' * 20}")
    print("Tablero final:")
    print(board.display())
    print(f"{'=' * 20}")
    result = game.get_status()
    if result == "empate":
        print("\n🟰 ¡Empate! Buen partido.")
    else:
        print(f"\n🎉 ¡Jugador {result} gana!")
    return result if result is not None else "empate"


def ask_rematch() -> bool:
    """Pregunta al usuario si quiere jugar otra partida.

    Returns:
        ``True`` para revancha, ``False`` para salir.
    """
    while True:
        choice = input("\n¿Otra partida? (s/n): ").strip().lower()
        if choice in ("s", "si", "sí", "y", "yes"):
            return True
        if choice in ("n", "no", "nope"):
            return False
        print("❌ Responde 's' (sí) o 'n' (no).")


def show_stats(history: History) -> None:
    """Muestra estadísticas del historial."""
    s = history.stats()
    print("\n--- Estadísticas (historial) ---")
    print(f"  Total partidas: {s['total']}")
    print(f"  Victorias X:    {s['victorias_x']}")
    print(f"  Victorias O:    {s['victorias_o']}")
    print(f"  Empates:        {s['empates']}")


def main() -> None:
    """Entry point — flujo principal del juego.

    Maneja selección de modo, bucle de partida, revancha, historial
    y salida limpia con ``KeyboardInterrupt``.
    """
    print("=" * 40)
    print("   TIC-TAC-TOE  (Juego del Gato)")
    print("=" * 40)
    try:
        # Configuración inicial
        mode = select_mode()
        dificultad: Dificultad = "experto"
        if mode == "pve":
            dificultad = select_difficulty()
        game = Game(mode=mode, dificultad=dificultad)
        # Mostrar estadísticas si hay historial
        if game.history.stats()["total"] > 0:
            show_stats(game.history)
        # Bucle de partidas con revancha
        keep_playing = True
        while keep_playing:
            jogos = play_game(game)
            game.record_game(jogos)
            game.history.save()
            # Nueva opción: guardar partida actual
            if input(
                "\n¿Deseas guardar la partida actual? (s/n): "
            ).strip().lower() in ("s", "si", "sí", "y", "yes"):
                saved = game.save_game()
                print(
                    f"\n✅ Partida guardada: {saved['fecha']} — {saved['modo']} — {saved['ganador']} después de {saved['jugadas']} jugadas"
                )
            keep_playing = ask_rematch()
            if keep_playing:
                game.reset()
        print("\n¡Gracias por jugar! 👋")
    except KeyboardInterrupt:
        print("\n\n¡Juego interrumpido! Saliendo limpiamente... 👋")
    except EOFError:
        print("\n\nEntrada cerrada. Saliendo... 👋")


if __name__ == "__main__":
    main()
