# Proposta Inicial do Jogo

Este documento apresenta a ideia inicial, escopo e planejamento para o desenvolvimento do jogo do grupo.

## 1. Nome provisório do jogo

> Sonica Runner

## 2. Integrantes do grupo

- Integrante 1: Carolina Almeida Mendes de Souza
- Integrante 2: Giovanni Arenare Mota
- Integrante 3: Gustavo Alberto Araujo de Sa

## 3. Tipo de jogo

> Corrida simples com obstáculos (Infinite Runner) — Paródia de Sonic

## 4. Descrição geral do jogo

O jogo se passa em um cenário bidimensional onde o fundo e o chão se movem continuamente para a esquerda, simulando que o personagem está correndo para a direita. Na tela, aparecerão o personagem principal, a pontuação atual, o recorde máximo e a quantidade de vidas. O jogador controla as ações de desvio do personagem. O objetivo é desviar dos obstáculos terrestres e aéreos que surgem aleatoriamente na tela. À medida que o tempo passa, a velocidade do cenário aumenta sutilmente, elevando o desafio.

## 5. Objetivo do jogador

Sobreviver pelo maior tempo possível, evitando os obstáculos para acumular a maior pontuação e superar o recorde máximo (High Score) registrado no sistema.

## 6. Regras principais

- **Regra 1:** O jogador inicia a partida com 3 vidas.
- **Regra 2:** A pontuação aumenta de forma contínua com base no tempo de sobrevivência e na coleta de itens.
- **Regra 3:** Cada colisão com um obstáculo (morcegos ou cactos) remove 1 vida do jogador.
- **Regra 4:** Após uma colisão, o jogador ganha um breve período de invulnerabilidade piscante para não perder todas as vidas de uma vez.
- **Regra 5:** A velocidade de deslocamento dos obstáculos aumenta sutilmente ao longo do tempo para elevar a dificuldade.

## 7. Condição de vitória

Por ser um jogo de corrida infinita, não há uma condição de vitória definitiva (fim de jogo por linha de chegada). A vitória pessoal do jogador consiste em superar o recorde (High Score) salvo no sistema.

## 8. Condição de derrota ou encerramento

A partida é encerrada imediatamente (tela de Game Over) quando o contador de vidas do jogador chega a zero.

## 9. Elementos previstos no jogo

### Jogador ou elemento principal
Um personagem posicionado no canto esquerdo da tela que possui comandos para pular e desviar dos perigos, interagindo diretamente com a física e gravidade simulada para o pulo.

### Obstáculos, inimigos ou desafios
Obstáculos terrestres estáticos que exigem um pulo preciso e obstáculos aéreos (como morcegos) em alturas variadas que exigem o cálculo do tempo correto de esquiva.

### Itens, alvos ou objetos de interação
Coelhos dourados (gemas) que aparecem esporadicamente na pista e, se coletados, concedem um bônus imediato de 15 pontos e emitem um efeito sonoro.

### Pontuação, vidas, tempo ou progresso
O jogo exibirá de forma nítida na interface (HUD): o Score Atual (cresce com o tempo), o High Score (carregado de um arquivo externo) e a quantidade de vidas representadas por ícones de corações com contorno estilizado.

## 10. Controles previstos

- **Seta para Cima ou Espaço:** Realizar o pulo do personagem.
- **Seta para Baixo:** Fazer o personagem se agachar (reduzir sua caixa de colisão).
- **ESC:** Sair do jogo na tela de Game Over.
- **Tecla R:** Reiniciar a partida quando o jogo acabar.

## 11. Organização do código

A estrutura modular do projeto está dividida da seguinte forma:
- `main.py` — Ponto de entrada do jogo que inicializa e executa o loop principal.
- `src/config.py` — Armazena todas as constantes do projeto (tamanho da tela, caminhos de pastas e FPS).
- `src/dados.py` — Funções responsáveis por carregar e salvar o recorde em um arquivo externo `.txt`.
- `src/sprites.py` — Função utilitária para recortar e escalar os sprites da folha de imagens principal.
- `src/funcoes.py` — Contém a lógica de cálculo de pontos, mecânica de dano, colisões e verificação de fim de jogo.

## 12. Recursos externos previstos

- Sprites customizados baseados na temática do jogo.
- Efeitos sonoros gratuitos (sons de pulo, dano, coleta e fim de jogo).
- Música de fundo em formato `.mp3` reproduzida em loop contínuo através das telas.

## 13. Principais dificuldades esperadas

- Ajuste fino da física de gravidade e colisão dos retângulos (Hitboxes).
- Sincronização e repetição contínua da música através da máquina de estados (Menu -> Jogo -> Game Over).
- Gerenciamento dinâmico de spawn e remoção dos obstáculos na tela.

## 14. Escopo mínimo para a entrega final

Um personagem capaz de pular, uma pista com geração contínua de obstáculos, detecção funcional de colisão, sistema de perda de vidas com interface gráfica, exibição da pontuação atual na tela e uma tela de Game Over funcional com opção de reinício rápido.

## 15. Possíveis melhorias, caso haja tempo

- Criação de uma tela de Menu inicial estilizada com imagem de fundo e contornos nos textos.
- Sistema automatizado que salva a maior pontuação persistente no computador do usuário.
- Inclusão de efeitos sonoros dedicados para cada ação e música de fundo dedicada.