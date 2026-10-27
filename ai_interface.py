from typing import Literal, Protocol

from game_board import GameBoard

Difficulty = Literal["easy", "medium", "hard"]
DIFFICULTIES: tuple[Difficulty, ...] = ("easy", "medium", "hard")


class AIPlayer(Protocol):

    def choose_move(
        self,
        board: GameBoard,
        player: int,
        difficulty: Difficulty,
    ) -> int:
        ...
