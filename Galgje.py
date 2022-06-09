"""
Tekkieworden: Leer galgje in Python
gebruik: python3 galgje.py
gemaakt door: Jurre van CodeCafé
"""

import random

GALGJE_ASCII = ['''
  +---+
  |   |
      |
      |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
      |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
  |   |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\  |
   \  |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========''']


def toon_bord(woord, fout_gok, goed_gok):
    print(GALGJE_ASCII[fout_gok])

    huidige_woord = woord
    for letter in woord:
        if letter not in goed_gok:
            huidige_woord = huidige_woord.replace(letter, '_')
    print(huidige_woord)


def main():
    moeilijke_woorden = []
    f = open("moeilijke_woorden.txt")
    for line in f.readlines():
        moeilijke_woorden += line.replace('\n', ' ').split()

    # taak 1: uitkiezen woord
    woord = moeilijke_woorden[random.randint(0, len(moeilijke_woorden) - 1)]
    toon_bord(woord, 0, "")

    gok_geschiedenis = []
    goed_gok = ""
    fout_gok = 0

    while True:
        gok = str(input("Geef mij een letter: ")).lower()
        while len(gok) != 1 or not gok.isalpha():
            gok = str(input("Geef mij ÉÉN letter: ")).lower()

        if gok in woord:
            if gok not in gok_geschiedenis:
                goed_gok += gok
                gok_geschiedenis.append(gok)
                toon_bord(woord, fout_gok, goed_gok)

                if len(set(goed_gok)) == len(set(woord)):
                    print("Gefeliciteerd, je hebt gewonnen!")

                    speel_nog_een_keer = str(input("Wil je nog een keer spelen?")).lower()

                    if speel_nog_een_keer == "ja" or speel_nog_een_keer == "j":
                        main()
                    else:
                        exit()

            else:
                print(f"Je hebt deze letter {gok} al eens ingevuld.")
                continue

        else:
            print(gok_geschiedenis)
            if gok not in gok_geschiedenis:
                fout_gok += 1
                gok_geschiedenis.append(gok)
                toon_bord(woord, fout_gok, goed_gok)

                if fout_gok >= 6:
                    toon_bord(woord, fout_gok, goed_gok)
                    print(woord)
                    print("Helaas, je hebt verloren.")

                    speel_nog_een_keer = str(input("Wil je nog een keer spelen?")).lower()

                    if speel_nog_een_keer == "ja" or speel_nog_een_keer == "j":
                        main()
                    else:
                        exit()


if __name__ == "__main__":
    main()
