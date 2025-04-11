import pygame
import sys
import math
import numpy as np

from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import sys
sys.path.append("RubiksCube-TwophaseSolver/")
import solver

from Enum import *



def dessinerCarre(point1:tuple, point2:tuple, point3:tuple, point4:tuple, couleur:tuple) -> None:
    glColor3f(couleur[0], couleur[1], couleur[2])
    glVertex3f(point1[0], point1[1], point1[2])
    glVertex3f(point2[0], point2[1], point2[2])
    glVertex3f(point3[0], point3[1], point3[2])
    glVertex3f(point4[0], point4[1], point4[2])


def dessinerCube(origine:tuple, baseLocale:tuple, couleur:tuple) -> None:
    dessinerCarre((origine[0], origine[1], origine[2]), (origine[0]+baseLocale[0][0], origine[1]+baseLocale[0][1], origine[2]+baseLocale[0][2]), (origine[0]+baseLocale[0][0]+baseLocale[1][0], origine[1]+baseLocale[0][1]+baseLocale[1][1], origine[2]+baseLocale[0][2]+baseLocale[1][2]), (origine[0]+baseLocale[1][0], origine[1]+baseLocale[1][1], origine[2]+baseLocale[1][2]), couleur) # Face avant
    dessinerCarre((origine[0]+baseLocale[2][0], origine[1]+baseLocale[2][1], origine[2]+baseLocale[2][2]), (origine[0]+baseLocale[0][0]+baseLocale[2][0], origine[1]+baseLocale[0][1]+baseLocale[2][1], origine[2]+baseLocale[0][2]+baseLocale[2][2]), (origine[0]+baseLocale[0][0]+baseLocale[1][0]+baseLocale[2][0], origine[1]+baseLocale[0][1]+baseLocale[1][1]+baseLocale[2][1], origine[2]+baseLocale[0][2]+baseLocale[1][2]+baseLocale[2][2]), (origine[0]+baseLocale[1][0]+baseLocale[2][0], origine[1]+baseLocale[1][1]+baseLocale[2][1], origine[2]+baseLocale[1][2]+baseLocale[2][2]), couleur) # Face arrière
    dessinerCarre((origine[0], origine[1], origine[2]), (origine[0]+baseLocale[1][0], origine[1]+baseLocale[1][1], origine[2]+baseLocale[1][2]), (origine[0]+baseLocale[1][0]+baseLocale[2][0], origine[1]+baseLocale[1][1]+baseLocale[2][1], origine[2]+baseLocale[1][2]+baseLocale[2][2]), (origine[0]+baseLocale[2][0], origine[1]+baseLocale[2][1], origine[2]+baseLocale[2][2]), couleur) # Face gauche
    dessinerCarre((origine[0]+baseLocale[0][0], origine[1]+baseLocale[0][1], origine[2]+baseLocale[0][2]), (origine[0]+baseLocale[0][0]+baseLocale[1][0], origine[1]+baseLocale[0][1]+baseLocale[1][1], origine[2]+baseLocale[0][2]+baseLocale[1][2]), (origine[0]+baseLocale[0][0]+baseLocale[1][0]+baseLocale[2][0], origine[1]+baseLocale[0][1]+baseLocale[1][1]+baseLocale[2][1], origine[2]+baseLocale[0][2]+baseLocale[1][2]+baseLocale[2][2]), (origine[0]+baseLocale[0][0]+baseLocale[2][0], origine[1]+baseLocale[0][1]+baseLocale[2][1], origine[2]+baseLocale[0][2]+baseLocale[2][2]), couleur) # Face droite
    dessinerCarre((origine[0]+baseLocale[1][0], origine[1]+baseLocale[1][1], origine[2]+baseLocale[1][2]), (origine[0]+baseLocale[0][0]+baseLocale[1][0], origine[1]+baseLocale[0][1]+baseLocale[1][1], origine[2]+baseLocale[0][2]+baseLocale[1][2]), (origine[0]+baseLocale[0][0]+baseLocale[1][0]+baseLocale[2][0], origine[1]+baseLocale[0][1]+baseLocale[1][1]+baseLocale[2][1], origine[2]+baseLocale[0][2]+baseLocale[1][2]+baseLocale[2][2]), (origine[0]+baseLocale[1][0]+baseLocale[2][0], origine[1]+baseLocale[1][1]+baseLocale[2][1], origine[2]+baseLocale[1][2]+baseLocale[2][2]), couleur) # Face supérieure
    dessinerCarre((origine[0], origine[1], origine[2]), (origine[0]+baseLocale[0][0], origine[1]+baseLocale[0][1], origine[2]+baseLocale[0][2]), (origine[0]+baseLocale[0][0]+baseLocale[2][0], origine[1]+baseLocale[0][1]+baseLocale[2][1], origine[2]+baseLocale[0][2]+baseLocale[2][2]), (origine[0]+baseLocale[2][0], origine[1]+baseLocale[2][1], origine[2]+baseLocale[2][2]), couleur) # Face inférieure


