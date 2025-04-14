from Enum import *

import pygame

IMAGE_CUBE = pygame.image.load("Images\PhotoCube.png")
IMAGE_CUBE_2 = pygame.image.load("Images\PhotoCube2.png")
IMAGE_CUBE_3 = pygame.image.load("Images\PhotoCube3.png")
IMAGE_CUBE_4 = pygame.image.load("Images\PhotoCube4.png")
IMAGE_CUBE_5 = pygame.image.load("Images\PhotoCube5.png")
IMAGE_CUBE_6 = pygame.image.load("Images\PhotoCube6.png")
IMAGE_CUBE_7 = pygame.image.load("Images\PhotoCube7.png")

IMAGE_CARRE_3 = pygame.image.load("Images\PhotoCarre.png")
IMAGE_CARRE_4 = pygame.image.load("Images\PhotoCarre4.png")
IMAGE_CARRE_5 = pygame.image.load("Images\PhotoCarre5.png")

IMAGE_PIVOT_2x3 = pygame.image.load("Images\PhotoPivot.png")
IMAGE_PIVOT_3x3 = pygame.image.load("Images\PhotoPivot3x3.png")
IMAGE_PIVOT_3x4 = pygame.image.load("Images\PhotoPivot3x4.png")


class Bouton:
    def __init__(self, position:tuple, texte:str, taille:tuple, arrondiBords:int=0, couleur:tuple=VERT, taillePolice=35, positionTexte=(63, 10), image=None, positionImage=None):
        self.position = (int(position[0]), int(position[1])) # (x, y)
        self.taille = (int(taille[0]), int(taille[1])) # (largeur, hauteur)
        self.texte = texte
        self.taillePolice = int(taillePolice)
        self.positionTexte = positionTexte # (deltaX, deltaY) par rapport au coin supérieur gauche
        self.couleur = couleur
        self.arrondiBords = arrondiBords
        
        self.zoneCollision = pygame.Rect(self.position[0], self.position[1], self.taille[0], self.taille[1])
        self.appuye = False
        
        self.image = image
        self.positionImage = positionImage
        
    def afficher(self, screen) -> None:
        decalage = (0,0)
        if self.appuye:
            decalage = (2,3) # pour faire comme si le bouton s'appuyait vers son ombre
        
        pygame.draw.rect(screen, (40,40,40), pygame.Rect(self.position[0]+2, self.position[1]+3, self.taille[0], self.taille [1]), 0, self.arrondiBords) # ombre
        pygame.draw.rect(screen, self.couleur, pygame.Rect(self.position[0]+decalage[0], self.position[1]+decalage[1], self.taille[0], self.taille[1]), 0, self.arrondiBords) # remplissage coloré
        pygame.draw.rect(screen, (0,0,0), pygame.Rect(self.position[0]+decalage[0], self.position[1]+decalage[1], self.taille[0], self.taille[1]), 2, self.arrondiBords) # bordure
        
        if self.image is not None:
            screen.blit(self.image, (self.position[0]+self.positionImage[0]+decalage[0], self.position[1]+self.positionImage[1]+decalage[1]))
        
        texte = pygame.font.Font(None, self.taillePolice).render(self.texte, 1, (0,0,0))
        screen.blit(texte, (self.position[0] + self.positionTexte[0] + decalage[0], self.position[1] + self.positionTexte[1] + decalage[1]))


