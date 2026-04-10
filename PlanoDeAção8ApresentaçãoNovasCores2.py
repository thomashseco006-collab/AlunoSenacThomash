import tkinter as tk
from tkinter import ttk, messagebox
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

# LOGIN
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

        # USUÁRIO
        self.usuario = tk.Entry(frame, width=30, fg=COR_MARROM)
        self.usuario.insert(0, "Nome ou Email")
        self.usuario.pack(pady=10)
        self.usuario.bind("<FocusIn>", self.limpar_usuario)

        # SENHA
        senha_frame = tk.Frame(frame, bg=COR_VERDE_MEDIO)
        senha_frame.pack(pady=10)

        self.senha = tk.Entry(senha_frame, width=25, fg=COR_MARROM)
        self.senha.insert(0, "Senha")
        self.senha.pack(side="left")
        self.senha.bind("<FocusIn>", self.limpar_senha)

        # BOTÃO OLHO
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
        
        print("LOGADO!")

    # PLACEHOLDER
    def limpar_usuario(self, event):
        if self.usuario.get() == "Nome ou Email":
            self.usuario.delete(0, tk.END)
            self.usuario.config(fg=COR_TEXTO_ESCURO)

    def limpar_senha(self, event):
        if self.senha.get() == "Senha":
            self.senha.delete(0, tk.END)
            self.senha.config(show="*", fg=COR_TEXTO_ESCURO)

    def toggle_senha(self):
        self.mostrar = not self.mostrar
        self.senha.config(show="" if self.mostrar else "*")

    def limpar_esquerda(self):
        for w in self.esquerda.winfo_children():
            w.destroy()

    # LOGIN DE USUÁRIO
    def login(self):
        usuario = self.usuario.get()
        senha = self.senha.get()

        if usuario in ["", "Nome ou Email"] or senha in ["", "Senha"]:
            messagebox.showerror("Erro", "Preencha os campos")
            return

        if "@" in usuario and not re.match(r"[^@]+@[^@]+\.[^@]+", usuario):
            messagebox.showerror("Erro", "Email inválido")
            return

        if not re.match(r'^(?=.*[A-Z])(?=.*\d).{8,}$', senha):
            messagebox.showerror("Erro", "Senha deve ter 8 caracteres com número e maiúscula")
            return

        usuarios = carregar_dados(ARQ_USUARIOS)

        if not usuarios:
            messagebox.showerror("Erro", "Nenhum usuário cadastrado")
            return

        for u in usuarios:
            if (u["usuario"] == usuario or u.get("email") == usuario) and u["senha"] == senha:
                self.root.withdraw()  #Esconde a tela de login
                abrir_sistema(self.root)

        messagebox.showerror("Erro", "Sem cadastro")

    # CADASTRO
    def tela_cadastro(self):
        self.limpar_esquerda()

        campos = {}
        lista = ["Nome Completo", "Nascimento", "Telefone", "Email", "Senha", "CPF/RG"]

        for item in lista:
            tk.Label(self.esquerda, text=item,
                     bg=COR_VERDE_CLARO).pack()
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

            # AUTO PREENCHER LOGIN
            self.usuario.delete(0, tk.END)
            self.usuario.insert(0, email)

            self.senha.delete(0, tk.END)

        tk.Button(self.esquerda, text="Salvar",
                  bg=COR_VERMELHO, fg="white",
                  command=salvar).pack(pady=10)

    # RECUPERAR
    def tela_recuperar(self):
        self.limpar_esquerda()

        tk.Label(self.esquerda, text="Nome ou Email",
                 bg=COR_VERDE_CLARO).pack()
        user = tk.Entry(self.esquerda)
        user.pack()

        tk.Label(self.esquerda, text="Nova Senha",
                 bg=COR_VERDE_CLARO).pack()
        nova = tk.Entry(self.esquerda)
        nova.pack()

        def atualizar():
            usuarios = carregar_dados(ARQ_USUARIOS)

            for u in usuarios:
                if u["usuario"] == user.get() or u.get("email") == user.get():

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

