import pygame
import sys

# Inicializar o pygame
pygame.init()

# Definir as dimensões da tela
largura_tela = 800
altura_tela = 600
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Jogo 2D Simples")

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AZUL = (0, 0, 255)

# Carregar o fundo
fundo = pygame.image.load('dist/assets/fundo.jpg')

# Música de fundo
pygame.mixer.music.load('dist/assets/musica_fundo.mp3')
pygame.mixer.music.play(-1, 0.0)  # Toca a música em loop

# Função do menu
def menu():
    rodando = True
    while rodando:
        tela.fill(PRETO)  # Cor de fundo preta
        if fundo:
            tela.blit(fundo, (0, 0))  # Desenha o fundo
        else:
            pygame.draw.rect(tela, AZUL, (0, 0, largura_tela, altura_tela))  # Cor de fundo azul

        fonte = pygame.font.Font(None, 74)
        texto_menu = fonte.render("Menu do Jogo", True, BRANCO)
        tela.blit(texto_menu, (largura_tela // 2 - texto_menu.get_width() // 2, 100))

        fonte_botao = pygame.font.Font(None, 50)
        texto_iniciar = fonte_botao.render("Iniciar Jogo", True, BRANCO)
        texto_sair = fonte_botao.render("Sair", True, BRANCO)

        # Botão Iniciar Jogo
        iniciar_rect = pygame.Rect(largura_tela // 2 - texto_iniciar.get_width() // 2, 250, texto_iniciar.get_width(), texto_iniciar.get_height())
        pygame.draw.rect(tela, AZUL, iniciar_rect)
        tela.blit(texto_iniciar, (largura_tela // 2 - texto_iniciar.get_width() // 2, 250))

        # Botão Sair
        sair_rect = pygame.Rect(largura_tela // 2 - texto_sair.get_width() // 2, 350, texto_sair.get_width(), texto_sair.get_height())
        pygame.draw.rect(tela, AZUL, sair_rect)
        tela.blit(texto_sair, (largura_tela // 2 - texto_sair.get_width() // 2, 350))

        pygame.display.update()

        # Ações no menu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if iniciar_rect.collidepoint(event.pos):  # Se o clique foi no botão "Iniciar"
                    print("Iniciar Jogo clicado")
                    jogo()
                if sair_rect.collidepoint(event.pos):  # Se o clique foi no botão "Sair"
                    rodando = False
                    pygame.quit()
                    sys.exit()

# Função do jogo
def jogo():
    rodando = True
    jogador = pygame.Rect(100, 500, 50, 50)  # Um bloco que representa o personagem
    velocidade = 5  # Velocidade do jogador
    pulo = -15  # Velocidade do pulo
    gravidade = 1  # Gravidade
    jump = False  # Flag de pulo

    while rodando:
        tela.fill(PRETO)
        if fundo:
            tela.blit(fundo, (0, 0))  # Desenha o fundo

        # Desenhar o personagem (bloco)
        pygame.draw.rect(tela, (0, 255, 0), jogador)  # Jogador representado por um bloco verde

        # Movimentação do personagem
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            jogador.x -= velocidade
        if keys[pygame.K_RIGHT]:
            jogador.x += velocidade
        if not jump:
            if keys[pygame.K_SPACE]:
                jump = True
        else:
            if jogador.y > 400:  # Se o bloco estiver no chão
                jogador.y += gravidade
            else:
                jump = False
                jogador.y += pulo

        # Verificar se o personagem saiu da tela
        if jogador.x < 0:
            jogador.x = 0
        elif jogador.x > largura_tela - jogador.width:
            jogador.x = largura_tela - jogador.width

        if jogador.y > altura_tela - jogador.height:  # Colisão com o chão
            jogador.y = altura_tela - jogador.height

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                sys.exit()

# Função principal para rodar o jogo
if __name__ == "__main__":
    menu()
