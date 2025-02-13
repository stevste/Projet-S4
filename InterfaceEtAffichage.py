import pygame
import sys

from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from Enum import *
import RubiksCubeTailleN


def dessinerCarre(point1:tuple, point2:tuple, point3:tuple, point4:tuple, couleur:tuple):
    glColor3f(couleur[0], couleur[1], couleur[2])
    glVertex3f(point1[0], point1[1], point1[2])
    glVertex3f(point2[0], point2[1], point2[2])
    glVertex3f(point3[0], point3[1], point3[2])
    glVertex3f(point4[0], point4[1], point4[2])
    

def dessinerRubiksCube(rubiksCube):
    glBegin(GL_QUADS)
    
    origine = (-(rubiksCube.taille+2)/2, -(rubiksCube.taille+2)/2, -(rubiksCube.taille+2)/2)
    
    for x in range(1, rubiksCube.taille +1):
        for y in range(1, rubiksCube.taille +1):
            for z in range(1, rubiksCube.taille +1):
                couleur = (0.1, 0.1, 0.1) # Noir
                dessinerCarre((origine[0]+x, origine[1]+y, origine[2]+z), (origine[0]+x+1, origine[1]+y, origine[2]+z), (origine[0]+x+1, origine[1]+y+1, origine[2]+z), (origine[0]+x, origine[1]+y+1, origine[2]+z), couleur) # Face avant
                dessinerCarre((origine[0]+x, origine[1]+y, origine[2]+z+1), (origine[0]+x+1, origine[1]+y, origine[2]+z+1), (origine[0]+x+1, origine[1]+y+1, origine[2]+z+1), (origine[0]+x, origine[1]+y+1, origine[2]+z+1), couleur) # Face arrière
                dessinerCarre((origine[0]+x, origine[1]+y, origine[2]+z), (origine[0]+x, origine[1]+y+1, origine[2]+z), (origine[0]+x, origine[1]+y+1, origine[2]+z+1), (origine[0]+x, origine[1]+y, origine[2]+z+1), couleur) # Face gauche
                dessinerCarre((origine[0]+x+1, origine[1]+y, origine[2]+z), (origine[0]+x+1, origine[1]+y+1, origine[2]+z), (origine[0]+x+1, origine[1]+y+1, origine[2]+z+1), (origine[0]+x+1, origine[1]+y, origine[2]+z+1), couleur) # Face droite
                dessinerCarre((origine[0]+x, origine[1]+y+1, origine[2]+z), (origine[0]+x+1, origine[1]+y+1, origine[2]+z), (origine[0]+x+1, origine[1]+y+1, origine[2]+z+1), (origine[0]+x, origine[1]+y+1, origine[2]+z+1), couleur) # Face supérieure
                dessinerCarre((origine[0]+x, origine[1]+y, origine[2]+z), (origine[0]+x+1, origine[1]+y, origine[2]+z), (origine[0]+x+1, origine[1]+y, origine[2]+z+1), (origine[0]+x, origine[1]+y, origine[2]+z+1), couleur) # Face inférieure

                if rubiksCube.configuration[x+1][y][z] != STRUCTURE:
                    couleur = Couleur.LIST.value[rubiksCube.configuration[x+1][y][z]]
                    dessinerCarre((origine[0]+x+1.001, origine[1]+y+0.05, origine[2]+z+0.05), (origine[0]+x+1.001, origine[1]+y+0.95, origine[2]+z+0.05), (origine[0]+x+1.001, origine[1]+y+0.95, origine[2]+z+0.95), (origine[0]+x+1.001, origine[1]+y+0.05, origine[2]+z+0.95), couleur)
                elif rubiksCube.configuration[x-1][y][z] != STRUCTURE:
                    couleur = Couleur.LIST.value[rubiksCube.configuration[x-1][y][z]]
                    dessinerCarre((origine[0]+x-0.001, origine[1]+y+0.05, origine[2]+z+0.05), (origine[0]+x-0.001, origine[1]+y+0.95, origine[2]+z+0.05), (origine[0]+x-0.001, origine[1]+y+0.95, origine[2]+z+0.95), (origine[0]+x-0.001, origine[1]+y+0.05, origine[2]+z+0.95), couleur)
                if rubiksCube.configuration[x][y+1][z] != STRUCTURE:
                    couleur = Couleur.LIST.value[rubiksCube.configuration[x][y+1][z]]
                    dessinerCarre((origine[0]+x+0.05, origine[1]+y+1.001, origine[2]+z+0.05), (origine[0]+x+0.95, origine[1]+y+1.001, origine[2]+z+0.05), (origine[0]+x+0.95, origine[1]+y+1.001, origine[2]+z+0.95), (origine[0]+x+0.05, origine[1]+y+1.001, origine[2]+z+0.95), couleur)
                elif rubiksCube.configuration[x][y-1][z] != STRUCTURE:
                    couleur = Couleur.LIST.value[rubiksCube.configuration[x][y-1][z]]
                    dessinerCarre((origine[0]+x+0.05, origine[1]+y-0.001, origine[2]+z+0.05), (origine[0]+x+0.95, origine[1]+y-0.001, origine[2]+z+0.05), (origine[0]+x+0.95, origine[1]+y-0.001, origine[2]+z+0.95), (origine[0]+x+0.05, origine[1]+y-0.001, origine[2]+z+0.95), couleur)
                if rubiksCube.configuration[x][y][z+1] != STRUCTURE:
                    couleur = Couleur.LIST.value[rubiksCube.configuration[x][y][z+1]]
                    dessinerCarre((origine[0]+x+0.05, origine[1]+y+0.05, origine[2]+z+1.001), (origine[0]+x+0.95, origine[1]+y+0.05, origine[2]+z+1.001), (origine[0]+x+0.95, origine[1]+y+0.95, origine[2]+z+1.001), (origine[0]+x+0.05, origine[1]+y+0.95, origine[2]+z+1.001), couleur)
                elif rubiksCube.configuration[x][y][z-1] != STRUCTURE:
                    couleur = Couleur.LIST.value[rubiksCube.configuration[x][y][z-1]]
                    dessinerCarre((origine[0]+x+0.05, origine[1]+y+0.05, origine[2]+z-0.001), (origine[0]+x+0.95, origine[1]+y+0.05, origine[2]+z-0.001), (origine[0]+x+0.95, origine[1]+y+0.95, origine[2]+z-0.001), (origine[0]+x+0.05, origine[1]+y+0.95, origine[2]+z-0.001), couleur)

    glEnd()


