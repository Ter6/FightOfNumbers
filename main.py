import sys
import pygame
import mechanics

pygame.init()

screen = pygame.display.set_mode((1104, 1004))
screen.fill((35, 35, 35))
pygame.display.set_caption("FoN")
img = pygame.image.load("icon.png")
pygame.display.set_icon(img)
font = pygame.font.SysFont("ComicSans", 20)

side = ["red", "red"]
numbs = {"r": 1, "b": 1}
field = mechanics.field
size_block = 50
margin = 12
grey = (80, 80, 80)
lum_grey = (100, 100, 100)
red = (200, 0, 0)
lum_red = (220, 0, 0)
blue = (0, 0, 200)
lum_blue = (0, 0, 220)
white = (240, 240, 240)
lum = []
win = ""


def create_strips(x, y, numb_strips):
    if numb_strips == 1 or numb_strips == 3:
        pygame.draw.line(screen, white, (x + size_block // 2, y + 5), (x + size_block // 2, y + size_block - 5))
        if numb_strips == 3:
            pygame.draw.line(screen, white, (x + size_block // 4, y + 5), (x + size_block // 4, y + size_block - 5))
            pygame.draw.line(screen, white, (x + size_block // 4 * 3, y + 5),
                             (x + size_block // 4 * 3, y + size_block - 5))
    if numb_strips == 2:
        pygame.draw.line(screen, white, (x + size_block // 3, y + 5), (x + size_block // 3, y + size_block - 5))
        pygame.draw.line(screen, white, (x + size_block // 3 * 2, y + 5), (x + size_block // 3 * 2, y + size_block - 5))
    if 4 <= numb_strips <= 8:
        pygame.draw.line(screen, white, (x + size_block // 5, y + 5), (x + size_block // 5, y + size_block - 5))
        pygame.draw.line(screen, white, (x + size_block // 5 * 4, y + 5), (x + size_block // 5 * 4, y + size_block - 5))
        pygame.draw.line(screen, white, (x + size_block // 5 * 3, y + 5), (x + size_block // 5 * 3, y + size_block - 5))
        pygame.draw.line(screen, white, (x + size_block // 5 * 2, y + 5), (x + size_block // 5 * 2, y + size_block - 5))
        if 5 <= numb_strips <= 6:
            pygame.draw.line(screen, white, (x + 5, y + 10), (x + size_block - 5, y + size_block - 10))
            if numb_strips == 6:
                pygame.draw.line(screen, white, (x + 5, y + size_block - 10), (x + size_block - 5, y + 10))
        if numb_strips == 7:
            pygame.draw.line(screen, white, (x + 5, y + size_block // 2), (x + size_block - 5, y + size_block // 2))
            pygame.draw.line(screen, white, (x + 5, y + size_block // 4), (x + size_block - 5, y + size_block // 4))
            pygame.draw.line(screen, white, (x + 5, y + size_block - (size_block // 4)),
                                            (x + size_block - 5, y + size_block - (size_block // 4)))
        if numb_strips == 8:
            pygame.draw.line(screen, white, (x + 5, y + size_block // 5), (x + size_block - 5, y + size_block // 5))
            pygame.draw.line(screen, white, (x + 5, y + size_block // 5 * 2), (x + size_block - 5, y + size_block // 5 * 2))
            pygame.draw.line(screen, white, (x + 5, y + size_block // 5 * 3), (x + size_block - 5, y + size_block // 5 * 3))
            pygame.draw.line(screen, white, (x + 5, y + size_block // 5 * 4), (x + size_block - 5, y + size_block // 5 * 4))


def cell_count():
    global field, numbs
    f_numbers = [0, 0]
    for row in range(16):
        for col in range(16):
            if field[row][col][0] == "r":
                f_numbers[0] += 1
            if field[row][col][0] == "b":
                f_numbers[1] += 1
    numbs = {"r": f_numbers[0], "b": f_numbers[1]}


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if win != "":
            continue
        if event.type == pygame.MOUSEBUTTONDOWN:
            x_mouse, y_mouse = pygame.mouse.get_pos()
            if x_mouse > 992:
                if side[0] == side[1]:
                    side[1] = "yellow"
                else:
                    if side[0] == "red":
                        side = ["blue", "blue"]
                    else:
                        side = ["red", "red"]
            y_place = y_mouse // (size_block + margin)
            x_place = x_mouse // (size_block + margin)
            if x_place < 16:
                if side[0] != side[1]:
                    mechanics.add_numb(field[y_place][x_place], numbs[side[0][0]])
                    numbs[side[0][0]] -= 1
                    continue
                if (y_place, x_place) in lum:
                    mechanics.move(lum[0], (y_place, x_place))
                    cell_count()
                    if numbs["r"] == 0:
                        win = "blue"
                    elif numbs["b"] == 0:
                        win = "red"
                if field[y_place][x_place][0] == side[0][0]:
                    lum = [(y_place, x_place), (max(0, y_place - 1), x_place), (min(15, y_place + 1), x_place),
                           (y_place, max(0, x_place - 1)), (y_place, min(15, x_place + 1))]
            else:
                lum = []
    if win != "":
        pygame.draw.rect(screen, (20, 20, 20), (0, 0, 1104, 1004))
        pygame.draw.line(screen, win, (15, 15), (1089, 989))
        pygame.draw.line(screen, win, (1089, 15), (15, 989))
        pygame.display.update()
        continue
    for row in range(16):
        for col in range(16):
            x = col * size_block + (col + 1) * margin
            y = row * size_block + (row + 1) * margin
            if field[row][col][0] == "n":
                if (row, col) in lum:
                    pygame.draw.rect(screen, lum_grey, (x, y, size_block, size_block))
                else:
                    pygame.draw.rect(screen, grey, (x, y, size_block, size_block))
            if field[row][col][0] == "r":
                if (row, col) in lum:
                    pygame.draw.rect(screen, lum_red, (x, y, size_block, size_block))
                else:
                    pygame.draw.rect(screen, red, (x, y, size_block, size_block))
            if field[row][col][0] == "b":
                if (row, col) in lum:
                    pygame.draw.rect(screen, lum_blue, (x, y, size_block, size_block))
                else:
                    pygame.draw.rect(screen, blue, (x, y, size_block, size_block))
            create_strips(x, y, field[row][col][1])
    pygame.draw.rect(screen, side[0], (1004, margin, 88, 892))
    pygame.draw.rect(screen, side[1], (1004, 904, 88, 88))
    pygame.display.update()
