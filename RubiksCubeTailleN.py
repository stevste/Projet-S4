from Enum import *


class RubiksCube:
    def __init__(self, taille:int=3):
        self.taille = taille
        
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
    
    def pivoterPlan(self, axe:int=Axes.X, abscisseFace:int=0, sens=Sens.HORAIRE) -> None:
        xAParcourir = range(self.taille +2)
        yAParcourir = range(self.taille +2)
        zAParcourir = range(self.taille +2)
        
        if axe == Axes.X:
            xAParcourir = [abscisseFace]
        elif axe == Axes.Y:
            yAParcourir = [abscisseFace]
            sens *= -1 # car la base (y, x, z) est indirecte alors que (x, y, z) et (z, x, y) sont directes
        else: # axe == AXE_Z:
            zAParcourir = [abscisseFace]
        
        listeDesCouleurs = []
        for x in xAParcourir:
            for y in yAParcourir:
                for z in zAParcourir:
                    listeDesCouleurs.append(self.configuration[x][y][z])
        
        n = 0 # nombre de valeurs déjà insérées
        for x in xAParcourir:
            for y in yAParcourir:
                for z in zAParcourir:
                    if sens == Sens.ANTIHORAIRE:
                        indiceAInserer = (n%(self.taille+2))*(self.taille+2) + self.taille+1 - n//(self.taille+2)
                    else: # sens == SENS_HORAIRE:
                        indiceAInserer = (self.taille+1-n%(self.taille+2))*(self.taille+2) + n//(self.taille+2)
                    self.configuration[x][y][z] = listeDesCouleurs[indiceAInserer]
                    n += 1
    
    def pivoterFace(self, nomFace:int=Faces.FRONT, sens=Sens.HORAIRE, distanceAuBord:int=1) -> None:
        if distanceAuBord == 1:
            couronnesATourner = [0, 1]
        elif distanceAuBord <= self.taille//2:
            couronnesATourner = [distanceAuBord]
        else:
            print('Attention à bien respecter la notation : la distance au bord doit être comprise entre 1 et taille//2 inclus.')
        
        for couronne in couronnesATourner:
            if nomFace == Faces.FRONT:
                self.pivoterPlan(Axes.Y, couronne, -sens)
            elif nomFace == Faces.BACK:
                self.pivoterPlan(Axes.Y, self.taille+1 - couronne, sens)
            elif nomFace == Faces.LEFT:
                self.pivoterPlan(Axes.X, couronne, -sens)
            elif nomFace == Faces.RIGHT:
                self.pivoterPlan(Axes.X, self.taille+1 - couronne, sens)
            elif nomFace == Faces.DOWN:
                self.pivoterPlan(Axes.Z, couronne, -sens)
            else: # nomFace == UP:
                self.pivoterPlan(Axes.Z, self.taille+1 - couronne, sens)

            
'''
cube = RubiksCube(3)
print(cube)
cube.pivoterFace(UP, SENS_HORAIRE)
print(cube)
cube.pivoterFace(RIGHT, SENS_HORAIRE)
print(cube)'''