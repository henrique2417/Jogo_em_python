import pygame
import sys
import random

# Inicializa o Pygame
pygame.init()

# Constantes
LARGURA_TELA = 800
ALTURA_TELA = 600
FPS = 60

# Cores
BRANCO = (255, 255, 255)
AZUL = (0, 0, 255)
AZUL_CLARO = (173, 216, 230)  # Azul claro para o laser
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)
PRETO = (0, 0, 0)
MARROM = (120, 64, 8)

# Configurações do jogador
LARGURA_JOGADOR = 50
ALTURA_JOGADOR = 60
GRAVIDADE = 1
FORCA_PULO = 15

# Configurações do inimigo
LARGURA_INIMIGO = 40
ALTURA_INIMIGO = 40
VELOCIDADE_MIN_INIMIGO = 2
VELOCIDADE_MAX_INIMIGO = 5
TAXA_MIN_SPAWN_INIMIGO = 60  # Mínimo de frames até um novo inimigo aparecer
TAXA_MAX_SPAWN_INIMIGO = 80  # Máximo de frames até um novo inimigo aparecer

# Configura a tela
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Pense e corra")

# Clock para controlar a taxa de frames
relógio = pygame.time.Clock()

# Classe do jogador
class Jogador:
    def __init__(self):
        self.rect = pygame.Rect(100, ALTURA_TELA - ALTURA_JOGADOR, LARGURA_JOGADOR, ALTURA_JOGADOR)
        self.velocidade_y = 0
        self.em_chao = True
        self.vivo = True
        self.pode_atirar = True  # Permite que o jogador atire

    def atualizar(self):
        if self.vivo:
            if not self.em_chao:
                self.velocidade_y += GRAVIDADE
            else:
                self.velocidade_y = 0

            self.rect.y += self.velocidade_y

            if self.rect.bottom >= ALTURA_TELA:
                self.rect.bottom = ALTURA_TELA
                self.em_chao = True
            else:
                self.em_chao = False

    def pular(self):
        if self.em_chao and self.vivo:
            self.velocidade_y = -FORCA_PULO
            self.em_chao = False

    def morrer(self):
        self.vivo = False

# Classe do inimigo
class Inimigo:
    def __init__(self, x, y, velocidade):
        self.rect = pygame.Rect(x, y, LARGURA_INIMIGO, ALTURA_INIMIGO)
        self.velocidade = velocidade

    def atualizar(self):
        self.rect.x -= self.velocidade  # Move o inimigo para a esquerda

# Classe do laser
class Laser:
    def __init__(self, start_pos, end_pos):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.active = True
        self.timer = 0  # Timer para controlar a duração do laser

    def atualizar(self, delta_time):
        if self.active:
            self.timer += delta_time
            if self.timer >= 200:  # 300 ms
                self.active = False

    def desenhar(self, surface):
        if self.active:
            pygame.draw.line(surface, AZUL_CLARO, self.start_pos, self.end_pos, 5)  # Desenha a linha do laser

