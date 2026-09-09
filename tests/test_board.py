"""Pruebas unitarias para la clase Board — Fases 1-3.

Cubre: inicialización, movimientos válidos/inválidos, detección de
victoria (filas, columnas, diagonales), empate, reinicio.
"""

from tic_tac_toe import EMPTY, Board

# ---------------------------------------------------------------------------
# Inicialización
# ---------------------------------------------------------------------------


class TestBoardInit:
    """Pruebas de inicialización del tablero."""

    def test_init_empty_board(self) -> None:
        """Board() inicializa con 9 espacios vacíos."""
        board = Board()
        assert len(board.grid) == 9
        assert all(cell == EMPTY for cell in board.grid)

    def test_init_is_list(self) -> None:
        """grid es una lista mutable."""
        board = Board()
        assert isinstance(board.grid, list)

    def test_board_is_empty_after_creation(self) -> None:
        """available_moves retorna todas las 9 casillas vacías."""
        board = Board()
        assert board.available_moves() == [0, 1, 2, 3, 4, 5, 6, 7, 8]


# ---------------------------------------------------------------------------
# Movimientos
# ---------------------------------------------------------------------------


class TestBoardMoves:
    """Pruebas de make_move y validación."""

    def test_make_valid_move(self) -> None:
        """make_move aplica ficha en casilla vacía."""
        board = Board()
        result = board.make_move(0, "X")
        assert result is True
        assert board.grid[0] == "X"

    def test_make_move_returns_true_on_success(self) -> None:
        """make_move retorna True cuando el movimiento es exitoso."""
        board = Board()
        assert board.make_move(4, "O") is True

    def test_make_move_occupied_cell(self) -> None:
        """Mover en casilla ocupada retorna False y no sobrescribe."""
        board = Board()
        board.make_move(0, "X")
        result = board.make_move(0, "O")
        assert result is False
        assert board.grid[0] == "X"  # no se sobrescribió

    def test_make_invalid_move_ignored(self) -> None:
        """Mover en casilla ocupada no la sobrescribe."""
        board = Board()
        board.make_move(1, "X")
        board.make_move(1, "O")  # intento de sobrescribir
        assert board.grid[1] == "X"

    def test_make_move_negative_position(self) -> None:
        """Posición negativa no causa crash."""
        board = Board()
        assert board.make_move(-1, "X") is False

    def test_make_move_out_of_range(self) -> None:
        """Posición fuera de rango (>=9) retorna False."""
        board = Board()
        assert board.make_move(9, "X") is False
        assert board.make_move(100, "X") is False

    def test_make_move_multiple(self) -> None:
        """Múltiples movimientos válidos se aplican correctamente."""
        board = Board()
        board.make_move(0, "X")
        board.make_move(4, "O")
        board.make_move(8, "X")
        assert board.grid[0] == "X"
        assert board.grid[4] == "O"
        assert board.grid[8] == "X"
        assert board.available_moves() == [1, 2, 3, 5, 6, 7]

    def test_is_valid_position(self) -> None:
        """is_valid_position valida rango 0-8."""
        assert Board.is_valid_position(0) is True
        assert Board.is_valid_position(8) is True
        assert Board.is_valid_position(-1) is False
        assert Board.is_valid_position(9) is False
        # Los floats no son posiciones válidas
        assert Board.is_valid_position(4.0) is False  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# Detección de victoria
# ---------------------------------------------------------------------------


class TestBoardWinner:
    """Pruebas de check_winner para filas, columnas y diagonales."""

    def test_winner_rows(self) -> None:
        """Detecta 3 en línea horizontal (filas 1, 2, 3)."""
        # Fila 1: posiciones 0,1,2 → X
        board = Board()
        for i in (0, 1, 2):
            board.make_move(i, "X")
        assert board.check_winner() == "X"

        # Fila 2: posiciones 3,4,5 → O
        board2 = Board()
        for i in (3, 4, 5):
            board2.make_move(i, "O")
        assert board2.check_winner() == "O"

        # Fila 3: posiciones 6,7,8 → X
        board3 = Board()
        for i in (6, 7, 8):
            board3.make_move(i, "X")
        assert board3.check_winner() == "X"

    def test_winner_columns(self) -> None:
        """Detecta 3 en línea vertical (columnas 1, 2, 3)."""
        # Columna 1: 0,3,6
        board = Board()
        for i in (0, 3, 6):
            board.make_move(i, "X")
        assert board.check_winner() == "X"

        # Columna 2: 1,4,7
        board2 = Board()
        for i in (1, 4, 7):
            board2.make_move(i, "O")
        assert board2.check_winner() == "O"

        # Columna 3: 2,5,8
        board3 = Board()
        for i in (2, 5, 8):
            board3.make_move(i, "X")
        assert board3.check_winner() == "X"

    def test_winner_diagonals(self) -> None:
        """Detecta 3 en línea diagonal (principal y secundaria)."""
        # Diagonal principal: 0,4,8
        board = Board()
        for i in (0, 4, 8):
            board.make_move(i, "X")
        assert board.check_winner() == "X"

        # Diagonal secundaria: 2,4,6
        board2 = Board()
        for i in (2, 4, 6):
            board2.make_move(i, "O")
        assert board2.check_winner() == "O"

    def test_no_winner_partial_board(self) -> None:
        """No hay ganador en un tablero parcial."""
        board = Board()
        board.make_move(0, "X")
        board.make_move(4, "O")
        board.make_move(1, "X")
        assert board.check_winner() is None

    def test_no_winner_empty_board(self) -> None:
        """Tablero vacío no tiene ganador."""
        assert Board().check_winner() is None

    def test_winner_after_full_board(self) -> None:
        """Detecta ganador incluso si el tablero se llena."""
        # X gana con diagonal 0,4,8; O juega el resto
        board = Board()
        # X: 0,4,8 (gana)
        # O: 1,2,3,5,6
        board.make_move(0, "X")
        board.make_move(1, "O")
        board.make_move(4, "X")
        board.make_move(2, "O")
        board.make_move(8, "X")
        board.make_move(3, "O")
        board.make_move(5, "O")
        board.make_move(6, "O")
        board.make_move(7, "X")
        assert board.check_winner() == "X"


