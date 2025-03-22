import pygame
import math
import copy


COTE_CASES = 150
NOMBRE_RAYONS_ROULETTES = 8

COULEUR_FOND = (220,220,190)
COULEUR_DOS_GRILLE = (135,105,75)
COULEUR_BORDURE_GRILLE = (45,35,25)
COULEUR_PIECES = (180,140,100)
COULEUR_BORD_PIECES = (90,70,50)
COULEUR_ROULETTES = (170,140,120)

SENS_HORAIRE = -1
SENS_ANTIHORAIRE = 1

IMAGE = pygame.transform.scale(pygame.image.load("imageMulticolore.jpg"), (3*COTE_CASES, 3*COTE_CASES))



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
    def __init__(self, position:tuple, couleur:tuple, valeur:int, portionImage:tuple):
        self.position = position # [x,y] en pixels
        self.positionArrivee = position
        self.couleur = couleur
        self.valeur = valeur
        self.texte = str(self.valeur)
        self.portionImage = portionImage # (x,y) : point à partir duquel la pièce découpe un carré de l'image fournie pour ensuite l'afficher
    
    def dessiner(self, screen) -> None:
        '''screen.blit(IMAGE, self.position, (self.portionImage[0], self.portionImage[1], COTE_CASES, COTE_CASES))
        pygame.draw.rect(screen, COULEUR_BORD_PIECES, pygame.Rect(self.position[0], self.position[1], COTE_CASES, COTE_CASES), 2)'''
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
    def __init__(self, origine:tuple, rayon:int):
        self.origine = origine # (x,y) en pixels
        self.rayon = rayon # COTE_CASES*0.78
        self.zoneCollision = pygame.Rect(self.origine[0]-self.rayon, self.origine[1]-self.rayon, 2*self.rayon, 2*self.rayon)
        self.estCliquee = False
        self.angleRotation = 0 # en radians
        self.angleArrivee = 0 # en radians
        
    def dessiner(self, screen) -> None:
        if self.estCliquee:
            couleurReliefs = (250,250,250)
        else:
            couleurReliefs = COULEUR_BORD_PIECES
        pygame.draw.circle(screen, COULEUR_PIECES, self.origine, self.rayon)
        pygame.draw.circle(screen, couleurReliefs, self.origine, self.rayon, 3)
        
        for numeroRayon in range(NOMBRE_RAYONS_ROULETTES):
            cosinus = math.cos(numeroRayon*2*3.14159/NOMBRE_RAYONS_ROULETTES+self.angleRotation)
            sinus = math.sin(numeroRayon*2*3.14159/NOMBRE_RAYONS_ROULETTES+self.angleRotation)
            pygame.draw.line(screen, couleurReliefs, self.origine, (self.origine[0]+cosinus*0.85*self.rayon, self.origine[1]+sinus*0.85*self.rayon), 3)
    
    def tourner(self) -> bool: # True si la rotation est terminée
        if self.angleArrivee != self.angleRotation and abs(self.angleArrivee - self.angleRotation) > 0.1:
            signe = (self.angleArrivee-self.angleRotation)/abs(self.angleArrivee-self.angleRotation)
            self.angleRotation += signe*0.1*0.25*2*3.14159
            return False
        else:
            self.angleRotation = self.angleArrivee
            return True


