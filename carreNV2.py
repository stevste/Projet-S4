import pygame
from Enum import *


dimensionsEcran = (1150, 650)

VITESSE = 0.07
COULEUR1 = (51, 91, 255)
COULEUR2 = (94, 255, 51)
COULEUR3 = (255, 51, 175)
COULEUR4 = (25, 51, 175)

COULEUR5 = (50, 175, 25)
LISTE_COULEURS = [COULEUR1, COULEUR2, COULEUR3, COULEUR4, COULEUR5]


class Piece:
    def __init__(self, position:tuple, taille:tuple, couleur:tuple):
        self.position = position # (x, y) en pixels
        self.taille = taille #(largeur, hauteur)
        self.couleur = couleur
        
    def changerPosition(self,newX:int, newY:int)-> None:
        self.position=(newX,newY)
        
    def afficher(self, screen)-> None:
        pygame.draw.rect(screen, self.couleur, pygame.Rect(self.position[0], self.position[1], self.taille[0], self.taille[1]), 0, 3)
        pygame.draw.rect(screen, (0,0,0), pygame.Rect(self.position[0], self.position[1], self.taille[0], self.taille[1]), 2, 3)

class Bouton: # pour débuter solveur
    def __init__(self, position:tuple, texte:str, taille:tuple, couleur:tuple, taillePolice:int=35, positionTexte:str=(11.5, 3)):
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

        
class Case: # pour masquer le déplacement des pièces hors de la grille de jeu
    def __init__(self, position:tuple, taille:tuple):
        self.position = position # (x, y)
        self.taille = taille # (largeur, hauteur)
        
    def afficher(self, screen) -> None:
         pygame.draw.rect(screen, (205, 214, 215), pygame.Rect(self.position[0], self.position[1], self.taille[0], self.taille[1]), 0)

    
