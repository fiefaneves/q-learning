# Projeto Q-Learning para Amongois

Este repositório contém a implementação do algoritmo Q-Learning para controlar o personagem "Amongois" em um jogo 3D, com o objetivo de fazê-lo navegar por plataformas e alcançar um bloco preto final.

## Visão Geral do Projeto

O projeto consiste em desenvolver um agente de inteligência artificial usando Q-Learning para aprender a melhor sequência de movimentos no jogo Amongois. O jogo, disponibilizado como um executável, simula um ambiente com plataformas onde o personagem "Amongois" deve se locomover para atingir um objetivo específico. A comunicação entre o algoritmo e o jogo é estabelecida via um servidor local.

## Conteúdo do Repositório

* **`client.py`**: Este arquivo é onde o algoritmo Q-Learning deve ser implementado. Ele se conectará ao jogo e enviará as ações, recebendo em troca o estado atual e a recompensa.
* **`connection.py`**: Este arquivo, fornecido, gerencia a conexão com o servidor local do jogo. Ele contém funções para conectar ao jogo (`connect()`) e para enviar ações e receber o estado e a recompensa (`get_state_reward()`).
* **`Q_table.txt`**: Este arquivo conterá a Q-table gerada pelo algoritmo Q-Learning, documentando os valores aprendidos para cada par estado-ação.

## O Jogo Amongois

No jogo, o personagem "Amongois" precisa atravessar diversas plataformas para chegar ao bloco preto final. O Amongois pode realizar três movimentos básicos: girar para a esquerda, girar para a direita e pular para a frente.

### Movimentos do Amongois

As ações são enviadas ao jogo como strings específicas:
* `"left"`: Gira o Amongois para a esquerda.
* `"right"`: Gira o Amongois para a direita.
* `"jump"`: Faz o Amongois pular para a frente.

Para jogar manualmente, utilize as setas direcionais (esquerda e direita para mudar a direção) e a barra de espaço para pular.

### Atalhos de Teclado no Jogo

* `1`: Aumenta a velocidade do Amongois.
* `2`: Diminui a velocidade do Amongois.
* `3` a `7`: Alteram o tamanho da tela para tamanhos progressivamente menores.

## Conectando o Algoritmo ao Jogo

Para que o algoritmo se comunique com o jogo, é necessário importar o arquivo `connection.py` para dentro do `client.py`. A conexão é iniciada chamando a função `connect()`, que retorna um socket de conexão. A função `connect()` recebe como argumento a porta utilizada pelo executável do jogo.

Após a conexão ser estabelecida, a comunicação com o jogo ocorre através da função `get_state_reward()`. Esta função recebe a ação a ser realizada pelo personagem e o socket de conexão, e retorna o estado atual do jogo e a recompensa obtida.

Exemplo de conexão e interação:

```python
import connection as cn

s = cn.connect(2037) # Conecta à porta 2037 do jogo
estado, recompensa = cn.get_state_reward(s, "jump") # Envia a ação "jump" e recebe o novo estado e recompensa
```

## Formato das Informações

### Estado

O estado é representado por um vetor binário que concatena a informação da plataforma em que o personagem se encontra e a direção para a qual ele está virado.

* **Plataforma**: Existem 24 plataformas possíveis, representadas por 5 dígitos binários.
* **Direção**: A direção é representada por dois dígitos binários:
    * `00` = Norte
    * `01` = Leste
    * `10` = Sul
    * `11` = Oeste

A função `get_state_reward()` envia o estado do servidor para o cliente. Por exemplo, um estado como `1010100` indica que o personagem está na Plataforma 21 e virado para o Norte.

### Recompensa

A recompensa é um número inteiro negativo que varia de -1 a -14. O valor da recompensa é determinado pelo estado resultante da *ação anterior* realizada pelo personagem.

## Objetivo do Projeto

O principal objetivo deste projeto é implementar o algoritmo Q-Learning no arquivo `client.py` para que o Amongois aprenda o trajeto ideal no jogo.

## Entrega do Projeto

Para a entrega do projeto, serão necessários dois arquivos:

1.  **`client.py`**: Contendo o algoritmo Q-Learning implementado. É importante que este arquivo esteja organizado e bem documentado para facilitar a compreensão e correção.
2.  **`Q_table.txt`**: Um arquivo de texto contendo a Q-table gerada pelo algoritmo. A Q-table deve conter *apenas os dados* e estar ordenada de acordo com o estado correspondente. Não deve incluir títulos de colunas ou números de linhas. A ordem das colunas na Q-table deve ser: [Giro para Esquerda, Giro para Direita, Pulo para Frente], respectivamente. A Q-table deve incluir *todos os 96 estados possíveis* (24 plataformas x 4 direções). Um exemplo do formato pode ser encontrado no arquivo `resultado.txt` do repositório GitHub supracitado.