from fileinput import close
import pygame
import random

# 10 x 20 square grid
# shapes: S, Z, Line, Block, J, L, T
# represented in order by 0 - 6

# Global vars
s_width = 600
s_height = 700
play_width = 300
play_height = 600
block_size = 30

top_left_x = play_width // 4
top_left_y = s_height - play_height

grid = {}
win = pygame.display.set_mode((s_width, s_height))

# SHAPE FORMATS

S = [['...',
      '.00',
      '00.'],
     ['.0.',
      '.00',
      '..0']]

Z = [['...',
      '00.',
      '.00'],
     ['.0.',
      '00.',
      '0..']]

Line = [['....',
         # '....',
         # '....',
         '0000'],
        ['.0..',
         '.0..',
         '.0..',
         '.0..']]

Block = [['...',
          '.00',
          '.00']]

J = [['...',
      '0..',
      '000',
      '...'],
     ['...',
      '.00',
      '.0.',
      '.0.'],
     ['...',
      '...',
      '000',
      '..0'],
     ['...',
      '.0.',
      '.0.',
      '00.']]

L = [['...',
      '..0',
      '000',
      '...'],
     ['...',
      '.0.',
      '.0.',
      '.00'],
     ['...',
      '...',
      '000',
      '0..'],
     ['...',
      '00.',
      '.0.',
      '.0.']]

T = [['...',
      '.0.',
      '000',
      '...'],
     ['...',
      '.0.',
      '.00',
      '.0.'],
     ['...',
      '...',
      '000',
      '.0.'],
     ['...',
      '.0.',
      '00.',
      '.0.']]

# index 0 - 6 represent shape
shapes = [S, Z, Line, Block, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0),
                (255, 165, 0), (0, 0, 255), (128, 0, 128)]


class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0


def create_grid(locked_positions):
    build_grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]

    for ii in range(len(build_grid)):
        for jj in range(len(build_grid[ii])):
            if (jj, ii) in locked_positions:
                build_grid[ii][jj] = locked_positions[(jj, ii)]
    return build_grid


def convert_shape_layout(shape):
    positions = []
    layout = shape.shape[shape.rotation % len(shape.shape)]

    for ii, line in enumerate(layout):
        row = list(line)
        for jj, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + jj, shape.y + ii))
    return positions


def valid_space(shape, valid_grid):
    accepted_positions = [[(jj, ii) for jj in range(10) if valid_grid[ii][jj] == (0, 0, 0)] for ii in range(20)]
    accepted_positions = [jj for sub in accepted_positions for jj in sub]

    for pos in convert_shape_layout(shape):
        if pos not in accepted_positions:
            if pos[1] > -2:
                return False

    return True


def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False


def get_shape():
    return Piece(3, -2, random.choice(shapes))


def draw_text_middle(text, size, color, surface):
    pygame.font.init()
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, True, color)

    pygame.draw.rect(surface, 'black', (s_width / 2 - label.get_width() / 2,
                                        s_height / 2 - label.get_height(),
                                        label.get_width(), label.get_height()))

    surface.blit(label, (s_width / 2 - label.get_width() / 2,
                         s_height / 2 - label.get_height()))


def draw_score(text, size, color, surface):
    pygame.font.init()
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, True, color, 'black')

    surface.blit(label, (s_width / 2 - label.get_width() / 2,
                         s_height / 2 - label.get_height() + 150))


def draw_grid(surface, d_grid):
    for ii in range(len(d_grid)):
        for jj in range(len(d_grid[ii])):
            pygame.draw.rect(surface, d_grid[ii][jj], (top_left_x + jj * block_size,
                                                       top_left_y + ii * block_size,
                                                       block_size, block_size))
            pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 1)


def clear_rows(clear_grid, locked):
    # need to see if row is clear to shift every other row above down one
    check = 0
    score = 0
    while check < 4:
        check += 1
        for ii in range(len(clear_grid) - 1, -1, -1):
            row = clear_grid[ii]
            inc = 0
            if (0, 0, 0) not in row:
                score += 1
                # add positions to remove from locked
                inc += 1
                ind = ii
                for jj in range(len(row)):
                    try:
                        del locked[(jj, ii)]
                    finally:
                        continue
                if inc > 0:
                    for key in sorted(list(locked), key=lambda _: _[1])[::-1]:
                        x, y = key
                        if y < ind:
                            new_key = (x, y + inc)
                            locked[new_key] = locked.pop(key)

                clear_grid = create_grid(locked)

    return score


