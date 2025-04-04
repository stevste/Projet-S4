from Enum import *
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
                self.pivoterPlan(Axes.Y, couronne, -sens.value)
            elif nomFace == Faces.BACK:
                self.pivoterPlan(Axes.Y, self.taille+1 - couronne, sens.value)
            elif nomFace == Faces.LEFT:
                self.pivoterPlan(Axes.X, couronne, -sens.value)
            elif nomFace == Faces.RIGHT:
                self.pivoterPlan(Axes.X, self.taille+1 - couronne, sens.value)
            elif nomFace == Faces.DOWN:
                self.pivoterPlan(Axes.Z, couronne, -sens.value)
            else: # nomFace == Faces.UP:
                self.pivoterPlan(Axes.Z, self.taille+1 - couronne, sens.value)
    
    def coinsEtAretes(self): # avec la face verte devant et la face orange en haut
        c = self.configuration
        coins = [(c[0][self.taille][1], c[1][self.taille][0], c[1][self.taille+1][1]), # URF
                 (c[0][self.taille][self.taille], c[1][self.taille+1][self.taille], c[1][self.taille][self.taille+1]), # UFL
                 (c[0][1][self.taille], c[1][1][self.taille+1], c[1][0][self.taille]), # ULB
                 (c[0][1][1], c[1][0][1], c[1][1][0]), # UBR
                 (c[self.taille+1][self.taille][1], c[self.taille][self.taille+1][1], c[self.taille][self.taille][0]), # DFR
                 (c[self.taille+1][self.taille][self.taille], c[self.taille][self.taille][self.taille+1], c[self.taille][self.taille+1][self.taille]), # DLF
                 (c[self.taille+1][1][self.taille], c[self.taille][0][self.taille], c[self.taille][1][self.taille+1]), # DBL
                 (c[self.taille+1][1][1], c[self.taille][1][0], c[self.taille][0][1])] # DRB
            
        aretes = [(c[1][self.taille+1][2], c[0][self.taille][2]), # FU
                  (c[2][self.taille+1][1], c[2][self.taille][0]), # FR
                  (c[self.taille][self.taille+1][2], c[self.taille+1][self.taille][2]), # FD
                  (c[2][self.taille+1][self.taille], c[2][self.taille][self.taille+1]), # FL
                  (c[1][0][2], c[0][1][2]), # BU
                  (c[2][0][1], c[2][1][0]), # BR
                  (c[self.taille][0][2], c[self.taille+1][1][2]), # BD
                  (c[2][0][self.taille], c[2][1][self.taille+1]), # BL
                  (c[1][2][self.taille+1], c[0][2][self.taille]), # LU
                  (c[self.taille][2][self.taille+1], c[self.taille+1][2][self.taille]), # LD
                  (c[1][2][0], c[0][2][1]), # RU
                  (c[self.taille][2][0], c[self.taille+1][2][1])] # RD
        
        return coins, aretes


def test_coinsEtAretes():
    cube = RubiksCube()
    cube.pivoterFace(Faces.DOWN)
    cube.pivoterFace(Faces.RIGHT)
    cube.pivoterFace(Faces.LEFT)
    cube.pivoterFace(Faces.UP)
    cube.pivoterFace(Faces.DOWN)
    cube.pivoterFace(Faces.RIGHT)

    coins, aretes = cube.coinsEtAretes()
    couleurs = ['bleu', 'vert', 'rouge', 'orange', 'blanc', 'jaune']
    
    testCoins = []
    for coin in coins:
        testCoins.append((couleurs[coin[0].value], couleurs[coin[1].value], couleurs[coin[2].value]))
    print(testCoins)
    
    testAretes = []
    for arete in aretes:
        testAretes.append((couleurs[arete[0].value], couleurs[arete[1].value]))
    print(testAretes)
    
#test_coinsEtAretes()

#cube = RubiksCube()
#cube.coinsEtAretes()
'''print(cube)
cube.pivoterFace(Faces.DOWN, Sens.HORAIRE)
print(cube)
cube.pivoterFace(Faces.RIGHT, Sens.HORAIRE)
print(cube)
'''