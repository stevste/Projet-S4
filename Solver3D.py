import RubiksCubeTailleN
import random
from Enum import *

class cubeSimplifie:
    def __init__(self):
        self.config = [
            [ #FRONT FACE (vert)
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0]
            ],

            [ #UP FACE (orange)
                [1, 1, 1],
                [1, 1, 1],
                [1, 1, 1]
            ],

            [ #DOWN FACE (rouge)
                [2, 2, 2],
                [2, 2, 2],
                [2, 2, 2]
            ],

            [ #RIGHT FACE (jaune)
                [3, 3, 3],
                [3, 3, 3],
                [3, 3, 3]
            ],

            [ #LEFT FACE (blanc)
                [4, 4, 4],
                [4, 4, 4],
                [4, 4, 4]
            ],

            [ #BACK FACE (bleue)
                [5, 5, 5],
                [5, 5, 5],
                [5, 5, 5]
            ]
        ]

        self.corner = []
        self.edges = []

    def GetCorner(self):
        self.corner = []
        self.corner.append((self.config[1][2][2], self.config[3][0][0], self.config[0][0][2])) #URF
        self.corner.append((self.config[1][2][0], self.config[0][0][0], self.config[4][0][2])) #UFL
        self.corner.append((self.config[1][0][0], self.config[4][0][0], self.config[5][0][2])) #ULB
        self.corner.append((self.config[1][0][2], self.config[5][0][0], self.config[3][0][2])) #UBR
        self.corner.append((self.config[2][0][2], self.config[0][2][2], self.config[3][0][2])) #DFR
        self.corner.append((self.config[2][0][0], self.config[4][2][2], self.config[0][2][0])) #DLF
        self.corner.append((self.config[2][2][0], self.config[5][2][2], self.config[4][2][0])) #DBL
        self.corner.append((self.config[2][2][2], self.config[3][2][2], self.config[5][0][2])) #DRB

def jouerFormule(formule: list, cube: RubiksCubeTailleN):
    for i in formule:
        cube.ajouterAction(i)

def generateScrambleSubGroup():
    scramble = []

    for i in range (10):
        move = random.randint(0, 5)

        if move == 0:
            sens = random.randint(0, 1)
            if sens == 0:
                scramble.append((Faces.UP, Sens.HORAIRE))
            else:
                scramble.append((Faces.UP, Sens.ANTIHORAIRE))

        elif move == 1:
            sens = random.randint(0, 1)
            if sens == 0:
                scramble.append((Faces.DOWN, Sens.HORAIRE))
            else:
                scramble.append((Faces.DOWN, Sens.ANTIHORAIRE))
        
        elif move == 2:
            scramble.append((Faces.RIGHT, Sens.HORAIRE))
            scramble.append((Faces.RIGHT, Sens.HORAIRE))
        
        elif move == 3:
            scramble.append((Faces.LEFT, Sens.HORAIRE))
            scramble.append((Faces.LEFT, Sens.HORAIRE))
        
        elif move == 4:
            scramble.append((Faces.FRONT, Sens.HORAIRE))
            scramble.append((Faces.FRONT, Sens.HORAIRE))
        
        elif move == 5:
            scramble.append((Faces.BACK, Sens.HORAIRE))
            scramble.append((Faces.BACK, Sens.HORAIRE))

    return scramble