class Grille:
    def __init__(self, tailleFenetre:tuple, taille:int, coteCases:int):
        self.origine = ((tailleFenetre[0] - coteCases*taille)/2, tailleFenetre[1]*0.1 + (tailleFenetre[1]*0.9 - coteCases*taille)/2)
        self.coteCases = coteCases
        self.taille = taille

        self.pieces = []
        for ligne in range(taille):
            self.pieces.append([])
            for colonne in range(taille):
                self.pieces[ligne].append(Piece((self.origine[0]+colonne*coteCases, self.origine[1]+ligne*coteCases), (coteCases, coteCases), LISTE_COULEURS[ligne]))
        
        self.pieceSelectionnee = None
        self.cases=[

            Case((self.origine[0]+taille*self.coteCases+1, self.origine[1]), (self.coteCases, taille*self.coteCases)),
            Case((self.origine[0]-self.coteCases, self.origine[1]), (self.coteCases-1, taille*self.coteCases)),
            Case((self.origine[0], self.origine[1]-self.coteCases), (taille*self.coteCases, self.coteCases-1)),
            Case((self.origine[0], self.origine[1]+taille*self.coteCases+1), (taille*self.coteCases, self.coteCases))]
    
    def __repr__(self) -> str:
        texte = ""
        for ligne in range(len(self.pieces)):
            for colonne in range(len(self.pieces[ligne])):
                texte += str(LISTE_COULEURS.index(self.pieces[ligne][colonne].couleur)) + ' '
            texte += "\n"
        return texte
    
    def affichergrille(self, screen)-> None:
        pygame.draw.rect(screen, (50, 50, 50), pygame.Rect(self.origine[0]-3, self.origine[1]-3, self.taille*self.coteCases +6, self.taille*self.coteCases +6), 0, 3) # fond
        for ligne in range(len(self.pieces)):
            for piece in self.pieces[ligne]:
                piece.afficher(screen)                
        for case in self.cases:
            case.afficher(screen)
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(self.origine[0]-3, self.origine[1]-3, self.taille*self.coteCases +6, self.taille*self.coteCases +6), 3, 3) # contour
        self.boutonSolveur.afficher(screen)
        
    def trouverPiece(self, position:tuple)->tuple:
        px = (position[0] - self.origine[0]) // self.coteCases
        py = (position[1] - self.origine[1]) // self.coteCases
        return (int(px), int(py))
    
    def animerDeplacement(self, screen, piecesADeplacer:list, direction:int, axe:str, listeBoutons) -> None:

        for i in range(int(1/VITESSE)):
            screen.fill((205, 214, 215))
            pygame.draw.rect(screen, (50, 50, 50), pygame.Rect(self.origine[0]-3, self.origine[1]-3, self.taille*self.coteCases +6, self.taille*self.coteCases +6), 0, 3) # fond grille
            for ligne in range(len(self.pieces)):
                for piece in self.pieces[ligne]:
                    cloneX, cloneY = None, None
    
                    if piece in piecesADeplacer:
                        if axe == 'x':
                            piece.position = (piece.position[0]+direction*VITESSE*self.coteCases, piece.position[1])
                            if piece.position[0] < self.origine[0]:
                                cloneX = piece.position[0] + self.taille*self.coteCases # à droite
                            elif piece.position[0] >= self.origine[0] + (self.taille-1)*self.coteCases:
                                cloneX = piece.position[0] - self.taille*self.coteCases # à gauche
                        else: # axe == 'y':
                            piece.position = (piece.position[0], piece.position[1]+direction*VITESSE*self.coteCases)
                            if piece.position[1] < self.origine[1]:
                                cloneY = piece.position[1] + self.taille*self.coteCases # en bas
                            elif piece.position[1] >= self.origine[1] + (self.taille-1)*self.coteCases:
                                cloneY = piece.position[1] - self.taille*self.coteCases # en haut
    
                    pygame.draw.rect(screen, piece.couleur, pygame.Rect(piece.position[0], piece.position[1], self.coteCases, self.coteCases), 0, 3)
                    pygame.draw.rect(screen, (0,0,0), pygame.Rect(piece.position[0], piece.position[1], self.coteCases, self.coteCases), 2, 3)
                    
                    if cloneX is not None:
                        pygame.draw.rect(screen, piece.couleur, pygame.Rect(cloneX, piece.position[1], self.coteCases, self.coteCases), 0, 3)
                        pygame.draw.rect(screen, (0,0,0), pygame.Rect(cloneX, piece.position[1], self.coteCases, self.coteCases), 2, 3)
                    if cloneY is not None:
                        pygame.draw.rect(screen, piece.couleur, pygame.Rect(piece.position[0], cloneY, self.coteCases, self.coteCases), 0, 3)
                        pygame.draw.rect(screen, (0,0,0), pygame.Rect(piece.position[0], cloneY, self.coteCases, self.coteCases), 2, 3)
            
            for a in self.cases:
                a.afficher(screen)
            
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(self.origine[0]-3, self.origine[1]-3, self.taille*self.coteCases +6, self.taille*self.coteCases +6), 3, 3) # contour
            self.boutonSolveur.afficher(screen)
            for bouton in listeBoutons:
                bouton.afficher(screen)
            pygame.display.update()
            pygame.time.delay(20)

        for piece in piecesADeplacer:
            if axe == 'x':
                piece.position = (self.origine[0] + self.coteCases*(round((piece.position[0]-self.origine[0])/self.coteCases)%self.taille), piece.position[1])
            else:
                piece.position = (piece.position[0], self.origine[1] + self.coteCases*(round((piece.position[1]-self.origine[1])/self.coteCases)%self.taille))
                
    def deplacerLigne(self, py:int, direction:int, screen, listeBoutons) -> None: # direction 1 vers droite
        pieces = []
        for ligne in range(len(self.pieces)):
            for piece in self.pieces[ligne]:
                if (piece.position[1] - self.origine[1])//self.coteCases == py:
                    pieces.append(piece)
        
        self.animerDeplacement(screen, pieces, direction, 'x', listeBoutons)
        
        piecesDeplacees = []
        for colonne in range(self.taille):
            piecesDeplacees.append(self.pieces[py][colonne])
        for colonne in range(len(piecesDeplacees)):
                self.pieces[py][colonne] = piecesDeplacees[(colonne-direction)%self.taille]
        
    
    def deplacerColonne(self, px:int, direction:int, screen, listeBoutons) -> None: # direction 1 vers bas      
        pieces = []
        for ligne in range(len(self.pieces)):
            for piece in self.pieces[ligne]:
                if (piece.position[0] - self.origine[0])//self.coteCases == px:
                    pieces.append(piece)
        
        self.animerDeplacement(screen, pieces, direction, 'y', listeBoutons)   
        
        piecesDeplacees = []
        for ligne in range(self.taille):
            piecesDeplacees.append(self.pieces[ligne][px])
        for ligne in range(len(piecesDeplacees)):
                self.pieces[ligne][px] = piecesDeplacees[(ligne-direction)%self.taille]
            
        
