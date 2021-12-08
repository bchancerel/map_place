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
### DECLARATION DES FONCTION
#
#

'''
Affiche la carte dans le terminal
'''
def print_map() :
    global MAP
    
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

'''
Place une croix aux coordonnées indiquées sur la carte
'''
def __transform_coords(x, y):
    map_x = MAP_X if (MAP_X % 2 == 0) else MAP_X - 1
    map_y = MAP_Y if (MAP_Y % 2 == 0) else MAP_Y - 1
    x = int(x + map_x / 2)
    y = int(y + map_y / 2)
    return(x, y)

def place(x, y) :
    x, y = __transform_coords(x, y)
    MAP[y][x] = 'X'
    print_map()

def remove(x, y):
    global BUFFER
    x, y = __transform_coords(x, y)
    MAP[y][x] = '0'
    BUFFER.append([x, y])
    print(BUFFER)
    print_map()

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

def get_cardinals(i) :
    return [[i, 0], [0, i], [-i, 0], [0, -i]]

def get_limites(i):
    return [[i, i], [-i, i], [-i, -i], [i, -i]]

def get_intervalles(i, j):
    return [[i, j], [j, i], [-j, i], [-i, j],
            [-i, -j], [-j, -i], [j, -i], [i, -j]]

def turn(index):
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

def verif_cmd_turn(cmd):
    if len(cmd) == 2 \
        and cmd[1].isnumeric() \
        and int(cmd[1]) <= (MAP_X - 1) / 2 :
        place(0, 0)
        turn(int(cmd[1]))
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
                pass
            elif cmd[0] == "place" :
                pass
            elif cmd[0] == "turn" :
               verif_cmd_turn(cmd)
            elif cmd[0] == "remove" :
                remove(1 , 2)
            else :
                print(cmd + "ne correspond a auccune instruction.")

### Run programme with args
#
#
main(int(args.map))