def dessinerRubiksCube(rubiksCube) -> None:
    glBegin(GL_QUADS)
    origine = (-(rubiksCube.taille+2)/2, -(rubiksCube.taille+2)/2, -(rubiksCube.taille+2)/2)
    
    if rubiksCube.axeRotationEnCours == Axes.X:
        xLocal = (1, 0, 0)
        yLocal = (0, math.cos(rubiksCube.angleRotationEnCours*math.pi/180), math.sin(rubiksCube.angleRotationEnCours*math.pi/180))
        zLocal = (0, math.cos(math.pi/2 + rubiksCube.angleRotationEnCours*math.pi/180), math.sin(math.pi/2 + rubiksCube.angleRotationEnCours*math.pi/180))
    elif rubiksCube.axeRotationEnCours == Axes.Y:
        xLocal = (math.cos(rubiksCube.angleRotationEnCours*math.pi/180), 0, math.sin(rubiksCube.angleRotationEnCours*math.pi/180))
        yLocal = (0, 1, 0)
        zLocal = (math.cos(math.pi/2 + rubiksCube.angleRotationEnCours*math.pi/180), 0, math.sin(math.pi/2 + rubiksCube.angleRotationEnCours*math.pi/180))
    else: # rubiksCube.axeRotationEnCours == Axes.Z:
        xLocal = (math.cos(rubiksCube.angleRotationEnCours*math.pi/180), math.sin(rubiksCube.angleRotationEnCours*math.pi/180), 0)
        yLocal = (math.cos(math.pi/2 + rubiksCube.angleRotationEnCours*math.pi/180), math.sin(math.pi/2 + rubiksCube.angleRotationEnCours*math.pi/180), 0)
        zLocal = (0, 0, 1)
    
    for x in range(1, rubiksCube.taille +1):
        for y in range(1, rubiksCube.taille +1):
            for z in range(1, rubiksCube.taille +1):
                if rubiksCube.mouvementEnCours and (x, y, z)[rubiksCube.axeRotationEnCours.value] == rubiksCube.abscisseFaceEnRotation:
                    uX = xLocal
                    uY = yLocal
                    uZ = zLocal
                    coordonneesCentrees = (x - (rubiksCube.taille+2)/2, y - (rubiksCube.taille+2)/2, z - (rubiksCube.taille+2)/2) # exemple pour un 3x3 : la "gommette" au centre de la face blanche devient (0, 0, 2) au lieu d'être (2, 2, 4)
                    origineCube = (coordonneesCentrees[0]*uX[0] + coordonneesCentrees[1]*uY[0] + coordonneesCentrees[2]*uZ[0], coordonneesCentrees[0]*uX[1] + coordonneesCentrees[1]*uY[1] + coordonneesCentrees[2]*uZ[1], coordonneesCentrees[0]*uX[2] + coordonneesCentrees[1]*uY[2] + coordonneesCentrees[2]*uZ[2])
                else:
                    uX = (1,0,0)
                    uY = (0,1,0)
                    uZ = (0,0,1)
                    origineCube = (origine[0]+x, origine[1]+y, origine[2]+z)
                
                couleur = (0.1, 0.1, 0.1) # Noir
                dessinerCube(origineCube, (uX, uY, uZ), couleur)
        
                # On colle les "gommettes" sur les faces du petit cube qu'on vient de dessiner :
                if rubiksCube.configurationAnterieure[x+1][y][z] != STRUCTURE:
                    couleur = Couleur.LIST.value[rubiksCube.configurationAnterieure[x+1][y][z].value]
                    dessinerCarre((origineCube[0]+1.001*uX[0]+0.05*uY[0]+0.05*uZ[0], origineCube[1]+1.001*uX[1]+0.05*uY[1]+0.05*uZ[1], origineCube[2]+1.001*uX[2]+0.05*uY[2]+0.05*uZ[2]), (origineCube[0]+1.001*uX[0]+0.95*uY[0]+0.05*uZ[0], origineCube[1]+1.001*uX[1]+0.95*uY[1]+0.05*uZ[1], origineCube[2]+1.001*uX[2]+0.95*uY[2]+0.05*uZ[2]), (origineCube[0]+1.001*uX[0]+0.95*uY[0]+0.95*uZ[0], origineCube[1]+1.001*uX[1]+0.95*uY[1]+0.95*uZ[1], origineCube[2]+1.001*uX[2]+0.95*uY[2]+0.95*uZ[2]), (origineCube[0]+1.001*uX[0]+0.05*uY[0]+0.95*uZ[0], origineCube[1]+1.001*uX[1]+0.05*uY[1]+0.95*uZ[1], origineCube[2]+1.001*uX[2]+0.05*uY[2]+0.95*uZ[2]), couleur)                
                elif rubiksCube.configurationAnterieure[x-1][y][z] != STRUCTURE:
                    couleur = Couleur.LIST.value[rubiksCube.configurationAnterieure[x-1][y][z].value]
                    dessinerCarre((origineCube[0]-0.001*uX[0]+0.05*uY[0]+0.05*uZ[0], origineCube[1]-0.001*uX[1]+0.05*uY[1]+0.05*uZ[1], origineCube[2]-0.001*uX[2]+0.05*uY[2]+0.05*uZ[2]), (origineCube[0]-0.001*uX[0]+0.95*uY[0]+0.05*uZ[0], origineCube[1]-0.001*uX[1]+0.95*uY[1]+0.05*uZ[1], origineCube[2]-0.001*uX[2]+0.95*uY[2]+0.05*uZ[2]), (origineCube[0]-0.001*uX[0]+0.95*uY[0]+0.95*uZ[0], origineCube[1]-0.001*uX[1]+0.95*uY[1]+0.95*uZ[1], origineCube[2]-0.001*uX[2]+0.95*uY[2]+0.95*uZ[2]), (origineCube[0]-0.001*uX[0]+0.05*uY[0]+0.95*uZ[0], origineCube[1]-0.001*uX[1]+0.05*uY[1]+0.95*uZ[1], origineCube[2]-0.001*uX[2]+0.05*uY[2]+0.95*uZ[2]), couleur)
                if rubiksCube.configurationAnterieure[x][y+1][z] != STRUCTURE:
                    couleur = Couleur.LIST.value[rubiksCube.configurationAnterieure[x][y+1][z].value]
                    dessinerCarre((origineCube[0]+0.05*uX[0]+1.001*uY[0]+0.05*uZ[0], origineCube[1]+0.05*uX[1]+1.001*uY[1]+0.05*uZ[1], origineCube[2]+0.05*uX[2]+1.001*uY[2]+0.05*uZ[2]), (origineCube[0]+0.95*uX[0]+1.001*uY[0]+0.05*uZ[0], origineCube[1]+0.95*uX[1]+1.001*uY[1]+0.05*uZ[1], origineCube[2]+0.95*uX[2]+1.001*uY[2]+0.05*uZ[2]), (origineCube[0]+0.95*uX[0]+1.001*uY[0]+0.95*uZ[0], origineCube[1]+0.95*uX[1]+1.001*uY[1]+0.95*uZ[1], origineCube[2]+0.95*uX[2]+1.001*uY[2]+0.95*uZ[2]), (origineCube[0]+0.05*uX[0]+1.001*uY[0]+0.95*uZ[0], origineCube[1]+0.05*uX[1]+1.001*uY[1]+0.95*uZ[1], origineCube[2]+0.05*uX[2]+1.001*uY[2]+0.95*uZ[2]), couleur)
                elif rubiksCube.configurationAnterieure[x][y-1][z] != STRUCTURE:
                    couleur = Couleur.LIST.value[rubiksCube.configurationAnterieure[x][y-1][z].value]
                    dessinerCarre((origineCube[0]+0.05*uX[0]-0.001*uY[0]+0.05*uZ[0], origineCube[1]+0.05*uX[1]-0.001*uY[1]+0.05*uZ[1], origineCube[2]+0.05*uX[2]-0.001*uY[2]+0.05*uZ[2]), (origineCube[0]+0.95*uX[0]-0.001*uY[0]+0.05*uZ[0], origineCube[1]+0.95*uX[1]-0.001*uY[1]+0.05*uZ[1], origineCube[2]+0.95*uX[2]-0.001*uY[2]+0.05*uZ[2]), (origineCube[0]+0.95*uX[0]-0.001*uY[0]+0.95*uZ[0], origineCube[1]+0.95*uX[1]-0.001*uY[1]+0.95*uZ[1], origineCube[2]+0.95*uX[2]-0.001*uY[2]+0.95*uZ[2]), (origineCube[0]+0.05*uX[0]-0.001*uY[0]+0.95*uZ[0], origineCube[1]+0.05*uX[1]-0.001*uY[1]+0.95*uZ[1], origineCube[2]+0.05*uX[2]-0.001*uY[2]+0.95*uZ[2]), couleur)
                if rubiksCube.configurationAnterieure[x][y][z+1] != STRUCTURE:
                    couleur = Couleur.LIST.value[rubiksCube.configurationAnterieure[x][y][z+1].value]
                    dessinerCarre((origineCube[0]+0.05*uX[0]+0.05*uY[0]+1.001*uZ[0], origineCube[1]+0.05*uX[1]+0.05*uY[1]+1.001*uZ[1], origineCube[2]+0.05*uX[2]+0.05*uY[2]+1.001*uZ[2]), (origineCube[0]+0.95*uX[0]+0.05*uY[0]+1.001*uZ[0], origineCube[1]+0.95*uX[1]+0.05*uY[1]+1.001*uZ[1], origineCube[2]+0.95*uX[2]+0.05*uY[2]+1.001*uZ[2]), (origineCube[0]+0.95*uX[0]+0.95*uY[0]+1.001*uZ[0], origineCube[1]+0.95*uX[1]+0.95*uY[1]+1.001*uZ[1], origineCube[2]+0.95*uX[2]+0.95*uY[2]+1.001*uZ[2]), (origineCube[0]+0.05*uX[0]+0.95*uY[0]+1.001*uZ[0], origineCube[1]+0.05*uX[1]+0.95*uY[1]+1.001*uZ[1], origineCube[2]+0.05*uX[2]+0.95*uY[2]+1.001*uZ[2]), couleur)
                elif rubiksCube.configurationAnterieure[x][y][z-1] != STRUCTURE:
                    couleur = Couleur.LIST.value[rubiksCube.configurationAnterieure[x][y][z-1].value]
                    dessinerCarre((origineCube[0]+0.05*uX[0]+0.05*uY[0]-0.001*uZ[0], origineCube[1]+0.05*uX[1]+0.05*uY[1]-0.001*uZ[1], origineCube[2]+0.05*uX[2]+0.05*uY[2]-0.001*uZ[2]), (origineCube[0]+0.95*uX[0]+0.05*uY[0]-0.001*uZ[0], origineCube[1]+0.95*uX[1]+0.05*uY[1]-0.001*uZ[1], origineCube[2]+0.95*uX[2]+0.05*uY[2]-0.001*uZ[2]), (origineCube[0]+0.95*uX[0]+0.95*uY[0]-0.001*uZ[0], origineCube[1]+0.95*uX[1]+0.95*uY[1]-0.001*uZ[1], origineCube[2]+0.95*uX[2]+0.95*uY[2]-0.001*uZ[2]), (origineCube[0]+0.05*uX[0]+0.95*uY[0]-0.001*uZ[0], origineCube[1]+0.05*uX[1]+0.95*uY[1]-0.001*uZ[1], origineCube[2]+0.05*uX[2]+0.95*uY[2]-0.001*uZ[2]), couleur)
    glEnd()
    

