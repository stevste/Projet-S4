import RubiksCubeTailleN
import random
import math
from Enum import *

def ApplyConfig(dest: RubiksCubeTailleN, src: list):
    for i in range(0, len(src)):
        for j in range(0, len(src[i])):
            for k in range(0, len(src[i][j])):
                dest.configuration[i][j][k] = src[i][j][k]

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

def moveUp(liste, top, bot):
    save = liste[top]

    for i in range(top, bot):
        liste[i] = liste[i+1]
    liste[bot] = save

def ComparePiece(p1, p2):
    for i in p2:
        if i not in p1:
            return False
    return True

def GetPermCoord(pieceList, ref):
    coord = 0
    perm = list(pieceList)
    for i in range(len(ref)-1, 0, -1):
        k = 0
        while not ComparePiece(perm[i], ref[i]):
            moveUp(perm, 0, i)
            k += 1
        coord += k*math.factorial(i)

    return coord

def GetOriCoord(pieceList, ref, mod: CoordMod):
    coord = 0
    for i in pieceList:
        for j in ref:
            if ComparePiece(i, j):
                b = 0
                for c in i:
                    if c != j[0]:
                        b += 1
                    else:
                        break
                coord += b*pow(mod.value, pieceList.index(i))

    return coord

def GetUDSliceCoord():
    pass

def PhaseTwo(resultPhaseOne, refCorner, refEdges):
    actualCorner = resultPhaseOne
    coordP2 = (GetPermCoord())
    open = [(resultPhaseOne, )]

def PhaseOne():
    pass

def Solve(cube: RubiksCubeTailleN):
    clone = RubiksCubeTailleN()
    refCorner, refEdges = clone.coinsEtAretes()
    ApplyConfig(clone, cube.configuration)