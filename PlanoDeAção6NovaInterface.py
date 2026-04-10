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

# JSON
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

# LOGIN
class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("Login do Sistema")
        self.root.geometry("700x400")
        self.root.configure(bg=COR_VERDE_CLARO)
        self.root.resizable(False, False)

        # Frame lateral direita (igual ao modelo)
        frame = tk.Frame(root, bg=COR_VERDE_MEDIO, width=350, height=400)
        frame.pack(side="right", fill="y")

        tk.Label(frame, text="Sistema de Login",
                 bg=COR_VERDE_MEDIO, fg=COR_TEXTO_ESCURO,
                 font=("Arial", 20)).pack(pady=20)

        # Usuário
        tk.Entry(frame, width=30).pack(pady=10)
        self.usuario = frame.winfo_children()[-1]

        # Senha
        senha_frame = tk.Frame(frame, bg=COR_VERDE_MEDIO)
        senha_frame.pack(pady=10)

        self.senha = tk.Entry(senha_frame, width=25, show="*")
        self.senha.pack(side="left")

        # Botão visualizar senha (discreto)
        self.mostrar = False
        btn_eye = tk.Button(senha_frame, text="👁",
                            command=self.toggle_senha,
                            bg=COR_VERDE_MEDIO, bd=0)
        btn_eye.pack(side="left", padx=5)

        tk.Button(frame, text="Login", width=25,
                  bg=COR_VERMELHO, fg="white",
                  command=self.login).pack(pady=10)

        tk.Button(frame, text="Cadastrar", width=25,
                  bg=COR_MARROM, fg="white",
                  command=self.cadastrar).pack()

    def toggle_senha(self):
        self.mostrar = not self.mostrar
        self.senha.config(show="" if self.mostrar else "*")

    def login(self):
        if self.usuario.get() == "" or self.senha.get() == "":
            messagebox.showerror("Erro", "Preencha usuário e senha")
            return

        usuarios = carregar_dados(ARQ_USUARIOS)

        for u in usuarios:
            if u["usuario"] == self.usuario.get() and u["senha"] == self.senha.get():
                abrir_sistema(self.root)
                self.root.destroy()
                return

        messagebox.showerror("Erro", "Login inválido")

    def cadastrar(self):
        if self.usuario.get() == "" or self.senha.get() == "":
            messagebox.showwarning("Erro", "Preencha usuário e senha")
            return

        usuarios = carregar_dados(ARQ_USUARIOS)

        for u in usuarios:
            if u["usuario"] == self.usuario.get():
                messagebox.showerror("Erro", "Usuário já existe")
                return

        usuarios.append({
            "usuario": self.usuario.get(),
            "senha": self.senha.get()
        })

        salvar_dados(ARQ_USUARIOS, usuarios)
        messagebox.showinfo("Sucesso", "Usuário cadastrado!")