def draw_next_shape(shape, surface, score=0):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Shape', True, 'white')

    sx = top_left_x + play_width + 30
    sy = int(top_left_y + play_height / 2 - 100)
    layout = shape.shape[shape.rotation % len(shape.shape)]

    for ii, line in enumerate(layout):
        row = list(line)
        for jj, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + 30 + jj * 30, sy + ii * 30, 30, 30), 0)

    surface.blit(label, (sx, sy - 50))

    label = font.render(f'Your score: {score}', True, 'white')
    surface.blit(label, (sx - 10, sy + 120))


def draw_window(surface):
    surface.fill((0, 0, 0))

    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('Tetris', True, 'white')

    surface.blit(label, (top_left_x + play_width / 2 - label.get_width() / 2, 0))

    # draw grid and border
    draw_grid(surface, grid)
    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5)


def score_check(user_name, score):  # checks whether the new highscore is higher than the score reached previously.
    score_list = []
    with open('Tetris_highscore.txt', 'r') as f:
        for line in f.readlines():
            score_list += line.replace('\n', ' ').split()
        high_scores = score_list[1::2]
        user_names = score_list[::2]
        if user_name not in user_names:
            high_score = '0'
        else:
            high_score = high_scores[user_names.index(user_name)]

    # Checks if the reached score is higher than the high_score
    if score > int(high_score):
        # If so; then overwrite the Tetris_highscore.txt with the new values
        high_score = str(score)
        draw_score(f'Congrats! A new high score: {high_score}', 30, 'white', win)
        with open('Tetris_highscore.txt', 'w') as f:
            if user_name in user_names:
                high_scores[user_names.index(user_name)] = high_score
                write_to = ''
                for name in user_names:
                    scores = high_scores[user_names.index(name)]
                    write_to += name + ' ' + scores + ' \n'
                f.write(write_to)
            else:
                user_names.append(user_name)
                high_scores.append(high_score)
                write_to = ''
                for name in user_names:
                    scores = high_scores[user_names.index(name)]
                    write_to += name + ' ' + scores + ' \n'
                f.write(write_to)
    else:
        # If not; just display the reached score this game.
        draw_score(f'Your score is: {score} And your highest score is: {high_score}', 20, 'white', win)
    pygame.display.update()


def main(user_name):
    global grid

    locked_positions = {}
    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.2
    level_time = 0
    score = 0

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        # PIECE FALLING CODE

        if level_time / 1000 > 5:
            level_time = 0
            if fall_speed > 0.15:
                fall_speed -= 0.005

        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1

        if not (valid_space(current_piece, grid)) and current_piece.y > -1:
            current_piece.y -= 1
            change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:
                    current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)
                    if not (valid_space(current_piece, grid)):
                        current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)

        shape_pos = convert_shape_layout(current_piece)

        # add piece to the grid for drawing
        for ii in range(len(shape_pos)):
            x, y = shape_pos[ii]
            if y > -1:
                grid[y][x] = current_piece.color

        # IF PIECE HIT GROUND
        if change_piece:
            for pos in shape_pos:
                pp = (pos[0], pos[1])
                locked_positions[pp] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False

            # call four times to check for multiple clear rows
            score += clear_rows(grid, locked_positions)

        draw_window(win)
        draw_next_shape(next_piece, win, score)
        pygame.display.update()

        # Check if user lost
        if check_lost(locked_positions):
            run = False

    draw_text_middle("You Lost", 40, 'white', win)

    # Possibly write score to high scores list
    score_check(user_name, score)

    # Wait for player input to restart or quit
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                main(user_name)


def main_menu():
    run = True
    pygame.init()
    pygame.display.set_caption('Tetris')
    user_font_size = 40
    user_font = pygame.font.SysFont('comicsans', user_font_size)
    user_name = ''

    # Main menu loop, in which the player is asked to type their name.
    while run:
        win.fill('black')
        draw_text_middle('Enter your name for high scores.', 30, 'white', win)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # Player writes their name
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    main(user_name)
                elif event.key == pygame.K_BACKSPACE:
                    user_name = user_name[:-1]
                else:
                    user_name += event.unicode

        input_text = user_font.render(user_name, True, 'white')

        win.blit(input_text, (s_width / 2 - input_text.get_width() / 2,
                              s_height / 2))
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main_menu()  # Load main screen
