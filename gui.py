import pygame
from pygame.locals import *
import sys

import main
from main import Field
import enum



pygame.init()
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (127, 255, 0)
gray = (220, 220, 220)
window_size = (800, 800)
screen = pygame.display.set_mode(window_size)
screen.fill(white)
lines_coords = []
height = 5
width = 5
BORDER = 5
cell_size_h = window_size[0] // height
cell_size_w = window_size[1] // width
clock = pygame.time.Clock()
font = pygame.font.SysFont('arial', 50)


def get_cell_pos(mouse_pos):
    return mouse_pos[0] // cell_size_h, mouse_pos[1] // cell_size_w


def draw_cell(screen, x, y):
    rect = pygame.Rect((x*cell_size_h, y*cell_size_w, cell_size_h - BORDER, cell_size_w - BORDER))
    cell = game.field[x][y]
    if cell.is_open:
        if cell.mine:
            color = red
            pygame.draw.rect(screen, color, rect)
            return
        else:
            color = pygame.Color("white")
        pygame.draw.rect(screen, color, rect)
        text = font.render(str(cell.around_mines), True, (0, 0, 0))
        screen.blit(text, (x * cell_size_h + cell_size_h//2, y * cell_size_w + cell_size_w//2))
        return

    if cell.is_flag:
        color = pygame.Color("green")
        pygame.draw.rect(screen, color, rect)
        return

    elif not cell.is_open:
        color = pygame.Color("gray")
        pygame.draw.rect(screen, color, rect)
        return


def draw_cells(screen):
    for x, row in enumerate(game.field):
        for y, cell in enumerate(row):
            draw_cell(screen, x, y)


game = Field(height, width, 5)
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