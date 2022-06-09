# Snake tutorial youtube.com/watch?v=XGf2GcyHPhc vanaf 47 minuten

import pyautogui
import pygame
import random
import time
import tkinter as tk
from tkinter import messagebox


# De basis voor alle dynamische elementen in dit spel: de blokken.
class Cube(object):
    rows = 20
    w = 500

    def __init__(self, start, color=(255, 0, 0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    # De schakeling tussen positie(pos) van een blok en de richting van /
    # beweging(dirn) in de x en y richting. Ergo; de nieuwe positie berekenen.
    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    # De positie van een blok in zijn rij/kolom.
    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        # Het daadwerkelijk tekenen van een blok.
        pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 1, dis - 1))

        # En indien dit het Hoofd-blok is, teken er ogen bij.
        if eyes:
            centre = dis // 2
            radius = 3
            circle_middle = (i * dis + centre - radius, j * dis + 8)
            circle_middle2 = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, (0, 0, 0), circle_middle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circle_middle2, radius)


# De bewegende slang. Belangrijk onderdeel om te begrijpen is dat turns(dict) een locatiegebonden /
# bepaling is waar (dirnx, dirny) van een blok vastgezet wordt.
# Ergo; de blokken veranderen op de plek van turns van richting.
class Snake(object):
    body = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = Cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 0

    # Wanneer de slang moet bewegen.
    def move(self):
        # Wanneer een richting-knop wordt ingedrukt:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            # De verschillende knoppen met bijbehorende richting-wijziging.
            for _ in keys:
                if keys[pygame.K_w] and self.dirny < 1:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_d] and self.dirnx > -1:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_s] and self.dirny > -1:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_a] and self.dirnx < 1:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_ESCAPE]:
                    pygame.quit()
                    quit()

        # Dan nu het daadwerkelijke verplaatsen van de blokken. Hier wordt eerst een lijst gemaakt van /
        # alle blokken die het lichaam van de slang opmaken.
        cc: Cube
        for ii, cc in enumerate(self.body):
            pp = cc.pos[:]

            # Indien de blokken van richting moeten veranderen op deze plek:
            if pp in self.turns:
                turn = self.turns[pp]
                cc.move(turn[0], turn[1])

                # Zodra het laatste blok van de slang de plek van richtingswijziging heeft bereikt /
                # verwijder dan de richtingswijziging op deze plek.
                if ii == len(self.body) - 1:
                    self.turns.pop(pp)

            # Indien een blok het speelveld verlaat, komt het aan de andere kant weer in het veld.
            else:
                if cc.dirnx == -1 and cc.pos[0] <= 0:
                    cc.pos = (cc.rows - 1, cc.pos[1])
                elif cc.dirnx == 1 and cc.pos[0] >= cc.rows - 1:
                    cc.pos = (0, cc.pos[1])
                elif cc.dirny == 1 and cc.pos[1] >= cc.rows - 1:
                    cc.pos = (cc.pos[0], 0)
                elif cc.dirny == -1 and cc.pos[1] <= 0:
                    cc.pos = (cc.pos[0], cc.rows - 1)

                # Blijft het blok binnen het veld, dan verplaatst het één vak in de opgegeven richting.
                else:
                    cc.move(cc.dirnx, cc.dirny)

    # Reset turns list. Verwijdert alle blokken en de volgorde van bewegingen.
    def reset(self, pos):
        self.head = Cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    # Voeg een blok toe aan het uiteinde van de slang.
    def add_cube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        # Zorg dat het toegevoegde blok daadwerkelijk achteraan, aansluitend aan de slang wordt toegevoegd.
        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        cc: Cube
        for ii, cc in enumerate(self.body):
            if ii == 0:
                cc.draw(surface, True)
            else:
                cc.draw(surface)


def draw_grid(ww, draw_grid_rows, surface):
    size_between = ww // draw_grid_rows

    xx = 0
    yy = 0
    for ll in range(draw_grid_rows):
        xx = xx + size_between
        yy = yy + size_between

        pygame.draw.line(surface, (255, 255, 255), (xx, 0), (xx, ww))
        pygame.draw.line(surface, (255, 255, 255), (0, yy), (ww, yy))


def redraw_window(surface):
    # global grid_rows, width, ss, snack
    surface.fill((0, 0, 0))
    ss.draw(surface)
    snack.draw(surface)
    draw_grid(width, grid_rows, surface)
    pygame.display.update()


def random_snack(rows, item):
    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break

    return x, y


# Berichtenbox tekenen.
def message_box(subject, content):
    root = tk.Tk()
    root.withdraw()
    return messagebox.askretrycancel(subject, content)


width = 500
grid_rows = 20
ss = Snake((255, 0, 0), (10, 10))
snack = Cube(random_snack(grid_rows, ss), color=(0, 255, 0))


def main():
    global width, grid_rows, ss, snack
    win = pygame.display.set_mode((width, width))
    flag = True
    clock = pygame.time.Clock()

    while flag:
        pygame.time.delay(0)
        clock.tick(8)
        ss.move()
        if ss.body[0].pos == snack.pos:
            ss.add_cube()
            snack = Cube(random_snack(grid_rows, ss), color=(0, 255, 0))

        for x in range(len(ss.body)):
            if ss.body[0].pos in list(map(lambda z: z.pos, ss.body[x + 1:])):
                print("Score: ", len(ss.body))
                retry = message_box("Hap uit jezelf!", "Score: " + str(len(ss.body)) + "\nOpnieuw spelen?")
                if retry:
                    ss.reset((10, 10))
                    pyautogui.keyDown('alt')
                    time.sleep(.001)
                    pyautogui.press('tab')
                    time.sleep(.001)
                    pyautogui.keyUp('alt')
                elif retry is False:
                    pygame.quit()
                    exit()
            break

        redraw_window(win)

    pass


if __name__ == "__main__":
    main()