class Grille:
    def __init__(self, tailleFenetre:tuple, nombreLignes:int=3, nombreColonnes:int=3):
        self.origine = ((tailleFenetre[0] - COTE_CASES*nombreColonnes)/2, (tailleFenetre[1] - COTE_CASES*nombreLignes)/2)
        
        self.configInitiale = []
        self.pieces = []
        chiffre = 1
        for ligne in range(nombreLignes):
            self.pieces.append([])
            self.configInitiale.append([])
            for colonne in range(nombreColonnes):
                self.pieces[ligne].append(Piece([self.origine[0] + colonne*COTE_CASES,self.origine[1] + ligne*COTE_CASES], COULEUR_PIECES, chiffre, (colonne*COTE_CASES, ligne*COTE_CASES)))
                self.configInitiale[ligne].append(chiffre)
                chiffre += 1
        
        rayonRoulettesGaucheDroite = COTE_CASES*nombreLignes/(nombreLignes-1)/2
        if nombreColonnes > 3:
            rayonRoulettesHautBas = COTE_CASES*(nombreColonnes-2)/(nombreColonnes-3)/2
        self.roulettes = []
        for ligne in range(1, nombreLignes):
            self.roulettes.append([])
            for colonne in range(1, nombreColonnes):
                if colonne == 1: # à gauche de la grille
                    rayon = rayonRoulettesGaucheDroite
                    x = self.origine[0] + (colonne-0.8)*COTE_CASES
                    y = self.origine[1] + 2*rayon*ligne - rayon
                    zoneCollision = pygame.Rect(x - rayon, y - rayon, rayon - COTE_CASES*0.2, 2*rayon)
                elif colonne == nombreColonnes -1: # à droite de la grille
                    rayon = rayonRoulettesGaucheDroite
                    x = self.origine[0] + (colonne+0.8)*COTE_CASES
                    y = self.origine[1] + 2*rayon*ligne - rayon
                    zoneCollision = pygame.Rect(x + COTE_CASES*0.2, y - rayon, rayon - COTE_CASES*0.2, 2*rayon)
                elif ligne == 1: # au-dessus de la grille
                    rayon = rayonRoulettesHautBas
                    x = self.origine[0] + 2*rayon*(colonne-1) - rayon + COTE_CASES
                    y = self.origine[1] + (ligne-0.5)*COTE_CASES
                    zoneCollision = pygame.Rect(x - rayon, y - rayon, 2*rayon, rayon - COTE_CASES*0.5)
                elif ligne == nombreLignes -1: # en dessous de la grille
                    rayon = rayonRoulettesHautBas
                    x = self.origine[0] + 2*rayon*(colonne-1) - rayon + COTE_CASES
                    y = self.origine[1] + (ligne+0.5)*COTE_CASES
                    zoneCollision = pygame.Rect(x - rayon, y + COTE_CASES*0.5, 2*rayon, rayon - COTE_CASES*0.5)
                else:
                    print("ATTENTION : les cases du milieu n'ont pas de moyen d'être pivotées")
                self.roulettes[ligne-1].append(Roulette((x, y), rayon))
                self.roulettes[ligne-1][colonne-1].zoneCollision = zoneCollision
        
        self.mouvementEnCours = False
        self.rouletteSelectionnee = None
    
    def __repr__(self) -> str:
        texte = ''
        for ligne in range(len(self.pieces)):
            for colonne in range(len(self.pieces[0])):
                texte += self.pieces[ligne][colonne].texte
            texte += '\n'
        return texte
        
    def dessiner(self, screen) -> None:
        for ligne in range(len(self.roulettes)):
            for roulette in self.roulettes[ligne]:
                roulette.dessiner(screen)
        
        pygame.draw.rect(screen, COULEUR_DOS_GRILLE, pygame.Rect(self.origine[0]-8, self.origine[1]-8, COTE_CASES*len(self.pieces[0])+16, COTE_CASES*len(self.pieces)+16), 0, 3)
        pygame.draw.rect(screen, COULEUR_BORDURE_GRILLE, pygame.Rect(self.origine[0]-8, self.origine[1]-8, COTE_CASES*len(self.pieces[0])+16, COTE_CASES*len(self.pieces)+16), 8, 3)
        
        for ligne in range(len(self.pieces)):
            for colonne in range(len(self.pieces[0])):
                self.pieces[ligne][colonne].dessiner(screen)
    
    def deplacerPieces(self) -> None:
        self.mouvementEnCours = False
        for ligne in range(len(self.pieces)):
            for colonne in range(len(self.pieces[0])):
                if not self.pieces[ligne][colonne].deplacer(): # si l'une des pièces n'a pas fini de se déplacer
                    self.mouvementEnCours = True
        
        for ligne in range(len(self.roulettes)):
            for colonne in range(len(self.roulettes[0])):
                if not self.roulettes[ligne][colonne].tourner(): # si l'une des roulettes n'a pas fini de se déplacer
                    self.mouvementEnCours = True
    
    def pivoter(self, ligneRoulette:int, colonneRoulette:int, sens:int=SENS_HORAIRE) -> None:
        self.mouvementEnCours = True
        if sens == SENS_HORAIRE:
            self.roulettes[ligneRoulette][colonneRoulette].angleArrivee = self.roulettes[ligneRoulette][colonneRoulette].angleRotation + 3.14159/2
            pieceEnHautAGauche = self.pieces[ligneRoulette][colonneRoulette]
            self.pieces[ligneRoulette][colonneRoulette] = self.pieces[ligneRoulette+1][colonneRoulette]
            self.pieces[ligneRoulette+1][colonneRoulette] = self.pieces[ligneRoulette+1][colonneRoulette+1]
            self.pieces[ligneRoulette+1][colonneRoulette+1] = self.pieces[ligneRoulette][colonneRoulette+1]
            self.pieces[ligneRoulette][colonneRoulette+1] = pieceEnHautAGauche
        else:
            self.roulettes[ligneRoulette][colonneRoulette].angleArrivee = self.roulettes[ligneRoulette][colonneRoulette].angleRotation - 3.14159/2
            pieceEnHautAGauche = self.pieces[ligneRoulette][colonneRoulette]
            self.pieces[ligneRoulette][colonneRoulette] = self.pieces[ligneRoulette][colonneRoulette+1]
            self.pieces[ligneRoulette][colonneRoulette+1] = self.pieces[ligneRoulette+1][colonneRoulette+1]
            self.pieces[ligneRoulette+1][colonneRoulette+1] = self.pieces[ligneRoulette+1][colonneRoulette]
            self.pieces[ligneRoulette+1][colonneRoulette] = pieceEnHautAGauche
    
        for ligne in range(len(self.pieces)):
            for colonne in range(len(self.pieces[0])):
                self.pieces[ligne][colonne].positionArrivee = [self.origine[0] + colonne*COTE_CASES, self.origine[1] + ligne*COTE_CASES]

    def configActuelle(self) -> list:
        configuration = []
        for ligne in range(len(self.pieces)):
            configuration.append([])
            for colonne in range(len(self.pieces[0])):
                configuration[ligne].append(self.pieces[ligne][colonne].valeur)
        return configuration
    
    def determinerMeilleureConfig(self, listeOuverte:list) -> tuple:
        proprietesConfigDistMini = listeOuverte[0]
        for proprietesConfigEtudiee in listeOuverte[1:]: # (config, distance, parent)
            if proprietesConfigEtudiee[1][0] < proprietesConfigDistMini[1][0]:
                proprietesConfigDistMini = proprietesConfigEtudiee
        return proprietesConfigDistMini
    
    def disposerPieces(self, configurationDonnee:list) -> None:
        config = copy.deepcopy(configurationDonnee)
        for ligne in range(len(config)):
            for colonne in range(len(config[0])):
                for l in range(len(self.pieces)):
                    for c in range(len(self.pieces[0])):
                        if self.pieces[l][c].valeur == config[ligne][colonne]:
                            config[ligne][colonne] = self.pieces[l][c]
        self.pieces = config
    
    def estimerNombreCoupsRestantAJouer(self, configuration:list, solutionCherchee:list):
        sommeDistances = 0
        for ligne in range(len(solutionCherchee)):
            for colonne in range(len(solutionCherchee[0])):
                for l in range(len(configuration)):
                    for c in range(len(configuration[0])):
                        if solutionCherchee[ligne][colonne] == configuration[l][c]:
                            sommeDistances += abs(ligne-l) + abs(colonne-c)
        return sommeDistances
        
    def proprietes(self, configuration:list, distance:int, solutionCherchee:list):
        valeurHeuristique = self.estimerNombreCoupsRestantAJouer(configuration, solutionCherchee)
        return (valeurHeuristique + distance, distance, valeurHeuristique)
    
    def rechercherIndiceConfiguration(self, configCherchee:list, liste:list) -> int:
        for indice in range(len(liste)):
            if liste[indice][0] == configCherchee:
                return indice
        return -1
    
    def etablirSequenceRotations(self, proprietesConfig:list, listeFermee:list) -> list:
        sequenceRotations = []
        while proprietesConfig[2] is not None: # la config a un parent, ce n'est pas l'état de départ de la recherche
            sequenceRotations = [(proprietesConfig[3], proprietesConfig[4])] + sequenceRotations
            index = self.rechercherIndiceConfiguration(proprietesConfig[2], listeFermee)
            proprietesConfig = listeFermee[index]
        return sequenceRotations
        
    def aEtoile(self, solutionCherchee:list) -> list:
        configDepart = self.configActuelle()
        listeOuverte = [(configDepart, self.proprietes(configDepart, 0, solutionCherchee), None, -1)] # configurations à étudier
        listeFermee = [] # configurations déjà étudiées
        solutionTrouvee = False
        
        while not solutionTrouvee and len(listeOuverte) > 0:
            proprietesConfigEtudiee = self.determinerMeilleureConfig(listeOuverte)
            listeOuverte.remove(proprietesConfigEtudiee)
            listeFermee.append(proprietesConfigEtudiee)
            
            if proprietesConfigEtudiee[0] == solutionCherchee:
                solutionTrouvee = True
            
            listeRotations = []
            for ligne in range(len(self.roulettes)):
                for colonne in range(len(self.roulettes[0])):
                    self.disposerPieces(proprietesConfigEtudiee[0])
                    self.pivoter(ligne, colonne, SENS_HORAIRE)
                    configuration = self.configActuelle()
                    listeRotations.append((configuration, (ligne, colonne), SENS_HORAIRE))
                    
                    self.disposerPieces(proprietesConfigEtudiee[0])
                    self.pivoter(ligne, colonne, SENS_ANTIHORAIRE)
                    configuration = self.configActuelle()
                    listeRotations.append((configuration, (ligne, colonne), SENS_ANTIHORAIRE))
            
            for configSuivante in listeRotations:
                configuration = configSuivante[0]
                proprietesConfigSuivante = (configuration, self.proprietes(configuration, proprietesConfigEtudiee[1][1] +1, solutionCherchee), proprietesConfigEtudiee[0], configSuivante[1], configSuivante[2]) # (config, propriétés, configParent, pivotTourné, sensRotation)
                if self.rechercherIndiceConfiguration(configuration, listeFermee) == -1: # la configuration n'a pas encore été étudiée
                    index = self.rechercherIndiceConfiguration(configuration, listeOuverte)
                    if index == -1: # la config n'est pas dans la liste Ouverte
                        listeOuverte.append(proprietesConfigSuivante)
                    else: # la config est déjà dans la liste Ouverte
                        if proprietesConfigSuivante[1][1] < listeOuverte[index][1][1]: # le nombre de rotations pour atteindre la config est plus petit que pour la config déjà enregistrée
                            listeOuverte[index] = proprietesConfigSuivante # on remplace les anciennes propriétés
        
        for ligne in range(len(self.pieces)):
            for colonne in range(len(self.pieces[0])):
                self.pieces[ligne][colonne].positionArrivee = self.pieces[ligne][colonne].position
        
        for ligne in range(len(self.roulettes)):
            for colonne in range(len(self.roulettes[0])):
                self.roulettes[ligne][colonne].angleArrivee = self.roulettes[ligne][colonne].angleRotation
        
        if solutionTrouvee:
            rotationsAEffectuer = self.etablirSequenceRotations(proprietesConfigEtudiee, listeFermee)
            self.disposerPieces(listeFermee[0][0])
            return rotationsAEffectuer
        else:
            return []


