# Nome do Jogo: Sonica Runner

Projeto final da disciplina de Introdução a Algoritmos/Programação, desenvolvido com Python e Pygame.

Este repositório utiliza o template oficial da disciplina para o desenvolvimento de um jogo estilo Infinite Runner (Corrida Infinita com Obstáculos), evoluindo o código de forma modular e organizada ao longo das semanas.

## Integrantes do grupo

- Nome 1: Carolina Almeida Mendes de Souza
- Nome 2: Giovanni Arenare Mota
- Nome 3: Gustavo Alberto Araujo de Sa

## Estrutura do projeto

- `main.py`: ponto de entrada da aplicação.
- `src/`: código-fonte principal do jogo (loop, regras, sprites e dados).
- `assets/`: imagens, fontes e sons.
- `data/`: arquivos persistentes (recorde/ranking).
- `tests/`: testes unitários com `pytest`.
- `docs/`: documentação do projeto, incluindo proposta inicial.

## Descrição do jogo

O jogo consiste em controlar um personagem que corre automaticamente para a direita em um cenário contínuo. O jogador deve desviar de obstáculos terrestres e aéreos que surgem de forma aleatória na tela. A velocidade do jogo aumenta gradativamente conforme a pontuação sobe, tornando a sobrevivência mais desafiadora a cada segundo.

## Objetivo do jogador

O objetivo principal é sobreviver pelo maior tempo possível na corrida, desviando dos perigos para acumular a maior pontuação e quebrar o recorde máximo (High Score) gravado no sistema.

## Regras do jogo

- O jogador inicia a partida com um total de 3 vidas.
- A pontuação aumenta continuamente enquanto o personagem permanecer vivo.
- Colidir com qualquer obstáculo (terrestre ou aéreo) reduz 1 vida do jogador.
- Itens especiais (moedas) aparecem esporadicamente e concedem um bônus de 100 pontos se coletados.
- A partida termina (Game Over) imediatamente quando a quantidade de vidas chegar a zero.

## Controles

- Seta para cima / Barra de Espaço: Faz o personagem pular (evita obstáculos terrestres).
- Seta para baixo: Faz o personagem se abaixar (evita obstáculos aéreos).
- ESC: sair do jogo

## Como executar o projeto

### 1. Clonar o repositório

```bash
git clone LINK_DO_REPOSITORIO
cd NOME_DA_PASTA
pip install -r requirements.txt
python main.py
```

## Como executar os testes

```bash
python -m pytest
```

## Checklist mínimo para entrega

- Preencher este README com nome final, descrição real, regras e controles do jogo.
- Atualizar `docs/proposta.MD` com a proposta do grupo.
- Garantir que o jogo executa com `python main.py`.
- Garantir que os testes passam com `pytest`.

## Observações para os alunos

- Mantenham o código organizado em módulos pequenos e com responsabilidade clara.
- Comentem partes importantes da lógica, principalmente regras do jogo.
- Registrem decisões técnicas no README do grupo ao longo do desenvolvimento.
