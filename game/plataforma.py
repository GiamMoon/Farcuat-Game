import pygame
from .config import *

class Plataforma(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((ANCHO,60))
        self.image.fill(VERDE)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = ALTO - self.rect.height