pygame.init()
screen = pygame.display.set_mode([850, 650]) # taille fenêtre
pygame.display.set_caption("Pivot INP P12")

grille = Grille((850, 650), 3, 4)
boutonSolveur = Bouton((668, 580), "Résoudre", (110, 30), (40, 170, 60), 30, (10, 6))

anciennePositionSouris = None
solution = []

fenetreOuverte = True
while fenetreOuverte:
    positionSouris = pygame.mouse.get_pos()
    
    if not grille.mouvementEnCours and solution != []:
        grille.pivoter(solution[0][0][0], solution[0][0][1], solution[0][1])
        solution = solution[1:]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            fenetreOuverte = False
    
        if event.type == pygame.MOUSEBUTTONDOWN:
            grille.rouletteSelectionnee = None
            anciennePositionSouris = None
            for ligne in range(len(grille.roulettes)):
                for colonne in range(len(grille.roulettes[0])):
                    grille.roulettes[ligne][colonne].estCliquee = False
                    if grille.roulettes[ligne][colonne].zoneCollision.collidepoint(positionSouris):
                        grille.rouletteSelectionnee = (ligne, colonne)
                        grille.roulettes[ligne][colonne].estCliquee = True
                        anciennePositionSouris = positionSouris
            
            if boutonSolveur.zoneCollision.collidepoint(positionSouris):
                boutonSolveur.bouclesAppuiRestantes = 3
                screen.fill(COULEUR_FOND)
                grille.dessiner(screen)
                boutonSolveur.afficher(screen)
                pygame.display.update()
                solution = grille.aEtoile(grille.configInitiale)
        
        if event.type == pygame.MOUSEBUTTONUP:
            if grille.rouletteSelectionnee is not None:
                grille.roulettes[grille.rouletteSelectionnee[0]][grille.rouletteSelectionnee[1]].estCliquee = False
                grille.rouletteSelectionnee = None
            anciennePositionSouris = None
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                boutonSolveur.bouclesAppuiRestantes = 3
                screen.fill(COULEUR_FOND)
                grille.dessiner(screen)
                boutonSolveur.afficher(screen)
                pygame.display.update()
                solution = grille.aEtoile(grille.configInitiale)
         
    clicMaintenu = pygame.mouse.get_pressed(num_buttons=3)[0] # clic gauche
    if clicMaintenu and not grille.mouvementEnCours and grille.rouletteSelectionnee is not None and (abs(anciennePositionSouris[1]-positionSouris[1]) > 0.2*COTE_CASES or abs(anciennePositionSouris[0]-positionSouris[0]) > 0.2*COTE_CASES):
        if grille.rouletteSelectionnee[1] == 0:
            if anciennePositionSouris[1] > positionSouris[1]: # la souris monte
                grille.pivoter(grille.rouletteSelectionnee[0], grille.rouletteSelectionnee[1], SENS_HORAIRE)
            elif anciennePositionSouris[1] < positionSouris[1]: # la souris descend
                grille.pivoter(grille.rouletteSelectionnee[0], grille.rouletteSelectionnee[1], SENS_ANTIHORAIRE)
        elif grille.rouletteSelectionnee[1] == len(grille.roulettes[0]) -1:
            if anciennePositionSouris[1] > positionSouris[1]: # la souris monte
                grille.pivoter(grille.rouletteSelectionnee[0], grille.rouletteSelectionnee[1], SENS_ANTIHORAIRE)
            elif anciennePositionSouris[1] < positionSouris[1]: # la souris descend
                grille.pivoter(grille.rouletteSelectionnee[0], grille.rouletteSelectionnee[1], SENS_HORAIRE)
            
        elif grille.rouletteSelectionnee[0] == 0:
            if anciennePositionSouris[0] > positionSouris[0]: # la souris va à gauche
                grille.pivoter(grille.rouletteSelectionnee[0], grille.rouletteSelectionnee[1], SENS_ANTIHORAIRE)
            elif anciennePositionSouris[0] < positionSouris[0]: # la souris va à droite
                grille.pivoter(grille.rouletteSelectionnee[0], grille.rouletteSelectionnee[1], SENS_HORAIRE)
        elif grille.rouletteSelectionnee[0] == len(grille.roulettes) -1:
            if anciennePositionSouris[0] > positionSouris[0]: # la souris va à gauche
                grille.pivoter(grille.rouletteSelectionnee[0], grille.rouletteSelectionnee[1], SENS_HORAIRE)
            elif anciennePositionSouris[0] < positionSouris[0]: # la souris va à droite
                grille.pivoter(grille.rouletteSelectionnee[0], grille.rouletteSelectionnee[1], SENS_ANTIHORAIRE)

        anciennePositionSouris = positionSouris
    
    if grille.mouvementEnCours:
        grille.deplacerPieces()
    
    screen.fill(COULEUR_FOND)
    grille.dessiner(screen)
    boutonSolveur.afficher(screen)
    pygame.display.update()
    pygame.time.wait(50)
    
pygame.quit()