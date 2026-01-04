# Desenlance - PBL Algoritmos e Programacao (JEDI TEMPLE)

Uma implementação desktop do famoso jogo de palavras "Termo" (clone do Wordle), desenvolvida em **Python** utilizando a biblioteca **Tkinter** para a interface gráfica e estruturada no padrão de arquitetura **MVC (Model-View-Controller)**.

## 📖 Sobre o Projeto

Este projeto é uma **refatoração completa** de um trabalho acadêmico realizado originalmente em 2023. O desafio original propunha a criação de um jogo de palavras via linha de comando, focado em manipulação de strings e lógica estruturada.

A versão atual (**Desenlance**) eleva o nível técnico do projeto ao implementar:
* **Interface Gráfica (GUI):** Substituição do terminal por uma janela interativa.
* **Padrão MVC:** Separação clara entre a lógica do jogo (Model), a interface do usuário (View) e o gerenciamento de interações (Controller).
* **Programação Orientada a Objetos:** Uso de classes para modularização e escalabilidade.

## 🎮 Regras do Jogo

As regras seguem a proposta original do desafio PBL:
* **Objetivo:** Adivinhar uma palavra secreta de 5 letras.
* **Tentativas:** O jogador possui 6 chances para acertar.
* **Feedback Visual:**
    * 🟩 **Verde:** Letra correta na posição correta.
    * 🟨 **Amarelo:** Letra existe na palavra, mas na posição errada.
    * ⬛ **Cinza/Escuro:** Letra não existe na palavra.
* **Pontuação:** Cada rodada vale **120 pontos**. A cada tentativa falha, perdem-se **20 pontos**. Se não acertar em 6 tentativas, a pontuação da rodada é zerada.

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.13.9
* **GUI:** Tkinter
* **Arquitetura:** MVC

## 📂 Estrutura do Projeto

O código foi organizado para garantir a separação de responsabilidades:

```text
/Desenlance
│
├── Main.py               # Ponto de entrada da aplicação
├── words.txt             # Banco de dados de palavras
│
├── /Model                # Regras de negócio e dados
│   ├── GameManager.py    # Gerencia o fluxo global (partidas, placar)
│   ├── RoundManager.py   # Lógica de uma rodada específica
│   ├── WordBank.py       # Manipulação do arquivo de texto
│   └── Constants.py      # Configurações de cores e fontes
│
├── /View                 # Interface com o Usuário
│   ├── MainView.py       # Janela principal
│   ├── MenuView.py       # Tela de seleção de jogadores
│   └── GameView.py       # Tabuleiro e teclado visual
│
└── /Controller           # Ponte entre Model e View
    └── GameController.py # Tratamento de eventos (teclado/mouse)
