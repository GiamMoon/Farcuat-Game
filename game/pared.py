import pygame,os
from .config import *

class Pared(pygame.sprite.Sprite):
    def __init__(self,left,bottom,velocidad,dir_imagen):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = self.image =pygame.image.load(os.path.join(dir_imagen, "wall.jpg"))

        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.bottom = bottom
    
        self.velocidad = velocidad

        self.rect_top = pygame.Rect(self.rect.x,self.rect.y,self.rect.width,1)

    def update(self):
        self.rect.left -= self.velocidad

        self.rect_top.x = self.rect.x

    def parar(self):
        self.velocidad = 0

        
