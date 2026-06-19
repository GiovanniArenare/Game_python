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
    # --- CONFIGURAÇÃO DE BUFFER (Evita atraso no som do pulo e do dano) ---
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()
    pygame.mixer.init()
    
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption(TITULO_JOGO)

    relogio = pygame.time.Clock()
    rodando = True
    
    # --- MÁQUINA DE ESTADOS DO JOGO ---
    estado = "MENU"  # Pode ser "MENU", "JOGANDO" ou "GAME_OVER"

    # 2. CARREGAMENTO DE IMAGENS E FUNDOS
    player_image = pegar_sprite(CAMINHO_SPRITES, x=42, y=47, width=64, height=65, scale=0.8)
    bat_image    = pegar_sprite(CAMINHO_SPRITES, x=339, y=379, width=60, height=60, scale=1)
    gem_image    = pegar_sprite(CAMINHO_SPRITES, x=342, y=252, width=44, height=62, scale=0.6)
    nuvem_image  = pegar_sprite(CAMINHO_SPRITES, x=760, y=246, width=208, height=91, scale=0.6)
    
    # Fundo do Menu (Início)
    img_menu = pygame.image.load("assets/imagens/menu.jpg").convert()
    fundo_menu = pygame.transform.scale(img_menu, (LARGURA_TELA, ALTURA_TELA))

    # Fundo do Jogo (Gameplay)
    bg_original = pygame.image.load("assets/imagens/fundo.png").convert()
    fundo_jogo = pygame.transform.scale(bg_original, (LARGURA_TELA, ALTURA_TELA))

    # Fundo do Game Over
    imagem_original = pygame.image.load("assets/imagens/gameover.jpg").convert()
    fundo_game_over = pygame.transform.scale(imagem_original, (LARGURA_TELA, ALTURA_TELA))

    # 3. CARREGAMENTO DOS SONS
    try:
        som_coleta = pygame.mixer.Sound("assets/sons/coin.wav")
        som_dano = pygame.mixer.Sound("assets/sons/oof.wav")
        som_pulo = pygame.mixer.Sound("assets/sons/jump.wav")         # Novo som de pulo
        som_gameover = pygame.mixer.Sound("assets/sons/gameover.wav") # Novo som de game over
        
        som_coleta.set_volume(0.5)
        som_dano.set_volume(0.6)
        som_pulo.set_volume(0.5)
        som_gameover.set_volume(0.6)
        
        # --- CARREGAR E TOCAR A MÚSICA DE FUNDO EM LOOP (-1) ---
        pygame.mixer.music.load("assets/sons/musica_fundo.mp3")
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1) # O -1 faz ela tocar infinitamente através dos estados
        
    except pygame.error:
        print("Aviso: Arquivos de áudio não encontrados em assets/sons/. O jogo rodará mudo.")
        som_coleta = som_dano = som_pulo = som_gameover = None

    # 4. ESTRUTURAS DE SPRITES
    jogador = {"imagem": player_image, "rect": player_image.get_rect()}
    gema = {"imagem": gem_image, "rect": gem_image.get_rect()}
    nuvem = {"imagem": nuvem_image, "rect": nuvem_image.get_rect()}
    inimigos_na_tela = []

    # VARIÁVEIS DE JOGO
    velocidade = 6  
    pontos = 0
    vidas = 3
    recorde = carregar_recorde(CAMINHO_RECORDE)
    tempo_inicio = 0
    tempo_sobrevivencia = 0
    tempo_ultimo_spawn = 0
    intervalo_spawn = 1500
    posicao_chao = ALTURA_TELA - 50  

    # FÍSICA E POSIÇÕES
    velocidade_y = 0
    esta_no_chao = True
    jogador["rect"].bottom = posicao_chao
    jogador["rect"].x = 80
    gema["rect"].y = posicao_chao - 120
    gema["rect"].x = LARGURA_TELA + 300
    nuvem["rect"].x = LARGURA_TELA  
    nuvem["rect"].y = 50            
    velocidade_nuvem = 2  

    fonte_titulo = pygame.font.SysFont("Arial", 60, bold=True)
    fonte_texto = pygame.font.SysFont("Arial", 30)

    # --- LOOP PRINCIPAL ---
    while rodando:
        relogio.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            
            if evento.type == pygame.KEYDOWN:
                if estado == "MENU":
                    if evento.key == pygame.K_SPACE:
                        estado = "JOGANDO"
                        tempo_inicio = pygame.time.get_ticks()
                        tempo_ultimo_spawn = pygame.time.get_ticks()
                
                elif estado == "GAME_OVER":
                    if evento.key == pygame.K_r:
                        vidas = 3
                        pontos = 0
                        velocidade_y = 0
                        esta_no_chao = True
                        inimigos_na_tela.clear()
                        jogador["rect"].bottom = posicao_chao
                        gema["rect"].x = LARGURA_TELA + 300
                        nuvem["rect"].x = LARGURA_TELA
                        
                        # --- REINICIAR A MÚSICA DE FUNDO AO RECOMEÇAR O JOGO ---
                        if pygame.mixer.music.get_busy() == False:
                            pygame.mixer.music.play(-1)
                            
                        estado = "JOGANDO"
                        tempo_inicio = pygame.time.get_ticks()
                        tempo_sobrevivencia = 0
                        tempo_ultimo_spawn = pygame.time.get_ticks()
                    elif evento.key == pygame.K_ESCAPE:
                        rodando = False

        if estado == "JOGANDO":
            tempo_sobrevivencia = (pygame.time.get_ticks() - tempo_inicio) // 1000
            teclas = pygame.key.get_pressed()

            # Movimento Nuvem
            nuvem["rect"].x -= velocidade_nuvem
            if nuvem["rect"].right < 0:
                nuvem["rect"].x = LARGURA_TELA
                nuvem["rect"].y = random.randint(20, 80)

            # Pulo Variável
            if (teclas[pygame.K_SPACE] or teclas[pygame.K_UP]) and esta_no_chao:
                velocidade_y = -10  
                esta_no_chao = False
                # --- TOCAR SOM DE PULO ---
                if som_pulo: 
                    som_pulo.play()

            if not esta_no_chao:
                gravidade = 0.35 if ((teclas[pygame.K_SPACE] or teclas[pygame.K_UP]) and velocidade_y < 0) else 0.75
                velocidade_y += gravidade
                jogador["rect"].y += velocidade_y
                if jogador["rect"].bottom >= posicao_chao:
                    jogador["rect"].bottom = posicao_chao
                    velocidade_y = 0
                    esta_no_chao = True

            # Spawn Inimigos
            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - tempo_ultimo_spawn > intervalo_spawn:
                tipo_spawn = random.choice(["UNICO", "UNICO", "UNICO", "DUPLO"])
                if tipo_spawn == "UNICO":
                    n = bat_image.get_rect(bottom=posicao_chao, x=LARGURA_TELA)
                    inimigos_na_tela.append(n)
                elif tipo_spawn == "DUPLO":
                    c1 = bat_image.get_rect(bottom=posicao_chao, x=LARGURA_TELA)
                    c2 = bat_image.get_rect(bottom=posicao_chao, x=LARGURA_TELA + c1.width - 5)
                    inimigos_na_tela.extend([c1, c2])
                intervalo_spawn = random.randint(1000, 2200)
                tempo_ultimo_spawn = tempo_atual

            # Gema e Colisão
            gema["rect"].x -= velocidade
            if gema["rect"].right < 0: gema["rect"].x = LARGURA_TELA + random.randint(400, 900)
            if verificar_colisao(jogador["rect"], gema["rect"]):
                pontos = calcular_pontos(pontos, 15)
                if som_coleta: som_coleta.play()
                gema["rect"].x = LARGURA_TELA + 600  

            # Cactos e Colisão
            for cacto_rect in inimigos_na_tela[:]:
                cacto_rect.x -= velocidade
                if verificar_colisao(jogador["rect"], cacto_rect):
                    vidas = tomar_dano(vidas, 1)
                    if som_dano: som_dano.play()
                    inimigos_na_tela.remove(cacto_rect)
                    continue
                if cacto_rect.right < 0:
                    pontos = calcular_pontos(pontos, 5)
                    inimigos_na_tela.remove(cacto_rect)

            if jogador_perdeu(vidas):
                if pontos > recorde: salvar_recorde(CAMINHO_RECORDE, pontos)
                
                # --- PARAR MÚSICA E TOCAR SOM DE GAME OVER UMA VEZ ---
                pygame.mixer.music.stop()
                if som_gameover: 
                    som_gameover.play()
                    
                estado = "GAME_OVER"

        # --- RENDERIZAÇÃO ---
        if estado == "MENU":
            # 1. Desenha o fundo da foto de início
            tela.blit(fundo_menu, (0, 0))
            
            # 2. Desenha os textos por cima da foto
            txt_instrucao = fonte_texto.render("Aperte ESPAÇO para Começar", True, (240, 240, 240))
            txt_recorde = fonte_texto.render(f"Melhor Pontuação: {recorde}", True, (255, 215, 0))
            contorno_instrucao = fonte_texto.render("Aperte ESPAÇO para Começar", True, (0, 0, 0))
            contorno_recorde = fonte_texto.render(f"Melhor Pontuação: {recorde}", True, (0, 0, 0))
            
            pos_ins_x = LARGURA_TELA // 2 - 360
            pos_ins_y = ALTURA_TELA // 2 + 70
            
            pos_rec_x = LARGURA_TELA // 2 - 360
            pos_rec_y = ALTURA_TELA // 2 + 25

            # 3. Desenha o contorno e o texto do Recorde primeiro (pois a coordenada Y é menor, fica mais acima)
            tela.blit(contorno_recorde, (pos_rec_x - 2, pos_rec_y))
            tela.blit(contorno_recorde, (pos_rec_x + 2, pos_rec_y))
            tela.blit(contorno_recorde, (pos_rec_x, pos_rec_y - 2))
            tela.blit(contorno_recorde, (pos_rec_x, pos_rec_y + 2))
            tela.blit(txt_recorde, (pos_rec_x, pos_rec_y))

            # 4. Desenha o contorno e o texto de Instrução (fica mais abaixo)
            tela.blit(contorno_instrucao, (pos_ins_x - 2, pos_ins_y))
            tela.blit(contorno_instrucao, (pos_ins_x + 2, pos_ins_y))
            tela.blit(contorno_instrucao, (pos_ins_x, pos_ins_y - 2))
            tela.blit(contorno_instrucao, (pos_ins_x, pos_ins_y + 2))
            tela.blit(txt_instrucao, (pos_ins_x, pos_ins_y))

        elif estado == "JOGANDO":
            tela.blit(fundo_jogo, (0, 0))
            tela.blit(nuvem["imagem"], nuvem["rect"])
            tela.blit(gema["imagem"], gema["rect"])
            for c in inimigos_na_tela: tela.blit(bat_image, c)
            tela.blit(jogador["imagem"], jogador["rect"])
            
            # 1. HUD Vidas (Corações com Contorno Preto)
            for i in range(vidas):
                origem_x = 30 + i * 50  
                origem_y = 35

                pygame.draw.circle(tela, (0, 0, 0), (origem_x, origem_y), 12)
                pygame.draw.circle(tela, (0, 0, 0), (origem_x + 14, origem_y), 12)
                pygame.draw.polygon(tela, (0, 0, 0), [
                    (origem_x - 12, origem_y + 3), 
                    (origem_x + 26, origem_y + 3), 
                    (origem_x + 7, origem_y + 22)
                ])

                pygame.draw.circle(tela, (255, 40, 40), (origem_x, origem_y), 10)
                pygame.draw.circle(tela, (255, 40, 40), (origem_x + 14, origem_y), 10)
                pygame.draw.polygon(tela, (255, 40, 40), [
                    (origem_x - 10, origem_y + 3), 
                    (origem_x + 24, origem_y + 3), 
                    (origem_x + 7, origem_y + 18)
                ])

            # 2. Renderiza os textos do HUD (Frente)
            texto_tempo = fonte_texto.render(f"Tempo: {tempo_sobrevivencia}s", True, (255, 255, 255))
            texto_pontos = fonte_texto.render(f"Pontos: {pontos}", True, (255, 215, 0))
            
            # Renderiza as bordas do HUD (Preto)
            contorno_tempo = fonte_texto.render(f"Tempo: {tempo_sobrevivencia}s", True, (0, 0, 0))
            contorno_pontos = fonte_texto.render(f"Pontos: {pontos}", True, (0, 0, 0))

            # --- COORDENADAS DO HUD ---
            pos_tempo_x, pos_tempo_y = 20, 80
            pos_pontos_x, pos_pontos_y = 20, 120

            # 3. Desenha o contorno e o texto do Tempo
            tela.blit(contorno_tempo, (pos_tempo_x - 2, pos_tempo_y))
            tela.blit(contorno_tempo, (pos_tempo_x + 2, pos_tempo_y))
            tela.blit(contorno_tempo, (pos_tempo_x, pos_tempo_y - 2))
            tela.blit(contorno_tempo, (pos_tempo_x, pos_tempo_y + 2))
            tela.blit(texto_tempo, (pos_tempo_x, pos_tempo_y))

            # 4. Desenha o contorno e o texto dos Pontos
            tela.blit(contorno_pontos, (pos_pontos_x - 2, pos_pontos_y))
            tela.blit(contorno_pontos, (pos_pontos_x + 2, pos_pontos_y))
            tela.blit(contorno_pontos, (pos_pontos_x, pos_pontos_y - 2))
            tela.blit(contorno_pontos, (pos_pontos_x, pos_pontos_y + 2))
            tela.blit(texto_pontos, (pos_pontos_x, pos_pontos_y))
            
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