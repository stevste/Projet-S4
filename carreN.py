import pygame

ORIGINE=(100,100)
VITESSE=3
DIMENSION=3
LONGUEURTOTALE=300 
LONGUEURCASES=LONGUEURTOTALE//DIMENSION
COULEUR1=(51, 91, 255)
COULEUR2=(94, 255, 51)
COULEUR3=(255, 51, 175)
COULEUR4=(25, 51, 175)
COULEUR5=(94, 205, 51)
LISTE_COULEURS = [COULEUR1, COULEUR2, COULEUR3, COULEUR4,COULEUR5]


class Piece:
    def __init__(self, position:tuple, taille:tuple, couleur:tuple):
        self.position = position # (x, y)
        self.taille = taille #(largeur, hauteur)
        self.couleur = couleur
        
    def changerPosition(self,newX:int, newY:int)-> None:
        self.position=(newX,newY)
        
    def afficher(self, screen)-> None:
        pygame.draw.rect(screen, (20,20,20), pygame.Rect(self.position[0]*LONGUEURCASES+2+ORIGINE[0], self.position[1]*LONGUEURCASES+2+ORIGINE[1], self.taille[0]*LONGUEURCASES, self.taille [1]*LONGUEURCASES), 3, 3)
        pygame.draw.rect(screen, self.couleur, pygame.Rect(self.position[0]*LONGUEURCASES+ORIGINE[0], self.position[1]*LONGUEURCASES+ORIGINE[1], self.taille[0]*LONGUEURCASES, self.taille[1]*LONGUEURCASES), 0, 3)
        pygame.draw.rect(screen, (0,0,0), pygame.Rect(self.position[0]*LONGUEURCASES+ORIGINE[0], self.position[1]*LONGUEURCASES+ORIGINE[1], self.taille[0]*LONGUEURCASES, self.taille[1]*LONGUEURCASES), 2, 3)

    
class Bouton: # pour débuter solveur solveur
    def __init__(self, position:tuple, texte:str, taille:tuple, couleur:tuple, taillePolice:int=35, positionTexte:str=(11.5, 3)):
        self.position = position # (x, y)
        self.taille = taille # (largeur, hauteur)
        self.texte = texte
        self.taillePolice = taillePolice
        self.positionTexte = positionTexte # (deltaX, deltaY) par rapport au coin supérieur gauche
        self.couleur = couleur
        
        self.zoneCollision = pygame.Rect(self.position[0], self.position[1], self.taille[0], self.taille[1])
          
    def afficher(self, screen)-> None:
        pygame.draw.rect(screen, (20,20,20), pygame.Rect(self.position[0]+2, self.position[1]+2, self.taille[0], self.taille [1]), 3, 3)
        pygame.draw.rect(screen, self.couleur, pygame.Rect(self.position[0], self.position[1], self.taille[0], self.taille[1]), 0, 3)
        pygame.draw.rect(screen, (0,0,0), pygame.Rect(self.position[0], self.position[1], self.taille[0], self.taille[1]), 2, 3)
        texte = pygame.font.Font(None, int(self.taillePolice)).render(self.texte, 1, (0,0,0))
        screen.blit(texte, (self.position[0] + self.positionTexte[0], self.position[1] + self.positionTexte[1]))
   
        
class Case: # pour masquer le déplacement des pièces hors de la grille de jeu
    def __init__(self, position:tuple, taille:tuple, couleur:tuple):
        self.position = position # (x, y)
        self.taille = taille # (largeur, hauteur)
        self.couleur = couleur
        
    def afficher(self, screen)-> None:
         pygame.draw.rect(screen, self.couleur, pygame.Rect(self.position[0]*LONGUEURCASES+ORIGINE[0], self.position[1]*LONGUEURCASES+ORIGINE[1], self.taille[0]*LONGUEURCASES, self.taille[1]*LONGUEURCASES), 0, 3)

    