def tournerCube(angle:float, baseCamera:list, axe=Axes.X) -> list:
    nouvelleBaseCamera = [(), (), ()]
    glRotatef(-angle, baseCamera[axe.value][0], baseCamera[axe.value][1], baseCamera[axe.value][2])
    
    angle = angle*math.pi/180
    cosinus = math.cos(angle) # cos(angle + pi/2) = -sin(angle)
    sinus = math.sin(angle) # sin(angle + pi/2) = cos(angle)
    
    if axe == Axes.X:
        nouvelleBaseCamera[1] = (cosinus*baseCamera[1][0] + sinus*baseCamera[2][0], cosinus*baseCamera[1][1] + sinus*baseCamera[2][1], cosinus*baseCamera[1][2] + sinus*baseCamera[2][2])
        nouvelleBaseCamera[2] = (-sinus*baseCamera[1][0] + cosinus*baseCamera[2][0], -sinus*baseCamera[1][1] + cosinus*baseCamera[2][1], -sinus*baseCamera[1][2] + cosinus*baseCamera[2][2])
        nouvelleBaseCamera[0] = baseCamera[0]
    elif axe == Axes.Y:
        nouvelleBaseCamera[2] = (cosinus*baseCamera[2][0] + sinus*baseCamera[0][0], cosinus*baseCamera[2][1] + sinus*baseCamera[0][1], cosinus*baseCamera[2][2] + sinus*baseCamera[0][2])
        nouvelleBaseCamera[0] = (-sinus*baseCamera[2][0] + cosinus*baseCamera[0][0], -sinus*baseCamera[2][1] + cosinus*baseCamera[0][1], -sinus*baseCamera[2][2] + cosinus*baseCamera[0][2])
        nouvelleBaseCamera[1] = baseCamera[1]
    else: # axe == Axes.Z:
        nouvelleBaseCamera[0] = (cosinus*baseCamera[0][0] + sinus*baseCamera[1][0], cosinus*baseCamera[0][1] + sinus*baseCamera[1][1], cosinus*baseCamera[0][2] + sinus*baseCamera[1][2])
        nouvelleBaseCamera[1] = (-sinus*baseCamera[0][0] + cosinus*baseCamera[1][0], -sinus*baseCamera[0][1] + cosinus*baseCamera[1][1], -sinus*baseCamera[0][2] + cosinus*baseCamera[1][2])
        nouvelleBaseCamera[2] = baseCamera[2]

    return nouvelleBaseCamera


