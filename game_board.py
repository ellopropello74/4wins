from numpy import flip, zeros
from numpy.core._multiarray_umath import ndarray


class GameBoard:
    board: ndarray
    cols: int
    rows: int

    def __init__(self, rows=6, cols=7):
        self.rows = rows
        self.cols = cols
        self.board = zeros((rows, cols))

    def print_board(self):
        print(flip(self.board, 0))
        print(" ---------------------")
        print(" " + str([1, 2, 3, 4, 5, 6, 7]))

    def drop_piece(self, row, col, piece):
        self.board[row][col] = piece

    def is_valid_location(self, col):
        return self.board[self.rows - 1][col] == 0

    def get_next_open_row(self, col):
        for row in range(self.rows):
            if self.board[row][col] == 0:
                return row

    def check_square(self, piece, r, c):
        if r < 0 or r >= self.rows:
            return False

        if c < 0 or c >= self.cols:
            return False

        return self.board[r][c] == piece

    def horizontal_win(self, piece, r, c):
        return (
            self.check_square(piece, r, c)
            and self.check_square(piece, r, c + 1)
            and self.check_square(piece, r, c + 2)
            and self.check_square(piece, r, c + 3)
        )

    def vertical_win(self, piece, r, c):
        return (
            self.check_square(piece, r, c)
            and self.check_square(piece, r + 1, c)
            and self.check_square(piece, r + 2, c)
            and self.check_square(piece, r + 3, c)
        )

    def diagonal_win(self, piece, r, c):
        return (
            self.check_square(piece, r, c)
            and self.check_square(piece, r + 1, c + 1)
            and self.check_square(piece, r + 2, c + 2)
            and self.check_square(piece, r + 3, c + 3)
        ) or (
            self.check_square(piece, r, c)
            and self.check_square(piece, r - 1, c + 1)
            and self.check_square(piece, r - 2, c + 2)
            and self.check_square(piece, r - 3, c + 3)
        )

    def winning_move(self, piece):
        for c in range(self.cols):
            for r in range(self.rows):
                if self.horizontal_win(piece, r, c):
                    return [(r, c), (r, c + 1), (r, c + 2), (r, c + 3)]
                elif self.vertical_win(piece, r, c):
                    return [(r, c), (r + 1, c), (r + 2, c), (r + 3, c)]
                elif self.diagonal_win(piece, r, c):
                    if (
                        self.check_square(piece, r, c)
                        and self.check_square(piece, r + 1, c + 1)
                        and self.check_square(piece, r + 2, c + 2)
                        and self.check_square(piece, r + 3, c + 3)
                    ):
                        return [(r, c), (r + 1, c + 1), (r + 2, c + 2), (r + 3, c + 3)]
                    elif (
                        self.check_square(piece, r, c)
                        and self.check_square(piece, r - 1, c + 1)
                        and self.check_square(piece, r - 2, c + 2)
                        and self.check_square(piece, r - 3, c + 3)
                    ):
                        return [(r, c), (r - 1, c + 1), (r - 2, c + 2), (r - 3, c + 3)]
        return None

    def tie_move(self):
        slots_filled: int = 0

        for c in range(self.cols):
            for r in range(self.rows):
                if self.board[r][c] != 0:
                    slots_filled += 1

        return slots_filled == 42
