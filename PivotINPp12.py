import pygame
import math
import copy


ORIGINE_GRILLE = (165,140)
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



class Bouton:
    def __init__(self, position:tuple, texte:str, taille:tuple, couleur:tuple, taillePolice=35, positionTexte=(11.5, 3)):
        self.position = position # (x, y)
        self.taille = taille # (largeur, hauteur)
        self.texte = texte
        self.taillePolice = taillePolice
        self.positionTexte = positionTexte # (deltaX, deltaY) par rapport au coin supérieur gauche
        self.couleur = couleur
        
        self.zoneCollision = pygame.Rect(self.position[0], self.position[1], self.taille[0], self.taille[1])
        self.bouclesAppuiRestantes = 0
        
    def afficher(self, screen) -> None:
        decalage = (0,0)
        if self.bouclesAppuiRestantes > 0:
            decalage = (2,3) # pour faire comme si le bouton s'appuyait vers son ombre
            self.bouclesAppuiRestantes -= 1
        pygame.draw.rect(screen, (40,40,40), pygame.Rect(self.position[0]+2, self.position[1]+3, self.taille[0], self.taille [1]), 0, 3) # ombre
        pygame.draw.rect(screen, self.couleur, pygame.Rect(self.position[0]+decalage[0], self.position[1]+decalage[1], self.taille[0], self.taille[1]), 0, 3) # remplissage coloré
        pygame.draw.rect(screen, (0,0,0), pygame.Rect(self.position[0]+decalage[0], self.position[1]+decalage[1], self.taille[0], self.taille[1]), 2, 3) # bordure
        texte = pygame.font.Font(None, int(self.taillePolice)).render(self.texte, 1, (0,0,0))
        screen.blit(texte, (self.position[0] + self.positionTexte[0] + decalage[0], self.position[1] + self.positionTexte[1] + decalage[1]))


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
    def __init__(self, origine:tuple):
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
    
    def tourner(self) -> bool: # True si la rotation est terminée
        if self.angleArrivee != self.angleRotation and abs(self.angleArrivee - self.angleRotation) > 0.1:
            signe = (self.angleArrivee-self.angleRotation)/abs(self.angleArrivee-self.angleRotation)
            self.angleRotation += signe*0.1*0.25*2*3.14159
            return False
        else:
            self.angleRotation = self.angleArrivee
            return True


class Grille:
    def __init__(self, configPivot:list):
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
        
    def configActuelle(self) -> list:
        configuration = []
        for ligne in range(len(self.pieces)):
            configuration.append([])
            for colonne in range(len(self.pieces[0])):
                configuration[ligne].append(self.pieces[ligne][colonne].texte)
        return configuration
    
    def determinerConfigDistanceMinimale(self, listeOuverte:list) -> tuple:
        proprietesConfigDistMini = listeOuverte[0]
        for proprietesConfigEtudiee in listeOuverte[1:]: # (config, distance, parent)
            if proprietesConfigEtudiee[1] < proprietesConfigDistMini[1]:
                proprietesConfigDistMini = proprietesConfigEtudiee
        return proprietesConfigDistMini            
    
    def disposerPieces(self, configurationDonnee:list) -> None:
        for ligne in range(len(configurationDonnee)):
            for colonne in range(len(configurationDonnee[0])):
                for l in range(len(self.pieces)):
                    for c in range(len(self.pieces[0])):
                        if self.pieces[l][c].texte == configurationDonnee[ligne][colonne]:
                            configurationDonnee[ligne][colonne] = self.pieces[l][c]
        self.pieces = configurationDonnee
    
    def rechercherIndiceConfiguration(self, configCherchee:list, liste:list) -> int:
        position = -1
        for indice in range(len(liste)):
            if liste[indice][0] == configCherchee:
                return indice
        return position
    
    def etablirSequenceRotations(self, proprietesConfig:list, listeFermee:list) -> list:
        sequenceRotations = []
        while proprietesConfig[2] is not None: # la config a un parent, ce n'est pas l'état de départ de la recherche
            sequenceRotations = [proprietesConfig[3]] + sequenceRotations
            index = self.rechercherIndiceConfiguration(proprietesConfig[2], listeFermee)
            proprietesConfig = listeFermee[index]
        return sequenceRotations
        
    def aEtoile(self) -> list:
        listeOuverte = [(self.configActuelle(), 0, None, -1)] # configurations à étudier
        listeFermee = [] # configurations déjà étudiées
        solutionTrouvee = False
        
        while not solutionTrouvee and len(listeOuverte) > 0:
            proprietesConfigEtudiee = self.determinerConfigDistanceMinimale(listeOuverte)
            listeOuverte.remove(proprietesConfigEtudiee)
            listeFermee.append(proprietesConfigEtudiee)
            
            if proprietesConfigEtudiee[0] == [[' I', 'N', 'P'], ['p', '1', '2']]:
                solutionTrouvee = True
            
            self.disposerPieces(proprietesConfigEtudiee[0])
            self.pivoter1(SENS_HORAIRE)
            rotation1Horaire = self.configActuelle()
            
            self.disposerPieces(proprietesConfigEtudiee[0])
            self.pivoter1(SENS_ANTIHORAIRE)
            rotation1Antihoraire = self.configActuelle()
            
            self.disposerPieces(proprietesConfigEtudiee[0])
            self.pivoter2(SENS_HORAIRE)
            rotation2Horaire = self.configActuelle()
            
            self.disposerPieces(proprietesConfigEtudiee[0])
            self.pivoter2(SENS_ANTIHORAIRE)
            rotation2Antihoraire = self.configActuelle()
            
            listeRotations = [rotation1Horaire, rotation1Antihoraire, rotation2Horaire, rotation2Antihoraire]
            for configSuivante in listeRotations:
                proprietesConfigSuivante = (configSuivante, proprietesConfigEtudiee[1] +1, proprietesConfigEtudiee[0], listeRotations.index(configSuivante)) # (config, distance, configParent, rotationEffectuee)
                if self.rechercherIndiceConfiguration(configSuivante, listeFermee) == -1: # la configuration n'a pas encore été étudiée
                    index = self.rechercherIndiceConfiguration(configSuivante, listeOuverte)
                    if index == -1: # la config n'est pas dans la liste Ouverte
                        listeOuverte.append(proprietesConfigSuivante)
                    else: # la config est déjà dans la liste Ouverte
                        if proprietesConfigSuivante[1] < listeOuverte[index][1]: # le nombre de rotations pour atteindre la config est plus petit que pour la config déjà enregistrée
                            listeOuverte[index] = proprietesConfigSuivante # on remplace les anciennes propriétés
        
        if solutionTrouvee:
            rotationsAEffectuer = self.etablirSequenceRotations(proprietesConfigEtudiee, listeFermee)
            self.disposerPieces(listeFermee[0][0])
            for ligne in range(len(self.pieces)):
                for colonne in range(len(self.pieces[0])):
                    self.pieces[ligne][colonne].positionArrivee = self.pieces[ligne][colonne].position
            self.roulette1.angleArrivee = self.roulette1.angleRotation
            self.roulette2.angleArrivee = self.roulette2.angleRotation
            return rotationsAEffectuer
        

