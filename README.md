# Desenlance - PBL Algoritmos e Programação (JEDI TEMPLE)

Uma implementação de mesa (Desktop) do famoso jogo de palavras "Termo" (clone do Wordle), desenvolvida em **Python** utilizando a biblioteca **Tkinter** para a interface gráfica, estruturada no padrão de arquitetura **MVC (Model-View-Controller)** e empacotada com ferramentas de desenvolvimento modernas.

---

## 📸 Sobre o Projeto

Este projeto é uma **refatoração e modernização completa** de um trabalho acadêmico realizado originalmente em 2023. O desafio original propunha a criação de um jogo de palavras simples via terminal. 

A versão atual (**Desenlance**) eleva a arquitetura técnica e o visual do projeto ao implementar:
* **Interface Gráfica Premium (GUI):** Visual escuro moderno (Dark Mode) inspirado no Wordle com layouts fluidos.
* **Padrão MVC Limpo:** Separação estrita entre a lógica de pontuações e palavras (Model), telas e componentes (View) e tratamento unificado de eventos de clique e digitação (Controller).
* **Organização Orientada a Objetos:** Modularização completa facilitando manutenções e extensões.

---

## ✨ Novas Funcionalidades e Melhorias Estéticas

* **Históricos de Tentativas Laterais:** Caixas estilizadas à esquerda e à direita do grid principal que exibem em tempo real as palavras que cada jogador já tentou. Em partidas de **1 Jogador (Solo)**, o painel do Jogador 2 se oculta de forma invisível para manter o grid milimetricamente centralizado na janela.
* **Grid de Palavras com Rolagem (Scrollbar & MouseWheel):** O grid de palavras central é abrigado dentro de um `tk.Canvas` com barra de rolagem vertical. Se o tamanho da janela for reduzido, o grid não é cortado e pode ser rolado com a rodinha do mouse.
* **Logística de Digitação Fluida:**
  - Cursor inteligente limitado a posições válidas de digitação (`0` a `4`), sem desaparecer no final da linha.
  - Possibilidade de sobrescrever letras existentes diretamente clicando com as setas do teclado.
  - Backspace inteligente: apaga a letra da célula atual se preenchida; se vazia, retrocede o cursor e limpa a anterior.
* **Animações Aprimoradas:**
  - **Reveal Sequencial:** Cores de acerto reveladas letra por letra a cada 180ms.
  - **Jitter Shake (Vibração):** Vibração rápida de 10px em alta frequência (25ms) ao digitar palavras inválidas, com uma flag de estado `is_shaking` para evitar conflito com as rotinas de layout do Tkinter.
  - **Bloqueio de Teclas:** O usuário é impedido de digitar enquanto as animações de revelação estão ocorrendo.
* **Banco de Palavras:** Fusão com a base oficial de palavras do jogo Termo em português, contendo **6.072 palavras de 5 letras únicas**, limpas e normalizadas em `words.txt`.

---

## 🛠️ Tecnologias e Ferramentas

* **Linguagem:** Python 3.13+
* **Interface Gráfica:** Tkinter
* **Gerenciador de Dependências:** [Poetry](https://python-poetry.org/)
* **Linter e Formatador:** [Ruff](https://astral.sh/ruff)
* **Task Runner:** [Mise-en-place](https://mise.jdx.dev/)

---

## 📂 Estrutura do Projeto

```text
/Desenlance
│
├── Main.py               # Ponto de entrada da aplicação
├── words.txt             # Banco de dados com 6.072 palavras offline
├── pyproject.toml        # Configuração do Poetry e Ruff
├── poetry.lock           # Lockfile de dependências
├── .mise.toml            # Atalhos rápidos de tarefas (format, lint, run)
│
├── /Model                # Lógica de Negócios e Dados
│   ├── GameManager.py    # Fluxo global do jogo (pontuação, rodadas)
│   ├── RoundManager.py   # Lógica e regras de cada rodada
│   ├── WordBank.py       # Acesso e filtragem de palavras do words.txt
│   └── Constants.py      # Paleta de cores (HSL) e definições de fontes
│
├── /View                 # Telas e Elementos Visuais
│   ├── MainView.py       # Container e inicializador do Tkinter com DPI Awareness
│   ├── MenuView.py       # Tela inicial moderna de configuração de partida
│   └── GameView.py       # Grid interativo, histórico lateral e teclado virtual
│
└── /Controller           # Ponte entre Model e View
    └── GameController.py # Captura unificada de eventos físicos/virtuais e flags de animação
```

---

## 🚀 Como Executar

### Pré-requisitos
Certifique-se de ter o **Poetry** instalado em sua máquina. Se preferir usar o **Mise**, garanta que ele está configurado.

### 1. Instalar Dependências
```bash
poetry install
```

### 2. Rodar o Jogo
Você pode rodar diretamente via Poetry:
```bash
poetry run python main.py
```
Ou usando os atalhos do **Mise**:
```bash
mise run run
```

### 3. Lint e Formatação (Ruff)
Para validar o código contra as diretrizes de PEP8 e formatar automaticamente:
```bash
# Executa checagem de erros
mise run lint

# Formata os arquivos do projeto automaticamente
mise run format
```

### 4. Compilar para Executável Standalone (.exe)
Para gerar um único arquivo executável nativo do Windows (que funciona de forma totalmente autônoma, sem precisar do Python ou de dependências locais instaladas nas máquinas dos usuários):
```bash
# Usando o atalho do Mise:
mise run build

# Ou executando o PyInstaller diretamente pelo Poetry:
poetry run pyinstaller --onefile --windowed --add-data "words.txt;." main.py
```
O executável compilado contendo a base de dados embutida será gerado na pasta `dist/main.exe`.
Você pode pegar esse arquivo `.exe` e disponibilizá-lo diretamente como um asset na aba **Releases** do seu repositório GitHub para que outras pessoas baixem e joguem imediatamente!