def determinerPositionFacesCamera(baseCamera:list) -> list: # pour savoir quelles sont les faces devant, à gauche, à droite... depuis le point de vue de l'utilisateur
    orientationFaces = ((0,-1,0), (0,1,0), (1,0,0), (-1,0,0), (0,0,1), (0,0,-1)) # vecteurs normaux aux faces FRONT, BACK, RIGHT, LEFT, UP, DOWN du cube
    directionsBaseCamera = ((0,-1,0), (0,1,0), (1,0,0), (-1,0,0), (0,0,1), (0,0,-1)) # directions FRONT, BACK, RIGHT, LEFT, UP, DOWN  dans la base de la caméra
    facesVuesParCamera = [None, None, None, None, None, None] # sera rempli avec la face la plus proche de la position FRONT, BACK, RIGHT, LEFT, UP, DOWN pour l'observateur

    for direction in [Faces.FRONT, Faces.BACK, Faces.RIGHT, Faces.LEFT, Faces.UP, Faces.DOWN]:
        produitScalaireMaxi = 0
        for face in [Faces.FRONT, Faces.BACK, Faces.RIGHT, Faces.LEFT, Faces.UP, Faces.DOWN]:
            produitScalaire = round((directionsBaseCamera[direction.value][0]*baseCamera[0][0]+directionsBaseCamera[direction.value][1]*baseCamera[1][0]+directionsBaseCamera[direction.value][2]*baseCamera[2][0])*orientationFaces[face.value][0] + (directionsBaseCamera[direction.value][0]*baseCamera[0][1]+directionsBaseCamera[direction.value][1]*baseCamera[1][1]+directionsBaseCamera[direction.value][2]*baseCamera[2][1])*orientationFaces[face.value][1] + (directionsBaseCamera[direction.value][0]*baseCamera[0][2]+directionsBaseCamera[direction.value][1]*baseCamera[1][2]+directionsBaseCamera[direction.value][2]*baseCamera[2][2])*orientationFaces[face.value][2], 2)
            if produitScalaire >= produitScalaireMaxi and (face not in facesVuesParCamera): # le deuxième test sert en cas d'égalité de deux produits scalaires, pour ne pas avoir deux fois la même face dans la liste facesVuesParCamera
                produitScalaireMaxi = produitScalaire
                facesVuesParCamera[direction.value] = face
            
    return facesVuesParCamera

