from enum import Enum

STRUCTURE = 6

class Axes(Enum):
    X = 0
    Y = 1
    Z = 2

class Faces(Enum):
    FRONT = 0
    BACK = 1
    RIGHT = 2
    LEFT = 3
    UP = 4
    DOWN = 5

class Sens(Enum):
    HORAIRE = -1
    ANTIHORAIRE = 1

class Couleur(Enum):
    VERT = (0.1, 0.8, 0.2)
    BLEU = (0, 0, 0.9)
    ROUGE = (0.9, 0, 0)
    ORANGE = (1, 0.5, 0)
    JAUNE = (1, 1, 0)
    BLANC = (1, 1, 1)
    LIST = (VERT, BLEU, ROUGE, ORANGE, JAUNE, BLANC)