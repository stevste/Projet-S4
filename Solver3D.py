from RubiksCubeTailleN import RubiksCube
import random
import math
from Enum import *

def jouerFormule(formule: list, cube: RubiksCube):
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

def ApplyMove(m: Moves, cube: RubiksCube):
    match m:
        case Moves.U1:
            cube.pivoterFace(Faces.UP, Sens.HORAIRE)
        case Moves.U2:
            cube.pivoterFace(Faces.UP, Sens.HORAIRE)
            cube.pivoterFace(Faces.UP, Sens.HORAIRE)
        case Moves.U3:
            cube.pivoterFace(Faces.UP, Sens.ANTIHORAIRE)
        case Moves.D1:
            cube.pivoterFace(Faces.DOWN, Sens.HORAIRE)
        case Moves.D2:
            cube.pivoterFace(Faces.DOWN, Sens.HORAIRE)
            cube.pivoterFace(Faces.DOWN, Sens.HORAIRE)
        case Moves.D3:
            cube.pivoterFace(Faces.DOWN, Sens.ANTIHORAIRE)
        case Moves.R1:
            cube.pivoterFace(Faces.RIGHT, Sens.HORAIRE)
        case Moves.R2:
            cube.pivoterFace(Faces.RIGHT, Sens.HORAIRE)
            cube.pivoterFace(Faces.RIGHT, Sens.HORAIRE)
        case Moves.R3:
            cube.pivoterFace(Faces.RIGHT, Sens.ANTIHORAIRE)
        case Moves.L1:
            cube.pivoterFace(Faces.LEFT, Sens.HORAIRE)
        case Moves.L2:
            cube.pivoterFace(Faces.LEFT, Sens.HORAIRE)
            cube.pivoterFace(Faces.LEFT, Sens.HORAIRE)
        case Moves.L3:
            cube.pivoterFace(Faces.LEFT, Sens.ANTIHORAIRE)
        case Moves.F1:
            cube.pivoterFace(Faces.FRONT, Sens.HORAIRE)
        case Moves.F2:
            cube.pivoterFace(Faces.FRONT, Sens.HORAIRE)
            cube.pivoterFace(Faces.FRONT, Sens.HORAIRE)
        case Moves.F3:
            cube.pivoterFace(Faces.FRONT, Sens.ANTIHORAIRE)
        case Moves.B1:
            cube.pivoterFace(Faces.BACK, Sens.HORAIRE)
        case Moves.B2:
            cube.pivoterFace(Faces.BACK, Sens.HORAIRE)
            cube.pivoterFace(Faces.BACK, Sens.HORAIRE)
        case Moves.B3:
            cube.pivoterFace(Faces.BACK, Sens.ANTIHORAIRE)

def ApplyConfig(dest: RubiksCube, src: list):
    for i in range(0, len(src)):
        for j in range(0, len(src[i])):
            for k in range(0, len(src[i][j])):
                dest.configuration[i][j][k] = src[i][j][k]

def CompareConfig(config1, config2):
    for i in range(0, len(config1)):
        for j in range(0, len(config1[i])):
            for k in range(0, len(config1[i][j])):
                if config1[i][j][k] != config2[i][j][k]:
                    return False
    return True

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
    for i in range(7, 0, -1):
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

def GetUDSliceCoord(edgeList, refEdge):
    k = -1
    coord = 0
    for i in range(0, len(edgeList)):
        notUD = False
        for j in range(8, 12):
            if ComparePiece(edgeList[i], refEdge[j]):
                notUD = True
                break
        if notUD:
            k += 1
        elif k >= 0:
            coord += math.comb(i, k)

    return coord

def PhaseTwo(cube: RubiksCube, refCorner, refEdges):
    def GetLenght(coordP2):
        return coordP2[0]/40319 + coordP2[1]/(math.factorial(12)-1) + coordP2[2]/23
    
    actualCorner, actualEdge = cube.coinsEtAretes()
    solve = False
    coordP2 = (GetPermCoord(actualCorner, refCorner), GetPermCoord(actualEdge, refEdges), GetUDSliceCoord(actualEdge, refEdges))
    open = [(cube.configuration, None, coordP2, None)]
    close = []

    while not solve and len(open) > 0:
        distList = []
        for i in open:
            distList.append(GetLenght(i))
        
        minimal = min(distList)

        if minimal == 0:
            solve = True
        else:
            minimalIndex = distList.index(min(distList))
            minConfig = open[minimalIndex][0]
            ApplyConfig(cube, minConfig)

            for m in Moves.MOVELIST.value:
                if m in [Moves.R1, Moves.R3, Moves.L1, Moves.L3, Moves.F1, Moves.F3, Moves.B1, Moves.B3]:
                    continue
                else:
                    ApplyMove(m, cube)
                    inClose = False
                    for c in close:
                        if CompareConfig(cube, c[0]):
                            inClose = True
                    
                    if not inClose:
                        newCorners, newEdges = cube.coinsEtAretes()
                        coordP2 = (GetPermCoord(newCorners, refCorner), GetPermCoord(newEdges, refEdges), GetUDSliceCoord(newEdges, refEdges))
                        open.append(cube.configuration, minConfig, coordP2, m)
                    ApplyConfig(cube, minConfig)
            
            close.append(open[minimalIndex])
            open.pop(minimalIndex)


def PhaseOne():
    pass

def Solve(cube: RubiksCube):
    clone = RubiksCube()
    refCorner, refEdges = clone.coinsEtAretes()
    ApplyConfig(clone, cube.configuration)