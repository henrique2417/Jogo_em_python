import pygame
from constantes import *
import random

class InimigoBase:
    def __init__(self, x, y, velocidade):
        self.rect = pygame.Rect(x, y, LARGURA_INIMIGO, ALTURA_INIMIGO)
        self.velocidade = velocidade

    def atualizar(self):
        self.rect.x -= self.velocidade

    def desenhar(self, tela):
        raise NotImplementedError("Este método srá implementado de forma diferente pelas subclasses.")

class Inimigo(InimigoBase):
    def __init__(self, x, y, velocidade):
        super().__init__(x, y, velocidade)
        self.frames = [pygame.transform.scale(pygame.image.load(f'img/inimigo/inimigo{i}.png'), (50, 50)) for i in range(4)]
        self.frame_atual = 0
        self.frame_timer = 0
        self.frame_rate = 5  # Número de frames por segundo

    def atualizar_animacao(self):
        self.frame_timer += 1
        if self.frame_timer >= self.frame_rate:
            self.frame_timer = 0
            self.frame_atual = (self.frame_atual + 1) % len(self.frames)

    def desenhar(self, tela):
        tela.blit(self.frames[self.frame_atual], (self.rect.x, self.rect.y))
    
    @staticmethod
    def criar_inimigo():
        y_spawn = random.choice([ALTURA_TELA - 50, ALTURA_TELA - 150, ALTURA_TELA - 250, ALTURA_TELA - 350, ALTURA_TELA - 450])
        velocidade_inimigo = random.randint(VELOCIDADE_MIN_INIMIGO, VELOCIDADE_MAX_INIMIGO)

        if random.choice([True, False]):
            return Inimigo(LARGURA_TELA, y_spawn, velocidade_inimigo)
        else:
            return InimigoInvencivel(LARGURA_TELA, y_spawn, velocidade_inimigo)
        
        

class InimigoInvencivel(InimigoBase):
    def __init__(self, x, y, velocidade):
        super().__init__(x, y, velocidade)
        self.image = pygame.Surface((50, 50), pygame.SRCALPHA)  # Usando SRCALPHA para suporte à transparência
        aparencia = random.choice([
            pygame.image.load("img/rocks1.png"),
            pygame.image.load("img/rocks2.png"),
            pygame.image.load("img/rocks3.png"),
            pygame.image.load("img/rocks4.png"),
            pygame.image.load("img/rocks5.png"),
            pygame.image.load("img/rocks6.png")
        ])
        self.image.blit(aparencia, (0, 0))

    def desenhar(self, tela):
        tela.blit(self.image, (self.rect.x, self.rect.y))