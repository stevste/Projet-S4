import pygame
import sys
import math

from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from Enum import *
from Solver3D import *
import RubiksCubeTailleN



def dessinerCarre(point1:tuple, point2:tuple, point3:tuple, point4:tuple, couleur:tuple) -> None:
    glColor3f(couleur[0], couleur[1], couleur[2])
    glVertex3f(point1[0], point1[1], point1[2])
    glVertex3f(point2[0], point2[1], point2[2])
    glVertex3f(point3[0], point3[1], point3[2])
    glVertex3f(point4[0], point4[1], point4[2])


def dessinerCube(origine:tuple, baseLocale:tuple, couleur) -> None:
    dessinerCarre((origine[0], origine[1], origine[2]), (origine[0]+baseLocale[0][0], origine[1]+baseLocale[0][1], origine[2]+baseLocale[0][2]), (origine[0]+baseLocale[0][0]+baseLocale[1][0], origine[1]+baseLocale[0][1]+baseLocale[1][1], origine[2]+baseLocale[0][2]+baseLocale[1][2]), (origine[0]+baseLocale[1][0], origine[1]+baseLocale[1][1], origine[2]+baseLocale[1][2]), couleur) # Face avant
    dessinerCarre((origine[0]+baseLocale[2][0], origine[1]+baseLocale[2][1], origine[2]+baseLocale[2][2]), (origine[0]+baseLocale[0][0]+baseLocale[2][0], origine[1]+baseLocale[0][1]+baseLocale[2][1], origine[2]+baseLocale[0][2]+baseLocale[2][2]), (origine[0]+baseLocale[0][0]+baseLocale[1][0]+baseLocale[2][0], origine[1]+baseLocale[0][1]+baseLocale[1][1]+baseLocale[2][1], origine[2]+baseLocale[0][2]+baseLocale[1][2]+baseLocale[2][2]), (origine[0]+baseLocale[1][0]+baseLocale[2][0], origine[1]+baseLocale[1][1]+baseLocale[2][1], origine[2]+baseLocale[1][2]+baseLocale[2][2]), couleur) # Face arrière
    dessinerCarre((origine[0], origine[1], origine[2]), (origine[0]+baseLocale[1][0], origine[1]+baseLocale[1][1], origine[2]+baseLocale[1][2]), (origine[0]+baseLocale[1][0]+baseLocale[2][0], origine[1]+baseLocale[1][1]+baseLocale[2][1], origine[2]+baseLocale[1][2]+baseLocale[2][2]), (origine[0]+baseLocale[2][0], origine[1]+baseLocale[2][1], origine[2]+baseLocale[2][2]), couleur) # Face gauche
    dessinerCarre((origine[0]+baseLocale[0][0], origine[1]+baseLocale[0][1], origine[2]+baseLocale[0][2]), (origine[0]+baseLocale[0][0]+baseLocale[1][0], origine[1]+baseLocale[0][1]+baseLocale[1][1], origine[2]+baseLocale[0][2]+baseLocale[1][2]), (origine[0]+baseLocale[0][0]+baseLocale[1][0]+baseLocale[2][0], origine[1]+baseLocale[0][1]+baseLocale[1][1]+baseLocale[2][1], origine[2]+baseLocale[0][2]+baseLocale[1][2]+baseLocale[2][2]), (origine[0]+baseLocale[0][0]+baseLocale[2][0], origine[1]+baseLocale[0][1]+baseLocale[2][1], origine[2]+baseLocale[0][2]+baseLocale[2][2]), couleur) # Face droite
    dessinerCarre((origine[0]+baseLocale[1][0], origine[1]+baseLocale[1][1], origine[2]+baseLocale[1][2]), (origine[0]+baseLocale[0][0]+baseLocale[1][0], origine[1]+baseLocale[0][1]+baseLocale[1][1], origine[2]+baseLocale[0][2]+baseLocale[1][2]), (origine[0]+baseLocale[0][0]+baseLocale[1][0]+baseLocale[2][0], origine[1]+baseLocale[0][1]+baseLocale[1][1]+baseLocale[2][1], origine[2]+baseLocale[0][2]+baseLocale[1][2]+baseLocale[2][2]), (origine[0]+baseLocale[1][0]+baseLocale[2][0], origine[1]+baseLocale[1][1]+baseLocale[2][1], origine[2]+baseLocale[1][2]+baseLocale[2][2]), couleur) # Face supérieure
    dessinerCarre((origine[0], origine[1], origine[2]), (origine[0]+baseLocale[0][0], origine[1]+baseLocale[0][1], origine[2]+baseLocale[0][2]), (origine[0]+baseLocale[0][0]+baseLocale[2][0], origine[1]+baseLocale[0][1]+baseLocale[2][1], origine[2]+baseLocale[0][2]+baseLocale[2][2]), (origine[0]+baseLocale[2][0], origine[1]+baseLocale[2][1], origine[2]+baseLocale[2][2]), couleur) # Face inférieure


