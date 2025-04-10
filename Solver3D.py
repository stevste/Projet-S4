from RubiksCubeTailleN import RubiksCube
import random
import math
from Enum import *
import CubieCube as cb
import PrunningTable as prT

cubeRef = RubiksCube()
class SymClass:
    def __init__(self, cube: RubiksCube, ref = cubeRef):
        self.mainConfig = CopyConfig(cube.configuration)
        self.classMembers = [cube.coinsEtAretes()]

        for i in range(0, 3):
            self.classMembers.append(self.rotate(i))

        self.minCoord = GetP2Coord(self.classMembers[0], cubeRef.coinsEtAretes())

        for i in range(1, 4):
            coord = GetP2Coord(self.classMembers[i], cubeRef.coinsEtAretes())

            if coord < self.minCoord:
                self.minCoord = coord

    def rotate(self, startIndex = 0):
        newConfig = []

        for c in range(2):
            newConfig.append([])
            for i in range(len(self.classMembers[startIndex][c])):
                newConfig[c].append([])
                for j in self.classMembers[startIndex][c][i]:
                    match j:
                        case Faces.FRONT:
                            newConfig[c][i].append(Faces.RIGHT)
                        case Faces.RIGHT:
                            newConfig[c][i].append(Faces.BACK)
                        case Faces.BACK:
                            newConfig[c][i].append(Faces.LEFT)
                        case Faces.LEFT:
                            newConfig[c][i].append(Faces.FRONT)
                        case _:
                            newConfig[c][i].append(j)

        return newConfig

    def isInClass(self, pieceList):
        for i in self.classMembers:
            if ComparePiece(pieceList, i):
                return True
        
        return False

def jouerFormule(formule: list, cube: RubiksCube):
    for m in formule:
        match m:
            case Moves.U1.value:
                cube.ajouterAction((Faces.UP, Sens.HORAIRE))
            case Moves.U2.value:
                cube.ajouterAction((Faces.UP, Sens.HORAIRE))
                cube.ajouterAction((Faces.UP, Sens.HORAIRE))
            case Moves.U3.value:
                cube.ajouterAction((Faces.UP, Sens.ANTIHORAIRE))
            case Moves.D1.value:
                cube.ajouterAction((Faces.DOWN, Sens.HORAIRE))
            case Moves.D2.value:
                cube.ajouterAction((Faces.DOWN, Sens.HORAIRE))
                cube.ajouterAction((Faces.DOWN, Sens.HORAIRE))
            case Moves.D3.value:
                cube.ajouterAction(Faces.DOWN, Sens.ANTIHORAIRE)
            case Moves.R1.value:
                cube.ajouterAction((Faces.RIGHT, Sens.HORAIRE))
            case Moves.R2.value:
                cube.ajouterAction((Faces.RIGHT, Sens.HORAIRE))
                cube.ajouterAction((Faces.RIGHT, Sens.HORAIRE))
            case Moves.R3.value:
                cube.ajouterAction((Faces.RIGHT, Sens.ANTIHORAIRE))
            case Moves.L1.value:
                cube.ajouterAction((Faces.LEFT, Sens.HORAIRE))
            case Moves.L2.value:
                cube.ajouterAction((Faces.LEFT, Sens.HORAIRE))
                cube.ajouterAction((Faces.LEFT, Sens.HORAIRE))
            case Moves.L3.value:
                cube.ajouterAction((Faces.LEFT, Sens.ANTIHORAIRE))
            case Moves.F1.value:
                cube.ajouterAction((Faces.FRONT, Sens.HORAIRE))
            case Moves.F2.value:
                cube.ajouterAction((Faces.FRONT, Sens.HORAIRE))
                cube.ajouterAction((Faces.FRONT, Sens.HORAIRE))
            case Moves.F3.value:
                cube.ajouterAction((Faces.FRONT, Sens.ANTIHORAIRE))
            case Moves.B1.value:
                cube.ajouterAction((Faces.BACK, Sens.HORAIRE))
            case Moves.B2.value:
                cube.ajouterAction((Faces.BACK, Sens.HORAIRE))
                cube.ajouterAction((Faces.BACK, Sens.HORAIRE))
            case Moves.B3.value:
                cube.ajouterAction((Faces.BACK, Sens.ANTIHORAIRE))

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
                scramble.append(((Faces.DOWN, Sens.HORAIRE)))
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
        case Moves.U1.value:
            cube.pivoterFace(Faces.UP, Sens.HORAIRE)
        case Moves.U2.value:
            cube.pivoterFace(Faces.UP, Sens.HORAIRE)
            cube.pivoterFace(Faces.UP, Sens.HORAIRE)
        case Moves.U3.value:
            cube.pivoterFace(Faces.UP, Sens.ANTIHORAIRE)
        case Moves.D1.value:
            cube.pivoterFace((Faces.DOWN, Sens.HORAIRE))
        case Moves.D2.value:
            cube.pivoterFace((Faces.DOWN, Sens.HORAIRE))
            cube.pivoterFace((Faces.DOWN, Sens.HORAIRE))
        case Moves.D3.value:
            cube.pivoterFace(Faces.DOWN, Sens.ANTIHORAIRE)
        case Moves.R1.value:
            cube.pivoterFace(Faces.RIGHT, Sens.HORAIRE)
        case Moves.R2.value:
            cube.pivoterFace(Faces.RIGHT, Sens.HORAIRE)
            cube.pivoterFace(Faces.RIGHT, Sens.HORAIRE)
        case Moves.R3.value:
            cube.pivoterFace(Faces.RIGHT, Sens.ANTIHORAIRE)
        case Moves.L1.value:
            cube.pivoterFace(Faces.LEFT, Sens.HORAIRE)
        case Moves.L2.value:
            cube.pivoterFace(Faces.LEFT, Sens.HORAIRE)
            cube.pivoterFace(Faces.LEFT, Sens.HORAIRE)
        case Moves.L3.value:
            cube.pivoterFace(Faces.LEFT, Sens.ANTIHORAIRE)
        case Moves.F1.value:
            cube.pivoterFace(Faces.FRONT, Sens.HORAIRE)
        case Moves.F2.value:
            cube.pivoterFace(Faces.FRONT, Sens.HORAIRE)
            cube.pivoterFace(Faces.FRONT, Sens.HORAIRE)
        case Moves.F3.value:
            cube.pivoterFace(Faces.FRONT, Sens.ANTIHORAIRE)
        case Moves.B1.value:
            cube.pivoterFace(Faces.BACK, Sens.HORAIRE)
        case Moves.B2.value:
            cube.pivoterFace(Faces.BACK, Sens.HORAIRE)
            cube.pivoterFace(Faces.BACK, Sens.HORAIRE)
        case Moves.B3.value:
            cube.pivoterFace(Faces.BACK, Sens.ANTIHORAIRE)

