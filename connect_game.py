import math
import sys

import pygame

from ai_interface import AIPlayer, DIFFICULTIES, Difficulty
from config import BLACK
from events import GameOver, MouseClickEvent, PieceDropEvent, bus
from game_data import GameData
from game_renderer import GameRenderer


class ConnectGame:
    """Coordinate the board rules, GUI renderer, and existing event bus."""

    game_data: GameData
    renderer: GameRenderer

    def __init__(self, game_data: GameData, renderer: GameRenderer):
        self.game_data = game_data
        self.renderer = renderer

    def quit(self):
        pygame.quit()
        sys.exit()

    @bus.on("mouse:click")
    def mouse_click(self, event: MouseClickEvent):
        pygame.draw.rect(
            self.renderer.screen,
            BLACK,
            (0, 0, self.game_data.width, self.game_data.sq_size),
        )
        col = math.floor(event.posx / self.game_data.sq_size)
        self.play_move(col)

    def play_move(self, col: int) -> bool:
        """Apply a column move for the current player; return whether it was legal."""
        board = self.game_data.game_board
        if self.game_data.game_over or self.game_data.paused:
            return False
        if col not in board.get_valid_moves():
            return False

        player = self.game_data.current_player
        row = board.play_move(col, player)
        self.game_data.last_move_row.append(row)
        self.game_data.last_move_col.append(col)

        self.draw()
        bus.emit("piece:drop", PieceDropEvent(player))
        self.print_board()

        winning_pieces = board.winning_move(player)
        if winning_pieces:
            self.game_data.game_over = True
            bus.emit(
                "game:over",
                self.renderer,
                GameOver(False, player, winning_pieces),
            )
        elif board.is_draw():
            self.game_data.game_over = True
            bus.emit("game:over", self.renderer, GameOver(was_tie=True))
        else:
            self.game_data.turn = (self.game_data.turn + 1) % 2
        pygame.display.update()
        return True

    def choose_ai_move(self, ai_player: AIPlayer, difficulty: Difficulty) -> int:
        """Ask an AI for a move using a detached board and return its column.

        The real board is never passed to AI code. Raises ``ValueError`` for an
        unsupported difficulty or illegal response and ``RuntimeError`` after
        the game has ended.
        """
        if self.game_data.game_over or self.game_data.game_board.is_terminal():
            raise RuntimeError("cannot ask for an AI move after the game has ended")
        if difficulty not in DIFFICULTIES:
            raise ValueError(f"difficulty must be one of {DIFFICULTIES}")

        board_copy = self.game_data.game_board.copy()
        column = ai_player.choose_move(
            board_copy,
            self.game_data.current_player,
            difficulty,
        )
        if type(column) is not int or column not in board_copy.get_valid_moves():
            raise ValueError(f"AI returned an illegal column: {column!r}")
        return column

    @bus.on("game:undo")
    def undo(self):
        if self.game_data.game_over or not self.game_data.last_move_row:
            return

        row = self.game_data.last_move_row.pop()
        col = self.game_data.last_move_col.pop()
        self.game_data.game_board.remove_piece(row, col)
        self.game_data.turn = (self.game_data.turn - 1) % 2
        self.draw()

    def update(self):
        """Kept for the existing GUI loop; terminal checks happen on each move."""

    def draw(self):
        self.renderer.draw(self.game_data)

    def print_board(self):
        self.game_data.game_board.print_board()
