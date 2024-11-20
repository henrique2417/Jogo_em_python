import pygame
from constantes import *

class Laser:
    def __init__(self, start_pos, end_pos):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.active = True
        self.timer = 0

    def atualizar(self, delta_time):
        if self.active:
            self.timer += delta_time
            if self.timer >= 200:  # 200 ms
                self.active = False 

    def desenhar(self, surface):
        if self.active:
            pygame.draw.line(surface, AZUL_CLARO, self.start_pos, self.end_pos, 5)