import pygame
import sys
import math

from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from Enum import *

from Solver3D import *
import CubieCube as cc
import RubiksCubeTailleN



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
                    coordonneesCentrees = (x - (rubiksCube.taille+2)/2, y - (rubiksCube.taille+2)/2, z - (rubiksCube.taille+2)/2) # exemple pour un 3x3 : la "gomette" au centre de la face blanche devient (0, 0, 2) au lieu d'être (2, 2, 4)
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
    orientationFaces = ((0,-1,0), (0,1,0), (1,0,0), (-1,0,0), (0,0,1), (0,0,-1)) # FRONT, BACK, RIGHT, LEFT, UP, DOWN
    directionsBaseCamera = ((0,-1,0), (0,1,0), (1,0,0), (-1,0,0), (0,0,1), (0,0,-1))
    facesVuesParCamera = [None, None, None, None, None, None] # sera rempli avec la face la plus proche de la position FRONT, BACK, RIGHT, LEFT, UP, DOWN pour l'observateur
    
    for direction in [Faces.FRONT, Faces.BACK, Faces.RIGHT, Faces.LEFT, Faces.UP, Faces.DOWN]:
        produitScalaireMaxi = (directionsBaseCamera[direction.value][0]*baseCamera[0][0]+directionsBaseCamera[direction.value][1]*baseCamera[1][0]+directionsBaseCamera[direction.value][2]*baseCamera[2][0])*orientationFaces[Faces.FRONT.value][0] + (directionsBaseCamera[direction.value][0]*baseCamera[0][1]+directionsBaseCamera[direction.value][1]*baseCamera[1][1]+directionsBaseCamera[direction.value][2]*baseCamera[2][1])*orientationFaces[Faces.FRONT.value][1] + (directionsBaseCamera[direction.value][0]*baseCamera[0][2]+directionsBaseCamera[direction.value][1]*baseCamera[1][2]+directionsBaseCamera[direction.value][2]*baseCamera[2][2])*orientationFaces[Faces.FRONT.value][2]
        facesVuesParCamera[direction.value] = Faces.FRONT
        
        for face in [Faces.BACK, Faces.RIGHT, Faces.LEFT, Faces.UP, Faces.DOWN]:
            produitScalaire = (directionsBaseCamera[direction.value][0]*baseCamera[0][0]+directionsBaseCamera[direction.value][1]*baseCamera[1][0]+directionsBaseCamera[direction.value][2]*baseCamera[2][0])*orientationFaces[face.value][0] + (directionsBaseCamera[direction.value][0]*baseCamera[0][1]+directionsBaseCamera[direction.value][1]*baseCamera[1][1]+directionsBaseCamera[direction.value][2]*baseCamera[2][1])*orientationFaces[face.value][1] + (directionsBaseCamera[direction.value][0]*baseCamera[0][2]+directionsBaseCamera[direction.value][1]*baseCamera[1][2]+directionsBaseCamera[direction.value][2]*baseCamera[2][2])*orientationFaces[face.value][2]
            if produitScalaire >= produitScalaireMaxi and face not in facesVuesParCamera: # le deuxième test sert en cas d'égalité de deux produits scalaires, pour ne pas avoir deux fois la même face dans la liste facesVuesParCamera
                produitScalaireMaxi = produitScalaire
                facesVuesParCamera[direction.value] = face
    
    return facesVuesParCamera
    

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