def dessinerRubiksCube(rubiksCube):
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
    else: # rubiksCube.axeRotationEnCours == AXE_Z:
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
                    origineLocale = (x - (rubiksCube.taille+2)/2, y - (rubiksCube.taille+2)/2, z - (rubiksCube.taille+2)/2)
                    origineCube = (origineLocale[0]*uX[0] + origineLocale[1]*uY[0] + origineLocale[2]*uZ[0], origineLocale[0]*uX[1] + origineLocale[1]*uY[1] + origineLocale[2]*uZ[1], origineLocale[0]*uX[2] + origineLocale[1]*uY[2] + origineLocale[2]*uZ[2])
                else:
                    uX = (1,0,0)
                    uY = (0,1,0)
                    uZ = (0,0,1)
                    origineCube = (origine[0]+x, origine[1]+y, origine[2]+z)
                
                couleur = (0.1, 0.1, 0.1) # Noir
                dessinerCube(origineCube, (uX, uY, uZ), couleur)
        
                # On colle les "gomettes" sur les faces des petits cubes :
                if rubiksCube.configurationAnterieure[x+1][y][z] != STRUCTURE:
                    couleur = Couleur.LIST.value[rubiksCube.configurationAnterieure[x+1][y][z]]
                    dessinerCarre((origineCube[0]+1.001*uX[0]+0.05*uY[0]+0.05*uZ[0], origineCube[1]+1.001*uX[1]+0.05*uY[1]+0.05*uZ[1], origineCube[2]+1.001*uX[2]+0.05*uY[2]+0.05*uZ[2]), (origineCube[0]+1.001*uX[0]+0.95*uY[0]+0.05*uZ[0], origineCube[1]+1.001*uX[1]+0.95*uY[1]+0.05*uZ[1], origineCube[2]+1.001*uX[2]+0.95*uY[2]+0.05*uZ[2]), (origineCube[0]+1.001*uX[0]+0.95*uY[0]+0.95*uZ[0], origineCube[1]+1.001*uX[1]+0.95*uY[1]+0.95*uZ[1], origineCube[2]+1.001*uX[2]+0.95*uY[2]+0.95*uZ[2]), (origineCube[0]+1.001*uX[0]+0.05*uY[0]+0.95*uZ[0], origineCube[1]+1.001*uX[1]+0.05*uY[1]+0.95*uZ[1], origineCube[2]+1.001*uX[2]+0.05*uY[2]+0.95*uZ[2]), couleur)                
                elif rubiksCube.configurationAnterieure[x-1][y][z] != STRUCTURE:
                    couleur = Couleur.LIST.value[rubiksCube.configurationAnterieure[x-1][y][z]]
                    dessinerCarre((origineCube[0]-0.001*uX[0]+0.05*uY[0]+0.05*uZ[0], origineCube[1]-0.001*uX[1]+0.05*uY[1]+0.05*uZ[1], origineCube[2]-0.001*uX[2]+0.05*uY[2]+0.05*uZ[2]), (origineCube[0]-0.001*uX[0]+0.95*uY[0]+0.05*uZ[0], origineCube[1]-0.001*uX[1]+0.95*uY[1]+0.05*uZ[1], origineCube[2]-0.001*uX[2]+0.95*uY[2]+0.05*uZ[2]), (origineCube[0]-0.001*uX[0]+0.95*uY[0]+0.95*uZ[0], origineCube[1]-0.001*uX[1]+0.95*uY[1]+0.95*uZ[1], origineCube[2]-0.001*uX[2]+0.95*uY[2]+0.95*uZ[2]), (origineCube[0]-0.001*uX[0]+0.05*uY[0]+0.95*uZ[0], origineCube[1]-0.001*uX[1]+0.05*uY[1]+0.95*uZ[1], origineCube[2]-0.001*uX[2]+0.05*uY[2]+0.95*uZ[2]), couleur)
                if rubiksCube.configurationAnterieure[x][y+1][z] != STRUCTURE:
                    couleur = Couleur.LIST.value[rubiksCube.configurationAnterieure[x][y+1][z]]
                    dessinerCarre((origineCube[0]+0.05*uX[0]+1.001*uY[0]+0.05*uZ[0], origineCube[1]+0.05*uX[1]+1.001*uY[1]+0.05*uZ[1], origineCube[2]+0.05*uX[2]+1.001*uY[2]+0.05*uZ[2]), (origineCube[0]+0.95*uX[0]+1.001*uY[0]+0.05*uZ[0], origineCube[1]+0.95*uX[1]+1.001*uY[1]+0.05*uZ[1], origineCube[2]+0.95*uX[2]+1.001*uY[2]+0.05*uZ[2]), (origineCube[0]+0.95*uX[0]+1.001*uY[0]+0.95*uZ[0], origineCube[1]+0.95*uX[1]+1.001*uY[1]+0.95*uZ[1], origineCube[2]+0.95*uX[2]+1.001*uY[2]+0.95*uZ[2]), (origineCube[0]+0.05*uX[0]+1.001*uY[0]+0.95*uZ[0], origineCube[1]+0.05*uX[1]+1.001*uY[1]+0.95*uZ[1], origineCube[2]+0.05*uX[2]+1.001*uY[2]+0.95*uZ[2]), couleur)
                elif rubiksCube.configurationAnterieure[x][y-1][z] != STRUCTURE:
                    couleur = Couleur.LIST.value[rubiksCube.configurationAnterieure[x][y-1][z]]
                    dessinerCarre((origineCube[0]+0.05*uX[0]-0.001*uY[0]+0.05*uZ[0], origineCube[1]+0.05*uX[1]-0.001*uY[1]+0.05*uZ[1], origineCube[2]+0.05*uX[2]-0.001*uY[2]+0.05*uZ[2]), (origineCube[0]+0.95*uX[0]-0.001*uY[0]+0.05*uZ[0], origineCube[1]+0.95*uX[1]-0.001*uY[1]+0.05*uZ[1], origineCube[2]+0.95*uX[2]-0.001*uY[2]+0.05*uZ[2]), (origineCube[0]+0.95*uX[0]-0.001*uY[0]+0.95*uZ[0], origineCube[1]+0.95*uX[1]-0.001*uY[1]+0.95*uZ[1], origineCube[2]+0.95*uX[2]-0.001*uY[2]+0.95*uZ[2]), (origineCube[0]+0.05*uX[0]-0.001*uY[0]+0.95*uZ[0], origineCube[1]+0.05*uX[1]-0.001*uY[1]+0.95*uZ[1], origineCube[2]+0.05*uX[2]-0.001*uY[2]+0.95*uZ[2]), couleur)
                if rubiksCube.configurationAnterieure[x][y][z+1] != STRUCTURE:
                    couleur = Couleur.LIST.value[rubiksCube.configurationAnterieure[x][y][z+1]]
                    dessinerCarre((origineCube[0]+0.05*uX[0]+0.05*uY[0]+1.001*uZ[0], origineCube[1]+0.05*uX[1]+0.05*uY[1]+1.001*uZ[1], origineCube[2]+0.05*uX[2]+0.05*uY[2]+1.001*uZ[2]), (origineCube[0]+0.95*uX[0]+0.05*uY[0]+1.001*uZ[0], origineCube[1]+0.95*uX[1]+0.05*uY[1]+1.001*uZ[1], origineCube[2]+0.95*uX[2]+0.05*uY[2]+1.001*uZ[2]), (origineCube[0]+0.95*uX[0]+0.95*uY[0]+1.001*uZ[0], origineCube[1]+0.95*uX[1]+0.95*uY[1]+1.001*uZ[1], origineCube[2]+0.95*uX[2]+0.95*uY[2]+1.001*uZ[2]), (origineCube[0]+0.05*uX[0]+0.95*uY[0]+1.001*uZ[0], origineCube[1]+0.05*uX[1]+0.95*uY[1]+1.001*uZ[1], origineCube[2]+0.05*uX[2]+0.95*uY[2]+1.001*uZ[2]), couleur)
                elif rubiksCube.configurationAnterieure[x][y][z-1] != STRUCTURE:
                    couleur = Couleur.LIST.value[rubiksCube.configurationAnterieure[x][y][z-1]]
                    dessinerCarre((origineCube[0]+0.05*uX[0]+0.05*uY[0]-0.001*uZ[0], origineCube[1]+0.05*uX[1]+0.05*uY[1]-0.001*uZ[1], origineCube[2]+0.05*uX[2]+0.05*uY[2]-0.001*uZ[2]), (origineCube[0]+0.95*uX[0]+0.05*uY[0]-0.001*uZ[0], origineCube[1]+0.95*uX[1]+0.05*uY[1]-0.001*uZ[1], origineCube[2]+0.95*uX[2]+0.05*uY[2]-0.001*uZ[2]), (origineCube[0]+0.95*uX[0]+0.95*uY[0]-0.001*uZ[0], origineCube[1]+0.95*uX[1]+0.95*uY[1]-0.001*uZ[1], origineCube[2]+0.95*uX[2]+0.95*uY[2]-0.001*uZ[2]), (origineCube[0]+0.05*uX[0]+0.95*uY[0]-0.001*uZ[0], origineCube[1]+0.05*uX[1]+0.95*uY[1]-0.001*uZ[1], origineCube[2]+0.05*uX[2]+0.95*uY[2]-0.001*uZ[2]), couleur)

    glEnd()
    