# SISTEMA
class SistemaClinica:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Clínica")
        self.root.geometry("1100x600")

        self.menu = tk.Frame(self.root, bg=COR_VERMELHO_ESC, width=220)
        self.menu.pack(side="right", fill="y")

        self.main = tk.Frame(self.root, bg=COR_VERDE_CLARO)
        self.main.pack(side="left", expand=True, fill="both")

        def btn(text, cmd):
            tk.Button(self.menu, text=text, width=22,
                      bg=COR_VERMELHO, fg="white",
                      command=cmd).pack(pady=5)

        btn("Dashboard", self.dashboard)
        btn("Pacientes", self.pacientes)
        btn("Novo Paciente", self.novo_paciente)
        btn("Atendimentos", self.atendimentos)
        btn("Novo Atendimento", self.novo_atendimento)

        self.dashboard()

    def limpar(self):
        for w in self.main.winfo_children():
            w.destroy()

    def dashboard(self):
        self.limpar()

        pacientes = carregar_dados(ARQ_PACIENTES)
        atendimentos = carregar_dados(ARQ_ATENDIMENTOS)

        hoje = datetime.now().strftime("%d/%m/%Y")
        hoje_qtd = len([a for a in atendimentos if a["data"] == hoje])

        tk.Label(self.main, text="Dashboard",
                 bg=COR_VERDE_CLARO, font=("Arial", 24)).pack(pady=20)

        tk.Label(self.main, text=f"Pacientes: {len(pacientes)}",
                 bg=COR_VERDE_CLARO).pack()

        tk.Label(self.main, text=f"Atendimentos: {len(atendimentos)}",
                 bg=COR_VERDE_CLARO).pack()

        tk.Label(self.main, text=f"Hoje: {hoje_qtd}",
                 bg=COR_VERDE_CLARO).pack()

    def pacientes(self):
        self.limpar()

        busca = tk.Entry(self.main)
        busca.pack()

        tabela = ttk.Treeview(self.main)
        tabela.pack(expand=True, fill="both")

        def carregar():
            tabela.delete(*tabela.get_children())

            pacientes = carregar_dados(ARQ_PACIENTES)
            atendimentos = carregar_dados(ARQ_ATENDIMENTOS)

            for p in pacientes:
                if busca.get().lower() in p["nome"].lower() or busca.get() in p["telefone"]:
                    pai = tabela.insert("", "end", text=p["nome"])

                    tabela.insert(pai, "end", text=f"Telefone: {p['telefone']}")
                    tabela.insert(pai, "end", text=f"Email: {p['email']}")

                    for a in atendimentos:
                        if a["paciente"] == p["nome"]:
                            tabela.insert(pai, "end",
                                text=f"{a['tipo']} | {a['status']} | {a['data']}")

        busca.bind("<KeyRelease>", lambda e: carregar())
        carregar()

    def novo_paciente(self):
        self.limpar()

        campos = {}

        for c in ["Nome", "Nascimento", "Telefone", "Email", "CPF"]:
            tk.Label(self.main, text=c, bg=COR_VERDE_CLARO).pack()
            e = tk.Entry(self.main)
            e.pack()
            campos[c] = e

        def salvar():
            dados = carregar_dados(ARQ_PACIENTES)
            dados.append({
                "nome": campos["Nome"].get(),
                "nascimento": campos["Nascimento"].get(),
                "telefone": campos["Telefone"].get(),
                "email": campos["Email"].get(),
                "cpf": campos["CPF"].get()
            })
            salvar_dados(ARQ_PACIENTES, dados)
            messagebox.showinfo("Sucesso", "Paciente cadastrado")

        tk.Button(self.main, text="Salvar",
                  bg=COR_VERMELHO, fg="white",
                  command=salvar).pack(pady=10)

    def atendimentos(self):
        self.limpar()

        tabela = ttk.Treeview(self.main,
                              columns=("Paciente", "Tipo", "Status", "Data"),
                              show="headings")

        for col in ("Paciente", "Tipo", "Status", "Data"):
            tabela.heading(col, text=col)

        tabela.pack(expand=True, fill="both")

        for a in carregar_dados(ARQ_ATENDIMENTOS):
            tabela.insert("", "end",
                          values=(a["paciente"], a["tipo"], a["status"], a["data"]))

    def novo_atendimento(self):
        self.limpar()

        pacientes = carregar_dados(ARQ_PACIENTES)
        nomes = [p["nome"] for p in pacientes]

        tk.Label(self.main, text="Paciente", bg=COR_VERDE_CLARO).pack()
        paciente = ttk.Combobox(self.main, values=nomes)
        paciente.pack()

        tk.Label(self.main, text="Tipo", bg=COR_VERDE_CLARO).pack()
        tipo = tk.Entry(self.main)
        tipo.pack()

        tk.Label(self.main, text="Status", bg=COR_VERDE_CLARO).pack()
        status = ttk.Combobox(self.main, values=["Realizado", "Não realizado"])
        status.pack()

        def salvar():
            dados = carregar_dados(ARQ_ATENDIMENTOS)
            dados.append({
                "paciente": paciente.get(),
                "tipo": tipo.get(),
                "status": status.get(),
                "data": datetime.now().strftime("%d/%m/%Y")
            })
            salvar_dados(ARQ_ATENDIMENTOS, dados)
            messagebox.showinfo("Sucesso", "Atendimento cadastrado")

        tk.Button(self.main, text="Salvar Atendimento",
                  bg=COR_VERMELHO, fg="white",
                  command=salvar).pack(pady=10)

# ABRIR
def abrir_sistema(root_login):
    sistema = tk.Toplevel(root_login)
    SistemaClinica(sistema)

    def fechar():
        root_login.destroy()

    sistema.protocol("WM_DELETE_WINDOW", fechar)

# START
if __name__ == "__main__":
    root = tk.Tk()
    Login(root)
    root.mainloop()