class Aetoile:
   def __init__(self, grille, taille):
        self.taille = taille
        self.grille = grille
        self.config_actuelle = grille.pieces
        self.listePiece = []
        for ligne in range(len(self.config_actuelle)):
            self.listePiece.append([])
            for colonne in range(len(self.config_actuelle[0])):
                self.listePiece[ligne].append(LISTE_COULEURS.index(self.config_actuelle[ligne][colonne].couleur))

        self.etat_initial = [self.listePiece, None, 0,0,0] # pieces, parent, g,h,f 
            
        self.open = []
        self.close = [] 
        self.listeBut = [] # [[couleur] * taille for couleur in LISTE_COULEURS[:taille]]
        for ligne in range(self.taille):
            self.listeBut.append([ligne]*self.taille)
        #self.listeBut[0][0]=(0,0,0)
        
   def chemin(self, etatF:list, parent:list)-> list:
        chemin_trouve = []
        actuel = etatF  
        while actuel is not None:
             chemin_trouve.append(actuel)  
             prochain_actuel = None
             for item in self.close:            
                 etat, etat_parent = item[:2]  
                 if etat == parent:  
                     prochain_actuel = etat
                     parent = etat_parent  
                     break  
             actuel = prochain_actuel
        chemin_trouve.reverse() 
        return chemin_trouve   
    
   def verif_close(self, config:list) -> bool:  
        for etat in self.close:
            if config == etat[0]:
                return True
        return False

   def verif_open(self, config:list) -> bool:
       for etat in self.open:
           if config == etat[0]:
               return True
       return False
   
   def determinerIndiceDansOpen(self, config:list) -> int:
        for indice in range(len(self.open)):
            if config == self.open[indice][0]:
                return indice
        return -1

   def but(self, liste:list) -> bool:
        if liste == self.listeBut:
            return True

   def heuristique(self, liste):
       #h = self.heuristique2(liste)
       h = self.heuristiqueLigneDispersee(liste)
       h += self.heuristiqueColonneOrdonnee(liste)
       return 0.7*h
       
   def heuristique1(self, liste):
       h = 0
       for i in range(self.taille):
           for j in range(self.taille):
              if liste[i][j] != self.but[i][j]:
                  h += 1
       return h
   
   def heuristique2(self, liste):
        h = 0
        for ligne in range(self.taille):
            for colonne in range(self.taille):
                h += abs(liste[ligne][colonne]-ligne) # écart entre la ligne sur laquelle la piece doit se trouver et celle sur laquelle elle est
        '''for i in range(self.taille):
            for j in range(self.taille):
                if liste[i][j] != self.but[i][j]:
                    for x in range(self.taille):
                        if liste[i][j]==self.but[x][0]:  
                            h += abs(i - x)'''
        return 0#h
    
   def heuristiqueLigneDispersee(self, liste) -> int:
       h = 0
       for couleur in range(self.taille):
           nombreColonnesAyantCouleur = 0 # nombre de colonnes sur lesquelles la couleur est présente
           for colonne in range(self.taille):
               couleurPresente = 0
               for ligne in range(self.taille):
                   if liste[ligne][colonne] == couleur:
                       couleurPresente = 1
               nombreColonnesAyantCouleur += couleurPresente
           h -= nombreColonnesAyantCouleur#/self.taille
       return h#round(h, 1)
   
   def heuristiqueColonneOrdonnee(self, liste) -> int:
       h = 0
       for colonne in range(self.taille):
           coefficientsOrdre = [None]*self.taille
           for ligneDepart in range(self.taille):
               coeffOrdre = 0
               for variationLigne in range(self.taille):
                   coeffOrdre += abs(liste[(ligneDepart+variationLigne)%self.taille][colonne] - ((liste[ligneDepart][colonne]+variationLigne)%self.taille))
               coefficientsOrdre[ligneDepart] = coeffOrdre
           miniPermutations = min(coefficientsOrdre)
           ligneDepartMini = coefficientsOrdre.index(miniPermutations) # ligne à partir delaquelle les cases sont le plus dans l'ordre
           h += miniPermutations + abs(liste[ligneDepartMini][colonne] - ligneDepartMini)
       return h
   
   def symetrique(self, config:list) -> list:
        symetrique = [[None] * self.taille for _ in range(self.taille)]
        for ligne in range(self.taille):
            for colonne in range(self.taille):
                symetrique[ligne][colonne] = config[ligne][self.taille-colonne-1]
        return symetrique
   
   def ajouter_etat(self, config:list, parent:list, g:int, h:int):
       symetrique = self.symetrique(config)
       if not self.verif_close(config) and not self.verif_close(symetrique):
           f = g + h
           verifsDansOpen = (self.verif_open(config), self.verif_open(symetrique))
           if verifsDansOpen == (False, False):
               self.open.append([config, parent, g, h, f])
           elif verifsDansOpen[0]: # la config existe déjà dans open
               index = self.determinerIndiceDansOpen(config)
               if index != -1 and g < self.open[index][2]:
                   self.open[index] = [config, parent, g, h, f]
           else: # le symétrique existe déjà dans open
              index = self.determinerIndiceDansOpen(symetrique)
              if index != -1 and g < self.open[index][2]:
                  self.open[index] = [config, parent, g, h, f]
   
   def ligneDeplacement(self, enCours:list,ligne:int,direction:int) -> list: # dans le aetoile
       config = [[None] * self.taille for _ in range(self.taille)]
       for l in range(len(enCours)):
            for j in range(len(enCours[0])):
                  if l == ligne:
                       config[l][(j+direction)%self.taille]=enCours[l][j]
                  else:
                       config[l][j]=enCours[l][j]
       return config
   
   def colonneDeplacement(self,enCours:list,colonne:int,direction:int) -> list: # dans le aetoile
        config = [[None] * self.taille for _ in range(self.taille)]
        for l in range(len(enCours)):
            for j in range(len(enCours[0])):
                if j == colonne:
                    config[(l+direction)%self.taille][j]=enCours[l][j]
                else:
                    config[l][j]=enCours[l][j]
        return config
                      
   def mouvement(self) -> list:
       self.open.append(self.etat_initial)
       compteur = 0

       while self.open:
           compteur += 1
           print("compteur", compteur)
           self.open.sort(key=lambda x: x[4])
           enCours = self.open.pop(0)
           self.close.append(enCours)
           parent = enCours[0]
           #print(self.enCours[0])
           g = enCours[2] +1
           #self.h = self.heuristique2(enCours[0], self.listeBut) #+ self.heuristique1(enCours[0], self.listeBut)
           #self.f = self.g + self.h
           #print("f, g, h :", enCours[4], enCours[2], enCours[3])
           if self.but(parent):
               print("trouvé", compteur)
               return self.chemin(parent, enCours[1])

           for i in range(self.taille):
               for direction in [-1, 1]:
                   config = self.ligneDeplacement(parent, i, direction)
                   self.ajouter_etat(config, parent, g, self.heuristique(config))
                   config = self.colonneDeplacement(parent, i, direction)
                   self.ajouter_etat(config, parent, g, self.heuristique(config))
                     
   def reconstituer_chemin(self, liste_mouvement:list, screen, listeBoutons:list)-> None:
        if liste_mouvement:
            #print(liste_mouvement)
            etat_precedent = liste_mouvement[0] 
            for etat_suivant in liste_mouvement[1:]: 
                
                ligne_diff=0
                for i in range(self.taille):  
                    if etat_precedent[i]!= etat_suivant[i] :                                
                        ligne_diff+=1
                        l=i               
                if ligne_diff==1:
                    if all(etat_precedent[l][i] == etat_suivant[l][(i -1)] for i in range(self.taille)):
                        self.grille.deplacerLigne(l, -1, screen, listeBoutons)  
                    else :
                        self.grille.deplacerLigne(l, 1, screen, listeBoutons)
                    
                colonne_diff=0
                for j in range(self.taille):  
                    colonne_prec = [etat_precedent[x][j] for x in range(self.taille)]
                    colonne_suiv = [etat_suivant[x][j] for x in range(self.taille)]
                    if colonne_prec != colonne_suiv:
                        colonne_diff+=1
                        prec_traite=colonne_prec
                        suiv_traite=colonne_suiv
                        c=j
                if colonne_diff==1:
                    if all(prec_traite[i] == suiv_traite[(i - 1)] for i in range(self.taille)):
                        self.grille.deplacerColonne(c, -1, screen, listeBoutons)  
                    else: 
                        self.grille.deplacerColonne(c, 1, screen, listeBoutons) 
                        
                etat_precedent = etat_suivant
                         
           
