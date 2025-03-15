import pygame

origine=(200,100)
longueurCase=100
vitesse=3

class Piece:
    def __init__(self, position:tuple, taille:tuple, couleur:tuple):
        self.position = position # (x, y)
        self.taille = taille # (largeur, hauteur)
        self.couleur = couleur
        
    def changerPosition(self,newX:int, newY:int)-> None:
        self.position=(newX,newY)
        
    def afficher(self, screen)-> None:
        pygame.draw.rect(screen, (20,20,20), pygame.Rect(self.position[0]*longueurCase+2+origine[0], self.position[1]*longueurCase+2+origine[1], self.taille[0]*longueurCase, self.taille [1]*longueurCase), 3, 3)
        pygame.draw.rect(screen, self.couleur, pygame.Rect(self.position[0]*longueurCase+origine[0], self.position[1]*longueurCase+origine[1], self.taille[0]*longueurCase, self.taille[1]*longueurCase), 0, 3)
        pygame.draw.rect(screen, (0,0,0), pygame.Rect(self.position[0]*longueurCase+origine[0], self.position[1]*longueurCase+origine[1], self.taille[0]*longueurCase, self.taille[1]*longueurCase), 2, 3)

    
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
         pygame.draw.rect(screen, self.couleur, pygame.Rect(self.position[0]*longueurCase+origine[0], self.position[1]*longueurCase+origine[1], self.taille[0]*longueurCase, self.taille[1]*longueurCase), 0, 3)

    
