# Projeto Q-Learning: Navegação do Amongois

Este repositório contém a implementação do algoritmo **Q-Learning** para controlar o personagem "Amongois" em um jogo 3D, com o objetivo de fazê-lo navegar por plataformas e alcançar objetivo final.

## 🧠 Visão Geral do Projeto

O projeto consiste em desenvolver um agente de Inteligência Artificial usando Q-Learning para aprender a melhor sequência de ações com base em tentativas, erros e recompensas obtidas do ambiente. O jogo, disponibilizado como um executável, simula um ambiente com plataformas onde o personagem "Amongois" deve se locomover para alcançar o bloco preto. A comunicação entre o algoritmo e o jogo é estabelecida via um servidor local.

## 🧩 Conteúdo do Repositório

* **`client.py`**: Implementação do algoritmo de Q-Learning e da lógica de treino/teste.
* **`connection.py`**: Interface de comunicação com o jogo (fornecida pelo professor).
* **`resultado.txt`**: Arquivo que salva a Q-table com os valores aprendidos pelo agente.

## 🎮 Sobre o Jogo

O jogo consiste em plataformas que o personagem deve atravessar. Ele pode realizar três ações:
- `"left"` — girar para a esquerda
- `"right"` — girar para a direita
- `"jump"` — pular para frente

O estado do jogo é representado por um vetor binário de 7 bits:
- 5 bits para a plataforma atual (0–23)
- 2 bits para a direção:  
  - `00` = Norte  
  - `01` = Leste  
  - `10` = Sul  
  - `11` = Oeste

## 🚀 Como Rodar

1. Certifique-se de que o jogo (`.exe`) está rodando localmente na porta correta (ex: 2037)
2. Clone o repositório e navegue até a pasta:
   ```bash
   git clone https://github.com/seu-usuario/q-learning.git
   cd q-learning
3. Abra o jogo "Amongois"
4. Descomente a linha 'agent.trainAgent(socket)' no final do arquivo se quiser realizar o treinamento antes de testar
5. Rode a página 'client.py': python client.py
   
## 👩🏻‍💻 Equipe
- Ana Lívia da Costa Pessoa <alcp>
- Fernanda Marques Neves <fmn>
- Sara Carvalho Coelho Lustosa <sccl>
