'''Um plano de ação é um documento estruturado que transforma metas em 
etapas concretas, definindo o que será feito, quem será o responsável, 
prazos (cronograma) e recursos necessários. Essencial para gestão de projetos, 
ele garante foco e eficiência, sendo frequentemente estruturado pela metodologia
validação com regular expression (Expressões regulares para validar email e data)
'''

import tkinter as tk
from tkinter import ttk messegebox
import json
import os from datetime import datetime

ARQ_USUARIOS = "usuarios.jason"
ARQ_PACIENTES = "pacientes.json"
ARQ_ATENDIMENTOS = "atendimentos.jason"

def carregar_dados(arquivo):
    if os.path.exists(arquivo):
        with open(arquivo, "r"): as f:
        return json.load(f)
    return

def salvar_dados(arquivo, dados):
    with open(arquivo, "w") as f:
        json.dump(dados, f, indent=4)

class Login:
    def __init__(self, root):
        self.roottitle("Login")
        self.rootgeometry("300x250")

    tk.Label(root,
             text="Usuário").pack(pady=5)
    self.usuário = tk.Entry(root, show="*")
    self.usuário.pack()

    tk.Label(root, 
             text="Senha").pack(pady=5)
    self.senha = tk.Entry(root, show="*")
    self.senha.pack()

    tk.Button(root, 
              text="Login", command=self.login).pack(pady=10)
    tk.Button(root, text="Cadastrar", command=self.cadastrar).pack()

    '''
    para percorrer cada item (u) dentro de uma coleção:
    for - inicia o loop
    u - variável temporária do item
    in - operador para buscar item
    '''

    def login(self):
        usuários=carregar_dados(ARQ_USUARIOS)

        for u in usuários:
            if u["usuário"] == self.usuário.get() and u["senha"] == self.senha.get():
                self.root.destroy()
                abrir_sistema()
                return
            messagebox.showerror("Erro, Login inválido")

    def cadastrar(self):
        usuarios = carregar_dados(ARQ_USUARIOS)

        usuarios.append({
            "usuario": self.usuario.get(), "senha": self.senha.get()"
            })
        
'''
para apresentar no menu listagens acerca de:
dashboard principal, pacientes, atendimento, novo paciente
'''
                           
class SistemaClinica: #Tudo que for do Sistema
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Clínica")
        self.root.geometry("1000x600")

        self.criar_layout()
        self.mostrar_dashboard()

    def criar_layout(self):
        self.menu = tk.Frame(self.root, 
                             bg="#2c3e50", width=200)
        self.menu.pack(side="left", fill="y")
        
        self.main = tk.Frame(self.root, bg="#ecf0f1")
        self.main.pack(side="right", expand=True, fill="both")

        tk.Button(self.menu, 
                  text="Dashboard", width=20, 
                  command=self.mostrar_dashboard).pack(pady=10)
        
        tk.Button(self.menu,
                  text="Pacientes", width=20,
                  command=self.mostrar_pacientes).pack(pady=10)
        
        tk.Button(self.menu,
                  text="Atendimentos", width=20,
                  command=self.mostrar_atendimentos).pack(pady=10)
        
        tk.Button(self.menu,
                  text="Novo Paciente", width=20,
                  command=self.novo_paciente).pack(pady=10)
        
        tk.Button(self.menu,
                  text="Novo Atendimento", width=20,
                  command=self.novo_atendimento).pack(pady=10)
        
    def limpar_tela(self):
        for widget in self.main.winfo_children():
            widget.destroy()

    def mostrar_dashboard(self):
        self.limpar_tela()

        tk.Label(self.main,
                 text="Tela Inicial", font=("Arial", 24)).pack(pady=20)
        
        pacientes = carregar_dados(ARQ_PACIENTES)
        atendimentos = carregar_dados(ARQ_ATENDIMENTOS)

        tk.Label




