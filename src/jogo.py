import pygame

from src.config import (
    LARGURA_TELA,
    ALTURA_TELA,
    FPS,
    TITULO_JOGO,
    CINZA,
    CAMINHO_RECORDE,
    CAMINHO_SPRITES,
)

from src.funcoes import (
    calcular_pontos,
    jogador_perdeu,
    limitar_valor,
    verificar_colisao,
    tomar_dano,
)
from src.sprites import pegar_sprite
from src.dados import (
    salvar_recorde,
    carregar_recorde,
)


def executar_jogo():
    """Executa o loop principal do jogo e controla estado, colisões e pontuação."""
    pygame.init()
    
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption(TITULO_JOGO)

    relogio = pygame.time.Clock()
    rodando = True

    # 1. Carregando as imagens recortadas do Spritesheet
    # Jogador (Dinossauro) - Posição aproximada dele na folha branca
    player_image = pegar_sprite(CAMINHO_SPRITES, x=40, y=45, width=67, height=68, scale=0.6)

    # Obstáculo Terrestre (Cacto) - Substituindo a imagem antiga do morcego por um cacto real
    bat_image    = pegar_sprite(CAMINHO_SPRITES, x=339, y=379, width=62, height=60, scale=0.8)
    
    # Item Coletável (Pássaro/Pterodáctilo) - Substituindo a gema antiga por um obstáculo/item aéreo
    gem_image    = pegar_sprite(CAMINHO_SPRITES, x=342, y=252, width=44, height=62, scale=0.6)
    
    # 2. Criando a estrutura de Sprites usando Dicionários
    jogador = {
        "imagem": player_image,
        "rect": player_image.get_rect(topleft=(100, 100))
    }

    gema = {
        "imagem": gem_image,
        "rect": gem_image.get_rect(topleft=(500, 300))
    }
    
    inimigo = {
        "imagem": bat_image,
        "rect": bat_image.get_rect(topleft=(200, 500))
    }

    velocidade = 5
    pontos = 0
    vidas = 3
    recorde = carregar_recorde(CAMINHO_RECORDE)

    # --- VARIÁVEIS DE FÍSICA PARA CORRIDA INFINITA ---
    gravidade = 0.6
    velocidade_y = 0
    esta_no_chao = True
    posicao_chao = ALTURA_TELA - 50  

    # Posiciona o jogador fixo no chão à esquerda
    jogador["rect"].bottom = posicao_chao
    jogador["rect"].x = 80

    # Posiciona o inimigo (obstáculo) para surgir na ponta direita
    inimigo["rect"].bottom = posicao_chao
    inimigo["rect"].x = LARGURA_TELA

    # Coloca a gema flutuando para ser coletada no ar durante o pulo
    gema["rect"].y = posicao_chao - 120
    gema["rect"].x = LARGURA_TELA + 300

    # Loop principal: processa entrada, atualiza estado e renderiza a cena.
    while rodando:
        relogio.tick(FPS)

        # Captura de Eventos do Sistema
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        teclas = pygame.key.get_pressed()

        # --- MECÂNICA DE PULO (BOTÃO ESPAÇO OU SETA PARA CIMA) ---
        if (teclas[pygame.K_SPACE] or teclas[pygame.K_UP]) and esta_no_chao:
            velocidade_y = -13  # Força do pulo (impulso para cima)
            esta_no_chao = False

        # Aplicação da Gravidade
        if not esta_no_chao:
            velocidade_y += gravidade
            jogador["rect"].y += velocidade_y

            # Detecta se pousou no chão
            if jogador["rect"].bottom >= posicao_chao:
                jogador["rect"].bottom = posicao_chao
                velocidade_y = 0
                esta_no_chao = True

        # --- MOVIMENTAÇÃO DOS OBSTÁCULOS E ITENS (CORRENDO DA DIREITA PARA ESQUERDA) ---
        inimigo["rect"].x -= velocidade
        gema["rect"].x -= velocidade

        # Se o inimigo sair da tela pela esquerda, ele renasce na direita
        if inimigo["rect"].right < 0:
            inimigo["rect"].x = LARGURA_TELA + 50
            pontos = calcular_pontos(pontos, 5) # Pontos por desviar

        # Se a gema sair da tela, renasce na direita
        if gema["rect"].right < 0:
            gema["rect"].x = LARGURA_TELA + 400

        # --- VERIFICAÇÃO DE COLISÕES ---
        # Colisão com a Gema (Item Colecionável)
        if verificar_colisao(jogador["rect"], gema["rect"]):
            pontos = calcular_pontos(pontos, 15) # Bônus por pegar o item
            gema["rect"].x = LARGURA_TELA + 600  # Joga ela de volta para trás

        # Colisão com o Inimigo (Obstáculo)
        if verificar_colisao(jogador["rect"], inimigo["rect"]):
            vidas = tomar_dano(vidas, 1)
            inimigo["rect"].x = LARGURA_TELA + 100 # Afasta o inimigo para não perder tudo de uma vez

        # Regras de fim de jogo e recorde
        if jogador_perdeu(vidas):
            rodando = False

        if pontos > recorde:
            recorde = pontos
            salvar_recorde(CAMINHO_RECORDE, recorde)

        pygame.display.set_caption(
            f"{TITULO_JOGO} | Pontos: {pontos} | Recorde: {recorde} | Vidas: {vidas}"
        )

        tela.fill(CINZA)

        # Desenhando os elementos na tela passando a imagem e o rect de cada dicionário
        tela.blit(gema["imagem"], gema["rect"])
        tela.blit(inimigo["imagem"], inimigo["rect"])
        tela.blit(jogador["imagem"], jogador["rect"])

        pygame.display.flip()

    pygame.quit()