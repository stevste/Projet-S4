from enum import Enum, IntEnum
import pygame


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
    URF = 0
    UFL = 1
    ULB = 2
    UBR = 3
    DFR = 4
    DLF = 5
    DBL = 6
    DRB = 7
class Aretes(IntEnum):
    UR = 0
    UF = 1
    UL = 2
    UB = 3
    DR = 4
    DF = 5
    DL = 6
    DB = 7
    FR = 8
    FL = 9
    BL = 10
    BR = 11

class Moves(IntEnum):
    U1 = 0
    U2 = 1
    U3 = 2
    R1 = 3
    R2 = 4
    R3 = 5
    F1 = 6
    F2 = 7
    F3 = 8
    D1 = 9
    D2 = 10
    D3 = 11
    L1 = 12
    L2 = 13
    L3 = 14
    B1 = 15
    B2 = 16
    B3 = 17

# Pour l'enchaînement des fenêtres :
QUITTER = -1
MENU = 0
CARRES = 1
CUBES = 2
PIVOTS = 3
SOLVEUR = 4

CUBE_2 = 5
CUBE_3 = 6
CUBE_4 = 7
CUBE_5 = 8
CUBE_6 = 9
CUBE_7 = 10

CARRE_3 = 11
CARRE_4 = 12
CARRE_5 = 13

PIVOT_2X3 = 14
PIVOT_3X3 = 15
PIVOT_3X4 = 16

COULEUR_FOND = (150, 175, 215)#(175, 175, 215)
COULEUR_BOUTONS = (175, 215, 230)
ROUGE = (200, 130, 130)
VERT = (150, 215, 150)

IMAGE_MULTICOLORE = pygame.image.load("Images\imageMulticolore.jpg")
IMAGE_COLOREE = pygame.image.load("Images\imageColoree.jpg")
PHOTO_CUBES = pygame.image.load("Images\photoTousLesCubes.png")
