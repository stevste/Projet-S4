import pygame
import math
import copy
from Enum import *


#COTE_CASES = 180
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
        self.appuye = False
        
    def afficher(self, screen) -> None:
        decalage = (0,0)
        if self.appuye:
            decalage = (2,3) # pour faire comme si le bouton s'appuyait vers son ombre
        
        pygame.draw.rect(screen, (40,40,40), pygame.Rect(self.position[0]+2, self.position[1]+3, self.taille[0], self.taille [1]), 0, 4) # ombre
        pygame.draw.rect(screen, self.couleur, pygame.Rect(self.position[0]+decalage[0], self.position[1]+decalage[1], self.taille[0], self.taille[1]), 0, 4) # remplissage coloré
        pygame.draw.rect(screen, (0,0,0), pygame.Rect(self.position[0]+decalage[0], self.position[1]+decalage[1], self.taille[0], self.taille[1]), 2, 4) # bordure
        texte = pygame.font.Font(None, int(self.taillePolice)).render(self.texte, 1, (0,0,0))
        screen.blit(texte, (self.position[0] + self.positionTexte[0] + decalage[0], self.position[1] + self.positionTexte[1] + decalage[1]))


class Piece:
    def __init__(self, position:tuple, taille:int, couleur:tuple, valeur:int, image, portionImage:tuple):
        self.position = position # [x,y] en pixels
        self.taille = taille # longueur côté en pixels
        self.positionArrivee = position
        self.couleur = couleur
        self.valeur = valeur
        self.texte = str(self.valeur)
        self.image = image
        self.portionImage = portionImage # (x,y) : point à partir duquel la pièce découpe un carré de l'image fournie pour ensuite l'afficher
    
    def dessiner(self, screen) -> None:
        if self.image is not None:
            screen.blit(self.image, self.position, (self.portionImage[0], self.portionImage[1], self.taille, self.taille))
            pygame.draw.rect(screen, COULEUR_BORD_PIECES, pygame.Rect(self.position[0], self.position[1], self.taille, self.taille), 2)
        else:
            pygame.draw.rect(screen, self.couleur, pygame.Rect(self.position[0], self.position[1], self.taille, self.taille), 0, int(0.3*self.taille))
            pygame.draw.rect(screen, COULEUR_BORD_PIECES, pygame.Rect(self.position[0], self.position[1], self.taille, self.taille), 3, int(0.3*self.taille))
            texte = pygame.font.Font(None, int(self.taille*1.2)).render(self.texte, 1, COULEUR_BORDURE_GRILLE)
            screen.blit(texte, (self.position[0] + 42, self.position[1] + 30))
    
    def deplacer(self) -> bool: # True si le déplacement est terminé
        if abs(self.position[0]-self.positionArrivee[0]) + abs(self.position[1]-self.positionArrivee[1]) > 5:
            if self.position[0] != self.positionArrivee[0]:
                signeDeplacementX = (self.positionArrivee[0]-self.position[0])/abs(self.positionArrivee[0]-self.position[0])
                self.position[0] += 0.1*self.taille*signeDeplacementX
            if self.position[1] != self.positionArrivee[1]:
                signeDeplacementY = (self.positionArrivee[1]-self.position[1])/abs(self.positionArrivee[1]-self.position[1])
                self.position[1] += 0.1*self.taille*signeDeplacementY
            return False # pas encore arrivée à destination
        else:
            self.position = self.positionArrivee
            return True # arrivée à destination
    