pygame.init()
screen = pygame.display.set_mode([850, 650]) # taille fenêtre  
pygame.display.set_caption("Pivot INP P12")

grille = Grille([[' I', 'N', 'P'], ['p', '1', '2']])
boutonSolveur = Bouton((368, 550), "Résoudre", (110, 30), (40, 170, 60), 30, (10, 6))

anciennePositionSouris = None
solution = []

fenetreOuverte = True
while fenetreOuverte:
    positionSouris = pygame.mouse.get_pos()
    
    if not grille.mouvementEnCours and solution != []:
        if solution[0] == 0:
            grille.pivoter1(SENS_HORAIRE)
        elif solution[0] == 1:
            grille.pivoter1(SENS_ANTIHORAIRE)
        elif solution[0] == 2:
            grille.pivoter2(SENS_HORAIRE)
        else: # solution[0] == 3:
            grille.pivoter2(SENS_ANTIHORAIRE)
        solution = solution[1:]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            fenetreOuverte = False
    
        if event.type == pygame.MOUSEBUTTONDOWN:
            grille.rouletteSelectionnee = None
            anciennePositionSouris = None
            grille.roulette1.estCliquee = False
            grille.roulette2.estCliquee = False
            for zoneCollision in [grille.roulette1.zoneCollision, grille.roulette2.zoneCollision]:
                if zoneCollision.collidepoint(positionSouris):
                    grille.rouletteSelectionnee = [grille.roulette1.zoneCollision, grille.roulette2.zoneCollision].index(zoneCollision)
                    [grille.roulette1, grille.roulette2][grille.rouletteSelectionnee].estCliquee = True
                    anciennePositionSouris = positionSouris
            if boutonSolveur.zoneCollision.collidepoint(positionSouris):
                boutonSolveur.bouclesAppuiRestantes = 3
                screen.fill(COULEUR_FOND)
                grille.dessiner(screen)
                boutonSolveur.afficher(screen)
                pygame.display.update()
                solution = grille.aEtoile()
        
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
            elif event.key == pygame.K_UP and grille.rouletteSelectionnee is not None and not grille.mouvementEnCours:
                if grille.rouletteSelectionnee == 0:
                    grille.pivoter1(SENS_HORAIRE)
                else:
                    grille.pivoter2(SENS_ANTIHORAIRE)
            elif event.key == pygame.K_DOWN and grille.rouletteSelectionnee is not None and not grille.mouvementEnCours:
                if grille.rouletteSelectionnee == 0:
                    grille.pivoter1(SENS_ANTIHORAIRE)
                else:
                    grille.pivoter2(SENS_HORAIRE)
            elif event.key == pygame.K_r:
                boutonSolveur.bouclesAppuiRestantes = 3
                screen.fill(COULEUR_FOND)
                grille.dessiner(screen)
                boutonSolveur.afficher(screen)
                pygame.display.update()
                solution = grille.aEtoile()
        
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
    boutonSolveur.afficher(screen)
    pygame.display.update()
    pygame.time.wait(50)
    
pygame.quit()