def menuPrincipal(screen, dimensionsEcran:tuple, couleurFondEcran:tuple=(205, 214, 215)):
    imageCarre = pygame.transform.scale(IMAGE_CARRE_3, (dimensionsEcran[1]*0.3, dimensionsEcran[1]*0.3))
    imageCube = pygame.transform.scale(IMAGE_CUBE, (dimensionsEcran[0]*0.2, dimensionsEcran[1]*0.34))
    imagePivot = pygame.transform.scale(IMAGE_PIVOT_2x3, (dimensionsEcran[0]*0.245, dimensionsEcran[1]*0.26))
    
    boutonCarres = Bouton((dimensionsEcran[0]*0.075, dimensionsEcran[1]*0.4), "Carrés", (dimensionsEcran[0]*0.25, dimensionsEcran[1]*0.4), 10, COULEUR_BOUTONS, dimensionsEcran[1]/17, (dimensionsEcran[0]*0.09, dimensionsEcran[1]*0.02), imageCarre, (dimensionsEcran[0]*0.04, dimensionsEcran[1]*0.07))
    boutonCubes = Bouton((dimensionsEcran[0]*0.375, dimensionsEcran[1]*0.4), "Cubes", (dimensionsEcran[0]*0.25, dimensionsEcran[1]*0.4), 10, COULEUR_BOUTONS, dimensionsEcran[1]/17, (dimensionsEcran[0]*0.09, dimensionsEcran[1]*0.018), imageCube, (dimensionsEcran[0]*0.02, dimensionsEcran[1]*0.055))
    boutonPivots = Bouton((dimensionsEcran[0]*0.675, dimensionsEcran[1]*0.4), "Pivots", (dimensionsEcran[0]*0.25, dimensionsEcran[1]*0.4), 10, COULEUR_BOUTONS, dimensionsEcran[1]/17, (dimensionsEcran[0]*0.09, dimensionsEcran[1]*0.02), imagePivot, (2, dimensionsEcran[1]*0.085))
    
    boutonQuitter = Bouton((dimensionsEcran[0]*0.95, dimensionsEcran[1]*0.02), "x", (dimensionsEcran[0]*0.033, dimensionsEcran[1]*0.052), 4, ROUGE, dimensionsEcran[1]/15, (dimensionsEcran[0]*0.0097, dimensionsEcran[1]*0.003))
    listeBoutons = [boutonCarres, boutonCubes, boutonPivots, boutonQuitter]
        
    fenetreSuivante = MENU
    while fenetreSuivante == MENU:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fenetreSuivante = QUITTER
            
            if event.type == pygame.MOUSEBUTTONUP:
                positionSouris = pygame.mouse.get_pos()
                for bouton in listeBoutons:
                    bouton.appuye = False
                    if bouton.zoneCollision.collidepoint(positionSouris):
                        fenetreSuivante = [CARRES, CUBES, PIVOTS, QUITTER][listeBoutons.index(bouton)]
        
        clicGaucheMaintenu = pygame.mouse.get_pressed(num_buttons=3)[0]
        if clicGaucheMaintenu:
            positionSouris = pygame.mouse.get_pos()
            for bouton in listeBoutons:
                bouton.appuye = False
                if bouton.zoneCollision.collidepoint(positionSouris):
                    bouton.appuye = True
        
        # Affichage de la fenêtre :
        screen.fill(couleurFondEcran)
        for bouton in listeBoutons:
            bouton.afficher(screen)
        pygame.display.update()
        pygame.time.wait(100)
        
    return fenetreSuivante