class Roulette:
    def __init__(self, origine:tuple, rayon:int):
        self.origine = origine # (x,y) en pixels
        self.rayon = rayon
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
    def __init__(self, tailleFenetre:tuple, coteCases:int, nombreLignes:int=3, nombreColonnes:int=3, configAvecTexte:list=[''], image=None):
        if configAvecTexte != ['']: # un texte est précisé (comme [['] I', 'N', 'P'], ['p', '1', '2']] par exemple)
            nombreLignes = len(configAvecTexte)
            nombreColonnes = len(configAvecTexte[0])
        
        self.coteCases = coteCases
        self.origine = ((tailleFenetre[0] - self.coteCases*nombreColonnes)/2, tailleFenetre[1]*0.1 + (tailleFenetre[1]*0.9 - self.coteCases*nombreLignes)/2)
        self.textePieces = configAvecTexte
        
        self.configInitiale = []
        self.pieces = []
        chiffre = 1
        for ligne in range(nombreLignes):
            self.pieces.append([])
            self.configInitiale.append([])
            for colonne in range(nombreColonnes):
                self.pieces[ligne].append(Piece([self.origine[0] + colonne*self.coteCases, self.origine[1] + ligne*self.coteCases], self.coteCases, COULEUR_PIECES, chiffre, image, (colonne*self.coteCases, ligne*self.coteCases)))
                if configAvecTexte != ['']: # un texte est précisé (comme [['] I', 'N', 'P'], ['p', '1', '2']] par exemple)
                    self.pieces[ligne][colonne].texte = configAvecTexte[ligne][colonne]
                self.configInitiale[ligne].append(chiffre)
                chiffre += 1
        
        rayonRoulettesGaucheDroite = self.coteCases*nombreLignes/(nombreLignes-1)/2
        if nombreColonnes > 3:
            rayonRoulettesHautBas = self.coteCases*(nombreColonnes-2)/(nombreColonnes-3)/2
        self.roulettes = []
        for ligne in range(1, nombreLignes): # création des roulettes
            self.roulettes.append([])
            for colonne in range(1, nombreColonnes):
                if colonne == 1: # à gauche de la grille
                    rayon = rayonRoulettesGaucheDroite
                    x = self.origine[0] + (colonne-0.8)*self.coteCases
                    y = self.origine[1] + 2*rayon*ligne - rayon
                    zoneCollision = pygame.Rect(x - rayon, y - rayon, rayon - self.coteCases*0.2, 2*rayon)
                elif colonne == nombreColonnes -1: # à droite de la grille
                    rayon = rayonRoulettesGaucheDroite
                    x = self.origine[0] + (colonne+0.8)*self.coteCases
                    y = self.origine[1] + 2*rayon*ligne - rayon
                    zoneCollision = pygame.Rect(x + self.coteCases*0.2, y - rayon, rayon - self.coteCases*0.2, 2*rayon)
                elif ligne == 1: # au-dessus de la grille
                    rayon = rayonRoulettesHautBas
                    x = self.origine[0] + 2*rayon*(colonne-1) - rayon + self.coteCases
                    y = self.origine[1] + (ligne-0.5)*self.coteCases
                    zoneCollision = pygame.Rect(x - rayon, y - rayon, 2*rayon, rayon - self.coteCases*0.5)
                elif ligne == nombreLignes -1: # en dessous de la grille
                    rayon = rayonRoulettesHautBas
                    x = self.origine[0] + 2*rayon*(colonne-1) - rayon + self.coteCases
                    y = self.origine[1] + (ligne+0.5)*self.coteCases
                    zoneCollision = pygame.Rect(x - rayon, y + self.coteCases*0.5, 2*rayon, rayon - self.coteCases*0.5)
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
        
        pygame.draw.rect(screen, COULEUR_DOS_GRILLE, pygame.Rect(self.origine[0]-8, self.origine[1]-8, self.coteCases*len(self.pieces[0])+16, self.coteCases*len(self.pieces)+16), 0, 3)
        pygame.draw.rect(screen, COULEUR_BORDURE_GRILLE, pygame.Rect(self.origine[0]-8, self.origine[1]-8, self.coteCases*len(self.pieces[0])+16, self.coteCases*len(self.pieces)+16), 8, 3)
        
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
                self.pieces[ligne][colonne].positionArrivee = [self.origine[0] + colonne*self.coteCases, self.origine[1] + ligne*self.coteCases]

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


