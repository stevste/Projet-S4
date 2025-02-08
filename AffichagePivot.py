import pygame
import math


ORIGINE_GRILLE = (160,150)
COTE_CASES = 170
NOMBRE_RAYONS_ROULETTES = 8

COULEUR_FOND = (220,220,190)
COULEUR_DOS_GRILLE = (135,105,75)
COULEUR_BORDURE_GRILLE = (45,35,25)
COULEUR_PIECES = (180,140,100)
COULEUR_BORD_PIECES = (90,70,50)
COULEUR_ROULETTES = (170,140,120)

SENS_HORAIRE = -1
SENS_ANTIHORAIRE = 1



class Piece:
    def __init__(self, position:tuple, couleur:tuple, texte:str):
        self.position = position # [x,y] en pixels
        self.positionArrivee = position
        self.couleur = couleur
        self.texte = texte
    
    def dessiner(self, screen) -> None:
        pygame.draw.rect(screen, self.couleur, pygame.Rect(self.position[0], self.position[1], COTE_CASES, COTE_CASES), 0, int(0.3*COTE_CASES))
        pygame.draw.rect(screen, COULEUR_BORD_PIECES, pygame.Rect(self.position[0], self.position[1], COTE_CASES, COTE_CASES), 3, int(0.3*COTE_CASES))
        texte = pygame.font.Font(None, int(COTE_CASES)).render(self.texte, 1, COULEUR_BORDURE_GRILLE)
        screen.blit(texte, (self.position[0] + 42, self.position[1] + 30))
    
    def deplacer(self) -> bool: # True si le déplacement est terminé
        if self.position != self.positionArrivee:
            if self.position[0] != self.positionArrivee[0]:
                signeDeplacementX = (self.positionArrivee[0]-self.position[0])/abs(self.positionArrivee[0]-self.position[0])
                self.position[0] += 0.1*COTE_CASES*signeDeplacementX
            if self.position[1] != self.positionArrivee[1]:
                signeDeplacementY = (self.positionArrivee[1]-self.position[1])/abs(self.positionArrivee[1]-self.position[1])
                self.position[1] += 0.1*COTE_CASES*signeDeplacementY
            return False # pas encore arrivée à destination
        else:
            return True # arrivée à destination
    

class Roulette:
    def __init__(self, origine):
        self.origine = origine # (x,y) en pixels
        self.zoneCollision = pygame.Rect(self.origine[0]-COTE_CASES, self.origine[1]-COTE_CASES, 2*COTE_CASES, 2*COTE_CASES)
        self.estCliquee = False
        self.angleRotation = 0 # en radians
        self.angleArrivee = 0 # en radians
        
    def dessiner(self, screen) -> None:
        if self.estCliquee:
            couleurReliefs = (250,250,250)
        else:
            couleurReliefs = COULEUR_BORD_PIECES
        pygame.draw.circle(screen, COULEUR_PIECES, self.origine, COTE_CASES)
        pygame.draw.circle(screen, couleurReliefs, self.origine, COTE_CASES, 3)
        
        for numeroRayon in range(NOMBRE_RAYONS_ROULETTES):
            cosinus = math.cos(numeroRayon*2*3.14159/NOMBRE_RAYONS_ROULETTES+self.angleRotation)
            sinus = math.sin(numeroRayon*2*3.14159/NOMBRE_RAYONS_ROULETTES+self.angleRotation)
            pygame.draw.line(screen, couleurReliefs, self.origine, (self.origine[0]+cosinus*0.85*COTE_CASES, self.origine[1]+sinus*0.85*COTE_CASES), 3)
    
    def tourner(self) -> bool: # True si le déplacement est terminé
        if self.angleArrivee != self.angleRotation and abs(self.angleArrivee - self.angleRotation) > 0.1:
            signe = (self.angleArrivee-self.angleRotation)/abs(self.angleArrivee-self.angleRotation)
            self.angleRotation += signe*0.1*0.25*2*3.14159
            return False
        else:
            self.angleRotation = self.angleArrivee
            return True


