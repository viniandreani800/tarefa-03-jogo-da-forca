import os
import random
import tkinter as tk
from tkinter import messagebox

ARQUIVO_PALAVRAS = "palavras.txt"
ARQUIVO_ESTATISTICAS = "estatisticas.txt"
MAX_ERROS = 6


def carregar_palavras(arquivo):
    if not os.path.exists(arquivo):
        return ["PYTHON", "ALGORITMO", "UNIVERSIDADE"]
    with open(arquivo, "r", encoding="utf-8") as f:
        palavras = [linha.strip().upper() for linha in f if linha.strip()]
    return palavras


def escolher_palavra(lista):
    return random.choice(lista)


def atualizar_display(palavra, letras_tentadas):
    exibicao = [letra if letra in letras_tentadas else "_" for letra in palavra]
    return " ".join(exibicao)


def verificar_vitoria(palavra, letras_tentadas):
    return all(letra in letras_tentadas for letra in palavra)


def carregar_estatisticas():
    if not os.path.exists(ARQUIVO_ESTATISTICAS):
        return 0, 0
    try:
        with open(ARQUIVO_ESTATISTICAS, "r", encoding="utf-8") as f:
            dados = f.read().strip().split(",")
            return int(dados[0]), int(dados[1])
    except (ValueError, IndexError):
        return 0, 0


def salvar_estatisticas(vitorias, derrotas):
    with open(ARQUIVO_ESTATISTICAS, "w", encoding="utf-8") as f:
        f.write(f"{vitorias},{derrotas}")

def desenhar_boneco(canvas, erros):
    canvas.delete("all")
    # Estrutura fixa da forca
    canvas.create_line(30, 220, 130, 220, width=4, fill="#333333")  # Base
    canvas.create_line(60, 220, 60, 30, width=4, fill="#333333")    # Poste
    canvas.create_line(60, 30, 150, 30, width=4, fill="#333333")    # Topo
    canvas.create_line(150, 30, 150, 55, width=3, fill="#8B4513")   # Corda

    # 6 partes do boneco conforme os erros
    if erros >= 1:  # Cabeça
        canvas.create_oval(130, 55, 170, 95, width=3, outline="#1e1e1e")
    if erros >= 2:  # Tronco
        canvas.create_line(150, 95, 150, 150, width=3, fill="#1e1e1e")
    if erros >= 3:  # Braço esquerdo
        canvas.create_line(150, 110, 125, 135, width=3, fill="#1e1e1e")
    if erros >= 4:  # Braço direito
        canvas.create_line(150, 110, 175, 135, width=3, fill="#1e1e1e")
    if erros >= 5:  # Perna esquerda
        canvas.create_line(150, 150, 130, 190, width=3, fill="#1e1e1e")
    if erros >= 6:  # Perna direita
        canvas.create_line(150, 150, 170, 190, width=3, fill="#1e1e1e")