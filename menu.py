import pygame
import sys
from constantes import *
from pygame import mixer 

pygame.init()
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
relógio = pygame.time.Clock()
def menu():
    fonte = pygame.font.Font(None, 74)
    texto_jogar = fonte.render("Jogar", True, PRETO)
    texto_titulo = fonte.render("Pense e Corra", True, PRETO)
    mixer.init()
    mixer.music.load('musicaa.mp3')
    mixer.music.play()
    pygame.mixer.music.set_volume(0.7)
    fundo = pygame.image.load("img/fundo.webp")
    fundo = pygame.transform.scale(fundo, (800, 600))
    tela.blit(fundo, (0, 0))
    

    botao_jogar = pygame.Rect(LARGURA_TELA // 2 - 73, ALTURA_TELA // 2 + 40, 150, 75)

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONUP:
                if evento.button == 1:
                    mouse_x, mouse_y = evento.pos
                    if botao_jogar.collidepoint(mouse_x, mouse_y):
                        return

        tela.blit(texto_titulo, (LARGURA_TELA // 2 - texto_titulo.get_width () // 2, ALTURA_TELA // 2 - 100))
        pygame.draw.rect(tela, AZUL, botao_jogar)
        tela.blit(texto_jogar, (LARGURA_TELA // 2 - texto_jogar.get_width() // 2, ALTURA_TELA // 2 + 50))
        pygame.display.flip()
        relógio.tick(FPS)