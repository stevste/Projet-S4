from Enum import *
import copy
import sys
sys.path.append("RubiksCube-TwophaseSolver/")
import cubie as cb
from enums import *
class RubiksCube:
    def __init__(self, taille:int=3):
        self.taille = taille # nombre de petits cubes sur une arête du Rubik's
        
        self.configuration = []
        for x in range(self.taille +2):
            self.configuration.append([])
            for y in range(self.taille +2):
                self.configuration[x].append([])
                for z in range(self.taille +2):
                    if (x in [0, self.taille +1] and (y in [0, self.taille +1] or z in [0, self.taille +1])) or (z in [0, self.taille +1] and y in [0, self.taille +1]):
                        self.configuration[x][y].append(None)
                    elif x == 0:
                        self.configuration[x][y].append(Faces.LEFT)
                    elif x == self.taille +1:
                        self.configuration[x][y].append(Faces.RIGHT)
                    elif y == 0:
                        self.configuration[x][y].append(Faces.FRONT)
                    elif y == self.taille +1:
                        self.configuration[x][y].append(Faces.BACK)
                    elif z == 0:
                        self.configuration[x][y].append(Faces.DOWN)
                    elif z == self.taille +1:
                        self.configuration[x][y].append(Faces.UP)
                    else:
                        self.configuration[x][y].append(STRUCTURE)
        
        # Pour l'affichage des rotations :
        self.mouvementEnCours = False
        self.axeRotationEnCours = None # Axes.X, Axes.Y ou Axes.Z
        self.sensRotationEnCours = 1
        self.abscisseFaceEnRotation:int = 0 # abscisse selon l'axe de rotation (peut être X, Y ou Z)
        self.angleRotationEnCours = 0 # en degrés
        self.configurationAnterieure = self.configuration
        self.listActions = [] # Actions sous la forme: (Faces, sens)
        
        # Pour la mise en rotation avec la souris :
        self.caseCliquee = [None, (None, None)] # [Face, (ligne, colonne)]
    
    def __repr__(self):
        texte = ''
        for z in range(self.taille +1, -1, -1):
            for y in range(self.taille +1, -1, -1):
                for x in range(0, self.taille +2):
                    if self.configuration[x][y][z] == STRUCTURE:
                        texte += '¤ '
                    elif self.configuration[x][y][z] is not None:
                        texte += str(self.configuration[x][y][z].value) + ' '
                    else:
                        texte += '  '
                texte += '\n'
            texte += '\n'
        return texte + '----------'
    
    def AjouterAction(self, action: tuple):
        self.listActions.append(action)

    def pivoterPlan(self, axe:int=Axes.X, abscisseFace:int=0, sens=Sens.HORAIRE.value) -> None:
        self.abscisseFaceEnRotation = abscisseFace
        xAParcourir = range(self.taille +2)
        yAParcourir = range(self.taille +2)
        zAParcourir = range(self.taille +2)
        
        if axe == Axes.X:
            xAParcourir = [abscisseFace]
            self.axeRotationEnCours = Axes.X
        elif axe == Axes.Y:
            yAParcourir = [abscisseFace]
            sens *= -1 # car la base (y, x, z) est indirecte alors que (x, y, z) et (z, x, y) sont directes
            self.axeRotationEnCours = Axes.Y
        else: # axe == Axes.Z:
            zAParcourir = [abscisseFace]
            self.axeRotationEnCours = Axes.Z
        
        listeDesCouleurs = []
        for x in xAParcourir:
            for y in yAParcourir:
                for z in zAParcourir:
                    listeDesCouleurs.append(self.configuration[x][y][z])
        
        n = 0 # nombre de valeurs déjà insérées
        for x in xAParcourir:
            for y in yAParcourir:
                for z in zAParcourir:
                    if sens == Sens.ANTIHORAIRE.value:
                        indiceAInserer = (n%(self.taille+2))*(self.taille+2) + self.taille+1 - n//(self.taille+2)
                    else: # sens == Sens.HORAIRE.value:
                        indiceAInserer = (self.taille+1-n%(self.taille+2))*(self.taille+2) + n//(self.taille+2)
                    self.configuration[x][y][z] = listeDesCouleurs[indiceAInserer]
                    n += 1

    def pivoterFace(self, nomFace:int=Faces.FRONT, sens=Sens.HORAIRE, distanceAuBord:int=1) -> None:
        self.mouvementEnCours = True
        self.configurationAnterieure = copy.deepcopy(self.configuration)

        if distanceAuBord == 1:
            couronnesATourner = [0, 1] # on doit touner les "gommettes" sur la face et celles sur la tranche de la face
        elif 2 <= distanceAuBord <= (self.taille+1)//2:
            couronnesATourner = [distanceAuBord] # on ne tourne que les "gommettes" sur la tranche
        else:
            couronnesATourner = []
            self.mouvementEnCours = False
            #print("Les couronnes centrales ne pivotent pas.")
            print('Attention à bien respecter la notation : la distance au bord doit être comprise entre 1 et taille//2 +1 inclus.')
        
        for couronne in couronnesATourner:
            if nomFace == Faces.FRONT:
                self.sensRotationEnCours = sens.value
                self.pivoterPlan(Axes.Y, couronne, -sens.value)
            elif nomFace == Faces.BACK:
                self.sensRotationEnCours = -sens.value
                self.pivoterPlan(Axes.Y, self.taille+1 - couronne, sens.value)
            elif nomFace == Faces.LEFT:
                self.sensRotationEnCours = -sens.value
                self.pivoterPlan(Axes.X, couronne, -sens.value)
            elif nomFace == Faces.RIGHT:
                self.sensRotationEnCours = sens.value
                self.pivoterPlan(Axes.X, self.taille+1 - couronne, sens.value)
            elif nomFace == Faces.DOWN:
                self.sensRotationEnCours = -sens.value
                self.pivoterPlan(Axes.Z, couronne, -sens.value)
            else: # nomFace == Faces.UP:
                self.sensRotationEnCours = sens.value
                self.pivoterPlan(Axes.Z, self.taille+1 - couronne, sens.value)
    
    def coinsEtAretes(self):
        c = self.configuration
        coins = [(c[self.taille][1][self.taille+1], c[self.taille+1][1][self.taille], c[self.taille][0][self.taille]), #URF
                (c[1][1][self.taille+1], c[1][0][self.taille], c[0][1][self.taille]), #UFL
                (c[1][self.taille][self.taille+1], c[0][self.taille][self.taille], c[1][self.taille+1][self.taille]), # ULB
                (c[self.taille][self.taille][self.taille+1], c[self.taille][self.taille+1][self.taille], c[self.taille+1][self.taille][self.taille]), # UBR
                (c[self.taille][1][0], c[self.taille][0][1], c[self.taille+1][1][1]), # DFR
                (c[1][1][0], c[0][1][1], c[1][0][1]), # DLF
                (c[1][self.taille][0], c[1][self.taille+1][1], c[0][self.taille][1]), # DBL
                (c[self.taille][self.taille][0], c[self.taille+1][self.taille][1], c[self.taille][self.taille+1][1])] # DRB
            
        aretes = [(c[self.taille][2][self.taille+1], c[self.taille+1][2][self.taille]), # UR
                    (c[2][1][self.taille+1], c[2][0][self.taille]), #UF
                    (c[1][2][self.taille+1], c[0][2][self.taille]), # UL
                    (c[2][self.taille][self.taille+1], c[2][self.taille+1][self.taille]), # UB
                    (c[self.taille][2][0], c[self.taille+1][2][1]), # DR
                    (c[2][1][0], c[2][0][1]), # DF
                    (c[1][2][0], c[0][2][1]), # DL
                    (c[2][self.taille][0], c[2][self.taille+1][1]), # DB
                    (c[self.taille][0][2], c[self.taille+1][1][2]), # FR
                    (c[1][0][2], c[0][1][2]), # FL
                    (c[1][self.taille+1][2], c[0][self.taille][2]), # BL
                    (c[self.taille][self.taille+1][2], c[self.taille+1][self.taille][2])] # BR
        
        return coins, aretes

    def GetCubie(self):
        """transforme le cube en cube interpretable pour le solver
        """
        def ComparePiece(p1, p2):
            for i in p2:
                if i not in p1:
                    return False
            return True
        
        result = cb.CubieCube()
        cubeRef = RubiksCube()
        cFacelet, eFacelet = self.coinsEtAretes()
        cRef, eRef = cubeRef.coinsEtAretes()

        for i in range(len(cFacelet)):
            for j in range(len(cRef)):
                if ComparePiece(cFacelet[i], cRef[j]):
                    result.cp[i] = Corner(j)
                    b = 0
                    for c in cFacelet[i]:
                        if c != cRef[j][0]:
                            b += 1
                        else:
                            break
                    result.co[i] = b
        
        for i in range(len(eFacelet)):
            for j in range(len(eRef)):
                if ComparePiece(eFacelet[i], eRef[j]):
                    result.ep[i] = Edge(j)
                    if eFacelet[i][0] != eRef[j][0]:
                        result.eo[i] = 1
                    else:
                        result.eo[i] = 0

        return result

    def jouerFormule(self, formule: list):
        for m in formule:
            match m:
                case Moves.U1.value:
                    self.AjouterAction((Faces.UP, Sens.HORAIRE))
                case Moves.U2.value:
                    self.AjouterAction((Faces.UP, Sens.HORAIRE))
                    self.AjouterAction((Faces.UP, Sens.HORAIRE))
                case Moves.U3.value:
                    self.AjouterAction((Faces.UP, Sens.ANTIHORAIRE))
                case Moves.D1.value:
                    self.AjouterAction((Faces.DOWN, Sens.HORAIRE))
                case Moves.D2.value:
                    self.AjouterAction((Faces.DOWN, Sens.HORAIRE))
                    self.AjouterAction((Faces.DOWN, Sens.HORAIRE))
                case Moves.D3.value:
                    self.AjouterAction((Faces.DOWN, Sens.ANTIHORAIRE))
                case Moves.R1.value:
                    self.AjouterAction((Faces.RIGHT, Sens.HORAIRE))
                case Moves.R2.value:
                    self.AjouterAction((Faces.RIGHT, Sens.HORAIRE))
                    self.AjouterAction((Faces.RIGHT, Sens.HORAIRE))
                case Moves.R3.value:
                    self.AjouterAction((Faces.RIGHT, Sens.ANTIHORAIRE))
                case Moves.L1.value:
                    self.AjouterAction((Faces.LEFT, Sens.HORAIRE))
                case Moves.L2.value:
                    self.AjouterAction((Faces.LEFT, Sens.HORAIRE))
                    self.AjouterAction((Faces.LEFT, Sens.HORAIRE))
                case Moves.L3.value:
                    self.AjouterAction((Faces.LEFT, Sens.ANTIHORAIRE))
                case Moves.F1.value:
                    self.AjouterAction((Faces.FRONT, Sens.HORAIRE))
                case Moves.F2.value:
                    self.AjouterAction((Faces.FRONT, Sens.HORAIRE))
                    self.AjouterAction((Faces.FRONT, Sens.HORAIRE))
                case Moves.F3.value:
                    self.AjouterAction((Faces.FRONT, Sens.ANTIHORAIRE))
                case Moves.B1.value:
                    self.AjouterAction((Faces.BACK, Sens.HORAIRE))
                case Moves.B2.value:
                    self.AjouterAction((Faces.BACK, Sens.HORAIRE))
                    self.AjouterAction((Faces.BACK, Sens.HORAIRE))
                case Moves.B3.value:
                    self.AjouterAction((Faces.BACK, Sens.ANTIHORAIRE))
   
#test_coinsEtAretes()

#cube = RubiksCube()
#self.coinsEtAretes()
'''print(cube)
self.pivoterFace(Faces.DOWN, Sens.HORAIRE)
print(cube)
self.pivoterFace(Faces.RIGHT, Sens.HORAIRE)
print(cube)
'''