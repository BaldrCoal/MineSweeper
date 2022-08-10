import pygame
from pygame.locals import *
import sys
import main
from main import Field
import enum
import os
from pygame_widgets.button import Button

pygame.init()
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (127, 255, 0)
gray = (220, 220, 220)
clock = pygame.time.Clock()


def menu():
    menu_def = pygame.image.load('img/menu.png')
    menu_easy = pygame.image.load('img/menu_easy.png')
    menu_normal = pygame.image.load('img/menu_normal.png')
    menu_hard = pygame.image.load('img/menu_hard.png')
    menu_quit = pygame.image.load('img/menu_quit.png')
    menus = [menu_def, menu_easy, menu_normal, menu_hard, menu_quit]
    screen = pygame.display.set_mode((1000, 600))
    rect_easy = pygame.Rect(12, 280, 300, 100)
    rect_normal = pygame.Rect(350, 280, 300, 100)
    rect_hard = pygame.Rect(687, 280, 300, 100)
    rect_quit = pygame.Rect(345, 471, 300, 100)
    boxes = [rect_easy, rect_normal, rect_hard, rect_quit]
    difficulties = [(9, 9, 10), (16, 16, 40), (30, 16, 99)]

    while True:
        for event in pygame.event.get():  # User did something
            mouse_pos = pygame.mouse.get_pos()
            state = 0
            for ind, box in enumerate(boxes, start=1):
                if box.collidepoint(mouse_pos):
                    state = ind
            if event.type == pygame.QUIT:  # If user clicked close
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and state < 4:
                    play(difficulties[state-1])
                    return
        screen.blit(menus[state], (0, 0))
        pygame.display.update()
        clock.tick(60)


def play(config: tuple):
    height = config[0]
    width = config[1]
    mines_count = config[2]
    window_size = (width * 50, height * 50)
    screen = pygame.display.set_mode(window_size)
    screen.fill(white)
    cell_size_h = window_size[0] // width
    cell_size_w = window_size[1] // height
    clock = pygame.time.Clock()
    cell_closed = pygame.image.load('img/cell_closed.png')
    cell_flaged = pygame.image.load('img/cell_flaged.png')
    cell_opened_mine = pygame.image.load('img/cell_opened_mine.png')
    cell_opened = [pygame.image.load('img/cell_opened_0.png'), pygame.image.load('img/cell_opened_1.png'),
                   pygame.image.load('img/cell_opened_2.png'), pygame.image.load('img/cell_opened_3.png'),
                   pygame.image.load('img/cell_opened_4.png'), pygame.image.load('img/cell_opened_5.png'),
                   pygame.image.load('img/cell_opened_6.png'), pygame.image.load('img/cell_opened_7.png'),
                   pygame.image.load('img/cell_opened_8.png'), ]

    def get_cell_pos(mouse_pos):
        return mouse_pos[0] // cell_size_h, mouse_pos[1] // cell_size_w

    def draw_cell(screen, cell, x, y):
        if cell.is_open:
            if cell.mine:
                screen.blit(cell_opened_mine, (x * cell_size_h, y * cell_size_w))
                return
            around_mines = cell.around_mines
            screen.blit(cell_opened[around_mines], (x * cell_size_h, y * cell_size_w))
            return

        if cell.is_flag:
            screen.blit(cell_flaged, (x * cell_size_h, y * cell_size_w))
            return

        elif not cell.is_open:
            screen.blit(cell_closed, (x * cell_size_h, y * cell_size_w))
            return

    def draw_cells(screen):
        for x, row in enumerate(game.field):
            for y, cell in enumerate(row):
                draw_cell(screen, cell, x, y)

    game = Field(width, height, mines_count)
    game.start_game()

    while True:
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = get_cell_pos(pygame.mouse.get_pos())
                print(pygame.mouse.get_pos())
                print(x, y)
                print(event)
                if event.button == 1:
                    game.click_on_field(x, y)
                elif event.button == 3:
                    game.click_on_field(x, y, left_mouse=False)
        pygame.display.flip()
        draw_cells(screen)
        pygame.display.update()
        clock.tick(60)


menu()
