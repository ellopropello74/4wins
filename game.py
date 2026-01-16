import sys

import pygame
from pygame.locals import KEYDOWN, K_ESCAPE

from config import BLACK, BLUE, WHITE
from connect_game import ConnectGame
from events import MouseClickEvent, MouseHoverEvent, bus
from game_board import GameBoard
from game_data import GameData
from game_renderer import GameRenderer

# States
MENU = 0
PLAYING = 1
PAUSED = 2
GAME_OVER = 3

def quit():
    sys.exit()

def main_menu(screen):
    screen.fill(BLACK)
    message_display(screen, "CONNECT FOUR!!", WHITE, 350, 150, 75)
    message_display(screen, "HAVE FUN!", (23, 196, 243), 350, 300, 75)
    pygame.display.update()
    return MENU

def play_game(screen, game, data):
    game.print_board()
    game.draw()
    pygame.display.update()
    pygame.time.wait(1000)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.quit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE and not data.game_over:
                    data.paused = True
                    return PAUSED
                elif event.key == pygame.K_z:
                    mods = pygame.key.get_mods()
                    if mods & pygame.KMOD_CTRL:
                        bus.emit("game:undo", game)

            if not data.game_over and not data.paused:
                if event.type == pygame.MOUSEMOTION:
                    bus.emit("mouse:hover", game.renderer, MouseHoverEvent(event.pos[0]))

                if event.type == pygame.MOUSEBUTTONDOWN:
                    bus.emit("mouse:click", game, MouseClickEvent(event.pos[0]))

                game.update()
                game.draw()
            elif data.game_over:
                return GAME_OVER
            elif data.paused:
                return PAUSED

        pygame.display.update()

def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def message_display(screen, text, color, p, q, v):
    largeText = pygame.font.SysFont("monospace", v)
    TextSurf, TextRect = text_objects(text, largeText, color)
    TextRect.center = (p, q)
    screen.blit(TextSurf, TextRect)

def show_pause_menu(screen, game, data):
    next_state = None
    while next_state is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.quit()

        def restart_game():
            data.game_over = False
            data.paused = False
            data.turn = 0
            data.last_move_row = []
            data.last_move_col = []
            data.game_board = GameBoard()
            data.action = None
            game.print_board()
            game.draw()
            pygame.display.update()
            return PLAYING

        def resume_game():
            data.paused = False
            return PLAYING

        def back_to_menu():
            return MENU

        def button(msg, x, y, w, h, ic, ac, action=None):
            nonlocal next_state
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            if x + w > mouse[0] > x and y + h > mouse[1] > y:
                pygame.draw.rect(screen, ac, (x, y, w, h))

                if click[0] == 1 and action is not None:
                    next_state = action()
            else:
                pygame.draw.rect(screen, ic, (x, y, w, h))

            smallText = pygame.font.SysFont("monospace", 30)
            textSurf, textRect = text_objects(msg, smallText, WHITE)
            textRect.center = ((x + (w / 2)), (y + (h / 2)))
            screen.blit(textSurf, textRect)

        button("RESTART", 100, 400, 150, 50, WHITE, WHITE, restart_game)
        button("RESTART", 102, 402, 146, 46, BLACK, BLACK, restart_game)
        button("RESUME", 300, 400, 150, 50, WHITE, WHITE, resume_game)
        button("RESUME", 302, 402, 146, 46, BLACK, BLACK, resume_game)
        button("MENU", 500, 400, 100, 50, WHITE, WHITE, back_to_menu)
        button("MENU", 502, 402, 96, 46, BLACK, BLACK, back_to_menu)
        pygame.display.update()
    return next_state

def show_end_menu(screen, game, data):
    next_state = None
    while next_state is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.quit()

        def restart_game():
            data.game_over = False
            data.paused = False
            data.turn = 0
            data.last_move_row = []
            data.last_move_col = []
            data.game_board = GameBoard()
            data.action = None
            game.print_board()
            game.draw()
            pygame.display.update()
            return PLAYING

        def back_to_menu():
            return MENU

        def button(msg, x, y, w, h, ic, ac, action=None):
            nonlocal next_state
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            if x + w > mouse[0] > x and y + h > mouse[1] > y:
                pygame.draw.rect(screen, ac, (x, y, w, h))

                if click[0] == 1 and action is not None:
                    next_state = action()
            else:
                pygame.draw.rect(screen, ic, (x, y, w, h))

            smallText = pygame.font.SysFont("monospace", 30)
            textSurf, textRect = text_objects(msg, smallText, WHITE)
            textRect.center = ((x + (w / 2)), (y + (h / 2)))
            screen.blit(textSurf, textRect)

        button("RESTART", 150, 450, 200, 50, WHITE, WHITE, restart_game)
        button("RESTART", 152, 452, 196, 46, BLACK, BLACK, restart_game)
        button("MENU", 450, 450, 100, 50, WHITE, WHITE, back_to_menu)
        button("MENU", 452, 452, 96, 46, BLACK, BLACK, back_to_menu)
        pygame.display.update()
    return next_state

def main():
    pygame.init()
    data = GameData()
    screen = pygame.display.set_mode(data.size)
    pygame.display.set_caption("Connect Four | Joel Laux")

    state = MENU
    game = None

    while True:
        if state == MENU:
            state = main_menu(screen)
            if state == MENU:
                # Wait for button click
                running = True
                while running:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            quit()

                    def button(msg, x, y, w, h, ic, ac, action=None):
                        mouse = pygame.mouse.get_pos()
                        click = pygame.mouse.get_pressed()

                        if x + w > mouse[0] > x and y + h > mouse[1] > y:
                            pygame.draw.rect(screen, ac, (x, y, w, h))

                            if click[0] == 1 and action is not None:
                                nonlocal running
                                running = False
                                action()
                        else:
                            pygame.draw.rect(screen, ic, (x, y, w, h))

                        smallText = pygame.font.SysFont("monospace", 30)
                        textSurf, textRect = text_objects(msg, smallText, WHITE)
                        textRect.center = ((x + (w / 2)), (y + (h / 2)))
                        screen.blit(textSurf, textRect)

                    button("PLAY!", 150, 450, 100, 50, WHITE, WHITE, lambda: None)  # Start game
                    button("PLAY", 152, 452, 96, 46, BLACK, BLACK, lambda: None)
                    button("QUIT", 450, 450, 100, 50, WHITE, WHITE, quit)
                    button("QUIT", 452, 452, 96, 46, BLACK, BLACK, quit)
                    pygame.display.update()
                state = PLAYING
                game = ConnectGame(data, GameRenderer(screen, data))
        elif state == PLAYING:
            state = play_game(screen, game, data)
        elif state == PAUSED:
            state = show_pause_menu(screen, game, data)
        elif state == GAME_OVER:
            state = show_end_menu(screen, game, data)

if __name__ == "__main__":
    main()