# Função para exibir o menu
def menu():
    fonte = pygame.font.Font(None, 74)
    texto_jogar = fonte.render("Jogar", True, PRETO)
    texto_titulo = fonte.render("Venha e Pense", True, PRETO)

    botao_jogar = pygame.Rect(LARGURA_TELA // 2 - 65, ALTURA_TELA //  2 + 45, 150, 75)

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

        tela.fill(MARROM)
        tela.blit(texto_titulo, (LARGURA_TELA // 2 - texto_titulo.get_width() // 2, ALTURA_TELA // 2 - 100))
        pygame.draw.rect(tela, AZUL, botao_jogar)
        tela.blit(texto_jogar, (LARGURA_TELA // 2 - texto_jogar.get_width() // 2, ALTURA_TELA // 2 + 50))
        pygame.display.flip()
        relógio.tick(FPS)


perguntas = [
    {"pergunta": "Qual é a capital do Brasil?", "alternativas": ["A) São Paulo", "B) Rio de Janeiro", "C) Brasília", "D) Belo Horizonte", "E) Porto Alegre"], "resposta": "C) Brasília"},
    {"pergunta": "Qual é o maior planeta do sistema solar?", "alternativas": ["A) Terra", "B) Saturno", "C) Júpiter", "D) Urano", "E) Netuno"], "resposta": "C) Júpiter"},
    # Adicionar mais perguntas aqui
]

def main():
    jogador = Jogador()
    plataformas = [pygame.Rect(0, ALTURA_TELA - 20, LARGURA_TELA, 20)]
    inimigos = []
    lasers = []
    fonte = pygame.font.Font(None, 74)
    fonte2 = pygame.font.Font(None, 38)
    texto_game_over = fonte.render("Você Morreu!", True, PRETO)
    texto_reiniciar = fonte2.render("pressione R para recomeçar", True, PRETO)

    pontuação = 0
    timer_spawn = 0  # Timer para spawn de inimigos
    taxa_spawn = random.randint(TAXA_MIN_SPAWN_INIMIGO, TAXA_MAX_SPAWN_INIMIGO)  # Taxa de spawn aleatória
    timer_pergunta = 0  # Timer para controlar o tempo de perguntas
    pergunta_atual = None  # Armazena a pergunta atual
    resposta_atual = None  # Armazena a resposta atual
    timer_resposta = 0  # Timer para controlar o tempo de resposta
    timer_espera_pergunta = 0  # Timer para controlar o tempo de espera entre perguntas

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1 and jogador.pode_atirar:
                    mouse_x, mouse_y = evento.pos
                    if pergunta_atual is not None:
                        for i, alternativa in enumerate(pergunta_atual["alternativas"]):
                            if mouse_x > 100 and mouse_x < 300 and mouse_y > 300 + i * 50 and mouse_y < 350 + i * 50:
                                if alternativa == resposta_atual:
                                    pontuação += 5
                                    pergunta_atual = None
                                    resposta_atual = None
                                    timer_resposta = 0
                                    timer_espera_pergunta = 20 * FPS  # Inicia o timer de espera de 20 segundos
                                else:
                                    jogador.morrer()
                    else:
                        for inimigo in inimigos:
                            if inimigo.rect.collidepoint(mouse_x, mouse_y):
                                inimigos.remove(inimigo)
                                pontuação += 1
                                lasers.append(Laser((jogador.rect.centerx, jogador.rect.centery), (mouse_x, mouse_y)))  # Cria um novo laser
                                jogador.pode_atirar = False  # Impede que o jogador atire novamente

        teclas = pygame.key.get_pressed()
        if jogador.vivo:
            if teclas[pygame.K_SPACE]:
                jogador.pular()
        else:
            if teclas[pygame.K_r]:
                main()  # Reinicia o jogo
            if teclas[pygame.K_ESCAPE]:
                pygame.quit()  # Sai do jogo

        jogador.atualizar()
        for inimigo in inimigos:
            inimigo.atualizar()

        if jogador.vivo:
            for inimigo in inimigos:
                if jogador.rect.colliderect(inimigo.rect):
                    if jogador.rect.bottom <= inimigo.rect.top + 10:
                        inimigos.remove(inimigo)
                        pontuação += 1
                    else:
                        jogador.morrer()

        tela.fill(MARROM)
        for plataforma in plataformas:
            pygame.draw.rect(tela, VERDE, plataforma)

        if jogador.vivo:
            pygame.draw.rect(tela, AZUL, jogador.rect)
        else:
            tela.blit(texto_game_over, (LARGURA_TELA // 2 - 150, ALTURA_TELA // 2 - 50))
            tela.blit(texto_reiniciar, (LARGURA_TELA // 2 - 200, ALTURA_TELA // 2 + 50))

        for inimigo in inimigos:
            pygame.draw.rect(tela, VERMELHO, inimigo.rect)

        for laser in lasers:
            laser.desenhar(tela)
            laser.atualizar(relógio.tick(FPS))  # Atualiza o timer do laser
            if not laser.active:
                lasers.remove(laser)
                jogador.pode_atirar = True  # Permite que o jogador atire novamente

        texto_pontuação = fonte.render("Pontuação: " + str(pontuação), True, PRETO)
        tela.blit(texto_pontuação , (10, 10))

        # Spawn de inimigos
        if pergunta_atual is None:
            timer_spawn += 1
            if timer_spawn >= taxa_spawn:
                timer_spawn = 0
                taxa_spawn = random.randint(TAXA_MIN_SPAWN_INIMIGO, TAXA_MAX_SPAWN_INIMIGO)  # Gera uma nova taxa de spawn
                velocidade_inimigo = random.randint(VELOCIDADE_MIN_INIMIGO, VELOCIDADE_MAX_INIMIGO)  # Velocidade aleatória do inimigo
                inimigos.append(Inimigo(LARGURA_TELA, ALTURA_TELA - ALTURA_INIMIGO, velocidade_inimigo))

        # Exibe a pergunta e as alternativas
        timer_pergunta += 1
        if timer_espera_pergunta > 0:
            timer_espera_pergunta -= 1
        elif pergunta_atual is None:
            pergunta_atual = random.choice(perguntas)
            resposta_atual = pergunta_atual["resposta"]
            timer_resposta = 30 * FPS
        if pergunta_atual is not None:
            fonte_pergunta = pygame.font.Font(None, 24)
            texto_pergunta = fonte_pergunta.render(pergunta_atual["pergunta"], True, PRETO)
            tela.blit(texto_pergunta, (100, 250))
            for i, alternativa in enumerate(pergunta_atual["alternativas"]):
                texto_alternativa = fonte_pergunta.render(alternativa, True, PRETO)
                tela.blit(texto_alternativa, (100, 300 + i * 50))
            timer_resposta -= 1
            texto_timer = fonte_pergunta.render(str(timer_resposta // FPS), True, PRETO)
            tela.blit(texto_timer, (LARGURA_TELA - 50, 10))
            if timer_resposta <= 0:
                jogador.morrer()
                pergunta_atual = None
                resposta_atual = None
                timer_resposta = 0

        pygame.display.flip()
        relógio.tick(FPS)

if __name__ == "__main__":
    menu()
    main()