def afficherCarre(screen, dimensionsEcran, taille, fenetreActuelle):     
    pygame.display.set_caption("Rubik's carré")
    
    coteCases = int(dimensionsEcran[1]*0.7/taille)
    grille = Grille(dimensionsEcran, taille, coteCases)
    grille.boutonSolveur = Bouton((dimensionsEcran[0]*0.02, dimensionsEcran[1]*0.02), "Résoudre", (dimensionsEcran[0]*0.12, dimensionsEcran[1]*0.052), VERT, dimensionsEcran[1]/17, (dimensionsEcran[0]*0.008, dimensionsEcran[1]*0.009))

    boutonRetour = Bouton((dimensionsEcran[0]*0.74, dimensionsEcran[1]*0.02), "Retour", (dimensionsEcran[0]*0.09, dimensionsEcran[1]*0.052), COULEUR_BOUTONS, dimensionsEcran[1]/17, (dimensionsEcran[0]*0.008, dimensionsEcran[1]*0.009))
    boutonMenu = Bouton((dimensionsEcran[0]*0.85, dimensionsEcran[1]*0.02), "Menu", (dimensionsEcran[0]*0.08, dimensionsEcran[1]*0.052), COULEUR_BOUTONS, dimensionsEcran[1]/17, (dimensionsEcran[0]*0.01, dimensionsEcran[1]*0.009))
    boutonQuitter = Bouton((dimensionsEcran[0]*0.95, dimensionsEcran[1]*0.02), "x", (dimensionsEcran[0]*0.033, dimensionsEcran[1]*0.052), ROUGE, dimensionsEcran[1]/15, (dimensionsEcran[0]*0.0097, dimensionsEcran[1]*0.003))
    listeBoutons = [boutonRetour, boutonMenu, boutonQuitter]
    
    selection = False
    
    fenetreSuivante = fenetreActuelle
    while fenetreSuivante == fenetreActuelle:
        screen.fill((205, 214, 215))
        positionSouris = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fenetreSuivante = QUITTER
            
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_KP7:
                    grille.pieceSelectionnee = (0,0)
                if event.key==pygame.K_KP8:
                    grille.pieceSelectionnee = (1,0)
                if event.key==pygame.K_KP9:
                    grille.pieceSelectionnee = (2,0)
                if event.key==pygame.K_KP4:
                    grille.pieceSelectionnee = (0,1)
                if event.key==pygame.K_KP5:
                    grille.pieceSelectionnee = (1,1)
                if event.key==pygame.K_KP6:
                    grille.pieceSelectionnee = (2,1)
                if event.key==pygame.K_KP1:
                    grille.pieceSelectionnee = (0,2)
                if event.key==pygame.K_KP2:
                    grille.pieceSelectionnee = (1,2)
                if event.key==pygame.K_KP3:
                    grille.pieceSelectionnee = (2,2)
                
                
                elif event.key == pygame.K_UP and grille.pieceSelectionnee is not None:
                    grille.deplacerColonne(grille.pieceSelectionnee[0], -1, screen, listeBoutons)
                    
                elif event.key == pygame.K_DOWN and grille.pieceSelectionnee is not None:
                    grille.deplacerColonne(grille.pieceSelectionnee[0], 1, screen, listeBoutons )
               
                elif event.key == pygame.K_RIGHT and grille.pieceSelectionnee is not None:
                    grille.deplacerLigne(grille.pieceSelectionnee[1], 1, screen, listeBoutons )
                    
                elif event.key == pygame.K_LEFT and grille.pieceSelectionnee is not None:
                    grille.deplacerLigne(grille.pieceSelectionnee[1], -1, screen, listeBoutons )
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if grille.boutonSolveur.zoneCollision.collidepoint(positionSouris):
                    grille.boutonSolveur.appuye = True
                    grille.affichergrille(screen)
                    for bouton in listeBoutons:
                        bouton.afficher(screen)
                    pygame.display.update()
                    
                    aetoile = Aetoile(grille, taille)
                    liste_mouvement = aetoile.mouvement()
                    grille.boutonSolveur.appuye = False
                    aetoile.reconstituer_chemin(liste_mouvement, screen, listeBoutons)
                else:   
                    positionSourisAncienne = pygame.mouse.get_pos() # renvoie tuple (x,y)
                    pieceAncienne = grille.trouverPiece(positionSourisAncienne)
                    selection = True
                                                  
            if event.type == pygame.MOUSEBUTTONUP:
                if selection == True : 
                    positionSourisActuelle = pygame.mouse.get_pos()
                    pieceActuelle = grille.trouverPiece(positionSourisActuelle)
                    
                    if pieceActuelle != pieceAncienne:
                        if pieceActuelle[1] == pieceAncienne[1]:  
                            direction = 1 if pieceActuelle[0] > pieceAncienne[0] else -1 
                            grille.deplacerLigne(pieceAncienne[1], direction, screen, listeBoutons)                                     
                            
                        if pieceActuelle[0] == pieceAncienne[0]:  
                            direction = 1 if pieceActuelle[1] > pieceAncienne[1] else -1
                            grille.deplacerColonne(pieceAncienne[0], direction, screen, listeBoutons)   
                                  
                    selection = False
                
                for bouton in listeBoutons:
                    bouton.appuye = False
                    if bouton.zoneCollision.collidepoint(positionSouris):
                        fenetreSuivante = [CARRES, MENU, QUITTER][listeBoutons.index(bouton)]
                
        clicGaucheMaintenu = pygame.mouse.get_pressed(num_buttons=3)[0]
        if clicGaucheMaintenu:
            positionSouris = pygame.mouse.get_pos()
            for bouton in listeBoutons:
                bouton.appuye = False
                if bouton.zoneCollision.collidepoint(positionSouris):
                    bouton.appuye = True
            
        grille.affichergrille(screen)
        for bouton in listeBoutons:
            bouton.afficher(screen)
        pygame.display.update()
        pygame.time.wait(100)
        
    return fenetreSuivante