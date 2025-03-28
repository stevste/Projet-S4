from Enum import *
from movesAndSymetrie import *
from RubiksCubeTailleN import RubiksCube
from Solver3D import ComparePiece

cubeRef = RubiksCube()
class CubieCube:
    def __init__(self, FaceletCube = None, cp = None, co = None, ep = None, eo = None):
        self.cornerPerm = []
        self.cornerOri = []
        self.edgePerm = []
        self.edgeOri = []

        if FaceletCube != None:
            cFacelet, eFacelet = FaceletCube.coinsEtAretes()
            cRef, eRef = cubeRef.coinsEtAretes()

            for i in cFacelet:
                for j in range(len(cRef)):
                    if ComparePiece(i, cRef[j]):
                        self.cornerPerm.append(Coins(j))
                        b = 0
                        for c in i:
                            if c != cRef[j][0]:
                                b += 1
                            else:
                                break
                        self.cornerOri.append(b)
            
            for i in eFacelet:
                for j in range(len(eRef)):
                    if ComparePiece(i, eRef[j]):
                        self.edgePerm.append(Aretes(j))
                        b = 0
                        for c in i:
                            if c != eRef[j][0]:
                                b += 1
                            else:
                                break
                        self.edgeOri.append(b)
        else:
            if cp == None:
                self.cornerPerm = [Coins(i) for i in range(8)]
            else:
                self.cornerPerm = cp[:]
            if co == None:
                self.cornerOri = [0]*8
            else:
                self.cornerOri = co[:]
            if ep == None:
                self.edgePerm = [Aretes(i) for i in range(12)]
            else:
                self.edgePerm = ep[:]
            if eo == None:
                self.edgeOri = [0]*12
            else:
                self.edgeOri = eo[:]

    def __str__(self):
        """Print string for a cubie cube."""
        s = ''
        for i in Coins:
            s = s + '(' + str(self.cornerPerm[i].value()) + ',' + str(self.cornerOri[i]) + ')'
        s += '\n'
        for i in Aretes:
            s = s + '(' + str(self.edgePerm[i].value()) + ',' + str(self.edgeOri[i]) + ')'
        return s
    
    def __eq__(self, other):
        """Define equality of two cubie cubes."""
        if self.cornerPerm == other.cornerPerm and self.cornerOri == other.cornerOri and self.edgePerm == other.edgePerm and self.edgeOri == other.edgeOri:
            return True
        return False
    
    def cornerComposition(self, b):
        rPerm = [0]*8
        rOri = [0]*8

        for i in range(8):
            rPerm[i] = self.cornerPerm[b.cornerPerm[i].value]
            newOri = 0
            ori_a = self.cornerOri[b.cornerPerm[i].value]
            ori_b = b.cornerOri[i]

            if ori_a < 3 and ori_b < 3:  # two regular cubes
                newOri = (ori_a + ori_b)%3

            elif ori_a < 3 <= ori_b:  # cube b is in a mirrored state
                newOri = ori_a + ori_b
                if newOri >= 6:
                    newOri -= 3  # the composition also is in a mirrored state

            elif ori_a >= 3 > ori_b:  # cube a is in a mirrored state
                newOri = ori_a - ori_b
                if newOri < 3:
                    newOri += 3  # the composition is a mirrored cube
            elif ori_a >= 3 and ori_b >= 3:  # if both cubes are in mirrored states
                newOri = ori_a - ori_b
                if newOri < 0:
                    newOri += 3  # the composition is a regular cube
            rOri[i] = newOri
        for i in range(8):
            self.cornerPerm[i] = rPerm[i]
            self.cornerOri[i] = rOri[i]

    def edgeComposition(self, b):
        rPerm = [0]*12
        rOri = [0]*12

        for i in range(12):
            rPerm[i] = self.edgePerm[b.edgePerm[i].value]
            rOri[i] = (b.edgeOri[i] + self.edgeOri[b.edgeOri[i]])%2
        for i in range(12):
            self.edgePerm[i] = rPerm[i]
            self.edgeOri[i] = rOri[i]

    def Composition(self, b):
        self.cornerComposition(b)
        self.edgeComposition(b)
        print()

    def Move(self, m: Moves):
        self.Composition(moveTable[m.value])

standardMove = [0]*6
standardMove[0] = CubieCube(None, cpU, coU, epU, eoU)
standardMove[1] = CubieCube(None, cpD, coD, epD, eoD)
standardMove[2] = CubieCube(None, cpR, coR, epR, eoR)
standardMove[3] = CubieCube(None, cpL, coL, epL, eoL)
standardMove[4] = CubieCube(None, cpF, coF, epF, eoF)
standardMove[5] = CubieCube(None, cpB, coB, epB, eoB)

moveTable = [0]*18

for i in range(6):
    mCube = CubieCube()
    for k in range(3):
        mCube.Composition(standardMove[i])
        moveTable[i*3+k] = CubieCube(None, mCube.cornerPerm, mCube.cornerOri, mCube.edgePerm, mCube.edgeOri)