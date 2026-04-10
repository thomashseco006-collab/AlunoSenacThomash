import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
from datetime import datetime
import re

ARQ_USUARIOS = "usuarios.json"
ARQ_PACIENTES = "pacientes.json"
ARQ_ATENDIMENTOS = "atendimentos.json"

# ───────── CORES ───────── #
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

import re

class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("Login do Sistema")
        self.root.geometry("700x400")
        self.root.configure(bg=COR_VERDE_CLARO)
        self.root.resizable(False, False)

        # ESQUERDA DINÂMICA
        self.esquerda = tk.Frame(root, bg=COR_VERDE_CLARO, width=350)
        self.esquerda.pack(side="left", fill="both")

        # DIREITA LOGIN
        frame = tk.Frame(root, bg=COR_VERDE_MEDIO, width=350, height=400)
        frame.pack(side="right", fill="y")

        tk.Label(frame, text="Sistema de Login",
                 bg=COR_VERDE_MEDIO, fg=COR_TEXTO_ESCURO,
                 font=("Arial", 20)).pack(pady=20)

        # CAMPO USUÁRIO (placeholder discreto)
        self.usuario = tk.Entry(frame, width=30, fg=COR_MARROM)
        self.usuario.insert(0, "Nome ou Email")
        self.usuario.pack(pady=10)

        # CAMPO SENHA
        senha_frame = tk.Frame(frame, bg=COR_VERDE_MEDIO)
        senha_frame.pack(pady=10)

        self.senha = tk.Entry(senha_frame, width=25, fg=COR_MARROM)
        self.senha.insert(0, "Senha")
        self.senha.pack(side="left")

        # BOTÃO OLHO (mantido)
        self.mostrar = False
        tk.Button(senha_frame, text="👁",
                  command=self.toggle_senha,
                  bg=COR_VERDE_MEDIO, bd=0).pack(side="left", padx=5)

        tk.Button(frame, text="Entrar", width=25,
                  bg=COR_VERMELHO, fg="white",
                  command=self.login).pack(pady=10)

        tk.Button(frame, text="Cadastrar", width=25,
                  bg=COR_MARROM, fg="white",
                  command=self.tela_cadastro).pack(pady=5)

        tk.Button(frame, text="Esqueceu senha", width=25,
                  bg=COR_VERDE_MEDIO, bd=0,
                  command=self.tela_recuperar).pack()

    def toggle_senha(self):
        self.mostrar = not self.mostrar
        self.senha.config(show="" if self.mostrar else "*")

    def limpar_esquerda(self):
        for w in self.esquerda.winfo_children():
            w.destroy()

    # LOGIN
    def login(self):
        usuario = self.usuario.get()
        senha = self.senha.get()

        if usuario in ["", "Nome ou Email"] or senha in ["", "Senha"]:
            messagebox.showerror("Erro", "Preencha os campos")
            return

        if "@" in usuario and "@" not in usuario:
            messagebox.showerror("Erro", "Email inválido")
            return

        if not re.match(r'^(?=.*[A-Z])(?=.*\d).{8,}$', senha):
            messagebox.showerror("Erro", "Senha deve ter 8 caracteres, 1 número e 1 maiúscula")
            return

        usuarios = carregar_dados(ARQ_USUARIOS)

        if not usuarios:
            messagebox.showerror("Erro", "Nenhum usuário cadastrado")
            return

        for u in usuarios:
            if (u["usuario"] == usuario or u["email"] == usuario) and u["senha"] == senha:
                abrir_sistema(self.root)
                self.root.destroy()
                return

        messagebox.showerror("Erro", "Sem cadastro")

    # CADASTRO
    def tela_cadastro(self):
        self.limpar_esquerda()

        campos = {}
        lista = ["Nome Completo", "Nascimento (dd/mm/aaaa)", "Telefone",
                 "Email", "Senha", "CPF/RG"]

        for item in lista:
            tk.Label(self.esquerda, text=item,
                     bg=COR_VERDE_CLARO, fg=COR_TEXTO_ESCURO).pack()
            e = tk.Entry(self.esquerda)
            e.pack()
            campos[item] = e

        def salvar():
            nome = campos["Nome Completo"].get()
            email = campos["Email"].get()
            senha = campos["Senha"].get()

            if "" in [nome, email, senha]:
                messagebox.showerror("Erro", "Campos obrigatórios")
                return

            if "@" not in email:
                messagebox.showerror("Erro", "Email inválido")
                return

            if not re.match(r'^(?=.*[A-Z])(?=.*\d).{8,}$', senha):
                messagebox.showerror("Erro", "Senha inválida")
                return

            usuarios = carregar_dados(ARQ_USUARIOS)

            usuarios.append({
                "usuario": nome,
                "email": email,
                "senha": senha
            })

            salvar_dados(ARQ_USUARIOS, usuarios)
            messagebox.showinfo("Sucesso", "Cadastro realizado")

        tk.Button(self.esquerda, text="Salvar",
                  bg=COR_VERMELHO, fg="white",
                  command=salvar).pack(pady=10)

    # RECUPERAR SENHA
    def tela_recuperar(self):
        self.limpar_esquerda()

        tk.Label(self.esquerda, text="Nome ou Email",
                 bg=COR_VERDE_CLARO).pack()
        usuario = tk.Entry(self.esquerda)
        usuario.pack()

        tk.Label(self.esquerda, text="Nova Senha",
                 bg=COR_VERDE_CLARO).pack()
        nova = tk.Entry(self.esquerda)
        nova.pack()

        def atualizar():
            usuarios = carregar_dados(ARQ_USUARIOS)

            for u in usuarios:
                if u["usuario"] == usuario.get() or u["email"] == usuario.get():

                    if not re.match(r'^(?=.*[A-Z])(?=.*\d).{8,}$', nova.get()):
                        messagebox.showerror("Erro", "Senha inválida")
                        return

                    u["senha"] = nova.get()
                    salvar_dados(ARQ_USUARIOS, usuarios)

                    messagebox.showinfo("Sucesso", "Senha atualizada")
                    return

            messagebox.showerror("Erro", "Usuário não encontrado")

        tk.Button(self.esquerda, text="Atualizar",
                  bg=COR_VERMELHO, fg="white",
                  command=atualizar).pack(pady=10)
        
