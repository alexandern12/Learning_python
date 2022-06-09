# Vier op een rij, uit de serie pygames van https://www.youtube.com/watch?v=XGf2GcyHPhc 1:36:23
import math
import sys

import numpy as np
import pygame

blue = (0, 0, 255)
black = (0, 0, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)
green = (0, 255, 0)
row_count = 6
column_count = 7


def create_board():
    board = np.zeros((row_count, column_count))
    return board


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[row_count - 1][col] == 0


def get_next_open_row(board, col):
    for rr in range(row_count):
        if board[rr][col] == 0:
            return rr


def print_board(board):
    print(np.flip(board, 0))


def winning_move(board, piece):
    # Controleer de horizontale locaties om te winnen
    for cc in range(column_count - 3):
        for rr in range(row_count):
            if board[rr][cc] == piece and board[rr][cc + 1] == piece and board[rr][cc + 2] == piece and \
                    board[rr][cc + 3] == piece:
                for tt in range(cc, cc + 4):
                    pygame.draw.circle(screen, green, (int(tt * square_size + square_size / 2),
                                                       height - int(rr * square_size + square_size / 2)), radius / 2)
                return True

    # Controleer verticale locaties om te winnen
    for cc in range(column_count):
        for rr in range(row_count - 3):
            if board[rr][cc] == piece and board[rr + 1][cc] == piece and board[rr + 2][cc] == piece and \
                    board[rr + 3][cc] == piece:
                for tt in range(rr, rr + 4):
                    pygame.draw.circle(screen, green, (int(cc * square_size + square_size / 2),
                                                       height - int(tt * square_size + square_size / 2)), radius / 2)
                return True

    # Controleer oplopende schuine locaties om te winnen
    for cc in range(column_count - 3):
        for rr in range(row_count - 3):
            if board[rr][cc] == piece and board[rr + 1][cc + 1] == piece and \
                    board[rr + 2][cc + 2] == piece and board[rr + 3][cc + 3] == piece:
                pp = rr
                for tt in range(cc, cc + 4):
                    pygame.draw.circle(screen, green, (int(tt * square_size + square_size / 2),
                                                       height - int(pp * square_size + square_size / 2)), radius / 2)
                    pp = pp + 1
                return True

    # Controleer aflopende schuine locaties om te winnen
    for cc in range(column_count - 3):
        for rr in range(row_count):
            if board[rr][cc] == piece and board[rr - 1][cc + 1] == piece and \
                    board[rr - 2][cc + 2] == piece and board[rr - 3][cc + 3] == piece:
                pp = rr
                for tt in range(cc, cc + 4):
                    pygame.draw.circle(screen, green, (int(tt * square_size + square_size / 2),
                                                       height - int(pp * square_size + square_size / 2)), radius / 2)
                    pp = pp - 1
                return True


def draw_board(board3d):
    for cc in range(column_count):
        for rr in range(row_count):
            pygame.draw.rect(screen, blue, (cc * square_size, rr * square_size + square_size,
                                            square_size, square_size))
            pygame.draw.circle(screen, black,
                               (int(cc * square_size + square_size / 2),
                                int(rr * square_size + square_size + square_size / 2)), radius)

    for cc in range(column_count):
        for rr in range(row_count):
            if board3d[rr][cc] == 1:
                pygame.draw.circle(screen, red,
                                   (int(cc * square_size + square_size / 2),
                                    height - int(rr * square_size + square_size / 2)), radius)
            elif board3d[rr][cc] == 2:
                pygame.draw.circle(screen, yellow,
                                   (int(cc * square_size + square_size / 2),
                                    height - int(rr * square_size + square_size / 2)), radius)
    pygame.display.update()


square_size = 100
width = column_count * square_size
height = (row_count + 1) * square_size
size = (width, height)
radius = int(square_size / 2 - 5)

screen = pygame.display.set_mode(size)


def main():
    board = create_board()
    draw_board(board)
    pygame.init()
    game_over = False
    turn = 0
    my_font = pygame.font.SysFont("monospace", 75)
    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Vraag speler 1 om input
                if turn == 0:
                    pos_x = event.pos[0]
                    col = int(math.floor(pos_x / square_size))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 1)
                        # De beurt is aan de volgende speler
                        turn += 1
                        draw_board(board)

                        if winning_move(board, 1):
                            print("Speler 1 heeft gewonnen!")
                            label = my_font.render("Speler 1 wint!", True, red)
                            screen.blit(label, (40, 10))
                            game_over = True

                # Vraag speler 2 om input
                else:
                    pos_x = event.pos[0]
                    col = int(math.floor(pos_x / square_size))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 2)
                        # De beurt is aan de volgende speler
                        turn += 1
                        draw_board(board)

                        if winning_move(board, 2):
                            print("Speler 2 heeft gewonnen!")
                            label = my_font.render("Speler 2 wint!", True, yellow)
                            screen.blit(label, (40, 10))
                            game_over = True

                print_board(board)
                if game_over:
                    pygame.display.update()
                    pygame.time.wait(3000)
                    sys.exit()
                else:
                    # De beurt is aan de volgende speler
                    turn = turn % 2


if __name__ == "__main__":
    main()