class Grille:
    def __init__(self, configPivot):
        self.pieces = []
        for ligne in range(len(configPivot)):
            self.pieces.append([])
            for colonne in range(len(configPivot[0])):
                self.pieces[ligne].append(Piece([ORIGINE_GRILLE[0] + colonne*COTE_CASES,ORIGINE_GRILLE[1] + ligne*COTE_CASES], COULEUR_PIECES, configPivot[ligne][colonne]))
                
        self.mouvementEnCours = False
        self.rouletteSelectionnee = None
        
        self.roulette1 = Roulette((ORIGINE_GRILLE[0] + 0.5*COTE_CASES, ORIGINE_GRILLE[1] + COTE_CASES))
        self.roulette1.zoneCollision = pygame.Rect(self.roulette1.origine[0]-COTE_CASES, self.roulette1.origine[1]-COTE_CASES, COTE_CASES, 2*COTE_CASES)
        self.roulette2 = Roulette((ORIGINE_GRILLE[0] + 2.5*COTE_CASES, ORIGINE_GRILLE[1] + COTE_CASES))
        self.roulette2.zoneCollision = pygame.Rect(self.roulette2.origine[0], self.roulette2.origine[1]-COTE_CASES, COTE_CASES, 2*COTE_CASES)

    
    def __repr__(self) -> str:
        texte = ''
        for ligne in range(len(self.pieces)):
            for colonne in range(len(self.pieces[0])):
                texte += self.pieces[ligne][colonne].texte
            texte += '\n'
        return texte
        
    def dessiner(self, screen) -> None:
        self.roulette1.dessiner(screen)
        self.roulette2.dessiner(screen)
        
        pygame.draw.rect(screen, COULEUR_DOS_GRILLE, pygame.Rect(ORIGINE_GRILLE[0]-8, ORIGINE_GRILLE[1]-8, COTE_CASES*len(self.pieces[0])+16, COTE_CASES*len(self.pieces)+16), 0, 3)
        pygame.draw.rect(screen, COULEUR_BORDURE_GRILLE, pygame.Rect(ORIGINE_GRILLE[0]-8, ORIGINE_GRILLE[1]-8, COTE_CASES*len(self.pieces[0])+16, COTE_CASES*len(self.pieces)+16), 8, 3)
        
        for ligne in range(len(self.pieces)):
            for colonne in range(len(self.pieces[0])):
                self.pieces[ligne][colonne].dessiner(screen)
    
    def deplacerPieces(self) -> None:
        self.mouvementEnCours = False
        for ligne in range(len(self.pieces)):
            for colonne in range(len(self.pieces[0])):
                if not self.pieces[ligne][colonne].deplacer(): # si l'une des pièces n'a pas fini de se déplacer
                    self.mouvementEnCours = True
        if not self.roulette1.tourner() or not self.roulette2.tourner():
            self.mouvementEnCours = True
            
    def pivoter1(self, sens:int=SENS_HORAIRE) -> None:
        self.mouvementEnCours = True
        if sens == SENS_HORAIRE:
            self.roulette1.angleArrivee = self.roulette1.angleRotation + 3.14159/2
            self.pieces = [[self.pieces[1][0], self.pieces[0][0], self.pieces[0][2]], [self.pieces[1][1], self.pieces[0][1], self.pieces[1][2]]]
        else:
            self.roulette1.angleArrivee = self.roulette1.angleRotation - 3.14159/2
            self.pieces = [[self.pieces[0][1], self.pieces[1][1], self.pieces[0][2]], [self.pieces[0][0], self.pieces[1][0], self.pieces[1][2]]]
    
        for ligne in range(len(self.pieces)):
            for colonne in range(len(self.pieces[0])):
                self.pieces[ligne][colonne].positionArrivee = [ORIGINE_GRILLE[0] + colonne*COTE_CASES, ORIGINE_GRILLE[1] + ligne*COTE_CASES]
        
    def pivoter2(self, sens:int=SENS_HORAIRE) -> None:
        self.mouvementEnCours = True
        if sens == SENS_HORAIRE:
            self.roulette2.angleArrivee = self.roulette2.angleRotation + 3.14159/2
            self.pieces = [[self.pieces[0][0], self.pieces[1][1], self.pieces[0][1]], [self.pieces[1][0], self.pieces[1][2], self.pieces[0][2]]]
        else:
            self.roulette2.angleArrivee = self.roulette2.angleRotation - 3.14159/2
            self.pieces = [[self.pieces[0][0], self.pieces[0][2], self.pieces[1][2]], [self.pieces[1][0], self.pieces[0][1], self.pieces[1][1]]]
    
        for ligne in range(len(self.pieces)):
            for colonne in range(len(self.pieces[0])):
                self.pieces[ligne][colonne].positionArrivee = [ORIGINE_GRILLE[0] + colonne*COTE_CASES, ORIGINE_GRILLE[1] + ligne*COTE_CASES]
        
        

