import pygame
import random
import sys


def shuffle_deck():
    shuffled_deck = []
    while len(shuffled_deck) != 52:
        card = random.randrange(0, 52)
        if card not in shuffled_deck:
            shuffled_deck.append(card)

    return shuffled_deck


def standard_deck():
    a_standard_deck = []
    card_colour = 0
    while len(a_standard_deck) != 52:
        colour_set = 0
        card_number = 1
        while colour_set != 13:
            a_standard_deck.append((card_colour, card_number))
            card_number += 1
            colour_set += 1
        card_colour += 1

    return a_standard_deck


def starting_deck():
    shuffled_deck = shuffle_deck()
    look_up_deck = standard_deck()
    playing_deck = []
    for random_card in shuffled_deck:
        playing_deck.append(look_up_deck[random_card])

    return playing_deck


def start_up_board():
    # Zeven rijen, vier eindvakken, één aflegstapel en één trekstapel
    column1 = []; column2 = []; column3 = []; column4 = []; column5 = []; column6 = []; column7 = []
    drawing_column = []
    deck_of_cards = starting_deck()

    column1.append(deck_of_cards[0])
    for card in deck_of_cards[1:3]:
        column2.append(card)
    for card in deck_of_cards[3:6]:
        column3.append(card)
    for card in deck_of_cards[6:10]:
        column4.append(card)
    for card in deck_of_cards[10:15]:
        column5.append(card)
    for card in deck_of_cards[15:21]:
        column6.append(card)
    for card in deck_of_cards[21:28]:
        column7.append(card)
    for card in deck_of_cards[28:52]:
        drawing_column.append(card)

    return column1, column2, column3, column4, column5, column6, column7, drawing_column


def visible_card_list(visible_cards, column1, column2, column3, column4, column5, column6, column7, discard_column):
    # only adds the top card to the list of visible cards
    def top_card(column):
        try:
            if column[-1] not in visible_cards:
                visible_cards.append(column[-1])
        except IndexError:
            pass

    top_card(column1)
    top_card(column2)
    top_card(column3)
    top_card(column4)
    top_card(column5)
    top_card(column6)
    top_card(column7)
    top_card(discard_column)

    return visible_cards


def draw_board(win, column1, column2, column3, column4, column5, column6, column7, drawing_column, discard_column,
               card_width, card_height,
               visible_cards, final_column1, final_column2, final_column3, final_column4, mpos_x, mpos_y):
    def draw_cards(column):
        pygame.font.init()
        font = pygame.font.SysFont('linuxlibertinegregular', 40)
        count = 0
        for card_type, card_number in column:
            # split cardtypes and -numbers
            if card_type == 0:
                card_symbol = '♠'
                card_colour = (0, 0, 0)
            elif card_type == 1:
                card_symbol = '♥'
                card_colour = (200, 0, 0)
            elif card_type == 2:
                card_symbol = '♣'
                card_colour = (0, 0, 0)
            else:
                card_symbol = '♦'
                card_colour = (200, 0, 0)

            # build cardtype and -number
            label = font.render(f'{card_symbol}{card_number}', True, card_colour)
            count += 1
            if count >= 8:
                count = 7

            if (card_type, card_number) in visible_cards:
                # draw white cards with number and symbol
                colour = (250, 250, 250)
                # card background
                pygame.draw.rect(win, colour, (
                        30 + cc * (card_width + 15), row * count * 40 + card_height + 20, card_width, card_height))
                # outline:
                pygame.draw.rect(win, (0, 0, 0), (
                        30 + cc * (card_width + 15), row * count * 40 + row * card_height + 20, card_width, card_height), 1)
                # symbol and number
                win.blit(label, (40 + cc * (card_width + 15), row * count * 40 + card_height + 20))

            else:
                # draw blue cards
                pygame.draw.rect(win, (0, 0, (100 + (count * 20))), (
                        30 + cc * (card_width + 15), row * count * 40 + row * card_height + 20, card_width, card_height))
                pygame.draw.rect(win, (0, 0, 0), (
                        30 + cc * (card_width + 15), row * count * 40 + row * card_height + 20, card_width, card_height), 1)

            # draw a yellow line around this card if selected by the player:
            def draw_selection():
                pygame.draw.rect(win, (200, 200, 0), (
                        30 + cc * (card_width + 15), row * count * 40 + row * card_height + 20, card_width, card_height), 5)

            # see if the card being drawn is the card the player selected, first by finding which column, -
            if 30 + cc * (card_width + 15) <= mpos_x <= 30 + (cc + 1) * (card_width + 15) - 15:
                # - then consider if the top card is clicked:
                if (card_type, card_number) == column[-1]:
                    if row * count * 40 + row * card_height + 20 <= mpos_y <= row * count * 40 + row * card_height + card_height + 19:
                        draw_selection()
                # - or if one the cards underneath the top card is clicked, in which case the area to click on is smaller.
                else:
                    if row * count * 40 + row * card_height + 20 <= mpos_y <= row * count * 40 + card_height + row * 40 + 19:
                        draw_selection()

    # select which column of cards to draw. cc = columns
    for cc in range(7):
        for row in range(2):
            if row == 1:
                if cc == 0:
                    draw_cards(column1)
                elif cc == 1:
                    draw_cards(column2)
                elif cc == 2:
                    draw_cards(column3)
                elif cc == 3:
                    draw_cards(column4)
                elif cc == 4:
                    draw_cards(column5)
                elif cc == 5:
                    draw_cards(column6)
                elif cc == 6:
                    draw_cards(column7)

            else:
                if cc == 0:
                    draw_cards(final_column1)
                elif cc == 1:
                    draw_cards(final_column2)
                elif cc == 2:
                    draw_cards(final_column3)
                elif cc == 3:
                    draw_cards(final_column4)
                elif cc == 4:
                    pass
                elif cc == 5:
                    draw_cards(discard_column)
                elif cc == 6:
                    draw_cards(drawing_column)

    pygame.display.update()


def main():
    # start by distributing random cards to the playing field
    column1, column2, column3, column4, column5, column6, column7, drawing_column = start_up_board()
    # generate empty lists for the:
    visible_cards = []; final_column1 = []; final_column2 = []; final_column3 = []; final_column4 = []
    discard_column = []
    width = 1200
    height = 800
    card_width = 150
    card_height = 200
    pygame.init()
    pygame.display.set_caption('Solitaire door Alexander')
    win = pygame.display.set_mode((width, height))
    win.fill((0, 55, 0))
    flag = True
    mpos_x = mpos_y = 0
    visible_cards = visible_card_list(visible_cards, column1, column2, column3, column4, column5, column6,
                                      column7, discard_column)
    draw_board(win, column1, column2, column3, column4, column5, column6, column7, drawing_column,
               discard_column, card_width, card_height,
               visible_cards, final_column1, final_column2, final_column3, final_column4, mpos_x, mpos_y)

    while flag:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # get the position of the mouse
                mpos_x, mpos_y = event.pos
                # check for new front-facing (visible) cards
                visible_cards = visible_card_list(visible_cards, column1, column2, column3, column4, column5, column6,
                                                  column7, discard_column)
                # draw the playing field
                draw_board(win, column1, column2, column3, column4, column5, column6, column7, drawing_column,
                           discard_column, card_width, card_height,
                           visible_cards, final_column1, final_column2, final_column3, final_column4, mpos_x, mpos_y)


if __name__ == "__main__":
    main()