def menuCarres(screen, dimensionsEcran:tuple, couleurFondEcran:tuple=(205, 214, 215)):
    image3 = pygame.transform.scale(IMAGE_CARRE_3, (dimensionsEcran[1]*0.3, dimensionsEcran[1]*0.3))
    image4 = pygame.transform.scale(IMAGE_CARRE_4, (dimensionsEcran[0]*0.18, dimensionsEcran[1]*0.3))
    image5 = pygame.transform.scale(IMAGE_CARRE_5, (dimensionsEcran[0]*0.18, dimensionsEcran[1]*0.3))
    
    bouton3 = Bouton((dimensionsEcran[0]*0.075, dimensionsEcran[1]*0.4), "3 x 3", (dimensionsEcran[0]*0.25, dimensionsEcran[1]*0.4), 10, COULEUR_BOUTONS, dimensionsEcran[1]/17, (dimensionsEcran[0]*0.1, dimensionsEcran[1]*0.02), image3, (dimensionsEcran[0]*0.04, dimensionsEcran[1]*0.07))
    bouton4 = Bouton((dimensionsEcran[0]*0.375, dimensionsEcran[1]*0.4), "4 x 4", (dimensionsEcran[0]*0.25, dimensionsEcran[1]*0.4), 10, COULEUR_BOUTONS, dimensionsEcran[1]/17, (dimensionsEcran[0]*0.1, dimensionsEcran[1]*0.02), image4, (dimensionsEcran[0]*0.036, dimensionsEcran[1]*0.07))
    bouton5 = Bouton((dimensionsEcran[0]*0.675, dimensionsEcran[1]*0.4), "5 x 5", (dimensionsEcran[0]*0.25, dimensionsEcran[1]*0.4), 10, COULEUR_BOUTONS, dimensionsEcran[1]/17, (dimensionsEcran[0]*0.1, dimensionsEcran[1]*0.02), image5, (dimensionsEcran[0]*0.036, dimensionsEcran[1]*0.07))
    
    boutonMenu = Bouton((dimensionsEcran[0]*0.85, dimensionsEcran[1]*0.02), "Menu", (dimensionsEcran[0]*0.08, dimensionsEcran[1]*0.052), 4, COULEUR_BOUTONS, dimensionsEcran[1]/17, (dimensionsEcran[0]*0.01, dimensionsEcran[1]*0.009))
    boutonQuitter = Bouton((dimensionsEcran[0]*0.95, dimensionsEcran[1]*0.02), "x", (dimensionsEcran[0]*0.033, dimensionsEcran[1]*0.052), 4, ROUGE, dimensionsEcran[1]/15, (dimensionsEcran[0]*0.0097, dimensionsEcran[1]*0.003))
    listeBoutons = [bouton3, bouton4, bouton5, boutonMenu, boutonQuitter]
    
    fenetreSuivante = CARRES
    while fenetreSuivante == CARRES:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fenetreSuivante = QUITTER
            
            if event.type == pygame.MOUSEBUTTONUP:
                positionSouris = pygame.mouse.get_pos()
                for bouton in listeBoutons:
                    bouton.appuye = False
                    if bouton.zoneCollision.collidepoint(positionSouris):
                        fenetreSuivante = [CARRE_3, CARRE_4, CARRE_5, MENU, QUITTER][listeBoutons.index(bouton)]
        
        clicGaucheMaintenu = pygame.mouse.get_pressed(num_buttons=3)[0]
        if clicGaucheMaintenu:
            positionSouris = pygame.mouse.get_pos()
            for bouton in listeBoutons:
                bouton.appuye = False
                if bouton.zoneCollision.collidepoint(positionSouris):
                    bouton.appuye = True
        
        # Affichage de la fenêtre :
        screen.fill(couleurFondEcran)
        for bouton in listeBoutons:
            bouton.afficher(screen)
        pygame.display.update()
        pygame.time.wait(100)
        
    return fenetreSuivante