pygame.init()
screen = pygame.display.set_mode([850, 650]) # taille fenêtre  
pygame.display.set_caption("Pivot INP P12")

grille = Grille([[' I', 'N', 'P'], ['p', '1', '2']])

anciennePositionSouris = None

fenetreOuverte = True
while fenetreOuverte:
    positionSouris = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            fenetreOuverte = False
    
        if event.type == pygame.MOUSEBUTTONDOWN:
            grille.rouletteSelectionnee = None
            anciennePositionSouris = None
            for zoneCollision in [grille.roulette1.zoneCollision, grille.roulette2.zoneCollision]:
                if zoneCollision.collidepoint(positionSouris[0], positionSouris[1]):
                    grille.rouletteSelectionnee = [grille.roulette1.zoneCollision, grille.roulette2.zoneCollision].index(zoneCollision)
                    [grille.roulette1, grille.roulette2][grille.rouletteSelectionnee].estCliquee = True
                    anciennePositionSouris = positionSouris
        
        if event.type == pygame.MOUSEBUTTONUP:
            if grille.rouletteSelectionnee is not None:
                [grille.roulette1, grille.roulette2][grille.rouletteSelectionnee].estCliquee = False
                grille.rouletteSelectionnee = None
            anciennePositionSouris = None
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                grille.rouletteSelectionnee = 0
                grille.roulette1.estCliquee = True
                grille.roulette2.estCliquee = False
            elif event.key == pygame.K_RIGHT:
                grille.rouletteSelectionnee = 1
                grille.roulette2.estCliquee = True
                grille.roulette1.estCliquee = False
            elif event.key == pygame.K_UP and grille.rouletteSelectionnee is not None:
                if grille.rouletteSelectionnee == 0:
                    grille.pivoter1(SENS_HORAIRE)
                else:
                    grille.pivoter2(SENS_ANTIHORAIRE)
            elif event.key == pygame.K_DOWN and grille.rouletteSelectionnee is not None:
                if grille.rouletteSelectionnee == 0:
                    grille.pivoter1(SENS_ANTIHORAIRE)
                else:
                    grille.pivoter2(SENS_HORAIRE)
        
    clicMaintenu = pygame.mouse.get_pressed(num_buttons=3)[0] # clic gauche
    if clicMaintenu and not grille.mouvementEnCours and grille.rouletteSelectionnee is not None and abs(anciennePositionSouris[1]-positionSouris[1]) > 0.2*COTE_CASES:
        if anciennePositionSouris[1] > positionSouris[1]: # la souris monte
            if grille.rouletteSelectionnee == 0:
                grille.pivoter1(SENS_HORAIRE)
            else:
                grille.pivoter2(SENS_ANTIHORAIRE)
        elif anciennePositionSouris[1] < positionSouris[1]: # la souris descend
            if grille.rouletteSelectionnee == 0:
                grille.pivoter1(SENS_ANTIHORAIRE)
            else:
                grille.pivoter2(SENS_HORAIRE)
        anciennePositionSouris = positionSouris
    if grille.mouvementEnCours:
        grille.deplacerPieces()
    
    screen.fill(COULEUR_FOND)
    grille.dessiner(screen)
    pygame.display.update()
    pygame.time.wait(50)
    
pygame.quit()