def CopyConfig(src: list):
    cpy = []
    for i in range(0, len(src)):
        cpy.append([])
        for j in range(0, len(src[i])):
            cpy[i].append([])
            for k in range(0, len(src[i][j])):
                cpy[i][j].append(src[i][j][k])
    return cpy

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

def GetCornerPermCoord(pieceList, ref):
    coord = 0
    perm = []

    for i in pieceList:
        j=0
        while not ComparePiece(i, ref[j]):
            j += 1
        perm.append(j)
    
    for i in range(1, len(perm)):
        k = 0
        for j in range(0, i):
            if perm[j] >= perm[i]:
                k += 1
        coord += k*math.factorial(i)

    return coord

def GetEdgePermCoord(pieceList, ref):
    coord = 0
    perm = []

    for i in pieceList:
        j=0
        while not ComparePiece(i, ref[j]) and j <=7 :
            j += 1
        if j<=7:
            perm.append(j)
    
    for i in range(1, len(perm)):
        k = 0
        for j in range(0, i):
            if perm[j] >= perm[i]:
                k += 1
        coord += k*math.factorial(i)

    return coord

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

def GetP2Coord(pieceList, refList):
    return GetCornerPermCoord(pieceList[0], refList[0]) + GetEdgePermCoord(pieceList[1], refList[1]) + GetUDSliceCoord(pieceList[1], refList[1])

def PhaseTwo(cube: cb.CubieCube):
    solve = False
    open = [(cube, -1, None, None)]
    close = []
    minimalIndex = 0
    mindist = 0

    corners = cube.GetCornerPermCoord()
    edges = cube.GetUDEdgeCoord()
    slicePerm = cube.GetUDSlicePerm()
    while not solve and len(open) > 0:
        corners = cube.GetCornerPermCoord()
        edges = cube.GetUDEdgeCoord()
        slicePerm = cube.GetUDSlicePerm()

        distList = []
        for i in open:
            distList.append(i[1])
        
        minimalIndex = distList.index(min(distList))
        if min(distList) == 0:
            solve = True
            close.append(open[minimalIndex])
        else:
            minConfig = open[minimalIndex]
            cube.configuration = CopyConfig(minConfig)
            mindist = minConfig[2]

            for m in Moves.MOVELIST.value:
                if m not in [Moves.R1.value, Moves.R3.value, Moves.L1.value, Moves.L3.value, Moves.F1.value, Moves.F3.value, Moves.B1.value, Moves.B3.value]:
                    newCorners = prT.corners_move[18*corners + m.value]
                    newUDEdges = prT.ud_edges_move[18*edges + m.value]

                    classId = prT.corner_classidx[newCorners]
                    symetrie = prT.corner_sym[newCorners]
                    newDistMod3 = prT.get_corners_ud_edges_depth3(40320*classId + prT.ud_edges_conj[(newUDEdges << 4) + symetrie])
                    newDist = prT.distance[3*mindist + newDistMod3]

                    open.append()
            
            close.append(open[minimalIndex])
            open.pop(minimalIndex)

    if solve:
        return GetResultAstar(close)
    else:
        print("ERROR")
        return 0

def GetResultAstar(tree: list):
    result = []
    currentIndex = len(tree)-1

    while tree[currentIndex][1] != -1:
        result.append(tree[currentIndex][2])
        currentIndex = tree[currentIndex][1]
    return list(reversed(result))

def PhaseOne():
    pass

def Solve(cube: RubiksCube):
    clone = RubiksCube()
    clone.configuration = CopyConfig(cube.configuration)
    sequence = PhaseTwo(clone)
    jouerFormule(sequence, cube)
