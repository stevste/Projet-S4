from Enum import *
from movesAndSymetrie import *
from RubiksCubeTailleN import RubiksCube
from Solver3D import ComparePiece

N_PERM_COORD = 40320
N_CORNERS_CLASS = 2768

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
                        if i[0] != eRef[j][0]:
                            self.edgeOri.append(1)
                        else:
                            self.edgeOri.append(0)
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

    def InvCube(self):
        inv = CubieCube()
        for i in Aretes:
            inv.edgePerm[self.edgePerm[i.value].value] = i
        for i in Aretes:
            inv.edgeOri[i.value] = self.edgeOri[inv.edgePerm[i.value]]

        for i in Coins:
            inv.cornerPerm[self.cornerPerm[i.value].value] = i
        for i in Coins:
            ori = self.cornerOri[inv.cornerPerm[i]]
            if ori >= 3:
                inv.cornerOri[i] = -ori
            else:
                inv.cornerOri[i] = -ori
                if inv.cornerOri[i] < 0:
                    inv.cornerOri[i] += 3

    def Move(self, m: Moves):
        self.Composition(moveTable[m.value])

    def GetCornerPermCoord(self):
        perm = list(self.cornerPerm)
        c = 0
        for i in range(7, 0, -1):
            k=0
            while perm[i].value != i:
                temp = perm[0]
                for j in range(0, j):
                    perm[j] = j[+1]
                perm[j] = temp
                k += 1
            c = (j+1)*c+k
        return c

    def getCornerOriCoord(self):
        c = 0
        for i in range(8):
            c = 3*c + self.cornerOri[i]
        return c
    
    def GetUDEdgeCoord(self):
        perm = list(self.cornerPerm)
        c = 0
        for i in range(7, 0, -1):
            k=0
            while perm[i].value != i:
                temp = perm[0]
                for j in range(0, j):
                    perm[j] = j[+1]
                perm[j] = temp
                k += 1
            c = (j+1)*c+k
        return c

    def SetCorner(self, cpCoord):
        self.cornerPerm = [i for i in Coins]
        for j in range(8):
            k = cpCoord % (j + 1)
            cpCoord //= j + 1
            while k > 0:
                temp = self.cornerPerm[j]
                for i in range(j, 0, -1):
                    self.cornerPerm[j] = self.cornerPerm[j-1]
                self.cornerPerm[0] = temp
                k -= 1
    
    def SetUDEdges(self, epCoord):
        ref = list(Aretes)[0:8]
        for j in range(8):
            k = epCoord % (j + 1)
            epCoord //= j + 1
            while k > 0:
                temp = self.edgePerm[j]
                for i in range(j, 0, -1):
                    ref[j] = self.edgePerm[j-1]
                self.edgePerm[0] = temp
                k -= 1

        i = 0
        for j in range(12):
            if self.edgePerm[j] in ref:
                self.edgePerm[j] = ref[i]
                i += 1
    
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

standardSym = [0]*4
standardSym[0] = CubieCube(None, cpROT_URF3, coROT_URF3, epROT_URF3, eoROT_URF3)
standardSym[1] = CubieCube(None, cpROT_F2, coROT_F2, epROT_F2, eoROT_F2)
standardSym[2] = CubieCube(None, cpROT_U4, coROT_U4, epROT_U4, eoROT_U4)
standardSym[3] = CubieCube(None, cpMIRR_LR2, coMIRR_LR2, epMIRR_LR2, eoMIRR_LR2)

sCube = CubieCube()
sTable = [0]*48

for i in range(3):
    for j in range(2):
        for k in range(4):
            for l in range(2):
                sTable.append(None, sCube.cornerPerm, sCube.cornerOri, sCube.edgePerm, sCube.edgeOri)
                sCube.Composition(standardSym[0])
            sCube.Composition(standardSym[1])
        sCube.Composition(standardSym[2])
    sCube.Composition(standardSym[3])

invId = [0] * 48
for j in range(48):
    for i in range(48):
        cc = CubieCube(None, sTable[j].cornerPerm, sTable[j].cornerOri, sTable[j].edgePerm, sTable[j].edgeOri)
        cc.corner_multiply(sTable[i])
        if cc.cornerPerm[Coins.URF.value] == Coins.URF.value and cc.cornerPerm[Coins.UFL.value] == Coins.UFL.value and cc.cornerPerm[Coins.ULB.value] == Coins.ULB:
            invId[j] = i
            break

cornerClassId = [65535]*N_PERM_COORD  # idx -> classidx
cornerSymTable = [0] * N_PERM_COORD  # idx -> symmetry
cornerRep = [0] * N_CORNERS_CLASS  # classidx -> idx of representant

classidx = 0
cc = CubieCube()
for cp in range(N_PERM_COORD):
    cc.SetCorner(cp)
    if (cp + 1) % 8000 == 0:
        print('.', end='', flush=True)

    if cornerClassId[cp] == 65535:
        cornerClassId[cp] = classidx
        cornerSymTable[cp] = 0
        cornerRep[classidx] = cp
    else:
        continue
    for s in range(16):  # conjugate representant by all 16 symmetries
        ss = CubieCube(None, sTable[invId[s]].cornerPerm, sTable[invId[s]].cornerOri, sTable[invId[s]].edgePerm,
                            sTable[invId[s]].edgeOri)  # copy cube
        ss.cornerComposition(cc)
        ss.cornerComposition(sTable[s])  # s^-1*cc*s
        cpNew = ss.get_corners()
        if cornerClassId[cpNew] == 65535:
            cornerClassId[cpNew] = classidx
            cornerSymTable[cpNew] = s
    classidx += 1

classidx = 0

UDEdgeConj = [0] * (N_PERM_COORD * 16) #phase 2 edgeCoordsym
for t in range(16):
    cc = CubieCube()
    cc.SetUDEdges(t)
    for s in range(16):
        ss = CubieCube(None, sTable[s].cornerPerm, sTable[s].cornerOri, sTable[s].edgePerm, sTable[s].edgeOri)  # copy cube
        ss.edge_multiply(cc)  # s*t
        ss.edge_multiply(sTable[invId[s]])  # s*t*s^-1
        UDEdgeConj[16 * t + s] = ss.get_ud_edges()