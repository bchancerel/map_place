import sys
from math import *
import argparse

### Parse args
#
#
parser = argparse.ArgumentParser()

parser.add_argument(
    "-m",
    "--map",
    help        = "Indiquez la taille de la carte : " \
        + "\tLa carte est carré, la valeur indiqué doit nécéssairement être" \
        + "\timpaire pour que la carte possède un centre.",
    required    = True
    )

args = parser.parse_args()

if not args.map.isnumeric() :
    print("-m, --map doit être un nombre entier non négatif.")
    exit(1) # instruction systhème
elif int(args.map) % 2 == 0 :
    print("-m, --map doit être un nombre entier impaire.")
    exit(1) # instruction systhème

### Gloabal définition
#
#
'''
Liste des inputs disponible
'''
INPUT_CMD   = {
    'auto'    :
        "Aucun arguements n'est attendu, place automatiquement un x à la" \
        + "prochaine case",
    'place'         : "Il faut indiquer deux nombre décimal",
    'turn'          :
        "Effectue une nombre d'auto_place équivalent au nombre indiqué en " \
        + "paramettre",
    'remove'        :
        "Supprime un x au coordonnées indiqué",
    'exit'          :
        "Quitte la programme."
    }

'''
La taille de la carte entré par l'utilisateur enregistré dans le scope global
du script
'''
MAP_SIZE    = 0
MAP         = []
MAP_X       = 0
MAP_Y       = 0
BUFFER      = []
NEXT_COORDS = []
### DECLARATION DES FONCTION
#
#

'''
Affiche la carte dans le terminal
'''
def print_map() :
    global MAP

    print(BUFFER)
    
    for row in MAP :
        for col in row :
            sys.stdout.write(col + ' ')
        print('')
    print('')

def create_map() :

    global MAP
    MAP = []
    for y in range(0, MAP_Y) :
        row = []
        for x in range(0, MAP_X) :
            row.append('o')
        MAP.append(row)


def print_coords(x, y) :
    print("coords : [" + str(x) + ", " + str(y) + "]")

'''
Transform le systhème de coordonné strictement positif en un sythème de
coordonné centré sur 0 0 et donne les coordonnées minimales
'''
def min_coords() :
    map_size = MAP_SIZE if (MAP_SIZE % 2 == 0 ) else MAP_SIZE - MAP_X
    return (-map_size / 2 / MAP_X, -map_size / 2 / MAP_Y)

'''
Transform le systhème de coordonné strictement positif en un sythème de
coordonné centré sur 0 0 et donne les coordonnées maximal
'''
def max_coords() :
    map_size = MAP_SIZE if (MAP_SIZE % 2 == 0 ) else MAP_SIZE - MAP_Y
    return (map_size / 2 / MAP_X, map_size / 2 / MAP_Y)

def __transform_coords(x, y):
    map_x = MAP_X if (MAP_X % 2 == 0) else MAP_X - 1
    map_y = MAP_Y if (MAP_Y % 2 == 0) else MAP_Y - 1
    x = int(x + map_x / 2)
    y = int(y + map_y / 2)
    return(x, y)

'''
Place une croix aux coordonnées indiquées sur la carte
'''
def get_next_cards(x, y):
    if y == 0 :
        y = x
        x = 0
    elif x == 0 and y > 0 :
        x = -y
        y = 0
    elif x == 0 and y < 0:
        x = -y
        y = -y
    
    NEXT_COORDS.append([x, y])
    if len(NEXT_COORDS) > 1 :
        del NEXT_COORDS[0]
        print(NEXT_COORDS)

def get_next_limites(x, y):
    if x == y:
        x = -y
    elif x < 0 and y > 0 :
        y = x
    elif x == 1 and y == -1 :
        x += 1
        y = 0
    elif x > 0 and y < 0 :
        y = 1
    
    NEXT_COORDS.append([x, y])
    if len(NEXT_COORDS) > 1 :
        del NEXT_COORDS[0]
        print(NEXT_COORDS)

def get_next_intervalles(x, y):
    if x > 1 and 0 < y < x :
        x, y = y, x
    elif y > 1 and 0 < x < y :
        x = -x
    elif y > 1 and x < 0 and abs(x) < abs(y) :
        x, y = -y, -x
    elif x < -1 and 0 < y :
        y = -y
    elif x < -1 and y < 0 and abs(y) < abs(x) :
        x, y = y, x
    elif y < -1 and x < 0 :
        x = -x
    elif x > 0 and y < -1  and abs(y) > abs(x):
        x, y = -y, -x
    elif x > 2 and y <= -1 and abs(x) - abs(y) > 1:
        y = abs(y) + 1
    elif x >= 2 and y <= -1 and abs(x) - abs(y) == 1 :
        x += 1
        y = 0

    NEXT_COORDS.append([x, y])
    if len(NEXT_COORDS) > 1 :
        del NEXT_COORDS[0]
        print(NEXT_COORDS)

def place(x, y) :
    global NEXT_COORDS
    _x, _y = __transform_coords(x, y)
    print(x, y)
    if MAP[_y][_x] == 'X' :
        print("Cette emplacement est déjà occupé, placment impossible")
    else :
        MAP[_y][_x] = 'X'
        # Calcul des prochaine coordonées 

        # Calcul du prochain cardinaux 
        if x == 0 and y == 0:
            x = 1
            NEXT_COORDS.append([x, y])
            if len(NEXT_COORDS) > 1 :
                del NEXT_COORDS[0]
        elif x == 0 or y == 0:
            get_next_cards(x, y)

        # Calcul de la prochaine limite 
        elif abs(x) == abs(y):
            get_next_limites(x, y)

        # Calcul de la prochiane intervalle 
        elif x != y and x != 0 and y != 0:
            get_next_intervalles(x, y)
           
        print_map()

