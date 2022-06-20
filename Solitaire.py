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


def selected_card(win, column1, column2, column3, column4, column5, column6, column7, drawing_column, discard_column,
                visible_cards, final_column1, final_column2, final_column3, final_column4, mpos_x, mpos_y, previous_selection):
    def draw_cards(column):
        # constants:
        pygame.font.init()
        font = pygame.font.SysFont('linuxlibertinegregular', 40)
        card_width = 150; card_height = 200; corner_radius = 10
        white = (250, 250, 250); black = (0, 0, 0); red = (200, 0, 0); yellow = (200, 200, 0)
        
        # variables:
        selection = []
        count = 0
        
        # now for every card in the list we're looking through:
        for card_type, card_number in column:
            # keep track of which card is currently worked on:
            count += 1
            # split cardtypes and -numbers
            if card_type == 0:
                card_symbol = '♠'
                card_colour = black
            elif card_type == 1:
                card_symbol = '♥'
                card_colour = red
            elif card_type == 2:
                card_symbol = '♣'
                card_colour = black
            else:
                card_symbol = '♦'
                card_colour = red

            # determine the location of the top left of the card on the board:
            card_location_y = (row * count * 40 + row * card_height + 20)
            card_location_x = (30 + cc * (card_width + 15))

            # determine which whether the current card is visible or closed:
            if (card_type, card_number) in visible_cards:
                # draw white cards with number and symbol
                
                # card background
                pygame.draw.rect(win, white, (card_location_x, card_location_y, card_width, card_height), 0, corner_radius)
                # outline:
                pygame.draw.rect(win, black, (card_location_x, card_location_y, card_width, card_height), 1, corner_radius)
                # symbol and number
                label = font.render(f'{card_symbol}{card_number}', True, card_colour)
                win.blit(label, (10 + card_location_x, card_location_y))

            else:
                # draw blue cards
                colour_count = count
                if colour_count >= 8:
                    colour_count = 7
                pygame.draw.rect(win, (0, 0, (100 + (colour_count * 20))), (
                        card_location_x, card_location_y, card_width, card_height), 0, corner_radius)
                pygame.draw.rect(win, black, (
                        card_location_x, card_location_y, card_width, card_height), 1, corner_radius)

            # draw a yellow line around this card if selected by the player:
            def draw_selection():
                pygame.draw.rect(win, yellow, (card_location_x, card_location_y, card_width, card_height), 3, corner_radius)

            def add_card():
                if previous_selection == []:
                    draw_selection()
                if previous_selection != []:
                    # print(f'previous_selection {previous_selection}')
                    for card in previous_selection:
                        if card not in column:
                            column.append(card)
                    # previous_selection = []
                selection.append((card_type, card_number))

            # see if the card being drawn is the card the player selected, first by finding which column, -
            if card_location_x <= mpos_x <= 30 + (cc + 1) * (card_width + 15) - 15:
                # - then consider if the top card is clicked:
                    if card_location_y <= mpos_y <= row * count * 40 + row * card_height + card_height + 19:
                        add_card()
                    elif card_location_y <= mpos_y <= row * count * 40 + card_height + row * 40 + 19:
                        add_card()
                      
        return selection

    selection1 = []
    # select which column of cards to draw and possibly select. cc = columns
    for cc in range(7):
        for row in range(2):
            if row == 1:
                if cc == 0:
                    possible_selection = draw_cards(column1)
                elif cc == 1:
                    possible_selection = draw_cards(column2)
                elif cc == 2:
                    possible_selection = draw_cards(column3)
                elif cc == 3:
                    possible_selection = draw_cards(column4)
                elif cc == 4:
                    possible_selection = draw_cards(column5)
                elif cc == 5:
                    possible_selection = draw_cards(column6)
                elif cc == 6:
                    possible_selection = draw_cards(column7)

            else:
                if cc == 0:
                    possible_selection = draw_cards(final_column1)
                elif cc == 1:
                    possible_selection = draw_cards(final_column2)
                elif cc == 2:
                    possible_selection = draw_cards(final_column3)
                elif cc == 3:
                    possible_selection = draw_cards(final_column4)
                elif cc == 4:
                    pass
                elif cc == 5:
                    possible_selection = draw_cards(discard_column)
                elif cc == 6:
                    possible_selection = draw_cards(drawing_column)
                    
        if possible_selection != []:
            selection1 = possible_selection
    pygame.display.update()
    return selection1


def main():
    # start by distributing random cards to the playing field
    column1, column2, column3, column4, column5, column6, column7, drawing_column = start_up_board()
    # generate empty lists for the:
    visible_cards = []; final_column1 = []; final_column2 = []; final_column3 = []; final_column4 = []
    discard_column = []
    
    pygame.init()
    pygame.display.set_caption('Solitaire door Alexander')
    win = pygame.display.set_mode((1200, 800))
    win.fill((0, 55, 0))
    flag = True
    mpos_x = mpos_y = 0
    empty_selection = 0
    previous_selection = []
    # make all top cards front-facing (visible) cards:
    visible_cards = visible_card_list(visible_cards, column1, column2, column3, column4, column5, column6,
                                      column7, discard_column)
    # draw the start-up board for the first time:
    selected_card(win, column1, column2, column3, column4, column5, column6, column7, drawing_column,
               discard_column, visible_cards, final_column1, final_column2, final_column3, final_column4, mpos_x, mpos_y, previous_selection)

    while flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # get the position of the mouse
                mpos_x, mpos_y = event.pos
                
                visible_cards = visible_card_list(visible_cards, column1, column2, column3, column4, column5, column6,
                                                    column7, discard_column)

                # draw the playing field
                selection1 = selected_card(win, column1, column2, column3, column4, column5, column6, column7, drawing_column,
                           discard_column, visible_cards, final_column1, final_column2, final_column3, final_column4, mpos_x, mpos_y, previous_selection)
                
                print(f'previous_selection {previous_selection}')
                print(f'selection {selection1}')
                print(f'empty {empty_selection}')

                if selection1 != [] and empty_selection != 1:
                    if previous_selection == selection1:
                        previous_selection = []
                        empty_selection = 0
                    else:
                        previous_selection = selection1
                        empty_selection += 1
                else:
                    previous_selection = []
                    empty_selection = 0


if __name__ == "__main__":
    main()
