"""Rules and state for a Connect Four board, independent of pygame and events."""

from __future__ import annotations

from typing import Optional

EMPTY = 0
PLAYER_ONE = 1
PLAYER_TWO = 2
PLAYERS = (PLAYER_ONE, PLAYER_TWO)
CONNECT_LENGTH = 4


class GameBoard:
    """A Connect Four position.

    ``board[row][column]`` uses zero-based indices. Row 0 is the bottom row,
    and column 0 is the leftmost column. Cells contain integers: 0 for empty,
    1 for player one (red), and 2 for player two (yellow).

    The board stores the position only; callers pass the player to each move.
    This keeps the rules model independent of turn management and the GUI.
    """

    def __init__(self, rows: int = 6, cols: int = 7):
        if rows <= 0 or cols <= 0:
            raise ValueError("rows and cols must be positive")
        self.rows = rows
        self.cols = cols
        self.board: list[list[int]] = [
            [EMPTY for _ in range(cols)] for _ in range(rows)
        ]

    def copy(self) -> GameBoard:
        """Return an independent copy of this position."""
        copied = GameBoard(self.rows, self.cols)
        copied.board = [row.copy() for row in self.board]
        return copied

    def print_board(self) -> None:
        for row in reversed(self.board):
            print(row)
        print(" ---------------------")
        print(" " + str(list(range(1, self.cols + 1))))

    def _is_full(self) -> bool:
        return all(self.board[self.rows - 1][col] != EMPTY for col in range(self.cols))

    def is_valid_location(self, col: int) -> bool:
        """Return whether ``col`` can accept another move in this position."""
        return (
            isinstance(col, int)
            and 0 <= col < self.cols
            and not self.is_terminal()
            and self.board[self.rows - 1][col] == EMPTY
        )

    def get_next_open_row(self, col: int) -> Optional[int]:
        """Return the next zero-based row in ``col``, or ``None`` if unavailable."""
        if not isinstance(col, int) or not 0 <= col < self.cols:
            return None
        if not self.is_valid_location(col):
            return None
        for row in range(self.rows):
            if self.board[row][col] == EMPTY:
                return row
        return None

    def get_valid_moves(self) -> list[int]:
        """Return zero-based columns that accept a move in the current position."""
        if self.is_terminal():
            return []
        return [
            col for col in range(self.cols)
            if self.board[self.rows - 1][col] == EMPTY
        ]

    def drop_piece(self, row: int, col: int, piece: int) -> None:
        """Place a piece at an explicit legal cell; raise ``ValueError`` otherwise."""
        if piece not in PLAYERS:
            raise ValueError("piece must be PLAYER_ONE (1) or PLAYER_TWO (2)")
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            raise ValueError("row or column is outside the board")
        if self.is_terminal():
            raise ValueError("cannot move after the game has ended")
        next_row = self.get_next_open_row(col)
        if next_row is None or next_row != row:
            raise ValueError("piece must be placed in the next open row")
        self.board[row][col] = piece

    def play_move(self, col: int, piece: int) -> int:
        """Apply a legal move and return the zero-based row where it landed."""
        row = self.get_next_open_row(col)
        if piece not in PLAYERS:
            raise ValueError("piece must be PLAYER_ONE (1) or PLAYER_TWO (2)")
        if row is None:
            raise ValueError(f"column {col!r} is not a legal move")
        self.drop_piece(row, col, piece)
        return row

    def remove_piece(self, row: int, col: int) -> int:
        """Remove the top piece at ``(row, col)`` and return its player number."""
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            raise ValueError("row or column is outside the board")
        if self.board[row][col] == EMPTY:
            raise ValueError("there is no piece at that position")
        if any(self.board[above][col] != EMPTY for above in range(row + 1, self.rows)):
            raise ValueError("only the top piece in a column can be removed")
        piece = self.board[row][col]
        self.board[row][col] = EMPTY
        return piece

    def simulate_move(self, col: int, piece: int) -> GameBoard:
        """Return a new board with the move applied; this board is not changed."""
        simulated = self.copy()
        simulated.play_move(col, piece)
        return simulated

    def check_square(self, piece: int, row: int, col: int) -> bool:
        """Return whether the in-bounds cell contains ``piece``."""
        return (
            0 <= row < self.rows
            and 0 <= col < self.cols
            and self.board[row][col] == piece
        )

    def winning_move(self, piece: int) -> Optional[list[tuple[int, int]]]:
        """Return one four-piece winning line for ``piece``, or ``None``."""
        if piece not in PLAYERS:
            return None
        directions = ((0, 1), (1, 0), (1, 1), (1, -1))
        for row in range(self.rows):
            for col in range(self.cols):
                if not self.check_square(piece, row, col):
                    continue
                for row_step, col_step in directions:
                    line = [
                        (row + offset * row_step, col + offset * col_step)
                        for offset in range(CONNECT_LENGTH)
                    ]
                    if all(self.check_square(piece, r, c) for r, c in line):
                        return line
        return None

    def get_winner(self) -> Optional[int]:
        """Return the winning player number, or ``None`` if no player has won."""
        for piece in PLAYERS:
            if self.winning_move(piece) is not None:
                return piece
        return None

    def is_draw(self) -> bool:
        """Return whether the board is full and neither player has won."""
        return self._is_full() and self.get_winner() is None

    def tie_move(self) -> bool:
        """Compatibility alias for ``is_draw`` used by older project code."""
        return self.is_draw()

    def is_terminal(self) -> bool:
        """Return whether this position is a win for either side or a draw."""
        return self.get_winner() is not None or self._is_full()