'''# Fonction pour faire des tests (même que celle au-dessus mais avec des print):
def determinerPositionFacesCameraPrint(baseCamera:list) -> list: # pour savoir quelles sont les faces devant, à gauche, à droite... depuis le point de vue de l'utilisateur
    orientationFaces = ((0,-1,0), (0,1,0), (1,0,0), (-1,0,0), (0,0,1), (0,0,-1)) # FRONT, BACK, RIGHT, LEFT, UP, DOWN
    directionsBaseCamera = ((0,-1,0), (0,1,0), (1,0,0), (-1,0,0), (0,0,1), (0,0,-1))
    facesVuesParCamera = [None, None, None, None, None, None] # sera rempli avec la face la plus proche de la position FRONT, BACK, RIGHT, LEFT, UP, DOWN pour l'observateur
    print()
    for direction in [Faces.FRONT, Faces.BACK, Faces.RIGHT, Faces.LEFT, Faces.UP, Faces.DOWN]:
        produitScalaireMaxi = 0
        print('------')
        for face in [Faces.FRONT, Faces.BACK, Faces.RIGHT, Faces.LEFT, Faces.UP, Faces.DOWN]:
            produitScalaire = round((directionsBaseCamera[direction.value][0]*baseCamera[0][0]+directionsBaseCamera[direction.value][1]*baseCamera[1][0]+directionsBaseCamera[direction.value][2]*baseCamera[2][0])*orientationFaces[face.value][0] + (directionsBaseCamera[direction.value][0]*baseCamera[0][1]+directionsBaseCamera[direction.value][1]*baseCamera[1][1]+directionsBaseCamera[direction.value][2]*baseCamera[2][1])*orientationFaces[face.value][1] + (directionsBaseCamera[direction.value][0]*baseCamera[0][2]+directionsBaseCamera[direction.value][1]*baseCamera[1][2]+directionsBaseCamera[direction.value][2]*baseCamera[2][2])*orientationFaces[face.value][2], 2)
            print(face, produitScalaire)
            if produitScalaire >= produitScalaireMaxi and (face not in facesVuesParCamera): # le deuxième test sert en cas d'égalité de deux produits scalaires, pour ne pas avoir deux fois la même face dans la liste facesVuesParCamera
                produitScalaireMaxi = produitScalaire
                facesVuesParCamera[direction.value] = face
            
    return facesVuesParCamera

# Fonction de vérification :
def verifierCoherence(facesVuesParCamera:list) -> bool:
    if abs(facesVuesParCamera[0].value-facesVuesParCamera[1].value) == 1 and abs(facesVuesParCamera[2].value-facesVuesParCamera[3].value) == 1 and abs(facesVuesParCamera[4].value-facesVuesParCamera[5].value) == 1:
        for indiceFace1 in range(len(facesVuesParCamera)):
            for face2 in facesVuesParCamera[0:indiceFace1] + facesVuesParCamera[indiceFace1 +1:]:
                if facesVuesParCamera[indiceFace1] == face2:
                    return False
        return True
    else:
        return False'''


def determinerEquationDroite(point1:tuple, point2:tuple) -> tuple: # équation "ax + by + c = 0" de la droite passant par les deux points donnés, renvoie a, b et c en pixels
    vecteurDirecteur = (point1[0] - point2[0], point1[1] - point2[1]) # (xb - xa, yb - ya)
    a = vecteurDirecteur[1]
    b = -vecteurDirecteur[0]
    c = -vecteurDirecteur[1]*point1[0] + vecteurDirecteur[0]*point1[1]
    return (a, b, c)


def estAuDessus(positionSouris:tuple, equationDroite:tuple) -> bool:
    if equationDroite[0]*positionSouris[0] + equationDroite[1]*positionSouris[1] + equationDroite[2] >= 0:
        return True
    return False


def estADroite(positionSouris:tuple, equationDroite:tuple) -> bool:
    if equationDroite[0]*positionSouris[0] + equationDroite[1]*positionSouris[1] + equationDroite[2] <= 0:
        return True
    return False


def visible(face:Faces, baseCamera:list) -> bool:
    orientationFaces = ((0,-1,0), (0,1,0), (1,0,0), (-1,0,0), (0,0,1), (0,0,-1)) # FRONT, BACK, RIGHT, LEFT, UP, DOWN
    produitScalaire = round(-baseCamera[1][0]*orientationFaces[face.value][0] - baseCamera[1][1]*orientationFaces[face.value][1] - baseCamera[1][2]*orientationFaces[face.value][2], 2)
    if produitScalaire >= 0:
        return True
    else:
        return False
    