class Grille:
    def __init__(self):
        self.piece=[]
        couleurs = LISTE_COULEURS[:DIMENSION]  
        positions = range(len(couleurs))  
        for position, couleur in zip(positions, couleurs):
            for i in range(DIMENSION):
                self.piece.append(Piece((i, position), (1, 1), couleur))
        
        self.boutonSolveur=Bouton((500,300),"solveur",(110,30),(255,255,255))
        self.pieceSelectionnee= None
        self.textedimension=Bouton((490,100),"dimention :",(130,30),(205, 214, 215),taillePolice=30)
        self.bouton3=Bouton((490,130),"3*3",(55,30),(255,255,255))
        self.bouton4=Bouton((490,160),"4*4",(55,30),(255,255,255))
        self.bouton5=Bouton((490,190),"5*5",(55,30),(255,255,255))
        self.cases=[
            Case((DIMENSION,0),(1,DIMENSION+1),(205, 214, 215)),
            Case((-1,0),(1,DIMENSION+1),(205, 214, 215)),
            Case((0,-1),(DIMENSION+1,1),(205, 214, 215)),
            Case((0,DIMENSION),(DIMENSION+1,1),(205, 214, 215))]
                
    def affichergrille(self,screen)-> None:
        for piece in self.piece:
            piece.afficher(screen)                
        for a in self.cases:
            a.afficher(screen)
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(ORIGINE[0], ORIGINE[1], DIMENSION * LONGUEURCASES+2, DIMENSION * LONGUEURCASES+2), 4)
        self.boutonSolveur.afficher(screen)
        self.bouton3.afficher((screen))
        self.bouton4.afficher((screen))
        self.bouton5.afficher((screen))
        self.textedimension.afficher(screen)
        
    def trouverPiece(self, position:tuple)->tuple:
        px = (position[0] - ORIGINE[0]) // LONGUEURCASES
        py = (position[1] - ORIGINE[1]) // LONGUEURCASES
        return (px,py)
    
    def animerDeplacement(self, screen, pieces:list, direction:int, axe:str)-> None:        
        for i in range(LONGUEURCASES // VITESSE):
            screen.fill((205, 214, 215))  
            for piece in self.piece:
                x, y = piece.position
                cloneX, cloneY = None, None

                if piece in pieces:
                    if axe == 'x':
                        x += direction * (i * VITESSE / LONGUEURCASES)
                        if x < 0:
                            cloneX = x + DIMENSION  #  à droite
                        elif x >= (DIMENSION-1):
                            cloneX = x - DIMENSION  #  à gauche
                    if axe == 'y':
                        y += direction * (i * VITESSE / LONGUEURCASES)
                        if y < 0:
                            cloneY = y + DIMENSION  #  en bas
                        elif y >= (DIMENSION-1):
                            cloneY = y - DIMENSION  #  en haut

                px = x * LONGUEURCASES + ORIGINE[0]
                py = y * LONGUEURCASES + ORIGINE[1]
                pygame.draw.rect(screen, (20,20,20), pygame.Rect(px+2, py+2, LONGUEURCASES, LONGUEURCASES), 3, 3)
                pygame.draw.rect(screen, piece.couleur, pygame.Rect(px, py, LONGUEURCASES, LONGUEURCASES))
                pygame.draw.rect(screen, (0,0,0), pygame.Rect(px, py, LONGUEURCASES, LONGUEURCASES), 2, 3)
                
                if cloneX is not None:
                    pxClone=cloneX * LONGUEURCASES + ORIGINE[0]
                    pygame.draw.rect(screen, (20,20,20), pygame.Rect(pxClone+2, py+2, LONGUEURCASES, LONGUEURCASES), 3, 3)
                    pygame.draw.rect(screen, piece.couleur, pygame.Rect(pxClone, py, LONGUEURCASES, LONGUEURCASES))
                    pygame.draw.rect(screen, (0,0,0), pygame.Rect(pxClone, py, LONGUEURCASES, LONGUEURCASES), 2, 3)
                if cloneY is not None:
                    pyClone=cloneY * LONGUEURCASES + ORIGINE[1]
                    pygame.draw.rect(screen, (20,20,20), pygame.Rect(px+2, pyClone+2, LONGUEURCASES, LONGUEURCASES), 3, 3)
                    pygame.draw.rect(screen, piece.couleur, pygame.Rect(px, pyClone, LONGUEURCASES, LONGUEURCASES))
                    pygame.draw.rect(screen, (0,0,0), pygame.Rect(px, pyClone, LONGUEURCASES, LONGUEURCASES), 2, 3)
            
            for a in self.cases:
                a.afficher(screen)
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(ORIGINE[0], ORIGINE[1], DIMENSION * LONGUEURCASES+2, DIMENSION * LONGUEURCASES+2), 4)
            self.boutonSolveur.afficher(screen)
            self.bouton3.afficher((screen))
            self.bouton4.afficher((screen))
            self.bouton5.afficher((screen))
            self.textedimension.afficher(screen)
            pygame.display.update()
            pygame.time.delay(20)

        for piece in pieces:
            if axe == 'x':
                newX = (piece.position[0] + direction) % DIMENSION
                piece.changerPosition(newX, piece.position[1])
            else:
                newY = (piece.position[1] + direction) % DIMENSION
                piece.changerPosition(piece.position[0], newY)
   
    def deplacerLigne(self, py:int, direction:int)-> None: # direction 1 vers droite
        pieces = [p for p in self.piece if p.position[1] == py]
        self.animerDeplacement(screen, pieces, direction, 'x')
    
    def deplacerColonne(self, px:int, direction:int)-> None: #direction 1 vers bas        
        pieces = [p for p in self.piece if p.position[0] == px]
        self.animerDeplacement(screen, pieces, direction, 'y')   

        