def afficherRubiksCube(rubiksCube) -> None:
    refC, refE = rubiksCube.coinsEtAretes()
    pygame.init()
    dimensionsEcran = (800,600)
    pygame.display.set_mode(dimensionsEcran, DOUBLEBUF|OPENGL)
    pygame.display.set_caption("Rubik's Cube")
    
    baseCamera = [(1,0,0), (0,0,-1), (0,1,0)]

    gluPerspective(40, dimensionsEcran[0]/dimensionsEcran[1], 1, 50)
    glTranslatef(0,0,-10)
    
    baseCamera = tournerCube(-30, baseCamera, Axes.Y)
    baseCamera = tournerCube(60, baseCamera, Axes.X)
    
    historiqueRotations = [(-30, baseCamera, Axes.Y), (60, baseCamera, Axes.X)] # Pour pouvoir réinitialiser la vue
        
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)
    
    positionClicSouris = None
    mouvementEnCours = False
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: # Réinitialisation de la vue
                    for indice in range(len(historiqueRotations)-1, 1, -1):
                        rotation = historiqueRotations[indice]
                        baseCamera = tournerCube(-rotation[0], rotation[1], rotation[2])
                    historiqueRotations = [(-30, baseCamera, Axes.Y), (60, baseCamera, Axes.X)]
                
                if event.key == pygame.K_i: # info, on peut y mettre n'importe quel print d'une variable pour faire des tests
                    print(determinerPositionFacesCamera(baseCamera))

        if len(rubiksCube.listActions) > 0 and (not rubiksCube.mouvementEnCours):
            rubiksCube.pivoterFace(rubiksCube.listActions[0][0], rubiksCube.listActions[0][1])
            del rubiksCube.listActions[0]
        
        keys = pygame.key.get_pressed()      
        positionFacesVuesParCamera = determinerPositionFacesCamera(baseCamera)
        
        clicDroitMaintenu = pygame.mouse.get_pressed(num_buttons=3)[2]
        if clicDroitMaintenu or keys[pygame.K_h]: # pour plus de facilité sans souris, on prend "g" pour clic gauche et "h" pour clic droit
            positionActuelle = pygame.mouse.get_pos()
            if positionClicSouris is None:
                positionClicSouris = positionActuelle
            else:
                deplacementHorizontal = int((positionActuelle[0] - positionClicSouris[0])*SENSIBILITE_SOURIS)
                baseCamera = tournerCube(-deplacementHorizontal, baseCamera, Axes.Z)
                historiqueRotations.append((-deplacementHorizontal, baseCamera, Axes.Z))
                
                deplacementVertical = int((positionActuelle[1] - positionClicSouris[1])*SENSIBILITE_SOURIS)
                baseCamera = tournerCube(-deplacementVertical, baseCamera, Axes.X)
                historiqueRotations.append((-deplacementVertical, baseCamera, Axes.X))
                positionClicSouris = positionActuelle
        else:
            positionClicSouris = None
        
        clicGaucheMaintenu = pygame.mouse.get_pressed(num_buttons=3)[0]
        if (clicGaucheMaintenu or keys[pygame.K_g]) and not rubiksCube.mouvementEnCours: # pour plus de facilité sans souris, on prend "g" pour clic gauche et "h" pour clic droit
            positionSouris = pygame.mouse.get_pos()
            positionCentree = [int(positionSouris[0] - dimensionsEcran[0]/2), int(-positionSouris[1] + dimensionsEcran[1]/2)]
            baseCubeDansBaseCamera = ((baseCamera[0][0], baseCamera[1][0], baseCamera[2][0]), (baseCamera[0][1], baseCamera[1][1], baseCamera[2][1]), (baseCamera[0][2], baseCamera[1][2], baseCamera[2][2]))
            
            coinBasGauche = [[0,0,0], [positionFacesVuesParCamera[Faces.FRONT.value], positionFacesVuesParCamera[Faces.DOWN.value], positionFacesVuesParCamera[Faces.LEFT.value]]] # [position, intersection de 3 faces]
            coinBasDroite = [[0,0,0], [positionFacesVuesParCamera[Faces.FRONT.value], positionFacesVuesParCamera[Faces.DOWN.value], positionFacesVuesParCamera[Faces.RIGHT.value]]] # [position, intersection de 3 faces]
            coinHautGauche = [[0,0,0], [positionFacesVuesParCamera[Faces.FRONT.value], positionFacesVuesParCamera[Faces.UP.value], positionFacesVuesParCamera[Faces.LEFT.value]]] # [position, intersection de 3 faces]
            coinHautDroite = [[0,0,0], [positionFacesVuesParCamera[Faces.FRONT.value], positionFacesVuesParCamera[Faces.UP.value], positionFacesVuesParCamera[Faces.RIGHT.value]]] # [position, intersection de 3 faces]
            for coin in [coinBasGauche, coinBasDroite, coinHautGauche, coinHautDroite]:
                positionCoinDansBaseCamera = coin[0]
                for face in coin[1]:
                    coordonnee = Faces.SIGNES_ABSCISSES.value[face.value]*rubiksCube.taille/2
                    positionCoinDansBaseCamera[0] += int(NB_DE_PIXELS_DANS_UNE_UNITE*baseCubeDansBaseCamera[Faces.AXES_ROTATION.value[face.value].value][0]*coordonnee)
                    positionCoinDansBaseCamera[1] += int(NB_DE_PIXELS_DANS_UNE_UNITE*baseCubeDansBaseCamera[Faces.AXES_ROTATION.value[face.value].value][1]*coordonnee)
                    positionCoinDansBaseCamera[2] += int(NB_DE_PIXELS_DANS_UNE_UNITE*baseCubeDansBaseCamera[Faces.AXES_ROTATION.value[face.value].value][2]*coordonnee)
            vecteurChangementDeLigne = ((coinHautGauche[0][0]-coinBasGauche[0][0])/rubiksCube.taille, (coinHautGauche[0][2]-coinBasGauche[0][2])/rubiksCube.taille) # déplacement nécessaire pour augmenter d'une ligne
            vecteurChangementDeColonne = ((coinBasDroite[0][0]-coinBasGauche[0][0])/rubiksCube.taille, (coinBasDroite[0][2]-coinBasGauche[0][2])/rubiksCube.taille) # déplacement nécessaire pour augmenter d'une colonne
            
            ligne = 0
            while ligne <= rubiksCube.taille and estAuDessus(positionCentree, determinerEquationDroite((coinBasGauche[0][0] + vecteurChangementDeLigne[0]*ligne, coinBasGauche[0][2] + vecteurChangementDeLigne[1]*ligne), (coinBasDroite[0][0] + vecteurChangementDeLigne[0]*ligne, coinBasDroite[0][2] + vecteurChangementDeLigne[1]*ligne))):
                ligne += 1
            if ligne == 0 or ligne == rubiksCube.taille +1:
                ligne = None # hors du cube
            
            colonne = 0
            while colonne <= rubiksCube.taille and estADroite(positionCentree, determinerEquationDroite((coinBasGauche[0][0] + vecteurChangementDeColonne[0]*colonne, coinBasGauche[0][2] + vecteurChangementDeColonne[1]*colonne), (coinHautGauche[0][0] + vecteurChangementDeColonne[0]*colonne, coinHautGauche[0][2] + vecteurChangementDeColonne[1]*colonne))):
                colonne += 1
            if colonne == 0 or colonne == rubiksCube.taille +1:
                colonne = None # hors du cube
            
            if rubiksCube.caseCliqueeSurFaceFRONT == (None, None):
                if ligne is not None and colonne is not None:
                    rubiksCube.caseCliqueeSurFaceFRONT = (ligne, colonne)
            else:
                if ligne is not None or colonne is not None: # on peut potentiellement être en dehors du cube tant qu'on est au moins sur une ligne ou sur une colonne (<=> l'un des deux peut être None mais pas les deux)
                    if ligne is None:
                        ligne = rubiksCube.caseCliqueeSurFaceFRONT[0]
                    elif colonne is None:
                        colonne = rubiksCube.caseCliqueeSurFaceFRONT[1]
                        
                    variationCase = (ligne-rubiksCube.caseCliqueeSurFaceFRONT[0], colonne-rubiksCube.caseCliqueeSurFaceFRONT[1])
                    rubiksCube.caseCliqueeSurFaceFRONT = (ligne, colonne)
                    if variationCase[0] != 0:
                        variationCase = (abs(variationCase[0])/variationCase[0], variationCase[1])
                    if variationCase[1] != 0:
                        variationCase = (variationCase[0], abs(variationCase[1])/variationCase[1])
                    
                    #print(ligne, colonne, variationCase)
                    if variationCase[0] != 0: # changement de ligne
                        if rubiksCube.caseCliqueeSurFaceFRONT[1]-variationCase[1] -1 <= rubiksCube.taille/2:
                            if variationCase[0] == 1:
                                sensDeRotation = Sens.ANTIHORAIRE
                            else:
                                sensDeRotation = Sens.HORAIRE
                            #print('gauche', sensDeRotation, rubiksCube.caseCliqueeSurFaceFRONT[1]-variationCase[1])
                            rubiksCube.pivoterFace(positionFacesVuesParCamera[Faces.LEFT.value], sensDeRotation, rubiksCube.caseCliqueeSurFaceFRONT[1]-variationCase[1])
                            sens = sensDeRotation.value*Faces.SENS_ROTATIONS.value[positionFacesVuesParCamera[Faces.LEFT.value].value]

                        else: #if rubiksCube.taille - (rubiksCube.caseCliqueeSurFaceFRONT[1]-variationCase[1]) <= rubiksCube.taille//2:
                            if variationCase[0] == 1:
                                sensDeRotation = Sens.HORAIRE
                            else:
                                sensDeRotation = Sens.ANTIHORAIRE
                            #print('droite', sensDeRotation, rubiksCube.taille - (rubiksCube.caseCliqueeSurFaceFRONT[1]-variationCase[1] -1))
                            rubiksCube.pivoterFace(positionFacesVuesParCamera[Faces.RIGHT.value], sensDeRotation, rubiksCube.taille - (rubiksCube.caseCliqueeSurFaceFRONT[1]-variationCase[1] -1))
                            sens = sensDeRotation.value*Faces.SENS_ROTATIONS.value[positionFacesVuesParCamera[Faces.RIGHT.value].value]
                    
                    elif variationCase[1] != 0: # changement de colonne
                        if rubiksCube.caseCliqueeSurFaceFRONT[0] -1 <= rubiksCube.taille/2:
                            if variationCase[1] == 1:
                                sensDeRotation = Sens.HORAIRE
                            else:
                                sensDeRotation = Sens.ANTIHORAIRE
                            #print('bas', sensDeRotation, rubiksCube.caseCliqueeSurFaceFRONT[0])
                            rubiksCube.pivoterFace(positionFacesVuesParCamera[Faces.DOWN.value], sensDeRotation, rubiksCube.caseCliqueeSurFaceFRONT[0])
                            sens = sensDeRotation.value*Faces.SENS_ROTATIONS.value[positionFacesVuesParCamera[Faces.DOWN.value].value]

                        else: #if rubiksCube.taille - rubiksCube.caseCliqueeSurFaceFRONT[0] <= rubiksCube.taille//2:
                            if variationCase[1] == 1:
                                sensDeRotation = Sens.ANTIHORAIRE
                            else:
                                sensDeRotation = Sens.HORAIRE
                            #print('haut', sensDeRotation, rubiksCube.taille - (rubiksCube.caseCliqueeSurFaceFRONT[0] -1))
                            rubiksCube.pivoterFace(positionFacesVuesParCamera[Faces.UP.value], sensDeRotation, rubiksCube.taille - (rubiksCube.caseCliqueeSurFaceFRONT[0] -1))
                            sens = sensDeRotation.value*Faces.SENS_ROTATIONS.value[positionFacesVuesParCamera[Faces.UP.value].value]

        else: # if not clicGaucheMaintenu
            rubiksCube.caseCliqueeSurFaceFRONT = (None, None)
        
        if not rubiksCube.mouvementEnCours:
            if keys[pygame.K_TAB] or keys[pygame.K_4]: # touche Tab ou prime
                sensRotation = Sens.ANTIHORAIRE
            else:
                sensRotation = Sens.HORAIRE
            
            if keys[pygame.K_u]:
                rubiksCube.ajouterAction((positionFacesVuesParCamera[Faces.UP.value], sensRotation))
                rubiksCube.sensRotationEnCours = sensRotation.value*Faces.SIGNES_ABSCISSES.value[positionFacesVuesParCamera[Faces.UP.value].value]
            elif keys[pygame.K_d]:
                rubiksCube.ajouterAction((positionFacesVuesParCamera[Faces.DOWN.value], sensRotation))
                rubiksCube.sensRotationEnCours = sensRotation.value*Faces.SIGNES_ABSCISSES.value[positionFacesVuesParCamera[Faces.DOWN.value].value]
            elif keys[pygame.K_l]:
                rubiksCube.ajouterAction((positionFacesVuesParCamera[Faces.LEFT.value], sensRotation))
                rubiksCube.sensRotationEnCours = sensRotation.value*Faces.SIGNES_ABSCISSES.value[positionFacesVuesParCamera[Faces.LEFT.value].value]
            elif keys[pygame.K_r]:
                rubiksCube.ajouterAction((positionFacesVuesParCamera[Faces.RIGHT.value], sensRotation))
                rubiksCube.sensRotationEnCours = sensRotation.value*Faces.SIGNES_ABSCISSES.value[positionFacesVuesParCamera[Faces.RIGHT.value].value]
            elif keys[pygame.K_f]:
                rubiksCube.ajouterAction((positionFacesVuesParCamera[Faces.FRONT.value], sensRotation))
                rubiksCube.sensRotationEnCours = sensRotation.value*Faces.SIGNES_ABSCISSES.value[positionFacesVuesParCamera[Faces.FRONT.value].value]
            elif keys[pygame.K_b]:
                rubiksCube.ajouterAction((positionFacesVuesParCamera[Faces.BACK.value], sensRotation))
                rubiksCube.sensRotationEnCours = sensRotation.value*Faces.SIGNES_ABSCISSES.value[positionFacesVuesParCamera[Faces.BACK.value].value]
            if keys[pygame.K_s]:
                scramble = generateScrambleSubGroup()
                jouerFormule(scramble, rubiksCube)
            if keys[pygame.K_s]:
                c, e = rubiksCube.coinsEtAretes()
                #print(GetEdgePermCoord(e, refE))
                Solve(rubiksCube)
            if keys[pygame.K_t]:
                test = cc.CubieCube(rubiksCube)
                #test.Move(Moves.F1)
                print("yes")

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
        
        glClearColor(0.3, 0.5, 0.5, 0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        dessinerRubiksCube(rubiksCube)
        
        pygame.display.flip()
        pygame.time.wait(40)
