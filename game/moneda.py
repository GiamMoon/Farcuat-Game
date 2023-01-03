import pygame,os
from .config import *

class Moneda(pygame.sprite.Sprite):

    def __init__(self,pos_x,pos_y,velocidad,dir_imagen):
        pygame.sprite.Sprite.__init__(self)
        self.image =pygame.image.load(os.path.join(dir_imagen, "coin.png"))

        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y

        self.velocidad = velocidad

    def update(self):
        self.rect.left -= self.velocidad    

    def parar(self):    
        self.velocidad = 0