class Aetoile:
   def __init__(self):
        self.config_actuelle=grille.piece   
        self.listePiece=[]
        self.listePiece=[[None] * DIMENSION for _ in range(DIMENSION)]
        
        for piece in self.config_actuelle:
            self.listePiece[piece.position[1]][piece.position[0]]=piece.couleur
        self.etat_initial=[self.listePiece,None,1,0,0]   #pieces, parent, g,h,f 
            
        self.open=[]
        self.close=[] 
        self.listeBut = [[couleur] * DIMENSION for couleur in LISTE_COULEURS[:DIMENSION]]

        
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
    
   def verif_close(self, config:list)-> bool:  
        for etat in self.close:
            if config == etat[0]:
                return True
        return False

   def verif_open(self, config:list)-> bool:
       for etat in self.open:
           if config == etat[0]:
               return True
       return False

   def but(self,liste:list)-> bool:
        return liste == self.listeBut
   
   def heuristique(self,liste,but):
       h=0
       for i in range(DIMENSION):
           for j in range(DIMENSION):
              if liste[i][j]!=but[i][j]:
                  h+=1
       return h
   
    
   def ajouter_etat(self, config: list, parent: list, g: int, h:int):
       if not self.verif_close(config) and not self.verif_open(config):
           f=g+h 
           self.open.append([config, parent, g, h, f])
   
   def ligneDeplacement(self,enCours:list,ligne:int,direction:int)->list: # dans le aetoile
       config = [[None] * DIMENSION for _ in range(DIMENSION)]
       for l in range(len(enCours)):
               for j in range(len(enCours[0])):
                   if l==ligne:
                       config[l][(j+direction)%DIMENSION]=enCours[l][j]
                   else:
                       config[l][j]=enCours[l][j]
       return config
   
   def ColonneDeplacement(self,enCours:list,colone:int,direction:int)->list: # dans le aetoile
        config = [[None] * DIMENSION for _ in range(DIMENSION)]
        for l in range(len(enCours)):
                        for j in range(len(enCours[0])):
                            if j==colone:
                                config[(l+direction)%DIMENSION][j]=enCours[l][j]
                            else:
                                config[l][j]=enCours[l][j]
        return config
                      
   def mouvement(self)->list:
       self.open.append(self.etat_initial)
       compteur = 0

       while self.open:
           compteur += 1
           print(compteur)
           self.open.sort(key=lambda x: x[4])  
           self.enCours = self.open.pop(0)
           self.close.append(self.enCours)  
           self.parent = self.enCours[0]
           self.g=self.enCours[2]+1
           self.h=self.heuristique(self.enCours[0], self.listeBut)
           self.f=self.g+self.h

           if self.but(self.parent):
               return self.chemin(self.parent, self.enCours[1])
