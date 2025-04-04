import Menu
import RubiksCubeTailleN
import InterfaceEtAffichage
import Pivots
import carreNV2
from Enum import *

import pygame
 

pygame.init()

PLEIN_ECRAN = True
if PLEIN_ECRAN:
    dimensionsEcran = (pygame.display.Info().current_w, pygame.display.Info().current_h)
    #print(pygame.display.Info().current_w, pygame.display.Info().current_h)
    screen = pygame.display.set_mode(dimensionsEcran, pygame.FULLSCREEN) # taille fenêtre
else:
    dimensionsEcran = (1150, 650)
    screen = pygame.display.set_mode(dimensionsEcran) # taille fenêtre

pygame.display.set_caption("Projet ~ Casse-têtes")

fenetreSuivante = MENU
while fenetreSuivante != QUITTER:
    if fenetreSuivante == MENU:
        fenetreSuivante = Menu.menuPrincipal(screen, dimensionsEcran, COULEUR_FOND)
    elif fenetreSuivante == CARRES:
        fenetreSuivante = Menu.menuCarres(screen, dimensionsEcran, COULEUR_FOND)
    elif fenetreSuivante == CUBES:
        fenetreSuivante = Menu.menuCubes(screen, dimensionsEcran, COULEUR_FOND)
    elif fenetreSuivante == PIVOTS:
        fenetreSuivante = Menu.menuPivots(screen, dimensionsEcran, COULEUR_FOND)
    
    elif fenetreSuivante in [CUBE_2, CUBE_3, CUBE_4, CUBE_5, CUBE_6, CUBE_7]:
        fenetreSuivante = [(CUBE_2, 2), (CUBE_3, 3), (CUBE_4, 4), (CUBE_5, 5), (CUBE_6, 6), (CUBE_7, 7)][[CUBE_2, CUBE_3, CUBE_4, CUBE_5, CUBE_6, CUBE_7].index(fenetreSuivante)]

        fenetreSuivante = InterfaceEtAffichage.afficherRubiksCube(RubiksCubeTailleN.RubiksCube(fenetreSuivante[1]), screen, dimensionsEcran, fenetreSuivante[0])
        if PLEIN_ECRAN:
            screen = pygame.display.set_mode(dimensionsEcran, pygame.FULLSCREEN) # taille fenêtre
        else:
            screen = pygame.display.set_mode(dimensionsEcran) # taille fenêtre
    
    elif fenetreSuivante == CARRE_3:
        fenetreSuivante = carreNV2.afficherCarre(screen, dimensionsEcran, 3, CARRE_3)
    elif fenetreSuivante == CARRE_4:
        fenetreSuivante = carreNV2.afficherCarre(screen, dimensionsEcran, 4, CARRE_4)
    elif fenetreSuivante == CARRE_5:
        fenetreSuivante = carreNV2.afficherCarre(screen, dimensionsEcran, 5, CARRE_5)
    
    elif fenetreSuivante == PIVOT_2X3:
        fenetreSuivante = Pivots.afficherPivot(screen, dimensionsEcran, 2, 3, [[' I', 'N', 'P'], ['p', '1', '2']], None, PIVOT_2X3)
    elif fenetreSuivante == PIVOT_3X3:
        fenetreSuivante = Pivots.afficherPivot(screen, dimensionsEcran, 3, 3, [''], IMAGE_MULTICOLORE, PIVOT_3X3)
    elif fenetreSuivante == PIVOT_3X4:
        fenetreSuivante = Pivots.afficherPivot(screen, dimensionsEcran, 3, 4, [''], IMAGE_COLOREE, PIVOT_3X4)

pygame.mixer.fadeout(500)
pygame.quit()