def afficherPivot(screen, dimensionsEcran:tuple, nbLignes:int, nbColonnes:int, configTexte:list=[''], image=None, fenetreActuelle=PIVOTS):
    pygame.display.set_caption("Pivot")
    coteCases = int((dimensionsEcran[1]*0.6)/(1.2 + 0.5*nbLignes))

    if image is not None:
        image = pygame.transform.scale(image, (nbColonnes*coteCases, nbLignes*coteCases))
    
    grille = Grille(dimensionsEcran, coteCases, nbLignes, nbColonnes, configTexte, image)
    
    boutonSolveur = Bouton((dimensionsEcran[0]*0.02, dimensionsEcran[1]*0.02), "Résoudre", (dimensionsEcran[0]*0.12, dimensionsEcran[1]*0.052), VERT, dimensionsEcran[1]/17, (dimensionsEcran[0]*0.008, dimensionsEcran[1]*0.009))
    boutonRetour = Bouton((dimensionsEcran[0]*0.74, dimensionsEcran[1]*0.02), "Retour", (dimensionsEcran[0]*0.09, dimensionsEcran[1]*0.052), COULEUR_BOUTONS, dimensionsEcran[1]/17, (dimensionsEcran[0]*0.008, dimensionsEcran[1]*0.009))
    boutonMenu = Bouton((dimensionsEcran[0]*0.85, dimensionsEcran[1]*0.02), "Menu", (dimensionsEcran[0]*0.08, dimensionsEcran[1]*0.052), COULEUR_BOUTONS, dimensionsEcran[1]/17, (dimensionsEcran[0]*0.01, dimensionsEcran[1]*0.009))
    boutonQuitter = Bouton((dimensionsEcran[0]*0.95, dimensionsEcran[1]*0.02), "x", (dimensionsEcran[0]*0.033, dimensionsEcran[1]*0.052), ROUGE, dimensionsEcran[1]/15, (dimensionsEcran[0]*0.0097, dimensionsEcran[1]*0.003))
    listeBoutons = [boutonSolveur, boutonRetour, boutonMenu, boutonQuitter]
    
    anciennePositionSouris = None
    solution = []
    
    fenetreSuivante = fenetreActuelle
    while fenetreSuivante == fenetreActuelle:
        positionSouris = pygame.mouse.get_pos()
        
        if not grille.mouvementEnCours and solution != []:
            grille.pivoter(solution[0][0][0], solution[0][0][1], solution[0][1])
            solution = solution[1:]
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fenetreSuivante = QUITTER
        
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
            
            if event.type == pygame.MOUSEBUTTONUP:
                if grille.rouletteSelectionnee is not None:
                    grille.roulettes[grille.rouletteSelectionnee[0]][grille.rouletteSelectionnee[1]].estCliquee = False
                    grille.rouletteSelectionnee = None
                anciennePositionSouris = None
            
                for bouton in listeBoutons:
                    bouton.appuye = False
                    if bouton.zoneCollision.collidepoint(positionSouris):
                        fenetreSuivante = [SOLVEUR, PIVOTS, MENU, QUITTER][listeBoutons.index(bouton)]
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    boutonSolveur.appuye = True
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_r:
                    boutonSolveur.appuye = False
                    fenetreSuivante = SOLVEUR
        
        if fenetreSuivante == SOLVEUR:
            solution = grille.aEtoile(grille.configInitiale)
            fenetreSuivante = fenetreActuelle
        
        clicGaucheMaintenu = pygame.mouse.get_pressed(num_buttons=3)[0] # clic gauche
        if clicGaucheMaintenu:
            for bouton in listeBoutons:
                bouton.appuye = False
                if bouton.zoneCollision.collidepoint(positionSouris):
                    bouton.appuye = True
            
            if not grille.mouvementEnCours and grille.rouletteSelectionnee is not None and (abs(anciennePositionSouris[1]-positionSouris[1]) > 0.2*coteCases or abs(anciennePositionSouris[0]-positionSouris[0]) > 0.2*coteCases):
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
        for bouton in listeBoutons:
            bouton.afficher(screen)        
        pygame.display.update()
        pygame.time.wait(50)
    
    return fenetreSuivante