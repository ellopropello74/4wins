import math
import os
import sys

import pygame

from config import BLACK
from events import GameOver, MouseClickEvent, PieceDropEvent, bus
from game_data import GameData
from game_renderer import GameRenderer


class ConnectGame:

    game_data: GameData
    renderer: GameRenderer

    def __init__(self, game_data: GameData, renderer: GameRenderer):

        self.game_data = game_data
        self.renderer = renderer

    def quit(self):

        sys.exit()

    @bus.on("mouse:click")
    def mouse_click(self, event: MouseClickEvent):

        pygame.draw.rect(
            self.renderer.screen,
            BLACK,
            (0, 0, self.game_data.width, self.game_data.sq_size),
        )

        col: int = int(math.floor(event.posx / self.game_data.sq_size))

        if self.game_data.game_board.is_valid_location(col):
            row: int = self.game_data.game_board.get_next_open_row(col)

            self.game_data.last_move_row.append(row)
            self.game_data.last_move_col.append(col)
            self.game_data.game_board.drop_piece(row, col, self.game_data.turn + 1)

            self.draw()

            bus.emit(
                "piece:drop", PieceDropEvent(self.game_data.game_board.board[row][col])
            )

            self.print_board()

            winning_pieces = self.game_data.game_board.winning_move(self.game_data.turn + 1)
            if winning_pieces:
                bus.emit(
                    "game:over", self.renderer, GameOver(False, self.game_data.turn + 1, winning_pieces)
                )
                self.game_data.game_over = True

            pygame.display.update()

            self.game_data.turn += 1
            self.game_data.turn = self.game_data.turn % 2

    @bus.on("game:undo")
    def undo(self):

        if self.game_data.last_move_row:
            self.game_data.game_board.drop_piece(
                self.game_data.last_move_row.pop(),
                self.game_data.last_move_col.pop(),
                0,
            )

        self.game_data.turn += 1
        self.game_data.turn = self.game_data.turn % 2

    def update(self):

        if self.game_data.game_board.tie_move():
            bus.emit("game:over", self.renderer, GameOver(was_tie=True))

            self.game_data.game_over = True

        if self.game_data.game_over:
            print(os.getpid())
            pygame.time.wait(1000)

    def draw(self):

        self.renderer.draw(self.game_data)

    def print_board(self):

        self.game_data.game_board.print_board()
