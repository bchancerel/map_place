import sys
from math import *

### DECLARATION DE CONSTANTE
#
#

'''
La carte doit être égale au carré d'un nombre impaire pour posséder un centre
'''
MAP_SIZE    = 121

MAP_X       = 11
MAP_Y       = 11

MAP         = [
    ['o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o'],
    ['o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o'],
    ['o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o'],
    ['o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o'],
    ['o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o'],
    ['o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o'],
    ['o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o'],
    ['o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o'],
    ['o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o'],
    ['o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o'],
    ['o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o'],
]

### DECLARATION DES FONCTION
#
#

'''
Affiche la carte dans le terminal
'''
def print_map() :
    for row in MAP :
        for col in row :
            sys.stdout.write(col + ' ')
        print('')
    print('')

def print_coords(x, y) :
    print("coords : [" + str(x) + ", " + str(y) + "]")

'''
Transform le systhème de coordonné strictement positif en un sythème de
coordonné centré sur 0 0 et donne les coordonnées minimales
'''
def min_coords() :
    map_size = MAP_SIZE if (MAP_SIZE % 2 == 0 ) else MAP_SIZE - MAP_X
    print(-map_size / 2 / MAP_X, -map_size / 2 / MAP_Y)
    return (-map_size / 2 / MAP_X, -map_size / 2 / MAP_Y)
'''
Transform le systhème de coordonné strictement positif en un sythème de
coordonné centré sur 0 0 et donne les coordonnées maximal
'''
def max_coords() :
    map_size = MAP_SIZE if (MAP_SIZE % 2 == 0 ) else MAP_SIZE - MAP_Y
    print(map_size / 2 / MAP_X, map_size / 2 / MAP_Y)
    return (map_size / 2 / MAP_X, map_size / 2 / MAP_Y)

def place(x, y) :
    map_x = MAP_X if (MAP_X % 2 == 0) else MAP_X - 1
    map_y = MAP_Y if (MAP_Y % 2 == 0) else MAP_Y - 1

    x = int(x + map_x / 2)
    y = int(y + map_y / 2)
    MAP[y][x] = 'X'
    print_map()

def cardinal(index):
    x = 0
    y = 0

    if index % 8 == 0:
        x += 1
    if index % 8 == 1:
        y += 1
        x += 1
    if index % 8 == 2:
        y += 1
    if index % 8 == 3:
        y += 1
        x -= 1
    if index % 8 == 4:
        x -= 1
    if index % 8 == 5:
        x -= 1
        y -= 1
    if index % 8 == 6:
        y -=1
    if index % 8 == 7:
        y -= 1
        x += 1

    place(x, y)

def ex():
    for k in range(0, 8):
        cardinal(k)
        k += 1

def run() :

    print_map()
    min_coords()
    max_coords()
    place(0, 0)
    ex()

run()