def afficherRubiksCube(rubiksCube):
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    pygame.display.set_caption("Rubik's Cube")
    
    gluPerspective(40, display[0]/display[1], 1, 50)
    glTranslatef(0,0,-10)
    glRotatef(-30, 0,0,1)
    angleRadiansZ = 30*math.pi/180
    rotationX = math.cos(angleRadiansZ)
    rotationY = math.sin(angleRadiansZ)
    glRotatef(-60, rotationX, rotationY, 0)
    
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

        if len(rubiksCube.listActions) > 0 and (not rubiksCube.mouvementEnCours):
            rubiksCube.pivoterFace(rubiksCube.listActions[0][0], rubiksCube.listActions[0][1])
            del rubiksCube.listActions[0]
                
        clicDroitMaintenu = pygame.mouse.get_pressed(num_buttons=3)[2]
        if clicDroitMaintenu:
            positionActuelle = pygame.mouse.get_pos()
            if positionClicSouris is None:
                positionClicSouris = positionActuelle
            else:
                glRotatef(int((positionActuelle[0] - positionClicSouris[0])*SENSIBILITE_SOURIS), 0,0,1)
                angleRadiansZ -= int((positionActuelle[0] - positionClicSouris[0])*SENSIBILITE_SOURIS)*math.pi/180
                glRotatef(int((positionActuelle[1] - positionClicSouris[1])*SENSIBILITE_SOURIS), rotationX, rotationY, 0)
                rotationX = math.cos(angleRadiansZ)
                rotationY = math.sin(angleRadiansZ)
                positionClicSouris = positionActuelle
        else:
            positionClicSouris = None
        
        keys = pygame.key.get_pressed()
        if True in keys:
            if not rubiksCube.mouvementEnCours:
                if keys[pygame.K_u]:
                    rubiksCube.ajouterAction((Faces.UP, Sens.HORAIRE))
                elif keys[pygame.K_d]:
                    rubiksCube.ajouterAction((Faces.DOWN, Sens.HORAIRE))
                elif keys[pygame.K_l]:
                    rubiksCube.ajouterAction((Faces.LEFT, Sens.HORAIRE))
                elif keys[pygame.K_r]:
                    rubiksCube.ajouterAction((Faces.RIGHT, Sens.HORAIRE))
                elif keys[pygame.K_f]:
                    rubiksCube.ajouterAction((Faces.FRONT, Sens.HORAIRE))
                elif keys[pygame.K_b]:
                    rubiksCube.ajouterAction((Faces.BACK, Sens.HORAIRE))
                if keys[pygame.K_j]:
                    jouerFormule([(Faces.RIGHT, Sens.HORAIRE), (Faces.RIGHT, Sens.HORAIRE), (Faces.UP, Sens.HORAIRE)], rubiksCube)

            if keys[pygame.K_UP]:
                glRotatef(-10, rotationX, rotationY, 0)
            elif keys[pygame.K_DOWN]:
                glRotatef(10, rotationX, rotationY, 0)
            if keys[pygame.K_LEFT]:
                glRotatef(-10, 0,0,1)
                angleRadiansZ += 10*math.pi/180
                rotationX = math.cos(angleRadiansZ)
                rotationY = math.sin(angleRadiansZ)
            elif keys[pygame.K_RIGHT]:
                glRotatef(10, 0,0,1)
                angleRadiansZ -= 10*math.pi/180
                rotationX = math.cos(angleRadiansZ)
                rotationY = math.sin(angleRadiansZ)
        
        if rubiksCube.mouvementEnCours:
            if abs(rubiksCube.angleRotationEnCours) < 90: # la face n'a pas encore fait un quart de tour
                rubiksCube.angleRotationEnCours -= 10
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