class SistemaClinica:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Clínica")
        self.root.geometry("1100x600")

        self.criar_layout()
        self.mostrar_dashboard()

    def criar_layout(self):
        # MENU AGORA NA DIREITA
        self.menu = tk.Frame(self.root, bg=COR_VERMELHO_ESC, width=220)
        self.menu.pack(side="right", fill="y")

        self.main = tk.Frame(self.root, bg=COR_VERDE_CLARO)
        self.main.pack(side="left", expand=True, fill="both")

        tk.Label(self.menu, text="CLÍNICA",
                 bg=COR_VERMELHO_ESC, fg="white",
                 font=("Arial", 16, "bold")).pack(pady=20)

        def btn(text, cmd):
            tk.Button(self.menu, text=text, width=22,
                      bg=COR_VERMELHO, fg="white",
                      bd=0, command=cmd).pack(pady=5)

        btn("Dashboard", self.mostrar_dashboard)
        btn("Pacientes", self.mostrar_pacientes)
        btn("Novo Paciente", self.novo_paciente)
        btn("Atendimentos", self.mostrar_atendimentos)
        btn("Novo Atendimento", self.novo_atendimento)

    def limpar_tela(self):
        for widget in self.main.winfo_children():
            widget.destroy()

    # DASHBOARD
    def mostrar_dashboard(self):
        self.limpar_tela()

        pacientes = carregar_dados(ARQ_PACIENTES)
        atendimentos = carregar_dados(ARQ_ATENDIMENTOS)

        hoje = datetime.now().strftime("%d/%m/%Y")
        atend_hoje = [a for a in atendimentos if a["data"] == hoje]

        tk.Label(self.main, text="Dashboard",
                 bg=COR_VERDE_CLARO,
                 font=("Arial", 24)).pack(pady=20)

        tk.Label(self.main, text=f"Total Pacientes: {len(pacientes)}",
                 bg=COR_VERDE_CLARO).pack()

        tk.Label(self.main, text=f"Total Atendimentos: {len(atendimentos)}",
                 bg=COR_VERDE_CLARO).pack()

        tk.Label(self.main, text=f"Atendimentos Hoje: {len(atend_hoje)}",
                 bg=COR_VERDE_CLARO).pack()

    # PACIENTES
    def mostrar_pacientes(self):
        self.limpar_tela()

        # BUSCA
        busca = tk.Entry(self.main)
        busca.pack(pady=5)

        tabela = ttk.Treeview(self.main)
        tabela.pack(expand=True, fill="both")

        def carregar():
            tabela.delete(*tabela.get_children())

            pacientes = carregar_dados(ARQ_PACIENTES)
            atendimentos = carregar_dados(ARQ_ATENDIMENTOS)

            for p in pacientes:
                if busca.get().lower() in p["nome"].lower() or busca.get() in p["telefone"]:
                    pai = tabela.insert("", "end", text=p["nome"], open=False)

                    # dados do paciente
                    tabela.insert(pai, "end", text=f"Nascimento: {p['nascimento']}")
                    tabela.insert(pai, "end", text=f"Telefone: {p['telefone']}")
                    tabela.insert(pai, "end", text=f"Email: {p['email']}")
                    tabela.insert(pai, "end", text=f"CPF: {p['cpf']}")

                    # atendimentos
                    for a in atendimentos:
                        if a["paciente"] == p["nome"]:
                            tabela.insert(pai, "end",
                                text=f"{a['tipo']} | {a['status']} | {a['historico']}")

        busca.bind("<KeyRelease>", lambda e: carregar())
        carregar()

    # NOVO PACIENTE
    def novo_paciente(self):
        self.limpar_tela()

        campos = {}
        lista = ["Nome", "Nascimento", "Telefone", "Email", "CPF"]

        for item in lista:
            tk.Label(self.main, text=item, bg=COR_VERDE_CLARO).pack()
            e = tk.Entry(self.main)
            e.pack()
            campos[item] = e

        def salvar():
            pacientes = carregar_dados(ARQ_PACIENTES)

            pacientes.append({
                "nome": campos["Nome"].get(),
                "nascimento": campos["Nascimento"].get(),
                "telefone": campos["Telefone"].get(),
                "email": campos["Email"].get(),
                "cpf": campos["CPF"].get()
            })

            salvar_dados(ARQ_PACIENTES, pacientes)
            messagebox.showinfo("Sucesso", "Paciente cadastrado!")

        tk.Button(self.main, text="Salvar",
                  bg=COR_VERMELHO, fg="white",
                  command=salvar).pack(pady=10)

    # ATENDIMENTOS
    def mostrar_atendimentos(self):
        self.limpar_tela()

        tabela = ttk.Treeview(self.main,
                              columns=("Paciente", "Tipo", "Status", "Data"),
                              show="headings")

        for col in ("Paciente", "Tipo", "Status", "Data"):
            tabela.heading(col, text=col)
            tabela.column(col, width=150)

        tabela.pack(expand=True, fill="both")

        atendimentos = carregar_dados(ARQ_ATENDIMENTOS)

        for a in atendimentos:
            tabela.insert("", "end",
                          values=(a["paciente"], a["tipo"], a["status"], a["data"]))

    # NOVO ATENDIMENTO
    def novo_atendimento(self):
        self.limpar_tela()

        pacientes = carregar_dados(ARQ_PACIENTES)
        nomes = [p["nome"] for p in pacientes]

        tk.Label(self.main, text="Paciente", bg=COR_VERDE_CLARO).pack()
        paciente = ttk.Combobox(self.main, values=nomes)
        paciente.pack()

        tk.Label(self.main, text="Tipo Atendimento", bg=COR_VERDE_CLARO).pack()
        tipo = tk.Entry(self.main)
        tipo.pack()

        tk.Label(self.main, text="Status", bg=COR_VERDE_CLARO).pack()
        status = ttk.Combobox(self.main, values=["Realizado", "Não realizado"])
        status.pack()

        tk.Label(self.main, text="Histórico Clínico", bg=COR_VERDE_CLARO).pack()
        historico = tk.Entry(self.main)
        historico.pack()

        def salvar():
            atendimentos = carregar_dados(ARQ_ATENDIMENTOS)

            atendimentos.append({
                "paciente": paciente.get(),
                "tipo": tipo.get(),
                "status": status.get(),
                "historico": historico.get(),
                "data": datetime.now().strftime("%d/%m/%Y")
            })

            salvar_dados(ARQ_ATENDIMENTOS, atendimentos)
            messagebox.showinfo("Sucesso", "Atendimento registrado!")

        tk.Button(self.main, text="Salvar Atendimento",
                  bg=COR_VERMELHO, fg="white",
                  command=salvar).pack(pady=10)
        
# ABERTURA
def abrir_sistema(root_login):
    sistema = tk.Toplevel(root_login)
    SistemaClinica(sistema)

# START
if __name__ == "__main__":
    root = tk.Tk()
    Login(root)
    root.mainloop()