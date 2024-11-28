import pygame
from constantes import *

class Jogador:
    def __init__(self):
        self.rect = pygame.Rect(100, ALTURA_TELA - ALTURA_JOGADOR, LARGURA_JOGADOR, ALTURA_JOGADOR)
        self.velocidade_y = 0
        self.vivo = True
        self.pode_atirar = True
        self.plataforma = 1

        self.frames = [pygame.transform.scale(pygame.image.load(f'img/correr/correr{i}.png'), (50, 50)) for i in range(12)]
        self.frame_atual = 0
        self.frame_timer = 0
        self.frame_rate = 2  # Número de frames por segundo
        

    def subir_plataforma(self):
        if self.rect.top > 0 and self.plataforma < 5:
            self.rect.y -= 100
            self.plataforma += 1

    def descer_plataforma(self):
        if self.rect.bottom < ALTURA_TELA:
            self.rect.y += 100
            self.plataforma -= 1

    def mover(self, teclas):
        if self.vivo:
            # Subir plataforma
            if teclas[pygame.K_w] and not self.tecla_w_pressionada:
                self.subir_plataforma()
                self.tecla_w_pressionada = True
            elif not teclas[pygame.K_w]:
                self.tecla_w_pressionada = False

            # Descer plataforma
            if teclas[pygame.K_s] and not self.tecla_s_pressionada:
                self.descer_plataforma()
                self.tecla_s_pressionada = True
            elif not teclas[pygame.K_s]:
                self.tecla_s_pressionada = False

            # Movimentação para a esquerda e direita
            if teclas[pygame.K_a]:
                if self.rect.x - 5 >= 0:  
                    self.rect.x -= 5
            if teclas[pygame.K_d]:
                if self.rect.x + 5 <= 800:
                    self.rect.x += 5

    def atualizar_animacao(self):
        self.frame_timer += 1
        if self.frame_timer >= self.frame_rate:
            self.frame_timer = 0
            self.frame_atual = (self.frame_atual + 1) % len(self.frames)

    def desenhar(self, tela):
        # Desenhar o frame atual na posição do jogador
        tela.blit(self.frames[self.frame_atual], (self.rect.x, self.rect.y))

    def morrer(self):
        self.vivo = False