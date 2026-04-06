'''Proximo Projeto 30/01-09/04'''
'''(.pack) gerenciador de geometria que posociona widgets através
de coordenadas absolutas(x, y)'''
'''(.ico)definir um icone,(root.iconbitmap)caminho do icone'''

'''
width=200, #Largura 
height=30, #Altura
button_color='green', #Cor do botão
progress_color='blue', #Preenchimento da escala fixa
fg_color='lightgray', #Preechimento do progresso
'''

import customtkinter as ctk
from tkinter import messagebox #, PhotoImage
from datetime import *
import re

class Aplicação():
    def __init__(self):
        self.tema()
    
    def tema(self):
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

    # ──────────────────────── Paleta de Cores ──────────────────────── #
    COR_VERMELHO      = "#AD2003"   # Primária / destaque / Botão
    COR_VERDE_CLARO   = "#E0E6AE"   # Fundo geral
    COR_VERDE_MEDIO   = "#BDD3B6"   # Cards / painéis
    COR_MARROM        = "#836868"   # Texto secundário / bordas / Botão
    COR_VERMELHO_ESC  = "#5F0609"   # Cabeçalho / rodapé
    COR_BRANCO        = "#FFFFFF"
    COR_TEXTO_ESCURO  = "#2B1A1A"

    def tela(self):
        janela = ctk.CTk()
        janela.geometry("700x400")
        janela.title("Sistema de Login")
        #janela.icombimap("icon.ico")
        janela.resizable(False, False)

    '''
    img = PhotoImage(file="log.png")
    label_img = custontkinter.CTkLabel(master=janela, image=img)
    label.img.pack(padx=5, pady=65)
    '''

    label_tt = ctk.CTkCheckBox(master=janela, text="Entre na sua conta", font=("Arial", 20), text_color="#836868") #00B0F0

    frame = ctk.CTkFrame(master=janela, width=350, height=396)
    frame.pack(side="right")

    label = ctk.CTkLabel(master=frame, text="Sistema de Login", font=("Arial", 20))
    label.pack(padx=25, pady=5)

    entry1 = ctk.CTkEntry(master=frame, placeholder_text="Nome de Usário", width=300, font=("Arial", 14)).pack(padx= 25, pady=105)
    label1 = ctk.CTkLabel(master=frame, text="O campo nome de usuário e de caracter obrigatório.", text_color="Green", font=("Arial", 8)).pack(padx= 25, pady=135)

    entry2 = ctk.CTkEntry(master=frame, placeholder_text="Senha de Usário", width=300, font=("Arial", 14), show="*").pack(padx= 25, pady=105)
    label2 = ctk.CTkLabel(master=frame, text="O campo nome de usuário e de caracter obrigatório.", text_color="Green", font=("Arial", 8)).pack(padx= 25, pady=135)

    checkbox = ctk.CTkCheckBox(master=frame, text="Lembra-se de mim sempre").pack(padx=25, pady= 235)

    login_button = ctk.CTkButton(master=frame, text="Entrar", width=300).pack(padx=25, pady= 235)

    resgister_span = ctk.CTkLabel(master=frame, text="Nenhuma conta registrada").pack(padx=25, pady= 325)

    def tela_register():
        login.frame.pack_forget() #Remover frame do login

        rg_frame = ctk.CTkButton(master=frame, width=350, height=396)
        rg_frame = ctk.CTkButton.pack(side="right")

        pass
    resgister_button = ctk.CTkButton(master=frame, text="Cadastrar-se", width=150, 
                                    fg_color="#2B1A1A", hover_color="#2D39334").pack(padx=175, pady= 325) #fg_collor="green"=hover_color="#2D39334"



janela.mainloop()