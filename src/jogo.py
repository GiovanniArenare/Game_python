import pygame
import random

from src.config import (
    LARGURA_TELA,
    ALTURA_TELA,
    FPS,
    TITULO_JOGO,
    COR_FUNDO,
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
    """Executa o loop principal do jogo e controla os estados: MENU, JOGANDO e GAME_OVER."""
    pygame.init()
    
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption(TITULO_JOGO)

    relogio = pygame.time.Clock()
    rodando = True
    
    # --- MÁQUINA DE ESTADOS DO JOGO ---
    estado = "MENU"  # Pode ser "MENU", "JOGANDO" ou "GAME_OVER"

    # 1. Carregando as imagens recortadas do Spritesheet e Fundos
    player_image = pegar_sprite(CAMINHO_SPRITES, x=40, y=46, width=67, height=68, scale=0.8)
    bat_image    = pegar_sprite(CAMINHO_SPRITES, x=339, y=379, width=62, height=60, scale=1)
    gem_image    = pegar_sprite(CAMINHO_SPRITES, x=342, y=252, width=44, height=62, scale=0.6)
    
    # Recorte da sua nuvem customizada
    nuvem_image  = pegar_sprite(CAMINHO_SPRITES, x=760, y=246, width=208, height=91, scale=0.6)
    
    imagem_original = pygame.image.load("assets/imagens/gameover.jpg").convert()
    fundo_game_over = pygame.transform.scale(imagem_original, (LARGURA_TELA, ALTURA_TELA))
    bg_original = pygame.image.load("assets/imagens/fundo.png").convert()
    fundo_jogo = pygame.transform.scale(bg_original, (LARGURA_TELA, ALTURA_TELA))

    # 2. Criando a estrutura de Sprites (Dicionários)
    jogador = {
        "imagem": player_image,
        "rect": player_image.get_rect()
    }
    gema = {"imagem": gem_image, "rect": gem_image.get_rect()}
    nuvem = {"imagem": nuvem_image, "rect": nuvem_image.get_rect()}
    
    # Lista dinâmica para os cactos aleatórios (Substitui o inimigo único antigo)
    inimigos_na_tela = []

    # Configuração do surgimento (spawn) de obstáculos
    tempo_ultimo_spawn = 0
    intervalo_spawn = 1500  # Tempo em milissegundos

    # Variáveis de Jogo
    velocidade = 6  
    pontos = 0
    vidas = 3
    recorde = carregar_recorde(CAMINHO_RECORDE)
    tempo_inicio = 0
    tempo_sobrevivencia = 0

    # Variáveis de Física do Pulo
    gravidade_base = 0.6
    velocidade_y = 0
    esta_no_chao = True
    posicao_chao = ALTURA_TELA - 50  

    # --- PREPARANDO AS POSIÇÕES INICIAIS ANTES DO LOOP ---
    jogador["rect"].bottom = posicao_chao
    jogador["rect"].x = 80

    gema["rect"].y = posicao_chao - 120
    gema["rect"].x = LARGURA_TELA + 300

    # Posição inicial da Nuvem no céu
    nuvem["rect"].x = LARGURA_TELA  
    nuvem["rect"].y = 50            
    velocidade_nuvem = 2  # Mais lenta que o cenário para dar sensação de profundidade

    # Configuração de Fontes (Para textos na tela)
    fonte_titulo = pygame.font.SysFont("Arial", 60, bold=True)
    fonte_texto = pygame.font.SysFont("Arial", 30)

    # Loop principal: processa entrada, atualiza estado e renderiza a cena.
    while rodando:
        relogio.tick(FPS)

        # 1. CAPTURA DE EVENTOS DO SISTEMA
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            
            if evento.type == pygame.KEYDOWN:
                # Se estiver no MENU, aperta Espaço para começar de fato
                if estado == "MENU":
                    if evento.key == pygame.K_SPACE:
                        estado = "JOGANDO"
                        tempo_inicio = pygame.time.get_ticks()
                        tempo_ultimo_spawn = pygame.time.get_ticks()  # Sincroniza o timer
                
                # Se perdeu, R reinicia ou ESC fecha
                elif estado == "GAME_OVER":
                    if evento.key == pygame.K_r:
                        vidas = 3
                        pontos = 0
                        velocidade_y = 0
                        esta_no_chao = True
                        inimigos_na_tela.clear()  # Limpa os cactos antigos da tela
                        jogador["rect"].bottom = posicao_chao
                        jogador["rect"].x = 80
                        gema["rect"].x = LARGURA_TELA + 300
                        nuvem["rect"].x = LARGURA_TELA  # Reseta a nuvem para o início
                        estado = "JOGANDO"
                        tempo_inicio = pygame.time.get_ticks()  # Reinicia o cronômetro perfeitamente
                        tempo_sobrevivencia = 0
                        tempo_ultimo_spawn = pygame.time.get_ticks()
                    elif evento.key == pygame.K_ESCAPE:
                        rodando = False

        # 2. ATUALIZAÇÃO DA LÓGICA (Apenas se o estado for JOGANDO)
        if estado == "JOGANDO":
            # Atualiza o cronômetro convertendo milissegundos em segundos
            tempo_sobrevivencia = (pygame.time.get_ticks() - tempo_inicio) // 1000
            teclas = pygame.key.get_pressed()

            # --- MOVIMENTAÇÃO DA NUVEM EM SEGUNDO PLANO ---
            nuvem["rect"].x -= velocidade_nuvem
            if nuvem["rect"].right < 0:
                nuvem["rect"].x = LARGURA_TELA
                nuvem["rect"].y = random.randint(20, 80)  # Varia de leve a altura no céu

            # --- MECÂNICA DE PULO VARIÁVEL ---
            # Impulso inicial ao apertar o botão (no chão)
            if (teclas[pygame.K_SPACE] or teclas[pygame.K_UP]) and esta_no_chao:
                velocidade_y = -10  
                esta_no_chao = False

            # No ar: Altera a gravidade se continuar segurando o botão
            if not esta_no_chao:
                if (teclas[pygame.K_SPACE] or teclas[pygame.K_UP]) and velocidade_y < 0:
                    gravidade_atual = 0.35  # Mais leve = pula mais alto
                else:
                    gravidade_atual = 0.75  # Mais pesada = cai rápido ao soltar

                velocidade_y += gravidade_atual
                jogador["rect"].y += velocidade_y

                # Detecta colisão com a linha do chão
                if jogador["rect"].bottom >= posicao_chao:
                    jogador["rect"].bottom = posicao_chao
                    velocidade_y = 0
                    esta_no_chao = True
            else:
                jogador["rect"].bottom = posicao_chao
                jogador["rect"].x = 80

            # --- MECANISMO DE SPAWN ALEATÓRIO DE CACTOS ---
            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - tempo_ultimo_spawn > intervalo_spawn:
                # Sorteia se vem 1 cacto sozinho ou 2 cactos grudados
                tipo_spawn = random.choice(["UNICO", "UNICO", "UNICO", "DUPLO"])
                
                if tipo_spawn == "UNICO":
                    novo_cacto = bat_image.get_rect()
                    novo_cacto.bottom = posicao_chao
                    novo_cacto.x = LARGURA_TELA
                    inimigos_na_tela.append(novo_cacto)
                
                elif tipo_spawn == "DUPLO":
                    cacto1 = bat_image.get_rect()
                    cacto1.bottom = posicao_chao
                    cacto1.x = LARGURA_TELA
                    
                    cacto2 = bat_image.get_rect()
                    cacto2.bottom = posicao_chao
                    cacto2.x = LARGURA_TELA + cacto1.width - 5  # Cola os dois cactos perfeitamente
                    
                    inimigos_na_tela.append(cacto1)
                    inimigos_na_tela.append(cacto2)
                
                # Gera uma distância variada para o próximo grupo
                intervalo_spawn = random.randint(1000, 2200)
                tempo_ultimo_spawn = tempo_atual

            # --- ATUALIZAÇÃO DA GEMA COLETÁVEL ---
            gema["rect"].x -= velocidade
            if gema["rect"].right < 0:
                gema["rect"].x = LARGURA_TELA + random.randint(400, 900)
                gema["rect"].y = posicao_chao - 120

            if verificar_colisao(jogador["rect"], gema["rect"]):
                pontos = calcular_pontos(pontos, 15)
                gema["rect"].x = LARGURA_TELA + 600  

            # --- ATUALIZAÇÃO E COLISÃO DOS CACTOS (LISTA) ---
            for cacto_rect in inimigos_na_tela[:]:
                cacto_rect.x -= velocidade
                
                # Se o Dino colidir com o cacto
                if verificar_colisao(jogador["rect"], cacto_rect):
                    vidas = tomar_dano(vidas, 1)
                    inimigos_na_tela.remove(cacto_rect)
                    continue
                
                # Se passou ileso, ganha pontos por desviar
                if cacto_rect.right < 0:
                    pontos = calcular_pontos(pontos, 5)
                    inimigos_na_tela.remove(cacto_rect)

            # --- VERIFICAÇÃO DE FIM DE JOGO E RECORDE ---
            if jogador_perdeu(vidas):
                if pontos > recorde:
                    recorde = pontos
                    salvar_recorde(CAMINHO_RECORDE, recorde)
                estado = "GAME_OVER"

        # 3. RENDERIZAÇÃO (DESENHO NA TELA)
        tela.fill(COR_FUNDO)

        if estado == "MENU":
            txt_titulo = fonte_titulo.render("Sonica Runner", True, (83, 83, 83))
            txt_instrucao = fonte_texto.render("Aperte ESPAÇO para Começar", True, (100, 100, 100))
            txt_recorde = fonte_texto.render(f"Melhor Pontuação: {recorde}", True, (50, 50, 50))
            
            tela.blit(txt_titulo, (LARGURA_TELA // 2 - 185, ALTURA_TELA // 2 - 80))
            tela.blit(txt_instrucao, (LARGURA_TELA // 2 - 180, ALTURA_TELA // 2 + 20))
            tela.blit(txt_recorde, (LARGURA_TELA // 2 - 140, ALTURA_TELA // 2 + 80))

        elif estado == "JOGANDO":
            tela.blit(fundo_jogo, (0, 0))
            tela.blit(nuvem["imagem"], nuvem["rect"])
            tela.blit(gema["imagem"], gema["rect"])
            for cacto_rect in inimigos_na_tela:
                tela.blit(bat_image, cacto_rect)
            tela.blit(jogador["imagem"], jogador["rect"])
            
            # 3ª CAMADA: Interface de Usuário (HUD dos Corações e Texto)
            for i in range(vidas):
                origem_x = 30 + i * 50  
                pygame.draw.circle(tela, (255, 40, 40), (origem_x, 35), 10)
                pygame.draw.circle(tela, (255, 40, 40), (origem_x + 14, 35), 10)
                pygame.draw.polygon(tela, (255, 40, 40), [(origem_x - 10, 38), (origem_x + 24, 38), (origem_x + 7, 58)])

            texto_tempo = fonte_texto.render(f"Tempo: {tempo_sobrevivencia}s", True, (255, 255, 255))
            tela.blit(texto_tempo, (20, 80))

            texto_pontos = fonte_texto.render(f"Pontos: {pontos}", True, (255, 215, 0))
            tela.blit(texto_pontos, (20, 120))
            
        elif estado == "GAME_OVER":
            tela.blit(fundo_game_over, (0, 0)) 
            txt_fim = fonte_titulo.render("GAME OVER", True, (255, 60, 60))
            txt_pts = fonte_texto.render(f"Pontos Finais: {pontos}", True, (255, 255, 255))
            txt_tempo = fonte_texto.render(f"Tempo Vivo: {tempo_sobrevivencia}s", True, (255, 255, 255))
            txt_reset = fonte_texto.render("Aperte R para Reiniciar \nOu ESC para Sair", True, (255, 255, 255))
            
            tela.blit(txt_fim, (LARGURA_TELA // 2 - 385, ALTURA_TELA // 2 - 200))
            tela.blit(txt_pts, (LARGURA_TELA // 2 - 360, ALTURA_TELA // 2 - 100))
            tela.blit(txt_tempo, (LARGURA_TELA // 2 - 360, ALTURA_TELA // 2 - 50))
            tela.blit(txt_reset, (LARGURA_TELA // 2 - 360, ALTURA_TELA // 2 ))

        pygame.display.flip()

    pygame.quit()