class Grille:
    def __init__(self):
        self.piece =[
        Piece((0,0), (1,1), (51, 91, 255)),
        Piece((1,0), (1,1), (51, 91, 255)),
        Piece((2,0),  (1,1), (51, 91, 255)),
        Piece((0,1),  (1,1), (94, 255, 51)),
        Piece((1,1), (1,1), (94, 255, 51)),
        Piece((2,1),  (1,1), (94, 255, 51)),
        Piece((0,2), (1,1), (255, 51, 175)),
        Piece((1,2),  (1,1), (255, 51, 175)),
        Piece((2,2),  (1,1), (255, 51, 175))]
        self.boutonSolveur=Bouton((0,0),"solveur",(110,30),(255,255,255))
        self.pieceSelectionnee= None
        self.cases=[
            Case((3,0),(1,4),(205, 214, 215)),
            Case((-1,0),(1,4),(205, 214, 215)),
            Case((0,-1),(4,1),(205, 214, 215)),
            Case((0,3),(4,1),(205, 214, 215))]
                
    def affichergrille(self,screen)-> None:
        for piece in self.piece:
            piece.afficher(screen)                
        for a in self.cases:
            a.afficher(screen)
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(origine[0], origine[1], 3 * longueurCase+2, 3 * longueurCase+2), 3)
        self.boutonSolveur.afficher(screen)
        
    def trouverPiece(self, position:tuple)->tuple:
        px = (position[0] - origine[0]) // longueurCase
        py = (position[1] - origine[1]) // longueurCase
        return (px,py)
    
    def animerDeplacement(self, screen, pieces:list, direction:int, axe:str)-> None:        
        for i in range(longueurCase // vitesse):
            screen.fill((205, 214, 215))  
            for piece in self.piece:
                x, y = piece.position
                cloneX, cloneY = None, None

                if piece in pieces:
                    if axe == 'x':
                        x += direction * (i * vitesse / longueurCase)
                        if x < 0:
                            cloneX = x + 3  #  à droite
                        elif x >= 2:
                            cloneX = x - 3  #  à gauche
                    if axe == 'y':
                        y += direction * (i * vitesse / longueurCase)
                        if y < 0:
                            cloneY = y + 3  #  en bas
                        elif y >= 2:
                            cloneY = y - 3  #  en haut

                px = x * longueurCase + origine[0]
                py = y * longueurCase + origine[1]
                pygame.draw.rect(screen, (20,20,20), pygame.Rect(px+2, py+2, longueurCase, longueurCase), 3, 3)
                pygame.draw.rect(screen, piece.couleur, pygame.Rect(px, py, longueurCase, longueurCase))
                pygame.draw.rect(screen, (0,0,0), pygame.Rect(px, py, longueurCase, longueurCase), 2, 3)
                
                if cloneX is not None:
                    pxClone=cloneX * longueurCase + origine[0]
                    pygame.draw.rect(screen, (20,20,20), pygame.Rect(pxClone+2, py+2, longueurCase, longueurCase), 3, 3)
                    pygame.draw.rect(screen, piece.couleur, pygame.Rect(pxClone, py, longueurCase, longueurCase))
                    pygame.draw.rect(screen, (0,0,0), pygame.Rect(pxClone, py, longueurCase, longueurCase), 2, 3)
                if cloneY is not None:
                    pyClone=cloneY * longueurCase + origine[1]
                    pygame.draw.rect(screen, (20,20,20), pygame.Rect(px+2, pyClone+2, longueurCase, longueurCase), 3, 3)
                    pygame.draw.rect(screen, piece.couleur, pygame.Rect(px, pyClone, longueurCase, longueurCase))
                    pygame.draw.rect(screen, (0,0,0), pygame.Rect(px, pyClone, longueurCase, longueurCase), 2, 3)
            
            for a in self.cases:
                a.afficher(screen)
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(origine[0], origine[1], 3 * longueurCase+2, 3 * longueurCase+2), 3)
            self.boutonSolveur.afficher(screen)
            pygame.display.update()
            pygame.time.delay(20)

        for piece in pieces:
            if axe == 'x':
                newX = (piece.position[0] + direction) % 3
                piece.changerPosition(newX, piece.position[1])
            else:
                newY = (piece.position[1] + direction) % 3
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
        self.listePiece=[[None,None,None],[None,None,None],[None,None,None]]
        
        for piece in self.config_actuelle:
            self.listePiece[piece.position[1]][piece.position[0]]=piece.couleur
        self.etat_initial=[self.listePiece,None,1,0,0]   #pieces, parent, g,h,f 
            
        self.open=[]
        self.close=[]        
        self.listeBut=[[(51, 91, 255),(51, 91, 255),(51, 91, 255)],[(94, 255, 51),(94, 255, 51),(94, 255, 51)],[(255, 51, 175),(255, 51, 175),(255, 51, 175)]]
    
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
    
   def ajouter_etat(self, config: list, parent: list, g: int):
       if not self.verif_close(config) and not self.verif_open(config):
           h=0
           f=g+h 
           self.open.append([config, parent, g, h, f])
   
   def ligneDeplacement(self,enCours:list,ligne:int,direction:int)->list: # dans le aetoile
       config=[[None,None,None],[None,None,None],[None,None,None]]
       for l in range(len(enCours)):
               for j in range(len(enCours[0])):
                   if l==ligne:
                       config[l][(j+direction)%3]=enCours[l][j]
                   else:
                       config[l][j]=enCours[l][j]
       return config
   
   def ColonneDeplacement(self,enCours:list,colone:int,direction:int)->list: # dans le aetoile
        config=[[None,None,None],[None,None,None],[None,None,None]]
        for l in range(len(enCours)):
                for j in range(len(enCours[0])):
                    if j==colone:
                        config[(l+direction)%3][j]=enCours[l][j]
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
           self.f=self.g+0

           if self.but(self.parent):
               return self.chemin(self.parent, self.enCours[1])

           for i in range(3):
               for direction in [-1, 1]:
                   self.ajouter_etat(self.ligneDeplacement(self.parent, i, direction), self.parent, self.f)
                   self.ajouter_etat(self.ColonneDeplacement(self.parent, i, direction), self.parent, self.f)
                     
   def reconstituer_chemin(self,liste_mouvement:list)-> None:
        if liste_mouvement:
            etat_precedent = liste_mouvement[0] 
            for etat_suivant in liste_mouvement[1:]: 
                
                ligne_diff=0
                for i in range(3):  
                    if etat_precedent[i]!= etat_suivant[i] :                                
                        ligne_diff+=1
                        l=i               
                if ligne_diff==1:
                    if etat_precedent[l][0]==etat_suivant[l][2] and etat_precedent[l][1]==etat_suivant[l][0] and etat_precedent[l][2]==etat_suivant[l][1]:
                        grille.deplacerLigne(l, -1)  
                    else :
                        grille.deplacerLigne(l, 1)
                    
                colonne_diff=0
                for j in range(3):  
                    colonne_prec = [etat_precedent[x][j] for x in range(3)]
                    colonne_suiv = [etat_suivant[x][j] for x in range(3)]
                    if colonne_prec != colonne_suiv:
                        colonne_diff+=1
                        prec_traite=colonne_prec
                        suiv_traite=colonne_suiv
                        c=j
                if colonne_diff==1:
                    if prec_traite[0]==suiv_traite[2] and prec_traite[1]==suiv_traite[0] and prec_traite[2]==suiv_traite[1]:
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
                grille.deplacerColonne(grille.pieceSelectionnee[0], -1)
                
            elif event.key == pygame.K_DOWN and grille.pieceSelectionnee is not None:
                grille.deplacerColonne(grille.pieceSelectionnee[0], 1 )
           
            elif event.key == pygame.K_RIGHT and grille.pieceSelectionnee is not None:
                grille.deplacerLigne(grille.pieceSelectionnee[1], 1 )
                
            elif event.key == pygame.K_LEFT and grille.pieceSelectionnee is not None:
                grille.deplacerLigne(grille.pieceSelectionnee[1], -1 )
    grille.affichergrille(screen)
    pygame.display.update()
    pygame.time.wait(100)
    
pygame.quit()