def menuCubes(screen, dimensionsEcran:tuple, couleurFondEcran:tuple=(205, 214, 215)):
    image2 = pygame.transform.scale(IMAGE_CUBE_2, (dimensionsEcran[0]*0.2, dimensionsEcran[1]*0.33))
    image3 = pygame.transform.scale(IMAGE_CUBE_3, (dimensionsEcran[0]*0.2, dimensionsEcran[1]*0.33))
    image4 = pygame.transform.scale(IMAGE_CUBE_4, (dimensionsEcran[0]*0.2, dimensionsEcran[1]*0.33))
    image5 = pygame.transform.scale(IMAGE_CUBE_5, (dimensionsEcran[0]*0.2, dimensionsEcran[1]*0.33))
    image6 = pygame.transform.scale(IMAGE_CUBE_6, (dimensionsEcran[0]*0.2, dimensionsEcran[1]*0.33))
    image7 = pygame.transform.scale(IMAGE_CUBE_7, (dimensionsEcran[0]*0.2, dimensionsEcran[1]*0.33))
    
    bouton2 = Bouton((dimensionsEcran[0]*0.075, dimensionsEcran[1]*0.1), "2 x 2 x 2", (dimensionsEcran[0]*0.25, dimensionsEcran[1]*0.4), 10, COULEUR_BOUTONS, dimensionsEcran[1]/17, (dimensionsEcran[0]*0.085, dimensionsEcran[1]*0.02), image2, (dimensionsEcran[0]*0.02, dimensionsEcran[1]*0.06))
    bouton3 = Bouton((dimensionsEcran[0]*0.375, dimensionsEcran[1]*0.1), "3 x 3 x 3", (dimensionsEcran[0]*0.25, dimensionsEcran[1]*0.4), 10, COULEUR_BOUTONS, dimensionsEcran[1]/17, (dimensionsEcran[0]*0.085, dimensionsEcran[1]*0.02), image3, (dimensionsEcran[0]*0.02, dimensionsEcran[1]*0.06))
    bouton4 = Bouton((dimensionsEcran[0]*0.675, dimensionsEcran[1]*0.1), "4 x 4 x 4", (dimensionsEcran[0]*0.25, dimensionsEcran[1]*0.4), 10, COULEUR_BOUTONS, dimensionsEcran[1]/17, (dimensionsEcran[0]*0.085, dimensionsEcran[1]*0.02), image4, (dimensionsEcran[0]*0.02, dimensionsEcran[1]*0.06))
    bouton5 = Bouton((dimensionsEcran[0]*0.075, dimensionsEcran[1]*0.55), "5 x 5 x 5", (dimensionsEcran[0]*0.25, dimensionsEcran[1]*0.4), 10, COULEUR_BOUTONS, dimensionsEcran[1]/17, (dimensionsEcran[0]*0.085, dimensionsEcran[1]*0.02), image5, (dimensionsEcran[0]*0.02, dimensionsEcran[1]*0.06))
    bouton6 = Bouton((dimensionsEcran[0]*0.375, dimensionsEcran[1]*0.55), "6 x 6 x 6", (dimensionsEcran[0]*0.25, dimensionsEcran[1]*0.4), 10, COULEUR_BOUTONS, dimensionsEcran[1]/17, (dimensionsEcran[0]*0.085, dimensionsEcran[1]*0.02), image6, (dimensionsEcran[0]*0.02, dimensionsEcran[1]*0.06))
    bouton7 = Bouton((dimensionsEcran[0]*0.675, dimensionsEcran[1]*0.55), "7 x 7 x 7", (dimensionsEcran[0]*0.25, dimensionsEcran[1]*0.4), 10, COULEUR_BOUTONS, dimensionsEcran[1]/17, (dimensionsEcran[0]*0.085, dimensionsEcran[1]*0.02), image7, (dimensionsEcran[0]*0.02, dimensionsEcran[1]*0.06))
    
    boutonMenu = Bouton((dimensionsEcran[0]*0.85, dimensionsEcran[1]*0.02), "Menu", (dimensionsEcran[0]*0.08, dimensionsEcran[1]*0.052), 4, COULEUR_BOUTONS, dimensionsEcran[1]/17, (dimensionsEcran[0]*0.01, dimensionsEcran[1]*0.009))
    boutonQuitter = Bouton((dimensionsEcran[0]*0.95, dimensionsEcran[1]*0.02), "x", (dimensionsEcran[0]*0.033, dimensionsEcran[1]*0.052), 4, ROUGE, dimensionsEcran[1]/15, (dimensionsEcran[0]*0.0097, dimensionsEcran[1]*0.003))
    listeBoutons = [bouton2, bouton3, bouton4, bouton5, bouton6, bouton7, boutonMenu, boutonQuitter]
    
    fenetreSuivante = PIVOTS
    while fenetreSuivante == PIVOTS:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fenetreSuivante = QUITTER
            
            if event.type == pygame.MOUSEBUTTONUP:
                positionSouris = pygame.mouse.get_pos()
                for bouton in listeBoutons:
                    bouton.appuye = False
                    if bouton.zoneCollision.collidepoint(positionSouris):
                        fenetreSuivante = [CUBE_2, CUBE_3, CUBE_4, CUBE_5, CUBE_6, CUBE_7, MENU, QUITTER][listeBoutons.index(bouton)]
        
        clicGaucheMaintenu = pygame.mouse.get_pressed(num_buttons=3)[0]
        if clicGaucheMaintenu:
            positionSouris = pygame.mouse.get_pos()
            for bouton in listeBoutons:
                bouton.appuye = False
                if bouton.zoneCollision.collidepoint(positionSouris):
                    bouton.appuye = True
        
        # Affichage de la fenêtre :
        screen.fill(couleurFondEcran)
        for bouton in listeBoutons:
            bouton.afficher(screen)
        pygame.display.update()
        pygame.time.wait(100)
        
    return fenetreSuivante


