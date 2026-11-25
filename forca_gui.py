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

def main():
    palavras = carregar_palavras(ARQUIVO_PALAVRAS)
    vitorias, derrotas = carregar_estatisticas()

    estado = {
        "palavra": "",
        "letras_tentadas": set(),
        "erros": 0,
        "jogo_ativo": True,
        "dicas_usadas": 0,
        "vitorias": vitorias,
        "derrotas": derrotas,
    }

    janela = tk.Tk()
    janela.title("Jogo da Forca - INE5201")
    janela.resizable(False, False)
    janela.configure(bg="#f4f4f9")

    # Topo: Estatísticas e Tentativas
    frame_topo = tk.Frame(janela, bg="#f4f4f9")
    frame_topo.pack(pady=10, padx=20, fill="x")

    lbl_stats = tk.Label(
        frame_topo,
        text=f"Vitórias: {estado['vitorias']}  |  Derrotas: {estado['derrotas']}",
        font=("Arial", 11, "bold"),
        bg="#f4f4f9",
        fg="#2c3e50",
    )
    lbl_stats.pack(side="left")

    lbl_tentativas = tk.Label(
        frame_topo,
        text=f"Tentativas restantes: {MAX_ERROS}",
        font=("Arial", 11, "bold"),
        bg="#f4f4f9",
        fg="#c0392b",
    )
    lbl_tentativas.pack(side="right")

    # Centro: Canvas da Forca + Palavra Oculta
    frame_centro = tk.Frame(janela, bg="#f4f4f9")
    frame_centro.pack(pady=5, padx=20)

    canvas = tk.Canvas(frame_centro, width=220, height=240, bg="white", relief="solid", bd=1)
    canvas.grid(row=0, column=0, padx=15)

    frame_palavra = tk.Frame(frame_centro, bg="#f4f4f9")
    frame_palavra.grid(row=0, column=1, padx=15)

    lbl_palavra = tk.Label(
        frame_palavra,
        text="",
        font=("Courier New", 24, "bold"),
        bg="#f4f4f9",
        fg="#1e1e1e",
    )
    lbl_palavra.pack(pady=15)

    lbl_status = tk.Label(
        frame_palavra,
        text="Escolha uma letra abaixo!",
        font=("Arial", 11),
        bg="#f4f4f9",
        fg="#555555",
        wraplength=260,
    )
    lbl_status.pack(pady=5)

    # Teclado Virtual A-Z
    frame_teclado = tk.Frame(janela, bg="#f4f4f9")
    frame_teclado.pack(pady=10, padx=20)

    botoes_letras = {}

    def atualizar_interface():
        lbl_palavra.config(text=atualizar_display(estado["palavra"], estado["letras_tentadas"]))
        restantes = MAX_ERROS - estado["erros"]
        lbl_tentativas.config(text=f"Tentativas restantes: {restantes}")
        lbl_stats.config(text=f"Vitórias: {estado['vitorias']}  |  Derrotas: {estado['derrotas']}")
        desenhar_boneco(canvas, estado["erros"])

    def encerrar_partida(venceu):
        estado["jogo_ativo"] = False
        for btn in botoes_letras.values():
            btn.config(state="disabled")
        if venceu:
            estado["vitorias"] += 1
            lbl_status.config(text="Parabéns! Você venceu!", fg="#27ae60")
            messagebox.showinfo("Vitória!", f"Você acertou a palavra: {estado['palavra']}")
        else:
            estado["derrotas"] += 1
            lbl_palavra.config(text=" ".join(estado["palavra"]))
            lbl_status.config(text=f"Fim de jogo! A palavra era: {estado['palavra']}", fg="#c0392b")
            messagebox.showerror("Derrota", f"Você perdeu! A palavra era: {estado['palavra']}")
        salvar_estatisticas(estado["vitorias"], estado["derrotas"])
        atualizar_interface()

    def tentar_letra(letra):
        if not estado["jogo_ativo"] or letra in estado["letras_tentadas"]:
            return

        estado["letras_tentadas"].add(letra)
        btn = botoes_letras[letra]

        if letra in estado["palavra"]:
            btn.config(state="disabled", bg="#a3e4d7", disabledforeground="#145a32")
            lbl_status.config(text=f"Boa! A letra '{letra}' está na palavra.", fg="#1e8449")
        else:
            estado["erros"] += 1
            btn.config(state="disabled", bg="#f5b7b1", disabledforeground="#78281f")
            lbl_status.config(text=f"Ops! A letra '{letra}' não existe.", fg="#c0392b")

        atualizar_interface()

        if verificar_vitoria(estado["palavra"], estado["letras_tentadas"]):
            encerrar_partida(True)
        elif estado["erros"] >= MAX_ERROS:
            encerrar_partida(False)

    def novo_jogo():
        estado["palavra"] = escolher_palavra(palavras)
        estado["letras_tentadas"] = set()
        estado["erros"] = 0
        estado["jogo_ativo"] = True
        estado["dicas_usadas"] = 0
        lbl_status.config(text="Novo jogo iniciado! Escolha uma letra.", fg="#555555")
        for letra, btn in botoes_letras.items():
            btn.config(state="normal", bg="#e0e0e0", fg="#1e1e1e")
        atualizar_interface()

    def desistir():
        if not estado["jogo_ativo"]:
            return
        if messagebox.askyesno("Desistir", "Tem certeza que deseja desistir desta partida?"):
            estado["erros"] = MAX_ERROS
            encerrar_partida(False)

    def usar_dica():
        if not estado["jogo_ativo"]:
            return
        letras_faltando = [l for l in set(estado["palavra"]) if l not in estado["letras_tentadas"]]
        if len(letras_faltando) <= 1:
            messagebox.showinfo("Dica", "Resta apenas uma letra! Tente adivinhar.")
            return
        if estado["dicas_usadas"] >= 2:
            messagebox.showwarning("Dica", "Limite de 2 dicas por partida atingido!")
            return
        estado["dicas_usadas"] += 1
        letra_revelada = random.choice(letras_faltando)
        tentar_letra(letra_revelada)

    alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for idx, letra in enumerate(alfabeto):
        btn = tk.Button(
            frame_teclado,
            text=letra,
            width=4,
            height=2,
            font=("Arial", 10, "bold"),
            bg="#e0e0e0",
            command=lambda l=letra: tentar_letra(l),
        )
        btn.grid(row=idx // 9, column=idx % 9, padx=3, pady=3)
        botoes_letras[letra] = btn

    # Botões de Controle: Novo Jogo, Dicas, Desistir
    frame_controles = tk.Frame(janela, bg="#f4f4f9")
    frame_controles.pack(pady=15)

    tk.Button(
        frame_controles,
        text="Novo Jogo",
        width=13,
        font=("Arial", 10, "bold"),
        bg="#2980b9",
        fg="white",
        command=novo_jogo,
    ).grid(row=0, column=0, padx=8)

    tk.Button(
        frame_controles,
        text="Dica",
        width=13,
        font=("Arial", 10, "bold"),
        bg="#f39c12",
        fg="white",
        command=usar_dica,
    ).grid(row=0, column=1, padx=8)

    tk.Button(
        frame_controles,
        text="Desistir",
        width=13,
        font=("Arial", 10, "bold"),
        bg="#c0392b",
        fg="white",
        command=desistir,
    ).grid(row=0, column=2, padx=8)

    novo_jogo()
    janela.mainloop()


if __name__ == "__main__":
    main()