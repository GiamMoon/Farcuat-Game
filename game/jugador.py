import pygame,os
from .config import *

class Jugador(pygame.sprite.Sprite):
    
    def __init__(self,left,botttom,dir_imagen):
        pygame.sprite.Sprite.__init__(self)


        self.imagenes =(pygame.image.load(os.path.join(dir_imagen, "farcu.png")),
                        pygame.image.load(os.path.join(dir_imagen, "farcujump.png")))
                        
        self.image = self.imagenes[0]
    
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.bottom = botttom

        self.pos_y = self.rect.bottom
        self.vel_y = 0

        self.puede_saltar = False

        self.jugando = True


    def colision(self,sprites):

        objetos = pygame.sprite.spritecollide(self,sprites,False)   
        if objetos:
            return objetos[0] 

        


    def colision_bottom(self,pared):
        return self.rect.colliderect(pared.rect_top)     

    def surfear(self,pared):
        self.pos_y = pared.rect.top
        self.vel_y = 0
        self.puede_saltar = True     
        self.image =  self.imagenes[0] 

    def validar_plataforma(self,plataforma):
        resultado = pygame.sprite.collide_rect(self,plataforma)   
        if resultado:
            self.vel_y = 0
            self.pos_y = plataforma.rect.top
            self.puede_saltar = True
            self.image =  self.imagenes[0]


    def salto(self):
        if self.puede_saltar: 
            self.vel_y = -23
            self.puede_saltar = False
            self.image = self.imagenes[1]


    def actualizar_posicion(self):
        self.vel_y += JUGADOR_GRAVEDAD
        self.pos_y += self.vel_y + 0.001 * JUGADOR_GRAVEDAD

    def update(self):
        if self.jugando:
            self.actualizar_posicion()

        self.rect.bottom = self.pos_y  

    def parar(self):
        self.jugando = False

        