# ---------------------------------------------------------------------------
# Empate
# ---------------------------------------------------------------------------


class TestBoardDraw:
    """Pruebas de detección de empate."""

    def test_full_board_no_winner_draw(self) -> None:
        """Tablero lleno sin 3 en línea = empate."""
        board = Board()
        # Configuración de empate:
        # X O X
        # X X O
        # O X O
        board.grid = list("XOXXOXOXO")  # 9 casillas, sin 3 en línea
        assert board.check_winner() is None
        assert board.is_full() is True
        assert board.is_draw() is True

    def test_full_board_with_winner_not_draw(self) -> None:
        """Tablero lleno con ganador no es empate."""
        board = Board()
        board.grid = list("XXXOOXOOO")  # X gana fila 1
        assert board.check_winner() == "X"
        assert board.is_full() is True
        assert board.is_draw() is False

    def test_partial_board_not_draw(self) -> None:
        """Tablero parcial no es empate."""
        board = Board()
        board.make_move(0, "X")
        assert board.is_draw() is False

    def test_empty_board_not_full(self) -> None:
        """Tablero vacío no está lleno."""
        assert Board().is_full() is False

    def test_is_game_over_winner(self) -> None:
        """is_game_over True cuando hay ganador."""
        board = Board()
        board.make_move(0, "X")
        board.make_move(1, "X")
        board.make_move(2, "X")
        assert board.is_game_over() is True

    def test_is_game_over_draw(self) -> None:
        """is_game_over True cuando hay empate."""
        board = Board()
        board.grid = list("XOXXOXOXO")
        assert board.is_game_over() is True

    def test_is_game_over_not_over(self) -> None:
        """is_game_over False con tablero activo."""
        board = Board()
        board.make_move(0, "X")
        assert board.is_game_over() is False


# ---------------------------------------------------------------------------
# Reinicio
# ---------------------------------------------------------------------------


class TestBoardReset:
    """Pruebas de reset y copy."""

    def test_reset_board(self) -> None:
        """reset() limpia el tablero a 9 vacíos."""
        board = Board()
        board.make_move(0, "X")
        board.make_move(4, "O")
        board.make_move(8, "X")
        board.reset()
        assert len(board.grid) == 9
        assert all(cell == EMPTY for cell in board.grid)
        assert board.available_moves() == [0, 1, 2, 3, 4, 5, 6, 7, 8]

    def test_reset_after_win(self) -> None:
        """reset() después de una victoria limpia el tablero."""
        board = Board()
        for i in (0, 1, 2):
            board.make_move(i, "X")
        assert board.check_winner() == "X"
        board.reset()
        assert board.check_winner() is None

    def test_copy(self) -> None:
        """copy() crea una copia independiente."""
        board = Board()
        board.make_move(0, "X")
        board_copy = board.copy()
        assert board_copy.grid == board.grid
        # Modificar el original no afecta la copia
        board.make_move(1, "O")
        assert board_copy.grid[1] == EMPTY
        assert board.grid[1] == "O"


# ---------------------------------------------------------------------------
# Display
# ---------------------------------------------------------------------------


class TestBoardDisplay:
    """Pruebas del método display."""

    def test_display_returns_string(self) -> None:
        """display() retorna un string."""
        board = Board()
        assert isinstance(board.display(), str)

    def test_display_has_separators(self) -> None:
        """display() incluye separadores de filas."""
        board = Board()
        output = board.display()
        assert "---+---+---" in output

    def test_display_empty_board_shows_numbers(self) -> None:
        """Tablero vacío muestra números 1-9 en cada casilla."""
        board = Board()
        output = board.display()
        # Las casillas vacías muestran el número (1-9)
        for n in range(1, 10):
            assert str(n) in output

    def test_display_filled_board_shows_symbols(self) -> None:
        """Tablero con fichas muestra X/O en lugar de números."""
        board = Board()
        board.make_move(0, "X")
        output = board.display()
        assert "X" in output
