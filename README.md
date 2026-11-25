# Jogo da Forca com Interface Gráfica (INE5201)

**Disciplina:** INE5201 - Introdução à Ciência da Computação com Python (UFSC)  
**Aluno:** Vinicius Andreani  

## Descrição do Projeto
Aplicação desktop do clássico Jogo da Forca desenvolvida em Python utilizando a biblioteca `tkinter`. O jogo realiza a leitura de palavras a partir de um arquivo externo (`palavras.txt`), controla tentativas e erros com desenho progressivo do boneco na forca, oferece sistema de dicas e salva o histórico acumulado de vitórias e derrotas em `estatisticas.txt`.

## Funcionalidades Implementadas
* **Display da palavra oculta:** Atualização dinâmica das letras reveladas e ocultas (`_`).
* **Teclado virtual (A–Z):** Botões interativos com destaque visual para acertos e erros e bloqueio de letras já tentadas.
* **Desenho gráfico da forca:** Representação progressiva das 6 partes do boneco conforme os erros.
* **Controles de partida:** Botões para **Novo Jogo**, **Dica** (limite de 2 por partida) e **Desistir**.
* **Persistência de dados:** Leitura de banco com 60 palavras (`palavras.txt`) e gravação automática de estatísticas (`estatisticas.txt`).

## Como Executar
1. Certifique-se de ter o Python 3 instalado.
2. Faça o download deste repositório ou baixe o projeto em formato ZIP.
3. Extraia os arquivos, abra o terminal na pasta do projeto e execute:
   ```bash
   python forca_gui.py# tarefa-03-jogo-da-forca
