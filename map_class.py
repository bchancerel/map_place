import sys
from math import *
import argparse

class MapTermPrinterMixin() :

    @staticmethod
    def print_coords(x : int, y : int) :
        print("coords : [" + str(x) + ", " + str(y) + "]")

    MAP         = []

    def __init__(self, map_x : int, map_y : int) :
        self.map    = MapTermPrinterMixin.MAP
        if not self.map_x or not self.map_y :
            raise MapException(
                "Map instance must be instanciate before this" + self.__class__
                )

        if not self.map :
            for y in range(0, self.map_y) :
                row = []
                for x in range(0, self.map_x) :
                    row.append('o')
                self.map.append(row)

    '''
    Affiche la carte dans le terminal
    '''
    def _print_map(self) :
        for row in self.map :
            for col in row :
                sys.stdout.write(col + ' ')
            print('')
        print('')

    '''
    Ecrit dans la carte
    '''
    def _write_to(self, x, y, symbole = 'x') :
        self.map[x][y] = symbole

class Map() :

    '''
    La taille de la carte entré par l'utilisateur enregistré dans le scope global
    du script
    '''
    MAP_SIZE    = 0

    MAP_X       = 0

    MAP_Y       = 0

    REMOVED     = []

    NEXT        = []

    def __init__(self, map_x : int, map_y : int) :
        # Assignation statique. Partage des variable de class avec l'instance.
        self.map_size   = Map.MAP_SIZE
        self.map_x      = Map.MAP_X
        self.map_y      = Map.MAP_Y
        self.removed    = Map.REMOVED
        self.next       = Map.NEXT

        # Assignation valeur à la carte
        self.map_x      = int(map_x)
        self.map_y      = int(map_y)
        self.map_size   = self.map_x * self.map_y

    '''
    Transform les coordonées centré sur [0, 0] en coordonées avec l'angle droit
    en [0, 0]
    '''
    def __transforms_coords(self, x : int, y : int) :
        map_x = self.map_x if (self.map_x % 2 == 0) else self.map_x - 1
        map_y = self.map_y if (self.map_y % 2 == 0) else self.map_y - 1
        x = int(x + map_x / 2)
        y = int(y + map_y / 2)
        return (x, y)

    '''
    Donne les coordonnées minimales avec le systhème de coordonné centré sur
    [0, 0]
    '''
    def get_min_coords(self) :
        if (self.map_size % 2 == 0 ) :
            map_size = self.map_size
        else :
            map_size = self.map_size - self.map_x
        return (-map_size / 2 / self.map_x, -map_size / 2 / self.map_y)

    '''
    Donne les coordonnées maximal avec le systhème de coordonné centré sur
    [0, 0]
    '''
    def get_max_coords(self) :
        if (self.map_size % 2 == 0 ) :
            map_size = self.map_size
        else :
            map_size = self.map_size - self.map_y
        return (map_size / 2 / self.map_x, map_size / 2 / self.map_y)


    def get_cardinals(self, last_x, last_y) :
        if last_y == 0 :
            last_y = last_x
            last_x = 0
        elif last_x == 0 and last_y > 0 :
            last_x = -last_y
            last_y = 0
        elif last_x == 0 and last_y < 0:
            last_x = -last_y
            last_y = -last_y

        self.next.append([last_x, last_y])
        if len(self.next) > 1 :
            del self.next[0]
            print(self.next)

    def get_limites(self, last_x, last_y) :
        if last_x == last_y:
            last_x = -last_y
        elif last_x < 0 and last_y > 0 :
            last_y = last_x
        elif last_x == 1 and last_y == -1 :
            last_x += 1
            last_y = 0
        elif last_x > 0 and last_y < 0 :
            last_y = 1

        self.next.append([last_x, last_y])
        if len(self.next) > 1 :
            del self.next[0]
            print(self.next)

    def get_interval(self, last_x, last_y) :
        if last_x > 1 and 0 < last_y < last_x :
            last_x, last_y = last_y, last_x
        elif last_y > 1 and 0 < last_x < last_y :
            last_x = -last_x
        elif last_y > 1 and last_x < 0 and abs(last_x) < abs(last_y) :
            last_x, last_y = -last_y, -last_x
        elif last_x < -1 and 0 < last_y :
            last_y = -last_y
        elif last_x < -1 and last_y < 0 and abs(last_y) < abs(last_x) :
            last_x, last_y = last_y, last_x
        elif last_y < -1 and last_x < 0 :
            last_x = -last_x
        elif last_x > 0 and last_y < -1  and abs(last_y) > abs(last_x):
            last_x, last_y = -last_y, -last_x
        elif last_x > 2 and last_y <= -1 and abs(last_x) - abs(last_y) > 1:
            last_y = abs(last_y) + 1
        elif last_x >= 2 and last_y <= -1 and abs(last_x) - abs(last_y) == 1 :
            last_x += 1
            last_y = 0

        self.next.append([last_x, last_y])
        if len(self.next) > 1 :
            del self.next[0]
            print(self.next)

    '''
    Le buffer stock les coordonées qui ont été placé mais qui on été supprimé
    par la suite.
    '''
    def get_buffer_coords(self) :
        if self.buffer :
            return self.buffer.pop()
        else :
            return None

    def place(self, x = None, y = None) :
        if x == None or y == None :
            x, y = 0, 0
            if self.removed :
                x = self.removed[0][0]
                y = self.removed[0][1]
                del self.removed[0]
            elif self.next :
                x = self.next[0][0]
                y = self.next[0][1]
                del self.next[0]
            if x == 0 or y == 0 :
                self.get_cardinals(x, y)
            elif abs(x) == abs(y):
                self.get_limites(x, y)
            elif x != y and x != 0 and y != 0:
                self.get_interval(x, y)
        return self.__transforms_coords(x, y)

    def remove(self, x, y):
        # Remove
        _x, _y = self.__transforms_coords(x, y)
        self.removed.append([x, y])
            
        return _x, _y 

