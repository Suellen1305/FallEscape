import pygame
import sys
import random

# Inicializa o Pygame
pygame.init()

# Configurações da tela
largura_tela = 800
altura_tela = 600
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption('Jogo do Bloco')

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AZUL = (0, 0, 128)

# Carregar a imagem de fundo
try:
    fundo = pygame.image.load(r'C:\Users\Suell\Downloads\ProjetoGame2d\FallEscape\dist\assets\fundo.jpg')  # Substitua pelo seu arquivo de fundo
    fundo = pygame.transform.scale(fundo, (largura_tela, altura_tela))  # Ajusta o fundo para a tela
except Exception as e:
    print(f"Erro ao carregar a imagem de fundo: {e}")
    fundo = None  # Se a imagem não puder ser carregada, fundo será None

# Bloco representando o personagem
bloco = pygame.Surface((50, 50))  # Um bloco de 50x50 pixels
bloco.fill(BRANCO)  # Cor do bloco (branco)
bloco_rect = bloco.get_rect()
bloco_rect.x = 100  # Posição inicial do bloco
bloco_rect.y = altura_tela - 150  # Posição inicial do bloco (no chão)

# Definir variáveis de movimento
velocidade_x = 5  # Velocidade de movimento horizontal
velocidade_y = 0  # Velocidade de movimento vertical
gravitacao = 0.5  # Gravidade
pulando = False  # Flag para pulo
pulo_forca = -15  # Força do pulo
velocidade_pulo_max = -12  # Velocidade máxima de pulo (evitar pulo muito alto)

# Carregar música de fundo
pygame.mixer.music.load(r'C:\Users\Suell\Downloads\ProjetoGame2d\FallEscape\dist\assets\musica_fundo.mp3')  # Coloque a sua música de fundo
pygame.mixer.music.play(-1, 0.0)  # Reproduz a música em loop (-1)

# Obstáculos
obstaculos = []
obstaculo_largura = 50
obstaculo_altura = 50
obstaculo_velocidade = 5  # Velocidade dos obstáculos


# Função para gerar obstáculos
def gerar_obstaculos():
    if len(obstaculos) == 0 or obstaculos[-1].x < largura_tela - 300:
        altura_obstaculo = random.randint(50, 150)  # Altura aleatória do obstáculo
        obstaculos.append(
            pygame.Rect(largura_tela, altura_tela - altura_obstaculo - 50, obstaculo_largura, altura_obstaculo))


# Função para desenhar o menu
def menu():
    font = pygame.font.SysFont(None, 55)
    texto = font.render("Pressione ENTER para começar", True, BRANCO)
    texto_rect = texto.get_rect(center=(largura_tela // 2, altura_tela // 2))

    sair_texto = font.render("Pressione ESC para sair", True, BRANCO)
    sair_texto_rect = sair_texto.get_rect(center=(largura_tela // 2, altura_tela // 2 + 100))

    rodando = True
    while rodando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return 'jogo'  # Retorna o estado de 'jogo' quando pressionar ENTER
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # Preenche a tela com fundo e desenha o texto do menu
        tela.fill(PRETO)
        if fundo:
            tela.blit(fundo, (0, 0))  # Desenha o fundo
        else:
            pygame.draw.rect(tela, AZUL, (0, 0, largura_tela, altura_tela))  # Cor de fundo azul, caso não tenha imagem
        tela.blit(texto, texto_rect)
        tela.blit(sair_texto, sair_texto_rect)

        pygame.display.update()
        pygame.time.Clock().tick(60)


# Função para desenhar a tela de Game Over
def game_over():
    font = pygame.font.SysFont(None, 55)
    texto = font.render("GAME OVER", True, BRANCO)
    texto_rect = texto.get_rect(center=(largura_tela // 2, altura_tela // 2 - 50))

    reiniciar_texto = font.render("Pressione N para reiniciar", True, BRANCO)  # Mudando o texto para 'N'
    reiniciar_texto_rect = reiniciar_texto.get_rect(center=(largura_tela // 2, altura_tela // 2 + 50))

    rodando = True
    while rodando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:  # Mudando de 'pygame.K_r' para 'pygame.K_n'
                    return 'jogo'  # Retorna 'jogo' se pressionar N
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # Preenche a tela com fundo e desenha o texto de Game Over
        tela.fill(PRETO)
        if fundo:
            tela.blit(fundo, (0, 0))  # Desenha o fundo
        tela.blit(texto, texto_rect)
        tela.blit(reiniciar_texto, reiniciar_texto_rect)

        pygame.display.update()
        pygame.time.Clock().tick(60)


# Função principal do jogo
def jogo():
    global bloco_rect, velocidade_y, pulando, obstaculos

    clock = pygame.time.Clock()
    rodando = True

    while rodando:
        # Verificando os eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not pulando:
                    velocidade_y = pulo_forca
                    pulando = True

        # Movimentação horizontal (esquerda/direita)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            bloco_rect.x -= velocidade_x
        if keys[pygame.K_RIGHT]:
            bloco_rect.x += velocidade_x

        # Movimento e física do pulo
        if pulando:
            velocidade_y += gravitacao  # Aplica a gravidade
            bloco_rect.y += velocidade_y

            # Se o bloco atingir o chão ou ultrapassar o limite do pulo
            if bloco_rect.y >= altura_tela - 150:
                bloco_rect.y = altura_tela - 150
                pulando = False
                velocidade_y = 0
        else:
            # Se não estiver pulando, faz o bloco permanecer no chão
            if bloco_rect.y < altura_tela - 150:
                bloco_rect.y += velocidade_y
                velocidade_y += gravitacao  # Aplique a gravidade até que o bloco chegue ao chão

        # Preencher a tela com a cor de fundo
        tela.fill(PRETO)
        if fundo:
            tela.blit(fundo, (0, 0))  # Desenha o fundo
        else:
            pygame.draw.rect(tela, AZUL, (0, 0, largura_tela, altura_tela))  # Cor de fundo azul, caso não tenha imagem

        # Desenha o bloco na tela
        tela.blit(bloco, bloco_rect)

        # Geração e movimento dos obstáculos
        gerar_obstaculos()
        for obstaculo in obstaculos:
            obstaculo.x -= obstaculo_velocidade  # Movimento dos obstáculos

            pygame.draw.rect(tela, (255, 0, 0), obstaculo)  # Desenha os obstáculos

            # Verifica se o bloco colidiu com o obstáculo
            if bloco_rect.colliderect(obstaculo):
                return 'game_over'  # Retorna 'game_over' se colidir com o obstáculo

            # Remove obstáculos que saíram da tela
            if obstaculo.x < -obstaculo_largura:
                obstaculos.remove(obstaculo)

        # Atualiza a tela
        pygame.display.update()

        # Controla a taxa de quadros (FPS)
        clock.tick(60)

    pygame.quit()
    sys.exit()


# Função principal que controla o fluxo de estados
def principal():
    estado = 'menu'
    while True:
        if estado == 'menu':
            estado = menu()  # Chama o menu
        elif estado == 'jogo':
            estado = jogo()  # Chama o jogo
        elif estado == 'game_over':
            estado = game_over()  # Chama o game over


# Iniciar o jogo
principal()
