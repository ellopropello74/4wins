from typing import Tuple, List

from game_board import GameBoard


class GameData:
    radius: int
    height: int
    width: int
    sq_size: int
    size: Tuple[int, int]
    game_over: bool
    paused: bool
    turn: int
    last_move_row: List[int]
    last_move_col: List[int]
    game_board: GameBoard

    def __init__(self):
        self.game_over = False
        self.paused = False
        self.turn = 0
        self.last_move_row = []
        self.last_move_col = []
        self.game_board = GameBoard()
        self.action = None

        self.sq_size: int = 100
        self.width: int = 7 * self.sq_size
        self.height: int = 7 * self.sq_size
        self.size: Tuple[int, int] = (self.width, self.height)
        self.radius: int = int(self.sq_size / 2 - 5)
