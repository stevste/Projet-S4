from Constantes import *
import copy


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
                        self.configuration[x][y].append(0)
                    elif x == self.taille +1:
                        self.configuration[x][y].append(1)
                    elif y == 0:
                        self.configuration[x][y].append(2)
                    elif y == self.taille +1:
                        self.configuration[x][y].append(3)
                    elif z == 0:
                        self.configuration[x][y].append(4)
                    elif z == self.taille +1:
                        self.configuration[x][y].append(5)
                    else:
                        self.configuration[x][y].append(STRUCTURE)
        
        # Pour l'affichage des rotations :
        self.mouvementEnCours = False
        self.axeRotationEnCours = None # AXE_X, AXE_Y ou AXE_Z
        self.abscisseFaceEnRotation:int = 0 # abscisse selon l'axe de rotation (peut être X, Y ou Z)
        self.angleRotationEnCours = 0 # en degrés
        self.configurationAnterieure = self.configuration
    
    def __repr__(self):
        texte = ''
        for z in range(self.taille +1, -1, -1):
            for y in range(self.taille +1, -1, -1):
                for x in range(0, self.taille +2):
                    if self.configuration[x][y][z] == STRUCTURE:
                        texte += '¤ '
                    elif self.configuration[x][y][z] is not None:
                        texte += str(self.configuration[x][y][z]) + ' '
                    else:
                        texte += '  '
                texte += '\n'
            texte += '\n'
        return texte + '----------'
    
    def pivoterPlan(self, axe:int=AXE_X, abscisseFace:int=0, sens=SENS_HORAIRE) -> None:
        self.abscisseFaceEnRotation = abscisseFace
        xAParcourir = range(self.taille +2)
        yAParcourir = range(self.taille +2)
        zAParcourir = range(self.taille +2)
        
        if axe == AXE_X:
            xAParcourir = [abscisseFace]
            self.axeRotationEnCours = AXE_X
        elif axe == AXE_Y:
            yAParcourir = [abscisseFace]
            sens *= -1 # car la base (y, x, z) est indirecte alors que (x, y, z) et (z, x, y) sont directes
            self.axeRotationEnCours = AXE_Y
        else: # axe == AXE_Z:
            zAParcourir = [abscisseFace]
            self.axeRotationEnCours = AXE_Z
        
        listeDesCouleurs = []
        for x in xAParcourir:
            for y in yAParcourir:
                for z in zAParcourir:
                    listeDesCouleurs.append(self.configuration[x][y][z])
        
        n = 0 # nombre de valeurs déjà insérées
        for x in xAParcourir:
            for y in yAParcourir:
                for z in zAParcourir:
                    if sens == SENS_ANTIHORAIRE:
                        indiceAInserer = (n%(self.taille+2))*(self.taille+2) + self.taille+1 - n//(self.taille+2)
                    else: # sens == SENS_HORAIRE:
                        indiceAInserer = (self.taille+1-n%(self.taille+2))*(self.taille+2) + n//(self.taille+2)
                    self.configuration[x][y][z] = listeDesCouleurs[indiceAInserer]
                    n += 1
    
    def pivoterFace(self, nomFace:int=FRONT, sens=SENS_HORAIRE, distanceAuBord:int=1) -> None:
        self.mouvementEnCours = True
        self.configurationAnterieure = copy.deepcopy(self.configuration)
        if distanceAuBord == 1:
            couronnesATourner = [0, 1] # on doit touner les "gomettes" sur la face et celles sur la tranche de la face
        elif distanceAuBord <= self.taille//2:
            couronnesATourner = [distanceAuBord] # on ne tourne que les "gomettes" sur la tranche
        else:
            self.mouvementEnCours = False
            print('Attention à bien respecter la notation : la distance au bord doit être comprise entre 1 et taille//2 inclus.')
        
        for couronne in couronnesATourner:
            if nomFace == FRONT:
                self.pivoterPlan(AXE_Y, couronne, -sens)
            elif nomFace == BACK:
                self.pivoterPlan(AXE_Y, self.taille+1 - couronne, sens)
            elif nomFace == LEFT:
                self.pivoterPlan(AXE_X, couronne, -sens)
            elif nomFace == RIGHT:
                self.pivoterPlan(AXE_X, self.taille+1 - couronne, sens)
            elif nomFace == DOWN:
                self.pivoterPlan(AXE_Z, couronne, -sens)
            else: # nomFace == UP:
                self.pivoterPlan(AXE_Z, self.taille+1 - couronne, sens)

            
'''
cube = RubiksCube(3)
print(cube)
cube.pivoterFace(UP, SENS_HORAIRE)
print(cube)
cube.pivoterFace(RIGHT, SENS_HORAIRE)
print(cube)'''