def afficherRubiksCube(rubiksCube):
    pygame.init()
    display = (800,600)
    screen = pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    pygame.display.set_caption("Rubik's Cube")
    
    gluPerspective(40, display[0]/display[1], 1, 50)
    glTranslatef(0,0,-10)
    glRotatef(-60, 1,0,0)
    glRotatef(-30, 0,0,1)
    
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)
    
    positionClicSouris = None
    mouvementEnCours = False
    angleRotationX = 30
    angleRotationY = 0
    angleRotationZ = -30
    rotationsXYenFonctionZ = ((1,0,1), (0,1,-1), (1,0,-1), (0,1,1))
    rotationX, rotationY, sens = rotationsXYenFonctionZ[0]
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            
        clicDroitMaintenu = pygame.mouse.get_pressed(num_buttons=3)[2]
        if clicDroitMaintenu:
            positionActuelle = pygame.mouse.get_pos()
            if positionClicSouris is None:
                positionClicSouris = positionActuelle
            else:
                glRotatef((positionActuelle[0] - positionClicSouris[0])*0.2, 0,0,1)
                angleRotationZ += (positionActuelle[0] - positionClicSouris[0])*0.2
                glRotatef((positionActuelle[1] - positionClicSouris[1])*0.2*sens, rotationX, rotationY, 0)
                angleRotationX += (positionActuelle[1] - positionClicSouris[1])*0.2*sens*rotationX
                angleRotationY += (positionActuelle[1] - positionClicSouris[1])*0.2*sens*rotationY                
                positionClicSouris = positionActuelle
        else:
            positionClicSouris = None
        
        keys = pygame.key.get_pressed()
        if True in keys:
            if not mouvementEnCours:
                if keys[pygame.K_u]:
                    rubiksCube.pivoterFace(Faces.UP)
                    mouvementEnCours = True
                elif keys[pygame.K_d]:
                    rubiksCube.pivoterFace(Faces.DOWN)
                    mouvementEnCours = True
                elif keys[pygame.K_l]:
                    rubiksCube.pivoterFace(Faces.LEFT)
                    mouvementEnCours = True
                elif keys[pygame.K_r]:
                    rubiksCube.pivoterFace(Faces.RIGHT)
                    mouvementEnCours = True
                elif keys[pygame.K_f]:
                    rubiksCube.pivoterFace(Faces.FRONT)
                    mouvementEnCours = True
                elif keys[pygame.K_b]:
                    rubiksCube.pivoterFace(Faces.BACK)
                    mouvementEnCours = True

            if keys[pygame.K_UP]:
                glRotatef(-10*sens, rotationX, rotationY, 0)
                angleRotationX += -10*sens*rotationX
                angleRotationY += -10*sens*rotationY
            elif keys[pygame.K_DOWN]:
                glRotatef(10*sens, rotationX, rotationY, 0)
                angleRotationX += 10*sens*rotationX
                angleRotationY += 10*sens*rotationY
            if keys[pygame.K_LEFT]:
                glRotatef(-10, 0,0,1)
                angleRotationZ -= 10
            elif keys[pygame.K_RIGHT]:
                glRotatef(10, 0,0,1)
                angleRotationZ += 10
        
        if abs(angleRotationZ) > 45:
            signeAngle = angleRotationZ/abs(angleRotationZ)
            angleRotationZ = angleRotationZ - signeAngle*90
            rotationX, rotationY, sens = rotationsXYenFonctionZ[int(rotationsXYenFonctionZ.index((rotationX, rotationY, sens)) + signeAngle)%4]
        if abs(angleRotationX) > 90:
            signeAngle = angleRotationX/abs(angleRotationX)
            glRotatef(-angleRotationX + signeAngle*90, 1,0,0)
            angleRotationX = signeAngle*90
        if abs(angleRotationY) > 90:
            signeAngle = angleRotationY/abs(angleRotationY)
            glRotatef(-angleRotationY + signeAngle*90, 0,1,0)
            angleRotationY = signeAngle*90
        
        if mouvementEnCours:
            # poursuivre la rotation en cours
            # if la rotation est terminée:
                # mouvementEnCours = False
            # Temporaire :
            pygame.time.wait(300)
            mouvementEnCours = False

                    
        glClearColor(0.3, 0.5, 0.5, 0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        
        dessinerRubiksCube(rubiksCube)
        
        pygame.display.flip()
        pygame.time.wait(40)


'''
verticies = (
   (1, -1, -1),
   (1, 1, -1),
   (-1, 1, -1),
   (-1, -1, -1),
   (1, -1, 1),
   (1, 1, 1),
   (-1, -1, 1),
   (-1, 1, 1)
)
edges = (
   (0,1),
   (0,3),
   (0,4),
   (2,1),
   (2,3),
   (2,7),
   (6,3),
   (6,4),
   (6,7),
   (5,1),
   (5,4),
   (5,7)
)

def Cube():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()
'''