class MapCMD(Map, MapTermPrinterMixin) :

    AVAILABLE_CMD   = {
        'auto'  : 'Aucun argument n\'est attendu, place automatiquement aux' \
                + 'prochaines coordonées disponible.',
        'place' : 'Il faut indiquer les coordonées décimale x et y.',
        'turn'  : 'Effectue un nombre d\'auto placement équivalent au nombre' \
                + 'indiqué en paramettres.',
        'remove': 'Supprime à l\'emplacement indiqué.',
        'exit'  : 'Quitte le programme'
        }

    def __parse_cmd(self, args) :
        if not args.map.isnumeric() :
            print("-m, --map doit être un nombre entier non négatif.")
            exit(1)
        elif int(args.map) % 2 == 0 :
            print("-m, --map doit être un nombre entier impaire.")
            exit(1)
        return args

    def __init__(self) :
        # Load command parser
        self.parser     = argparse.ArgumentParser()
        self.parser.add_argument(
            "-m",
            "--map",
            help        = "Indiquez la taille de la carte : " \
                        + "\t La carte est carré, la valeur indiqué doit être"
                        + "impaire pour qu'elle possède un centte.",
            required    = True
            )

        # Parse command
        args            = self.__parse_cmd(self.parser.parse_args())
        x               = args.map
        y               = args.map

        # Load tools to do stuff
        Map.__init__(self, x, y)
        MapTermPrinterMixin.__init__(self, x, y)

    def __parse_input(self, input = None) :
        if not input or not input in MapCMD.AVAILABLE_CMD.keys() :
            print("\nL'input doit être une de ces options :")
            for key in MapCMD.AVAILABLE_CMD.keys() :
                print("\t" + key + "\t\t: " + MapCMD.AVAILABLE_CMD[key])
            return False
        return True

    def __verif_cmd_place(self, cmd) :
        if len(cmd) == 3 :
            x = cmd[1]
            y = cmd[2]
            if x[0] == '-':
                x = x[1:]
            if y[0] == '-':
                y = y[1:]

            if x.isnumeric() \
            and y.isnumeric() \
            and int(cmd[1]) <= (self.map_x - 1) / 2 \
            and int(cmd[2]) <= (self.map_y - 1) / 2 :
                return True
        print("Error")
        return False


    def __verif_cmd_turn(self, cmd) :
        if len(cmd) == 2 \
            and cmd[1].isnumeric() :
            return True
        else :
            print("Error") # Indiqué la valeur max par le calcul
            return False

    def __verif_cmd_remove(self, cmd) :
        if len(cmd) == 3 :
            x = cmd[1]
            y = cmd[2]
            if x[0] == '-' :
                x = x[1:]
            if y[0] == '-' :
                y = y[1:]

            if x.isnumeric() \
            and y.isnumeric() \
            and int(cmd[1]) <= (self.map_x - 1) / 2 \
            and int(cmd[2]) <= (self.map_y - 1) / 2 :
                return True
        print("Error")
        return False

    def place(self, x, y) :
        x, y = super().place(x, y) # Pourquoi super ici ?
        if x != None and y != None :
            super()._write_to(x, y)

    def remove(self, x, y) :
        x, y = super().remove(x, y) # Pourquoi super ici ?
        if x != None and y != None :
            super()._write_to(x, y, symbole='o')

    def run(self) :
        self._print_map()
        while True :
            cmd = input("map_place $ ").split(" ")
            if self.__parse_input(cmd[0]) :
                if cmd[0] == "auto" :
                    self.place(x=None, y=None)
                    self._print_map() # Pourquoi pas super ici ?
                elif cmd[0] == "place" and self.__verif_cmd_place(cmd) :
                    self.place(int(cmd[1]), int(cmd[2]))
                    self._print_map() # Pourquoi pas super ici ?
                elif cmd[0] == "turn" and self.__verif_cmd_turn(cmd) :
                    for i in range(0, int(cmd[1])) :
                        self.place(x=None, y=None)
                    self._print_map() # Pourquoi pas super ici ?
                elif cmd[0] == "remove" and self.__verif_cmd_remove(cmd) :
                    self.remove(int(cmd[1]), int(cmd[2]))
                    self._print_map() # Pourquoi pas super ici ?
                elif cmd[0] == "exit" :
                    exit(0)


app = MapCMD()
app.run()