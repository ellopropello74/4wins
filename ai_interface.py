"""Contract for future Connect Four AI implementations.

An AI receives a detached board copy, the player number it must play for, and
one of the agreed difficulty labels. It returns a zero-based column number.
The game manager validates the returned move before exposing it to the caller.
No search strategy is implemented in this module.
"""

from typing import Literal, Protocol

from game_board import GameBoard

Difficulty = Literal["easy", "medium", "hard"]
DIFFICULTIES: tuple[Difficulty, ...] = ("easy", "medium", "hard")


class AIPlayer(Protocol):
    """Required method shape for a future AI opponent."""

    def choose_move(
        self,
        board: GameBoard,
        player: int,
        difficulty: Difficulty,
    ) -> int:
        """Return a legal zero-based column for player 1 or 2."""
        ...
