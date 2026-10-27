from __future__ import annotations

from typing import Optional

EMPTY = 0
PLAYER_ONE = 1
PLAYER_TWO = 2
PLAYERS = (PLAYER_ONE, PLAYER_TWO)
CONNECT_LENGTH = 4


class GameBoard:

    def __init__(self, rows: int = 6, cols: int = 7):
        if rows <= 0 or cols <= 0:
            raise ValueError("rows and cols must be positive")
        self.rows = rows
        self.cols = cols
        self.board: list[list[int]] = [
            [EMPTY for _ in range(cols)] for _ in range(rows)
        ]

    def copy(self) -> GameBoard:
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
        return (
            isinstance(col, int)
            and 0 <= col < self.cols
            and not self.is_terminal()
            and self.board[self.rows - 1][col] == EMPTY
        )

    def get_next_open_row(self, col: int) -> Optional[int]:
        if not isinstance(col, int) or not 0 <= col < self.cols:
            return None
        if not self.is_valid_location(col):
            return None
        for row in range(self.rows):
            if self.board[row][col] == EMPTY:
                return row
        return None

    def get_valid_moves(self) -> list[int]:
        if self.is_terminal():
            return []
        return [
            col for col in range(self.cols)
            if self.board[self.rows - 1][col] == EMPTY
        ]

    def drop_piece(self, row: int, col: int, piece: int) -> None:
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
        row = self.get_next_open_row(col)
        if piece not in PLAYERS:
            raise ValueError("piece must be PLAYER_ONE (1) or PLAYER_TWO (2)")
        if row is None:
            raise ValueError(f"column {col!r} is not a legal move")
        self.drop_piece(row, col, piece)
        return row

    def remove_piece(self, row: int, col: int) -> int:
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
        simulated = self.copy()
        simulated.play_move(col, piece)
        return simulated

    def check_square(self, piece: int, row: int, col: int) -> bool:
        return (
            0 <= row < self.rows
            and 0 <= col < self.cols
            and self.board[row][col] == piece
        )

    def winning_move(self, piece: int) -> Optional[list[tuple[int, int]]]:
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
        for piece in PLAYERS:
            if self.winning_move(piece) is not None:
                return piece
        return None

    def is_draw(self) -> bool:
        return self._is_full() and self.get_winner() is None

    def tie_move(self) -> bool:
        return self.is_draw()

    def is_terminal(self) -> bool:
        return self.get_winner() is not None or self._is_full()
