import RubiksCubeTailleN
import random
from Enum import *

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

def GetCornerPermCoord():
    pass

def GetCornerOriCoord():
    pass

def GetUDSliceCoord():
    pass

def GetEdgePermCoord():
    pass

def GetEdgeOriCoord():
    pass

def PhaseTwo():
    pass