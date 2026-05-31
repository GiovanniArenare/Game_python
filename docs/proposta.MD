# Proposta Inicial do Jogo

Este documento deve ser preenchido pelo grupo na Semana 1 do projeto.

A proposta deve apresentar uma ideia simples, clara e viável para ser desenvolvida com Python e Pygame dentro do prazo disponível.

## 1. Nome provisório do jogo

Escreva aqui o nome provisório do jogo.

> Sonica Runner

## 2. Integrantes do grupo

Liste os integrantes do grupo.

- Nome 1: Carolina Almeida Mendes de Souza
- Nome 2: Giovanni Arenare Mota
- Nome 3: Gustavo Alberto Araujo de Sa

## 3. Tipo de jogo

Indique o tipo de jogo que será desenvolvido.

Tipo escolhido pelo grupo:

> Corrida simples com obstáculos (Infinite Runner)

## 4. Descrição geral do jogo

Explique, em poucas linhas, como o jogo funcionará.

Descrição:

> O jogo se passa em um cenário bidimensional onde o fundo e o chão se movem continuamente para a esquerda, simulando que o personagem está correndo para a direita. Na tela, aparecerão o personagem principal, a pontuação atual, o recorde máximo e a quantidade de vidas. O jogador controla as ações de desvio do personagem. O objetivo é desviar dos obstáculos terrestres e aéreos que surgem aleatoriamente na tela. À medida que o tempo passa, a velocidade do cenário aumenta sutilmente, elevando o desafio.

## 5. Objetivo do jogador

Explique qual é o objetivo principal do jogador.

Objetivo:

> Sobreviver pelo maior tempo possível, evitando os obstáculos para acumular a maior pontuação e superar o recorde máximo (High Score) registrado.

## 6. Regras principais

Liste as principais regras do jogo.

Regras do grupo:

- Regra 1: O jogador inicia a partida com vidas limitadas.
- Regra 2: A pontuação aumenta de forma contínua com base no tempo de sobrevivência da corrida.
- Regra 3: Cada colisão com um obstáculo remove 1 vida do jogador.
- Regra 4: Após uma colisão, o jogador ganha um breve período de invulnerabilidade piscante para não perder todas as vidas de uma vez.
- Regra 5: A velocidade de deslocamento dos obstáculos aumenta a cada derterminado marco de pontos atingidos.

## 7. Condição de vitória

Explique como o jogador vence ou conclui o jogo.

Condição de vitória:

> Por ser um jogo de corrida infinita, não há uma condição de vitória definitiva (fim de jogo por chegada). A vitória pessoal do jogador consiste em superar o recorde (High Score) salvo no sistema.

## 8. Condição de derrota ou encerramento

Explique como o jogador perde ou quando a partida termina.

Condição de derrota ou encerramento:

> A partida é encerrada imediatamente (Game Over) quando o contador de vidas do jogador chega a zero.

## 9. Elementos previstos no jogo

Descreva os principais elementos que farão parte do jogo.

## Jogador ou elemento principal

Descrição:

> Um personagem posicionado no canto esquerdo da tela que possui comandos para pular e abaixar, simulando a esquiva dos perigos. Ele interage diretamente com a física da gravidade simulada para o pulo.

## Obstáculos, inimigos ou desafios

Descrição:

> Obstáculos terrestres estáticos (como cactos ou pedras) que exigem um pulo, e obstáculos aéreos em alturas variadas (como pássaros ou drones) que exigem que o jogador se abaixe ou calcule o tempo preciso do pulo.

## Itens, alvos ou objetos de interação

Descrição:

> Coelhos dourados que aparecem esporadicamente na pista e, se coletados, concedem um bônus imediato de 100 pontos.

## Pontuação, vidas, tempo ou progresso

Descrição:

> O jogo exibirá na parte superior da tela: o Score Atual (inteiro que cresce com o tempo), o High Score (carregado de um arquivo externo) e a quantidade de vidas representadas por ícones de corações.

## 10. Controles previstos

Informe os comandos que serão utilizados pelo jogador.

Controles do grupo:

- Tecla/comando: Seta para Cima ou Espaço (Realizar o pulo do personagem.)
- Tecla/comando: Seta para Baixo (Fazer o personagem se abaixar (reduzir sua caixa de colisão).)
- Tecla/comando: ESC (Pausar ou sair do jogo.)

## 11. Organização inicial do código

- `main.py` — ponto de entrada; inicializa o Pygame, cria a janela e chama o loop principal de src/jogo.py.
- `src/jogo.py` — contém o loop principal (while running), controle de estados (menu, jogando, game over) e renderização de cada frame.
- `src/funcoes.py` — funções auxiliares: detecção de colisão com pygame.Rect, cálculo de pontuação e aumento progressivo de velocidade.
- `src/entidades.py` — classes Personagem (lógica de pulo e agachamento), Obstaculo (cactos e pássaros) e Chao (rolagem infinita).
- `src/dados.py` — leitura e escrita do recorde em recorde.txt


## 12. Recursos externos previstos

- imagens feitas pelo grupo;
- sons gratuitos;
- tutorial usado apenas como referência;

Recursos previstos:

> Não pretendemos utilizar recursos externos.

## 13. Principais dificuldades esperadas

- movimentção do jogador e do cenário
- marcar a pontuação
- gameplay loop


## 14. Escopo mínimo para a entrega final

Descreva qual será a versão mínima aceitável do jogo.

Esta seção é importante para evitar que o grupo escolha uma ideia grande demais.

Escopo mínimo:

> Um personagem capaz de pular, uma pista com geração contínua de um tipo de obstáculo terrestre, detecção funcional de colisão, sistema de perda de vidas, exibição da pontuação atual na tela e uma tela simples de Game Over.

## 15. Possíveis melhorias, caso haja tempo

- Tela inicial
- Sistema capaz de registrar a melhor pontuação e quando ela foi conquistada
- Aumento de velocidade e dificuldade