def menuPivots(screen, dimensionsEcran:tuple, couleurFondEcran:tuple=(205, 214, 215)):
    image2x3 = pygame.transform.scale(IMAGE_PIVOT_2x3, (dimensionsEcran[0]*0.245, dimensionsEcran[1]*0.26))
    image3x3 = pygame.transform.scale(IMAGE_PIVOT_3x3, (dimensionsEcran[0]*0.24, dimensionsEcran[1]*0.32))
    image3x4 = pygame.transform.scale(IMAGE_PIVOT_3x4, (dimensionsEcran[0]*0.245, dimensionsEcran[1]*0.35))
    
    bouton2x3 = Bouton((dimensionsEcran[0]*0.075, dimensionsEcran[1]*0.4), "INP p12", (dimensionsEcran[0]*0.25, dimensionsEcran[1]*0.4), 10, COULEUR_BOUTONS, dimensionsEcran[1]/17, (dimensionsEcran[0]*0.085, dimensionsEcran[1]*0.02), image2x3, (dimensionsEcran[0]*0.003, dimensionsEcran[1]*0.09))
    bouton3x3 = Bouton((dimensionsEcran[0]*0.375, dimensionsEcran[1]*0.4), "3 x 3", (dimensionsEcran[0]*0.25, dimensionsEcran[1]*0.4), 10, COULEUR_BOUTONS, dimensionsEcran[1]/17, (dimensionsEcran[0]*0.1, dimensionsEcran[1]*0.018), image3x3, (dimensionsEcran[0]*0.005, dimensionsEcran[1]*0.06))
    bouton3x4 = Bouton((dimensionsEcran[0]*0.675, dimensionsEcran[1]*0.4), "3 x 4", (dimensionsEcran[0]*0.25, dimensionsEcran[1]*0.4), 10, COULEUR_BOUTONS, dimensionsEcran[1]/17, (dimensionsEcran[0]*0.1, dimensionsEcran[1]*0.012), image3x4, (dimensionsEcran[0]*0.0025, dimensionsEcran[1]*0.047))
    
    boutonMenu = Bouton((dimensionsEcran[0]*0.85, dimensionsEcran[1]*0.02), "Menu", (dimensionsEcran[0]*0.08, dimensionsEcran[1]*0.052), 4, COULEUR_BOUTONS, dimensionsEcran[1]/17, (dimensionsEcran[0]*0.01, dimensionsEcran[1]*0.009))
    boutonQuitter = Bouton((dimensionsEcran[0]*0.95, dimensionsEcran[1]*0.02), "x", (dimensionsEcran[0]*0.033, dimensionsEcran[1]*0.052), 4, ROUGE, dimensionsEcran[1]/15, (dimensionsEcran[0]*0.0097, dimensionsEcran[1]*0.003))
    listeBoutons = [bouton2x3, bouton3x3, bouton3x4, boutonMenu, boutonQuitter]
    
    fenetreSuivante = PIVOTS
    while fenetreSuivante == PIVOTS:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fenetreSuivante = QUITTER
            
            if event.type == pygame.MOUSEBUTTONUP:
                positionSouris = pygame.mouse.get_pos()
                for bouton in listeBoutons:
                    bouton.appuye = False
                    if bouton.zoneCollision.collidepoint(positionSouris):
                        fenetreSuivante = [PIVOT_2X3, PIVOT_3X3, PIVOT_3X4, MENU, QUITTER][listeBoutons.index(bouton)]
        
        clicGaucheMaintenu = pygame.mouse.get_pressed(num_buttons=3)[0]
        if clicGaucheMaintenu:
            positionSouris = pygame.mouse.get_pos()
            for bouton in listeBoutons:
                bouton.appuye = False
                if bouton.zoneCollision.collidepoint(positionSouris):
                    bouton.appuye = True
        
        # Affichage de la fenêtre :
        screen.fill(couleurFondEcran)
        for bouton in listeBoutons:
            bouton.afficher(screen)
        pygame.display.update()
        pygame.time.wait(100)
        
    return fenetreSuivante