def place_without_calcul(x, y):
    global NEXT_COORDS
    _x, _y = __transform_coords(x, y)
    print(x, y)
    if MAP[_y][_x] == 'X':
        print("Cette emplacement est déjà occupé, placment impossible")
    else :
        MAP[_y][_x] = 'X'
        print_map()

def verif_cmd_place(cmd):
    if len(cmd) == 3 :
        x = cmd[1]
        y = cmd[2]
        if x[0] == '-':
            x = x[1:]
        if y[0] == '-':
            y = y[1:]
        
        if x.isnumeric() \
        and y.isnumeric() \
        and int(cmd[1]) <= (MAP_X - 1) / 2 \
        and int(cmd[2]) <= (MAP_Y - 1) / 2 :
            place_without_calcul(int(cmd[1]), int(cmd[2]))
    else : 
        print("Les deuxième et troisième paramètre doivent être un nomnre" \
            + " et inférieur ou égale à la moitié de la carte")

def auto():
    global BUFFER
    if len(BUFFER) == 0:
        if len(NEXT_COORDS) == 0 :
            place(0, 0)
        else :
            place(NEXT_COORDS[0][0], NEXT_COORDS[0][1])
    else :
        place_without_calcul(BUFFER[0][0], BUFFER[0][1])
        del BUFFER[0]        

def remove(x, y):
    global BUFFER
    _x, _y = __transform_coords(x, y)
    if MAP[_y][_x] == 'o' or MAP[_y][_x] == '0':
       print("Veuillez choisir un autre emplacement celui-ci est vide")
    else : 
        MAP[_y][_x] = '0'
        BUFFER.append([x, y])
        print_map()

def verif_cmd_remove(cmd) :
    if len(cmd) == 3 :
        x = cmd[1]
        y = cmd[2]
        if x[0] == '-' :
            x = x[1:]
        if y[0] == '-' :
            y = y[1:]

        if x.isnumeric() \
        and y.isnumeric() \
        and int(cmd[1]) <= (MAP_X - 1) / 2 \
        and int(cmd[2]) <= (MAP_Y - 1) / 2 :
            remove(int(cmd[1]), int(cmd[2]))
    else :
        print("Les deuxième et troisième paramètre doivent être un nomnre" \
            + " et inférieur ou égale à la moitié de la carte")
'''
Prend une chaine de caractère et vérifie si celle-ci correspond a des
paramettres indiqués dans INPUT_CMD
'''
def parse_input(input) :
    if not input or not input in INPUT_CMD.keys() :
        print("\nL'input doit être une de ces options :")
        for key in INPUT_CMD :
            print("\t" + key + "\t\t: " + INPUT_CMD[key])
        print()
        return False
    # Intégrer des vérifications sur les paramettres de la commande
    return True

'''
Turn avec système de tableau qui obtient les valeurs via des fontions gat 
'''
def get_cardinals(i) :
    return [[i, 0], [0, i], [-i, 0], [0, -i]]

def get_limites(i):
    return [[i, i], [-i, i], [-i, -i], [i, -i]]

def get_intervalles(i, j):
    return [[i, j], [j, i], [-j, i], [-i, j],
            [-i, -j], [-j, -i], [j, -i], [i, -j]]

def turn_v1(index):
    global MAP
    for k in range(1, index + 1):
        cards       = get_cardinals(k)
        limites     = get_limites(k)
        # placement des points cardinaux
        for card in cards :
            place(card[0], card[1])
        # placements des diagonales
        for limite in limites :
            place(limite[0], limite[1])
        # placement des points d'intervalles
        for j in range(1, k) :
            intervalles = get_intervalles(k, j)
            for intervalle in intervalles :
                place(intervalle[0], intervalle[1])

'''
Turn avec le système calcul de place
'''

def turn_v2(index):
    for i in range(index):
        if len(NEXT_COORDS) == 0 :
            place(0, 0)
        else :
            place(NEXT_COORDS[0][0], NEXT_COORDS[0][1])

def verif_cmd_turn(cmd):
    if len(cmd) == 2 \
    and cmd[1].isnumeric() :
        turn_v2(int(cmd[1]))
    else :
        print("Le deuième paramètre doit être un nombre" \
            + " et inférieur ou égale à la moitié de la carte" 
            )

### Programme entrypoint
#
#
def main(size) :
    global MAP_SIZE
    global MAP_X
    global MAP_Y

    MAP_Y     = size
    MAP_X     = size
    MAP_SIZE  = MAP_X * MAP_Y
    i         = 0
    create_map()
    print_map()
    # min_coords()
    # max_coords()
    while True :
        cmd = input("map_place $ ").split(" ")
        if parse_input(cmd[0]) :
            print("Executons cette commande")
            if cmd[0] == "exit" :
                exit(0) # instruction systhème
            elif cmd[0] == "auto" :
                auto()
            elif cmd[0] == "place" :
                verif_cmd_place(cmd)
            elif cmd[0] == "turn" :
               verif_cmd_turn(cmd)
            elif cmd[0] == "remove" :
                verif_cmd_remove(cmd)
            else :
                print(cmd + "ne correspond a auccune instruction.")

### Run programme with args
#
#
main(int(args.map))