# TODO problemme si rectangle
           for i in range(DIMENSION):
               for direction in [-1, 1]:
                   self.ajouter_etat(self.ligneDeplacement(self.parent, i, direction), self.parent, self.g,self.h)
                   self.ajouter_etat(self.ColonneDeplacement(self.parent, i, direction), self.parent, self.g, self.h)
                     
   def reconstituer_chemin(self,liste_mouvement:list)-> None:
        if liste_mouvement:
            print(liste_mouvement)
            etat_precedent = liste_mouvement[0] 
            for etat_suivant in liste_mouvement[1:]: 
                
                ligne_diff=0
                for i in range(DIMENSION):  
                    if etat_precedent[i]!= etat_suivant[i] :                                
                        ligne_diff+=1
                        l=i               
                if ligne_diff==1:
                    if all(etat_precedent[l][i] == etat_suivant[l][(i -1)] for i in range(DIMENSION)):
                        grille.deplacerLigne(l, -1)  
                    else :
                        grille.deplacerLigne(l, 1)
                    
                colonne_diff=0
                for j in range(DIMENSION):  
                    colonne_prec = [etat_precedent[x][j] for x in range(DIMENSION)]
                    colonne_suiv = [etat_suivant[x][j] for x in range(DIMENSION)]
                    if colonne_prec != colonne_suiv:
                        colonne_diff+=1
                        prec_traite=colonne_prec
                        suiv_traite=colonne_suiv
                        c=j
                if colonne_diff==1:
                    if all(prec_traite[i] == suiv_traite[(i - 1)] for i in range(DIMENSION)):
                        grille.deplacerColonne(c, -1)  
                    else: 
                        grille.deplacerColonne(c, 1) 
                        
                etat_precedent = etat_suivant
                         
           
             
pygame.init()
screen = pygame.display.set_mode([700, 500]) # taille fenêtre  
pygame.display.set_caption("Rubik's carré")
grille =Grille()
fenetreOuverte = True
selection=False
while fenetreOuverte:
    screen.fill((205, 214, 215))
    positionSouris = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            fenetreOuverte = False
        
        if event.type == pygame.MOUSEBUTTONDOWN :
            if grille.boutonSolveur.zoneCollision.collidepoint(positionSouris):
                aetoile = Aetoile()
                liste_mouvement=aetoile.mouvement()
                aetoile.reconstituer_chemin(liste_mouvement)
            elif grille.bouton3.zoneCollision.collidepoint(positionSouris):
                DIMENSION=3
                LONGUEURCASES=LONGUEURTOTALE//DIMENSION
                grille =Grille()
            elif grille.bouton4.zoneCollision.collidepoint(positionSouris):
                    DIMENSION=4
                    LONGUEURCASES=LONGUEURTOTALE//DIMENSION
                    grille =Grille()
            elif grille.bouton5.zoneCollision.collidepoint(positionSouris):
                DIMENSION=5
                LONGUEURCASES=LONGUEURTOTALE//DIMENSION
                grille=Grille()
            else:   
                positionSourisAncienne = pygame.mouse.get_pos()  #renvoie tupple (x,y)
                pieceAncienne=grille.trouverPiece(positionSourisAncienne)
                selection=True
                                              
        if event.type == pygame.MOUSEBUTTONUP and selection==True : 
            positionSourisActuelle=pygame.mouse.get_pos()
            pieceActuelle=grille.trouverPiece(positionSourisActuelle)
            
            if pieceActuelle != pieceAncienne:
                if pieceActuelle[1] == pieceAncienne[1]:  
                    direction = 1 if pieceActuelle[0] > pieceAncienne[0] else -1 
                    grille.deplacerLigne(pieceAncienne[1], direction)                                     
                    
                if pieceActuelle[0] == pieceAncienne[0]:  
                    direction = 1 if pieceActuelle[1] > pieceAncienne[1] else -1
                    grille.deplacerColonne(pieceAncienne[0], direction)   
                          
            selection=False  
        
    grille.affichergrille(screen)
    pygame.display.update()
    pygame.time.wait(100)
    
pygame.quit()