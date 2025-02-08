import pygame

origine=(200,100)
longueurCase=100
class Piece:
    def __init__(self, position:tuple, texte:str, taille:tuple, couleur:tuple, taillePolice=35, positionTexte=(11.5, 3)):
        self.position = position # (x, y)
        self.taille = taille # (largeur, hauteur)
        self.texte = texte
        self.taillePolice = taillePolice
        self.positionTexte = positionTexte # (deltaX, deltaY) par rapport au coin supérieur gauche
        self.couleur = couleur
        
        self.zoneCollision = pygame.Rect(self.position[0], self.position[1], self.taille[0], self.taille[1])
        
    def changerPosition(self,newX, newY):
        self.position=(newX,newY)
        
    def afficher(self, screen):
        pygame.draw.rect(screen, (20,20,20), pygame.Rect(self.position[0]*longueurCase+2+origine[0], self.position[1]*longueurCase+2+origine[1], self.taille[0]*longueurCase, self.taille [1]*longueurCase), 3, 3)
        pygame.draw.rect(screen, self.couleur, pygame.Rect(self.position[0]*longueurCase+origine[0], self.position[1]*longueurCase+origine[1], self.taille[0]*longueurCase, self.taille[1]*longueurCase), 0, 3)
        pygame.draw.rect(screen, (0,0,0), pygame.Rect(self.position[0]*longueurCase+origine[0], self.position[1]*longueurCase+origine[1], self.taille[0]*longueurCase, self.taille[1]*longueurCase), 2, 3)
        texte = pygame.font.Font(None, int(self.taillePolice)).render(self.texte, 1, (0,0,0))
        screen.blit(texte, (self.position[0] + self.positionTexte[0], self.position[1] + self.positionTexte[1]))



class Grille:
    def __init__(self):
        self.piece =[
        Piece((0,0), "" , (1,1), (51, 91, 255)),
        Piece((1,0), "" , (1,1), (51, 91, 255)),
        Piece((2,0), "" , (1,1), (51, 91, 255)),
        Piece((0,1), "" , (1,1), (94, 255, 51)),
        Piece((1,1), "" , (1,1), (94, 255, 51)),
        Piece((2,1), "" , (1,1), (94, 255, 51)),
        Piece((0,2), "" , (1,1), (255, 51, 175)),
        Piece((1,2), "" , (1,1), (255, 51, 175)),
        Piece((2,2), "" , (1,1), (255, 51, 175))]

    def affichergrille(self,screen):
        for piece in self.piece:
            piece.afficher(screen)
            
    def trouverPiece(self, position):
        px = (position[0] - origine[0]) // longueurCase
        py = (position[1] - origine[1]) // longueurCase
        return (px,py)
    
    def deplacerLigne(self, py, direction):
        for piece in self.piece:
            if piece.position[1] == py:
                newX = (piece.position[0] + direction) % 3
                piece.changerPosition(newX, py)
     
    def deplacerColonne(self, px, direction):
        for piece in self.piece:
            if piece.position[0] == px:
                newY = (piece.position[1] + direction) % 3
                piece.changerPosition(px, newY)   
     
pygame.init()
screen = pygame.display.set_mode([700, 500]) # taille fenêtre  
pygame.display.set_caption("Rubik's carré")
grille =Grille()
fenetreOuverte = True

while fenetreOuverte:
    screen.fill((205, 214, 215))
    positionSouris = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            fenetreOuverte = False
              
        if event.type == pygame.MOUSEBUTTONDOWN:
            positionSourisAncienne = pygame.mouse.get_pos()  #renvoie tupple (x,y)
            pieceAncienne=grille.trouverPiece(positionSourisAncienne)
            
        if event.type == pygame.MOUSEBUTTONUP :
            positionSourisActuelle=pygame.mouse.get_pos()
            pieceActuelle=grille.trouverPiece(positionSourisActuelle)

            if pieceActuelle[1] == pieceAncienne[1]:  
                direction = 1 if pieceActuelle[0] > pieceAncienne[0] else -1
                grille.deplacerLigne(pieceAncienne[1], direction)                                     
                
            if pieceActuelle[0] == pieceAncienne[0]:  
                direction = 1 if pieceActuelle[1] > pieceAncienne[1] else -1
                grille.deplacerColonne(pieceAncienne[0], direction)     
    
    grille.affichergrille(screen)
    pygame.display.update()
    pygame.time.wait(100)
    
pygame.quit()