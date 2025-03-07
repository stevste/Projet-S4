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
    
    AXES_ROTATION = (Axes.Y, Axes.Y, Axes.X, Axes.X, Axes.Z, Axes.Z)
    SENS_ROTATIONS = (1, -1, 1, -1, 1, -1)
    SIGNES_ABSCISSES = (-1, 1, 1, -1, 1, -1) # 1 si la face a une abscisse positive par rapport à son axe de rotation, -1 sinon

class Sens(Enum):
    HORAIRE = 1
    ANTIHORAIRE = -1

class Couleur(Enum):
    VERT = (0.1, 0.8, 0.2)
    BLEU = (0, 0, 0.9)
    ROUGE = (0.9, 0, 0)
    ORANGE = (1, 0.5, 0)
    JAUNE = (1, 1, 0)
    BLANC = (0.9, 0.9, 0.9)
    
    LIST = (BLEU, VERT, ROUGE, ORANGE, BLANC, JAUNE) # dans l'ordre FRONT, BACK, RIGHT, LEFT, UP, DOWN

SENSIBILITE_SOURIS = 0.3

class Coins(Enum):
    """Liste des coins hiérarchisée pour le solveur

    """
    URF = 0
    UFL = 1
    ULB = 2
    UBR = 3
    DFR = 4
    DLF = 5
    DBL = 6
    DRB = 7

class Aretes(Enum):
    FU = 0
    FR = 1
    FD = 2
    FL = 3
    BU = 4
    BR = 5
    BD = 6
    BL = 7
    LU = 8
    LD = 9
    RU = 10
    RD = 11

class Moves(Enum):
    U1 = 0
    U2 = 1
    U3 = 2
    D1 = 3
    D2 = 4
    D3 = 5
    R1 = 6
    R2 = 7
    R3 = 8
    L1 = 9
    L2 = 10
    L3 = 11
    F1 = 12
    F2 = 13
    F3 = 14
    B1 = 15
    B2 = 16
    B3 = 17
    MOVELIST = [U1, U2, U3, D1, D2, D3, R1, R2, R3, L1, L2, L3, F1, F2, F3, B1, B2, B3]
    
NB_DE_PIXELS_DANS_UNE_UNITE = 82.64 # valeur empirique valable seulement pour cette perspective précise