import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

ARQ_USUARIOS = "usuarios.json"
ARQ_PACIENTES = "pacientes.json"
ARQ_ATENDIMENTOS = "atendimentos.json"

# ───────── CORES (DO PRIMEIRO CÓDIGO) ───────── #
COR_VERMELHO      = "#AD2003" # Primária / destaque / botões da barra lateral
COR_VERDE_CLARO   = "#E0E6AE" # Fundo geral
COR_VERDE_MEDIO   = "#BDD3B6" # Cards / painéis
COR_MARROM        = "#836868" # Campos vazios a serem preenchidos / texto secundário claro
COR_VERMELHO_ESC  = "#5F0609" # Botões / texto claro / botões da barra lateral / texto claro
COR_BRANCO        = "#FFFFFF" # Bordas / texto claro
COR_TEXTO_ESCURO  = "#2B1A1A" # Cabeçalho / rodapé / texto claro

def carregar_dados(arquivo):
    if not os.path.exists(arquivo):
        salvar_dados(arquivo, [])
    try:
        with open(arquivo, "r") as f:
            return json.load(f)
    except:
        return []

def salvar_dados(arquivo, dados):
    with open(arquivo, "w") as f:
        json.dump(dados, f, indent=4)