def rotationFace(positionSouris:list, baseCamera:list, positionFacesVuesParCamera:list, rubiksCube) -> None:    
    # Faces composant les coins (URF, UFL, ULB, UBR, DFR, DLF, DBL, DRB):
    coins = ((Faces.UP, Faces.RIGHT, Faces.FRONT), (Faces.UP, Faces.FRONT, Faces.LEFT), (Faces.UP, Faces.LEFT, Faces.BACK), (Faces.UP, Faces.BACK, Faces.RIGHT), (Faces.DOWN, Faces.FRONT, Faces.RIGHT), (Faces.DOWN, Faces.LEFT, Faces.FRONT), (Faces.DOWN, Faces.BACK, Faces.LEFT), (Faces.DOWN, Faces.RIGHT, Faces.BACK))
    
    # Toujours donnés dans l'ordre basGauche, basDroite, hautGauche, hautDroite pour la face considérée (pas besoin de la face BACK car elle n'est jamais visible):
    coinsFaceFRONT = (Coins.DLF, Coins.DFR, Coins.UFL, Coins.URF)
    coinsFaceRIGHT = (Coins.DFR, Coins.DRB, Coins.URF, Coins.UBR)
    coinsFaceLEFT = (Coins.DBL, Coins.DLF, Coins.ULB, Coins.UFL)
    coinsFaceUP = (Coins.UFL, Coins.URF, Coins.ULB, Coins.UBR)
    coinsFaceDOWN = (Coins.DBL, Coins.DRB, Coins.DLF, Coins.DFR)
    
    listeCoinsParFace = [coinsFaceFRONT, [], coinsFaceRIGHT, coinsFaceLEFT, coinsFaceUP, coinsFaceDOWN]

    listeDesListesDeCoins = []
    listeFaces = [Faces.FRONT, Faces.BACK, Faces.RIGHT, Faces.LEFT, Faces.UP, Faces.DOWN]
    
    for face in listeFaces:
        listeCoinsFace = []    
        if visible(positionFacesVuesParCamera[face.value], baseCamera):
            for coin in listeCoinsParFace[face.value]:
                coordonneesEtIntersections = [[0,0,0], []] # [position, intersection de 3 faces]
                for faceEnIntersection in coins[coin.value]:
                    coordonneesEtIntersections[1].append(positionFacesVuesParCamera[faceEnIntersection.value])
                listeCoinsFace.append(coordonneesEtIntersections)
        listeDesListesDeCoins.append(listeCoinsFace)

    for indexFaceVisible in range(len(listeDesListesDeCoins)):
        listeCoinsDUneFaceVisible = listeDesListesDeCoins[indexFaceVisible]
        for coinEtIntersections in listeCoinsDUneFaceVisible: # pour chacun des 4 coins de la face étudiée
            for face in coinEtIntersections[1]: # pour chacune des 3 faces qui se rejoignent au coin étudié
                coinEtIntersections[0][Faces.AXES_ROTATION.value[face.value].value] = Faces.SIGNES_ABSCISSES.value[face.value]*rubiksCube.taille/2
        
        if len(listeCoinsDUneFaceVisible) > 0 and ((rubiksCube.caseCliquee[0] != None and indexFaceVisible == rubiksCube.caseCliquee[0].value) or rubiksCube.caseCliquee[0] == None):
            vecteurChangementDeLigne = ((listeCoinsDUneFaceVisible[2][0][0]-listeCoinsDUneFaceVisible[0][0][0])/rubiksCube.taille, (listeCoinsDUneFaceVisible[2][0][1]-listeCoinsDUneFaceVisible[0][0][1])/rubiksCube.taille, (listeCoinsDUneFaceVisible[2][0][2]-listeCoinsDUneFaceVisible[0][0][2])/rubiksCube.taille) # déplacement nécessaire pour augmenter d'une ligne sur la face dans la base du cube
            vecteurChangementDeColonne = ((listeCoinsDUneFaceVisible[1][0][0]-listeCoinsDUneFaceVisible[0][0][0])/rubiksCube.taille, (listeCoinsDUneFaceVisible[1][0][1]-listeCoinsDUneFaceVisible[0][0][1])/rubiksCube.taille, (listeCoinsDUneFaceVisible[1][0][2]-listeCoinsDUneFaceVisible[0][0][2])/rubiksCube.taille) # déplacement nécessaire pour augmenter d'une colonne sur la face dans la base du cube
            
            intersections = [[], []]
            for coinEtIntersections in listeCoinsDUneFaceVisible:
                for ligne in range(rubiksCube.taille +1): # sur les segments gauche et droit de la face
                    pointAGauche = gluProject(listeCoinsDUneFaceVisible[0][0][0]+vecteurChangementDeLigne[0]*ligne, listeCoinsDUneFaceVisible[0][0][1]+vecteurChangementDeLigne[1]*ligne, listeCoinsDUneFaceVisible[0][0][2]+vecteurChangementDeLigne[2]*ligne)
                    pointADroite = gluProject(listeCoinsDUneFaceVisible[1][0][0]+vecteurChangementDeLigne[0]*ligne, listeCoinsDUneFaceVisible[1][0][1]+vecteurChangementDeLigne[1]*ligne, listeCoinsDUneFaceVisible[1][0][2]+vecteurChangementDeLigne[2]*ligne)
                    intersections[0].append(((int(pointAGauche[0]), int(pointAGauche[1])), (int(pointADroite[0]), int(pointADroite[1]))))
                
                for colonne in range(rubiksCube.taille +1): # sur les segments bas et haut de la face
                    pointEnBas = gluProject(listeCoinsDUneFaceVisible[0][0][0]+vecteurChangementDeColonne[0]*colonne, listeCoinsDUneFaceVisible[0][0][1]+vecteurChangementDeColonne[1]*colonne, listeCoinsDUneFaceVisible[0][0][2]+vecteurChangementDeColonne[2]*colonne)
                    pointEnHaut = gluProject(listeCoinsDUneFaceVisible[2][0][0]+vecteurChangementDeColonne[0]*colonne, listeCoinsDUneFaceVisible[2][0][1]+vecteurChangementDeColonne[1]*colonne, listeCoinsDUneFaceVisible[2][0][2]+vecteurChangementDeColonne[2]*colonne)
                    intersections[1].append(((int(pointEnBas[0]), int(pointEnBas[1])), (int(pointEnHaut[0]), int(pointEnHaut[1]))))
            
            ligne = 0
            while ligne <= rubiksCube.taille and estAuDessus(positionSouris, determinerEquationDroite(intersections[0][ligne][0], intersections[0][ligne][1])):
                ligne += 1
            
            colonne = 0
            while colonne <= rubiksCube.taille and estADroite(positionSouris, determinerEquationDroite(intersections[1][colonne][0], intersections[1][colonne][1])):
                colonne += 1
            
            if rubiksCube.caseCliquee[1] == (None, None):
                if 1 <= ligne <= rubiksCube.taille and 1 <= colonne <= rubiksCube.taille:
                    rubiksCube.caseCliquee = [listeFaces[indexFaceVisible], (ligne, colonne)]
            else:
                if 1 <= ligne <= rubiksCube.taille or 1 <= colonne <= rubiksCube.taille: # on peut potentiellement être en dehors du cube tant qu'on est au moins sur une ligne ou sur une colonne (<=> l'un des deux peut être en dehors mais pas les deux)
                    variationCase = (ligne-rubiksCube.caseCliquee[1][0], colonne-rubiksCube.caseCliquee[1][1])
                    rubiksCube.caseCliquee = [listeFaces[indexFaceVisible], (ligne, colonne)]
                    if variationCase[0] != 0 and variationCase[0] != 1: # on rend la variation de ligne unitaire
                        variationCase = (int(abs(variationCase[0])/variationCase[0]), variationCase[1])
                    if variationCase[1] != 0 and variationCase[1] != 1: # on rend la variation de colonne unitaire
                        variationCase = (variationCase[0], int(abs(variationCase[1])/variationCase[1]))
                    
                    positionRelativeFaces = [[Faces.RIGHT, Faces.LEFT, Faces.UP, Faces.DOWN], [], [Faces.BACK, Faces.FRONT, Faces.UP, Faces.DOWN], [Faces.FRONT, Faces.BACK, Faces.UP, Faces.DOWN], [Faces.RIGHT, Faces.LEFT, Faces.BACK, Faces.FRONT], [Faces.RIGHT, Faces.LEFT, Faces.FRONT, Faces.BACK]]
                    
                    if variationCase[0] != 0: # changement de ligne
                        if rubiksCube.caseCliquee[1][1]-variationCase[1] <= rubiksCube.taille/2:
                            if variationCase[0] == 1:
                                sensDeRotation = Sens.ANTIHORAIRE
                            else:
                                sensDeRotation = Sens.HORAIRE
                            rubiksCube.pivoterFace(positionFacesVuesParCamera[positionRelativeFaces[indexFaceVisible][1].value], sensDeRotation, rubiksCube.caseCliquee[1][1]-variationCase[1])
                            rubiksCube.sensRotationEnCours = sensDeRotation.value*Faces.SENS_ROTATIONS.value[positionFacesVuesParCamera[positionRelativeFaces[indexFaceVisible][1].value].value]
        
                        else:
                            if variationCase[0] == 1:
                                sensDeRotation = Sens.HORAIRE
                            else:
                                sensDeRotation = Sens.ANTIHORAIRE
                            rubiksCube.pivoterFace(positionFacesVuesParCamera[positionRelativeFaces[indexFaceVisible][0].value], sensDeRotation, rubiksCube.taille - (rubiksCube.caseCliquee[1][1]-variationCase[1] -1))
                            rubiksCube.sensRotationEnCours = sensDeRotation.value*Faces.SENS_ROTATIONS.value[positionFacesVuesParCamera[positionRelativeFaces[indexFaceVisible][0].value].value]
                    
                    elif variationCase[1] != 0: # changement de colonne
                        if rubiksCube.caseCliquee[1][0] <= rubiksCube.taille/2:
                            if variationCase[1] == 1:
                                sensDeRotation = Sens.HORAIRE
                            else:
                                sensDeRotation = Sens.ANTIHORAIRE
                            rubiksCube.pivoterFace(positionFacesVuesParCamera[positionRelativeFaces[indexFaceVisible][3].value], sensDeRotation, rubiksCube.caseCliquee[1][0])
                            rubiksCube.sensRotationEnCours = sensDeRotation.value*Faces.SENS_ROTATIONS.value[positionFacesVuesParCamera[positionRelativeFaces[indexFaceVisible][3].value].value]
        
                        else:
                            if variationCase[1] == 1:
                                sensDeRotation = Sens.ANTIHORAIRE
                            else:
                                sensDeRotation = Sens.HORAIRE
                            rubiksCube.pivoterFace(positionFacesVuesParCamera[positionRelativeFaces[indexFaceVisible][2].value], sensDeRotation, rubiksCube.taille - (rubiksCube.caseCliquee[1][0] -1))
                            rubiksCube.sensRotationEnCours = sensDeRotation.value*Faces.SENS_ROTATIONS.value[positionFacesVuesParCamera[positionRelativeFaces[indexFaceVisible][2].value].value]

    

