# Nome do Jogo: Sonica Runner

Projeto final da disciplina de Introdução a Algoritmos/Programação, desenvolvido com Python e Pygame.

Este repositório utiliza o template oficial da disciplina para o desenvolvimento de um jogo estilo Infinite Runner (Corrida Infinita com Obstáculos), evoluindo o código de forma modular e organizada ao longo das semanas.

## Integrantes do grupo

- Nome 1: Carolina Almeida Mendes de Souza
- Nome 2: Giovanni Arenare Mota
- Nome 3: Gustavo Alberto Araujo de Sa

## Estrutura do projeto

- `main.py`: Ponto de entrada da aplicação.
- `src/`: Código-fonte principal do jogo (loop, regras, sprites e dados).
- `assets/`: Imagens, fontes e sons (contém o `spritesheet.bmp`).
- `data/`: Arquivos persistentes (contém o `recorde.txt`).
- `tests/`: Testes unitários com `pytest`.
- `docs/`: Documentação do projeto, incluindo proposta inicial.

## Descrição do jogo

O jogo é uma releitura do clássico jogo do dinossauro do Google Chrome. O jogador controla o Dino em uma corrida automática para a direita em um cenário contínuo. Obstáculos terrestres (cactos) e itens aéreos (pássaros) surgem na tela vindo da direita em direção ao jogador. A sobrevivência se torna desafiadora devido ao surgimento aleatório de perigos simples ou duplos combinados.

## Objetivo do jogador

O objetivo principal é sobreviver pelo maior tempo possível na corrida, desviando dos cactos e coletando pássaros/gemas no ar para acumular a maior pontuação possível e quebrar o recorde máximo (High Score) gravado no sistema.

## Regras do jogo

- O jogador inicia a partida com um total de **3 vidas**.
- Desviar de obstáculos e sobreviver garante **+5 pontos** continuamente.
- Coletar a gema/pássaro aérea garante um bônus de **+15 pontos**.
- Colidir com um cacto reduz **1 vida** do jogador.
- A partida entra em estado de **Game Over** imediatamente quando a quantidade de vidas chegar a zero. No Game Over, o jogador pode reiniciar a partida instantaneamente.

## Controles

### Na Tela de Menu:
- **Barra de Espaço**: Inicia o jogo de fato.

### Durante a Partida (Jogando):
- **Barra de Espaço / Seta para Cima**: Faz o personagem pular.
  - *Mecânica Avançada:* **Segurar o botão** faz o Dino realizar um pulo mais alto e longo; **dar um clique rápido** faz um pulo curto.

### Na Tela de Game Over:
- **Tecla R**: Reinicia a partida imediatamente, limpando os obstáculos e resetando os pontos e vidas.
- **Tecla ESC**: Fecha o jogo e salva o progresso.

## Como executar o projeto

### 1. Preparar o ambiente e instalar dependências
Certifique-se de ter o Python instalado (compatível com Python 3.14+ e Pygame-CE).

```bash
pip install pytest pygame-ce