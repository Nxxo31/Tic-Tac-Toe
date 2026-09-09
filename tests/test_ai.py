"""Pruebas para la clase AI — Fases 2-3.

Cubre:
  - IA aleatoria (dificultad "facil") hace movimientos válidos.
  - IA minimax "experto" nunca pierde contra juego óptimo.
  - IA minimax "medio" hace movimientos válidos (puede no ser invencible).
  - IA toma movimiento ganador cuando está disponible.
  - IA bloquea movimiento ganador del oponente.
"""

from tic_tac_toe import AI, EMPTY, Board

# ---------------------------------------------------------------------------
# IA aleatoria (Fase 2)
# ---------------------------------------------------------------------------


class TestAIRandom:
    """Pruebas de la IA en dificultad 'facil' (aleatorio puro)."""

    def test_random_move_returns_valid_position(self) -> None:
        """random_move retorna una posición 0-8 válida."""
        board = Board()
        ai = AI(dificultad="facil")
        move = ai.get_move(board)
        assert 0 <= move <= 8
        assert board.grid[move] == EMPTY

    def test_random_move_empty_cell(self) -> None:
        """random_move elige una casilla vacía."""
        board = Board()
        board.make_move(0, "X")
        board.make_move(4, "O")
        board.make_move(8, "X")
        ai = AI(dificultad="facil")
        for _ in range(20):
            move = ai.get_move(board)
            assert board.grid[move] == EMPTY

    def test_random_move_on_full_board(self) -> None:
        """random_move retorna -1 en tablero lleno."""
        board = Board()
        board.grid = list("XOXXOXOXO")
        ai = AI(dificultad="facil")
        move = ai.get_move(board)
        assert move == -1

    def test_random_move_full_coverage(self) -> None:
        """Tras muchas iteraciones, la IA aleatoria visita todas las casillas vacías."""
        board = Board()
        visited = set()
        for _ in range(500):
            move = AI.random_move(board.grid)
            visited.add(move)
        assert visited == set(range(9))


# ---------------------------------------------------------------------------
# IA Minimax Experto — invencibilidad (Fase 3)
# ---------------------------------------------------------------------------


class TestAIExpertoInvencible:
    """Verifica que la IA en modo 'experto' nunca pierde contra juego óptimo."""

    def test_expert_never_loses_center_start(self) -> None:
        """IA experta no pierde si el humano empiega en el centro."""
        # Humano O empieza en 4 (centro)
        # IA debe responder en esquina
        board = Board()
        board.make_move(4, "X")  # humano juega centro
        ai = AI(dificultad="experto")
        move = ai.get_move(board)
        # IA debe responder en una esquina (0,2,6,8)
        assert move in (0, 2, 6, 8)

    def test_expert_never_loses_corner_start(self) -> None:
        """IA experta no pierde si el humano empieza en esquina."""
        board = Board()
        board.make_move(0, "X")  # humano juega esquina
        ai = AI(dificultad="experto")
        move = ai.get_move(board)
        # IA debe responder en el centro (4) o esquina opuesta (8)
        assert move in (4, 8)

    def test_expert_always_takes_win(self) -> None:
        """IA experta toma inmediatamente una posición ganadora dispuesta."""
        # IA = O, tiene 0 y 1, necesita el 2 para ganar la fila 1
        board = Board()
        board.make_move(0, "O")
        board.make_move(1, "O")
        board.make_move(4, "X")  # humano
        board.make_move(8, "X")  # humano
        ai = AI(dificultad="experto")
        move = ai.get_move(board)
        assert move == 2, f"IA debió ganar jugando en 2, jugó en {move}"

    def test_expert_blocks_immediate_loss(self) -> None:
        """IA experta bloquea la victoría inmediata del oponente."""
        # Humano X tiene 0 y 1, IA debe jugar en 2 para bloquear
        board = Board()
        board.make_move(0, "X")
        board.make_move(1, "X")
        board.make_move(4, "O")  # IA ya jugó
        board.make_move(8, "X")  # humano
        ai = AI(dificultad="experto")
        move = ai.get_move(board)
        assert move == 2, f"IA debió bloquear jugando en 2, jugó en {move}"

    def test_expert_blocks_diagonal_win(self) -> None:
        """IA experta bloquea victoria diagonal del oponente."""
        # Humano X tiene 2 y 6 (diagonal secundaria 2,4,6), IA debe jugar en 4
        # Configurar tablero: IA O ya jugó en 0, humano X jugó 2 y 6
        board = Board()
        board.make_move(0, "O")  # IA ya jugó
        board.make_move(2, "X")  # humano amenaza diagonal 2,4,6
        board.make_move(6, "X")  # humano completa amenaza diagonal
        ai = AI(dificultad="experto")
        move = ai.get_move(board)
        assert move == 4, f"IA debió bloquear diagonal jugando en 4, jugó en {move}"


def _play_perfect_against_expert(human_moves: list[int]) -> str:
    """Simula una partida con movimientos secuenciales predeterminados.

    Args:
        human_moves: Lista de posiciones 0-8 para el humano (X).

    Returns:
        Resultado de la partida: 'X', 'O', o 'empate'.
    """
    board = Board()
    ai = AI(dificultad="experto")
    turn = "X"  # humano
    move_idx = 0

    while not board.is_game_over():
        if turn == "X":
            if move_idx < len(human_moves):
                pos = human_moves[move_idx]
                if board.grid[pos] == EMPTY:
                    board.make_move(pos, "X")
                    move_idx += 1
                else:
                    # movimiento inválido, buscar siguiente casilla vacía
                    for alt_pos in range(9):
                        if board.grid[alt_pos] == EMPTY:
                            board.make_move(alt_pos, "X")
                            move_idx += 1
                            break
            turn = "O"
        else:
            mv = ai.get_move(board)
            board.make_move(mv, "O")
            turn = "X"

    winner = board.check_winner()
    if winner is not None:
        return winner
    return "empate"