def afficherRubiksCube(rubiksCube, screen, dimensionsEcran, fenetreActuelle):
    #pygame.init()
    #dimensionsEcran = (800,600)
    pygame.display.set_mode(dimensionsEcran, DOUBLEBUF|OPENGL)
    #pygame.display.gl_set_attribute(flag, value)
    pygame.display.set_caption("Rubik's Cube")
    
    baseCamera = [(1,0,0), (0,0,-1), (0,1,0)]

    gluPerspective(40, dimensionsEcran[0]/dimensionsEcran[1], 5, 21)
    glTranslatef(0,0,-3 -2*rubiksCube.taille)
    
    baseCamera = tournerCube(-30, baseCamera, Axes.Y)
    baseCamera = tournerCube(60, baseCamera, Axes.X)
    
    historiqueRotations = [(-30, baseCamera, Axes.Y), (60, baseCamera, Axes.X)] # Pour pouvoir réinitialiser la vue
        
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)
    
    positionClicSouris = None
    clicGaucheRotationCube = False
    mouvementEnCours = False
    
    fenetreSuivante = fenetreActuelle
    while fenetreSuivante == fenetreActuelle:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fenetreSuivante = QUITTER
                #pygame.quit()
                #sys.exit()
            
            if event.type == pygame.MOUSEBUTTONUP:
                clicGaucheRotationCube = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: # Réinitialisation de la vue
                    for indice in range(len(historiqueRotations)-1, 1, -1):
                        rotation = historiqueRotations[indice]
                        baseCamera = tournerCube(-rotation[0], rotation[1], rotation[2])
                    historiqueRotations = [(-30, baseCamera, Axes.Y), (60, baseCamera, Axes.X)]
                
                elif event.key == pygame.K_x:
                    fenetreSuivante = QUITTER
                elif event.key == pygame.K_m:
                    fenetreSuivante = MENU
                elif event.key == pygame.K_c:
                    fenetreSuivante = CUBES
                    
        positionSouris = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()
        clicGaucheMaintenu = pygame.mouse.get_pressed(num_buttons=3)[0]
        clicDroitMaintenu = pygame.mouse.get_pressed(num_buttons=3)[2]
        
        positionFacesVuesParCamera = determinerPositionFacesCamera(baseCamera)
        '''if not verifierCoherence(positionFacesVuesParCamera):
            print("ATTENTION : problème de cohérence des faces vues par la caméra !")'''
        
        if (clicGaucheMaintenu or keys[pygame.K_g]) and not clicGaucheRotationCube and not rubiksCube.mouvementEnCours: # pour plus de facilité sans souris, on prend "g" pour clic gauche et "h" pour clic droit
            positionAvecYVersLeHaut = (int(positionSouris[0]), int(dimensionsEcran[1]-positionSouris[1]))
            rotationFace(positionAvecYVersLeHaut, baseCamera, positionFacesVuesParCamera, rubiksCube)
            if rubiksCube.caseCliquee[0] is None:
                clicGaucheRotationCube = True # on fait tourner le cube au lieu de tourner une face
        else: # if not clicGaucheMaintenu
            rubiksCube.caseCliquee = (None, (None, None)) # [Face, (ligne, colonne)]
        
        if clicDroitMaintenu or clicGaucheRotationCube or keys[pygame.K_h]: # pour plus de facilité sans souris, on prend "g" pour clic gauche et "h" pour clic droit
            if positionClicSouris is None:
                positionClicSouris = positionSouris
            else:
                deplacementHorizontal = int((positionSouris[0] - positionClicSouris[0])*SENSIBILITE_SOURIS)
                baseCamera = tournerCube(-deplacementHorizontal, baseCamera, Axes.Z)
                historiqueRotations.append((-deplacementHorizontal, baseCamera, Axes.Z))
                
                deplacementVertical = int((positionSouris[1] - positionClicSouris[1])*SENSIBILITE_SOURIS)
                baseCamera = tournerCube(-deplacementVertical, baseCamera, Axes.X)
                historiqueRotations.append((-deplacementVertical, baseCamera, Axes.X))
                positionClicSouris = positionSouris
        else:
            positionClicSouris = None

        if len(rubiksCube.listActions) > 0 and (not rubiksCube.mouvementEnCours):
            rubiksCube.pivoterFace(rubiksCube.listActions[0][0], rubiksCube.listActions[0][1])
            del rubiksCube.listActions[0]
        
        if not rubiksCube.mouvementEnCours:
            if keys[pygame.K_TAB] or keys[pygame.K_4]: # touche Tab ou prime
                sensRotation = Sens.ANTIHORAIRE
            else:
                sensRotation = Sens.HORAIRE
            
            if keys[pygame.K_u]:
                rubiksCube.pivoterFace(positionFacesVuesParCamera[Faces.UP.value], sensRotation)
                rubiksCube.sensRotationEnCours = sensRotation.value*Faces.SENS_ROTATIONS.value[positionFacesVuesParCamera[Faces.UP.value].value]
            elif keys[pygame.K_d]:
                rubiksCube.pivoterFace(positionFacesVuesParCamera[Faces.DOWN.value], sensRotation)
                rubiksCube.sensRotationEnCours = sensRotation.value*Faces.SENS_ROTATIONS.value[positionFacesVuesParCamera[Faces.DOWN.value].value]
            elif keys[pygame.K_l]:
                rubiksCube.pivoterFace(positionFacesVuesParCamera[Faces.LEFT.value], sensRotation)
                rubiksCube.sensRotationEnCours = sensRotation.value*Faces.SENS_ROTATIONS.value[positionFacesVuesParCamera[Faces.LEFT.value].value]
            elif keys[pygame.K_r]:
                rubiksCube.pivoterFace(positionFacesVuesParCamera[Faces.RIGHT.value], sensRotation)
                rubiksCube.sensRotationEnCours = sensRotation.value*Faces.SENS_ROTATIONS.value[positionFacesVuesParCamera[Faces.RIGHT.value].value]
            elif keys[pygame.K_f]:
                rubiksCube.pivoterFace(positionFacesVuesParCamera[Faces.FRONT.value], sensRotation)
                rubiksCube.sensRotationEnCours = sensRotation.value*Faces.SENS_ROTATIONS.value[positionFacesVuesParCamera[Faces.FRONT.value].value]
            elif keys[pygame.K_b]:
                rubiksCube.pivoterFace(positionFacesVuesParCamera[Faces.BACK.value], sensRotation)
                rubiksCube.sensRotationEnCours = sensRotation.value*Faces.SENS_ROTATIONS.value[positionFacesVuesParCamera[Faces.BACK.value].value]
            elif keys[pygame.K_t]:
                rubiksCube.AjouterAction((Faces.UP, Sens.ANTIHORAIRE))
                print("yes")
            elif keys[pygame.K_s]:
                rubiksCube.jouerFormule(solver.solve(rubiksCube))
        if keys[pygame.K_UP]:
            baseCamera = tournerCube(10, baseCamera, Axes.X)
            historiqueRotations.append((10, baseCamera, Axes.X))
        if keys[pygame.K_DOWN]:
            baseCamera = tournerCube(-10, baseCamera, Axes.X)
            historiqueRotations.append((-10, baseCamera, Axes.X))
        if keys[pygame.K_LEFT]:
            baseCamera = tournerCube(10, baseCamera, Axes.Z)
            historiqueRotations.append((10, baseCamera, Axes.Z))
        if keys[pygame.K_RIGHT]:
            baseCamera = tournerCube(-10, baseCamera, Axes.Z)
            historiqueRotations.append((-10, baseCamera, Axes.Z))
        
        if rubiksCube.mouvementEnCours:
            if abs(rubiksCube.angleRotationEnCours) < 90: # la face n'a pas encore fait un quart de tour
                rubiksCube.angleRotationEnCours -= rubiksCube.sensRotationEnCours*10 # "-" parce qu'OpenGL compte les angles dans le sens horaire et pas trigo
            else: # la rotation est terminée
                rubiksCube.angleRotationEnCours = 0
                rubiksCube.axeRotationEnCours = None
                rubiksCube.mouvementEnCours = False
                rubiksCube.configurationAnterieure = rubiksCube.configuration
        
        glClearColor(0.6, 0.8, 0.8, 0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        dessinerRubiksCube(rubiksCube)
        
        pygame.display.flip()
        pygame.time.wait(40)
        
    return fenetreSuivante