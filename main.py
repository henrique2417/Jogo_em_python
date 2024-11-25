import pygame
import sys
import random
from constantes import *
from jogador import Jogador
from inimigos import Inimigo, InimigoInvencivel
from laser import Laser
from menu import menu
from perguntas import carregar_perguntas
from pygame import mixer 

def main():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    relógio = pygame.time.Clock()
    jogador = Jogador()
    mixer.init()
    mixer.music.load('musica.mp3')
    mixer.music.play()
    pygame.mixer.music.set_volume(0.7)
    tecla_w_pressionada = False  
    tecla_s_pressionada = False
    plataformas = [
        pygame.Rect(0, ALTURA_TELA - 0, LARGURA_TELA, 20),
        pygame.Rect(0, ALTURA_TELA - 100, LARGURA_TELA, 20),
        pygame.Rect(0, ALTURA_TELA - 200, LARGURA_TELA, 20),
        pygame.Rect(0, ALTURA_TELA - 300, LARGURA_TELA, 20),
        pygame.Rect(0, ALTURA_TELA - 400, LARGURA_TELA, 20)
    ]
    inimigos = []
    lasers = []
    perguntas = carregar_perguntas('perguntas.json')
    pos_x_alternativas = 700
    fonte = pygame.font.Font(None, 74)
    fonte2 = pygame.font.Font(None, 38)
    texto_game_over = fonte.render("Você Morreu!", True, PRETO)
    texto_reiniciar = fonte2.render("pressione R para recomeçar", True, PRETO)

    pontuação = 0
    timer_spawn = 0
    taxa_spawn = random.randint(TAXA_MIN_SPAWN_INIMIGO, TAXA_MAX_SPAWN_INIMIGO)
    pergunta_atual = None
    resposta_atual = None
    timer_espera_pergunta = 0

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1 and jogador.pode_atirar:
                    mouse_x, mouse_y = evento.pos
                    for inimigo in inimigos:
                        if isinstance(inimigo, InimigoInvencivel):
                            continue
                        if inimigo.rect.collidepoint(mouse_x, mouse_y):
                            inimigos.remove(inimigo)
                            pontuação += 1
                            lasers.append(Laser((jogador.rect.centerx, jogador.rect.centery), (mouse_x, mouse_y)))
                            jogador.pode_atirar = False

        teclas = pygame.key.get_pressed()
        if jogador.vivo:
            if teclas[pygame.K_w] and not tecla_w_pressionada:
                jogador.subir_plataforma()
                tecla_w_pressionada = True
            elif not teclas[pygame.K_w]:
                tecla_w_pressionada = False

            if teclas[pygame.K_s] and not tecla_s_pressionada:
                jogador.descer_plataforma()
                tecla_s_pressionada = True
            elif not teclas[pygame.K_s]:
                tecla_s_pressionada = False

            # Movimentação para a esquerda e direita
            if teclas[pygame.K_a]:
                jogador.mover("esquerda")
            if teclas[pygame.K_d]:
                jogador.mover("direita")
        else:
            if teclas[pygame.K_r]:
                main()
            if teclas[pygame.K_ESCAPE]:
                pygame.quit()

        for inimigo in inimigos:
            inimigo.atualizar()

        if jogador.vivo:
            for inimigo in inimigos:
                if jogador.rect.colliderect(inimigo.rect):
                    jogador.morrer()

        fundo = pygame.image.load("img/fundo.webp")
        fundo = pygame.transform.scale(fundo, (800, 600))
        tela.blit(fundo, (0, 0))
        for plataforma in plataformas: # mostrar plataformas
            chao = pygame.image.load('img/ground.png')
            chao = pygame.transform.scale(chao, (LARGURA_TELA, 20))
            tela.blit(chao, plataforma)

        if jogador.vivo:
            jogador.atualizar_animacao() 
            jogador.desenhar(tela)
        else:
            tela.blit(texto_game_over, (LARGURA_TELA // 2 - 150, ALTURA_TELA // 2 - 50))
            tela.blit(texto_reiniciar, (LARGURA_TELA // 2 - 200, ALTURA_TELA // 2 + 50))

        for inimigo in inimigos:
            if isinstance(inimigo, InimigoInvencivel):
                inimigo.desenhar(tela)  # Desenha a pedra
            else:
                inimigo.atualizar_animacao() 
                inimigo.desenhar(tela)

        for laser in lasers:
            laser.desenhar(tela)
            laser.atualizar(relógio.tick(FPS))
            if not laser.active:
                lasers.remove(laser)
                jogador.pode_atirar = True

        texto_pontuação = fonte.render("Pontuação: " + str(pontuação), True, PRETO)
        tela.blit(texto_pontuação, (10, 10))

        # Spawn de inimigos
        if pergunta_atual is None:
            timer_spawn += 1
            if timer_spawn >= taxa_spawn:
                timer_spawn = 0
                taxa_spawn = random.randint(TAXA_MIN_SPAWN_INIMIGO, TAXA_MAX_SPAWN_INIMIGO)
                velocidade_inimigo = random.randint(VELOCIDADE_MIN_INIMIGO, VELOCIDADE_MAX_INIMIGO)
                escolha = random.choice([1, 2, 3, 4, 5])
                if escolha == 1:
                    y_spawn = ALTURA_TELA - 50
                elif escolha == 2:
                    y_spawn = ALTURA_TELA - 150
                elif escolha == 3:
                    y_spawn = ALTURA_TELA - 250
                elif escolha == 4:
                    y_spawn = ALTURA_TELA - 350
                elif escolha == 5:
                    y_spawn = ALTURA_TELA - 450  
                
                if random.choice([True, False]):
                    inimigos.append(Inimigo(LARGURA_TELA, y_spawn, velocidade_inimigo))
                else:
                    inimigos.append(InimigoInvencivel(LARGURA_TELA, y_spawn, velocidade_inimigo))

        # Exibe a pergunta e as alternativas e o tempo entre elas
        fonte_timer = pygame.font.Font(None, 48)
        segundos = int(timer_espera_pergunta / 60) # traduzir para segundos
        texto_timer = fonte_timer.render("Tempo: " + str(segundos), True, PRETO)
        tela.blit(texto_timer, (600, 20))
        if timer_espera_pergunta > 0:
            timer_espera_pergunta -= 1
        elif pergunta_atual is None:
            if len(perguntas) == 0:  # Verifica se não há mais perguntas
                texto_acabou = fonte.render("Todas as perguntas foram feitas", True, PRETO)
                tela.blit(texto_acabou, (LARGURA_TELA // 2 - 400, ALTURA_TELA // 2 + 150))
                jogador.morrer()
            else:
                pergunta_atual = random.choice(perguntas)
                resposta_atual = pergunta_atual["resposta"]
                pos_x_alternativas = 700
        if pergunta_atual is not None:
            fonte_pergunta = pygame.font.Font(None, 40)
            texto_pergunta = fonte_pergunta.render(pergunta_atual["pergunta"], True, PRETO)
            tela.blit(texto_pergunta, (130, 100))
            
            pos_x_alternativas -= 1

            for i, alternativa in enumerate(pergunta_atual["alternativas"]):
                texto_alternativa = fonte_pergunta.render(alternativa, True, PRETO)
                tela.blit(texto_alternativa, (pos_x_alternativas, 165 + i * 100))
                alternativa_rect = pygame.Rect(pos_x_alternativas, 0, LARGURA_TELA, ALTURA_TELA)
                if pergunta_atual is not None:
                    if jogador.rect.colliderect(alternativa_rect):
                        if jogador.plataforma == resposta_atual:
                            pontuação += 5
                            perguntas.remove(pergunta_atual)
                            pergunta_atual = None
                            resposta_atual = None
                            timer_espera_pergunta = 20 * FPS
                        else:    
                            jogador.morrer()
            
        pygame.display.flip()
        relógio.tick(FPS)

if __name__ == "__main__":
    menu()
    main()