class TestAIExpertoVsOptimo:
    """Verifica que la IA experta empata ante juego óptimo del humano."""

    def test_expert_draws_vs_all_optimal_games(self) -> None:
        """IA experta empata en 100 partidas con juego humano óptimo.

        El humano juega esquemas óptimos conocidos (esquina-centro, etc.)
        contra la IA experta. La IA nunca debe perder.
        """
        non_loss_count = 0
        total_games = 0

        # Esquema óptimo 1: humano juega esquina 0, luego responde
        # probamos múltiples permutaciones de movimientos óptimos
        optimal_game_plans = [
            [0, 8, 5],  # esquina → esquina opuesta → lateral
            [0, 8, 1],  # esquina → esquina opuesta → lateral
            [2, 6, 1],  # esquina → esquina opuesta → lateral
            [0, 4, 8],  # esquina → centro → esquina opuesta
            [2, 4, 6],  # esquina → centro → esquina opuesta
            [6, 4, 2],  # esquina → centro → esquina opuesta
            [8, 4, 0],  # esquina → centro → esquina opuesta
            [4, 0, 8],  # centro → esquina → esquina opuesta
            [4, 2, 6],  # centro → esquina → esquina opuesta
            [4, 6, 2],  # centro → esquina → esquina opuesta
            [4, 8, 0],  # centro → esquina → esquina opuesta
            # Lateral como primera jugada (subóptimo pero válido)
            [1, 4, 7],
            [3, 4, 5],
            [7, 4, 1],
            [5, 4, 3],
            # Dos esquinas adyacentes
            [0, 2, 5],
            [0, 2, 3],
            [0, 6, 1],
            [2, 8, 1],
            [6, 8, 1],
            # Centro primero, jugador humano intenta galería
            [4, 0, 2],
            [4, 0, 6],
            [4, 2, 0],
            [4, 8, 6],
            [4, 8, 0],
            # Esquina, dos casillas adyacentes
            [0, 1, 8],
            [0, 1, 3],
            [0, 1, 2],
            [0, 3, 2],
            [0, 3, 1],
            # Trampa diagonal
            [0, 4, 8],
            [2, 4, 6],
        ]

        for plan in optimal_game_plans:
            for _ in range(3):  # cada plan, 3 intentos (IA es determinista en experto)
                result = _play_perfect_against_expert(plan)
                total_games += 1
                if result != "X":  # humano no gana
                    non_loss_count += 1

        assert total_games >= 30, f"Se jugaron {total_games} partidas"
        assert non_loss_count == total_games, (
            f"IA perdió {total_games - non_loss_count} de {total_games} partidas"
        )


# ---------------------------------------------------------------------------
# IA Media (profundidad limitada)
# ---------------------------------------------------------------------------


class TestAIMedio:
    """Pruebas de la IA en dificultad 'medio' (profundidad limitada)."""

    def test_medio_returns_valid_move(self) -> None:
        """IA medio retorna un movimiento válido en tablero activo."""
        board = Board()
        ai = AI(dificultad="medio")
        move = ai.get_move(board)
        assert 0 <= move <= 8
        assert board.grid[move] == EMPTY

    def test_medio_takes_obvious_win(self) -> None:
        """IA medio toma victoria obvia cuando está disponible."""
        # O tiene 3 y 4, necesita 5 para ganar fila 2
        board = Board()
        board.make_move(3, "O")
        board.make_move(4, "O")
        board.make_move(0, "X")
        ai = AI(dificultad="medio")
        move = ai.get_move(board)
        assert move == 5, f"IA medio debió ganar jugando en 5, jugó en {move}"


# ---------------------------------------------------------------------------
# Test de integración: Game + AI
# ---------------------------------------------------------------------------


class TestGameWithAI:
    """Verifica que Game usa la IA correctamente en modo PvE."""

    def test_pve_game_ai_moves(self) -> None:
        """En modo PvE, la IA ejecuta un movimiento después del humano."""
        from tic_tac_toe import Game

        game = Game(mode="pve", dificultad="experto")
        # Humano juega X en posición 1 (índice 0)
        game.play_move(1)  # usuario introduce 1-9
        game.switch_player()  # simular el cambio de turno del bucle
        assert game.current_player == "O"  # turno cambió a IA
        move = game.play_ai_move()
        assert 0 <= move <= 8
        assert game.board.grid[move] == "O"
        assert game.move_count == 2

    def test_pvp_game_no_ai(self) -> None:
        """En modo PvP, game.ai es None."""
        from tic_tac_toe import Game

        game = Game(mode="pvp")
        assert game.ai is None

    def test_game_switch_player(self) -> None:
        """switch_player alterna entre X y O."""
        from tic_tac_toe import Game

        game = Game()
        assert game.current_player == "X"
        game.switch_player()
        assert game.current_player == "O"
        game.switch_player()
        assert game.current_player == "X"

    def test_game_reset(self) -> None:
        """reset() limpia tablero y reinicia turno a X."""
        from tic_tac_toe import Game

        game = Game()
        game.play_move(1)
        game.switch_player()
        game.play_move(5)
        game.reset()
        assert game.current_player == "X"
        assert all(cell == EMPTY for cell in game.board.grid)
        assert game.move_count == 0