# SISTEMA
class SistemaClinica:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Clínica")
        self.root.geometry("1100x600")

        self.criar_layout()
        self.mostrar_dashboard()

    def criar_layout(self):
        # MENU LATERAL (AGORA ESTILIZADO)
        self.menu = tk.Frame(self.root, bg=COR_VERMELHO_ESC, width=220)
        self.menu.pack(side="left", fill="y")

        self.main = tk.Frame(self.root, bg=COR_VERDE_CLARO)
        self.main.pack(side="right", expand=True, fill="both")

        tk.Label(self.menu, text="CLÍNICA",
                 bg=COR_VERMELHO_ESC, fg="white",
                 font=("Arial", 16, "bold")).pack(pady=20)

        def btn(text, cmd):
            tk.Button(self.menu, text=text, width=22,
                      bg=COR_VERMELHO, fg="white",
                      bd=0, command=cmd).pack(pady=5)

        # BOTÕES ORGANIZADOS
        btn("Meu Cadastro", self.mostrar_dashboard)
        btn("Pacientes", self.mostrar_pacientes)
        btn("Novo Paciente", self.novo_paciente)
        btn("Atendimentos", self.mostrar_atendimentos)
        btn("Novo Atendimento", self.novo_atendimento)

    def limpar_tela(self):
        for widget in self.main.winfo_children():
            widget.destroy()

    def mostrar_dashboard(self):
        self.limpar_tela()

        tk.Label(self.main, text="Tela Inicial",
                 bg=COR_VERDE_CLARO,
                 font=("Arial", 24)).pack(pady=20)

        pacientes = carregar_dados(ARQ_PACIENTES)
        atendimentos = carregar_dados(ARQ_ATENDIMENTOS)

        tk.Label(self.main, text=f"Total Pacientes: {len(pacientes)}",
                 bg=COR_VERDE_CLARO).pack()
        tk.Label(self.main, text=f"Total Atendimentos: {len(atendimentos)}",
                 bg=COR_VERDE_CLARO).pack()

    # RESTANTE DO CÓDIGO NÃO FOI ALTERADO
    def mostrar_pacientes(self):
        self.limpar_tela()

        tabela = ttk.Treeview(self.main,
                              columns=("Nome", "Nascimento", "Telefone", "Email", "CPF"),
                              show="headings")

        for col in ("Nome", "Nascimento", "Telefone", "Email", "CPF"):
            tabela.heading(col, text=col)
            tabela.column(col, width=150)

        tabela.pack(expand=True, fill="both")

        pacientes = carregar_dados(ARQ_PACIENTES)

        for p in pacientes:
            tabela.insert("", "end",
                          values=(p["nome"], p["nascimento"], p["telefone"], p["email"], p["cpf"]))

    def novo_paciente(self):
        self.limpar_tela()

        tk.Label(self.main, text="Cadastro de Paciente",
                 bg=COR_VERDE_CLARO,
                 font=("Arial", 18)).pack(pady=10)

        campos = {}

        for campo in ["Nome Completo", "Data de Nascimento", "Telefone", "Email", "CPF"]:
            tk.Label(self.main, text=campo, bg=COR_VERDE_CLARO).pack()
            entry = tk.Entry(self.main)
            entry.pack()
            campos[campo] = entry

        def salvar():
            if campos["Nome Completo"].get() == "":
                messagebox.showerror("Erro", "Nome obrigatório")
                return

            pacientes = carregar_dados(ARQ_PACIENTES)

            pacientes.append({
                "nome": campos["Nome Completo"].get(),
                "nascimento": campos["Data de Nascimento"].get(),
                "telefone": campos["Telefone"].get(),
                "email": campos["Email"].get(),
                "cpf": campos["CPF"].get()
            })

            salvar_dados(ARQ_PACIENTES, pacientes)
            messagebox.showinfo("Sucesso", "Paciente cadastrado!")
            self.mostrar_pacientes()

        tk.Button(self.main, text="Salvar Paciente",
                  bg=COR_VERMELHO, fg="white",
                  command=salvar).pack(pady=10)

    def mostrar_atendimentos(self):
        self.limpar_tela()

        tabela = ttk.Treeview(self.main,
                              columns=("Paciente", "Procedimento", "Data"),
                              show="headings")

        for col in ("Paciente", "Procedimento", "Data"):
            tabela.heading(col, text=col)
            tabela.column(col, width=200)

        tabela.pack(expand=True, fill="both")

        atendimentos = carregar_dados(ARQ_ATENDIMENTOS)

        for a in atendimentos:
            tabela.insert("", "end",
                          values=(a["paciente"], a["procedimento"], a["data"]))

    def novo_atendimento(self):
        self.limpar_tela()

        tk.Label(self.main, text="Novo Atendimento",
                 bg=COR_VERDE_CLARO).pack()

        pacientes = carregar_dados(ARQ_PACIENTES)

        if not pacientes:
            messagebox.showwarning("Aviso", "Cadastre um paciente primeiro")
            return

        nomes = [p["nome"] for p in pacientes]

        tk.Label(self.main, text="Paciente", bg=COR_VERDE_CLARO).pack()
        paciente = ttk.Combobox(self.main, values=nomes)
        paciente.pack()

        tk.Label(self.main, text="Procedimento", bg=COR_VERDE_CLARO).pack()
        procedimento = tk.Entry(self.main)
        procedimento.pack()

        def salvar():
            if paciente.get() == "" or procedimento.get() == "":
                messagebox.showerror("Erro", "Preencha paciente e procedimento")
                return

            atendimentos = carregar_dados(ARQ_ATENDIMENTOS)

            atendimentos.append({
                "paciente": paciente.get(),
                "procedimento": procedimento.get(),
                "data": datetime.now().strftime("%d/%m/%Y")
            })

            salvar_dados(ARQ_ATENDIMENTOS, atendimentos)
            messagebox.showinfo("Sucesso", "Atendimento cadastrado!")
            self.mostrar_atendimentos()

        tk.Button(self.main, text="Salvar Atendimento",
                  bg=COR_VERMELHO, fg="white",
                  command=salvar).pack()

# ABERTURA
def abrir_sistema(root_login):
    sistema = tk.Toplevel(root_login)
    SistemaClinica(sistema)

# START
if __name__ == "__main__":
    root = tk.Tk()
    Login(root)
    root.mainloop()