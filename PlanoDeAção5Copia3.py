import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

ARQ_USUARIOS = "usuarios.json"
ARQ_PACIENTES = "pacientes.json"
ARQ_ATENDIMENTOS = "atendimentos.json"

#Entrada de dados
#Arquivos em Json
def carregar_dados(arquivo):
    if not os.path.exists(arquivo):
        salvar_dados(arquivo, []) #with open(arquivo, "w") as f: #Arquivo vazio pode dar erro
                                  #json.dump([], f)
    try:
        with open(arquivo, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def salvar_dados(arquivo, dados):
    with open(arquivo, "w") as f:
        json.dump(dados, f, indent=4)


#Login
class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("Login do Sistema")
        self.root.geometry("300x250")

        frame = tk.Frame(root)
        frame.pack(expand=True)

        tk.Label(frame, text="Usuário").pack(pady=5)
        self.usuario = tk.Entry(frame)
        self.usuario.pack()

        tk.Label(frame, text="Senha").pack(pady=5)
        self.senha = tk.Entry(frame, show="*")
        self.senha.pack()

        tk.Button(frame, text="Login", width=15, command=self.login).pack(pady=10)
        tk.Button(frame, text="Cadastrar", width=15, command=self.cadastrar).pack()

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

    #Usuário
    def cadastrar(self):
        if self.usuario.get() == "" or self.senha.get() == "":
            messagebox.showwarning("Erro", "Preencha usuário e senha")
            return

        usuarios = carregar_dados(ARQ_USUARIOS)

    #Verificar primeiro
        for u in usuarios:
            if u["usuario"] == self.usuario.get():
                messagebox.showerror("Erro", "Usuário já existe")
                return

    #Salvar depois
        usuarios.append({
            "usuario": self.usuario.get(),
            "senha": self.senha.get()
        })

        salvar_dados(ARQ_USUARIOS, usuarios)

        messagebox.showinfo("Sucesso", "Usuário cadastrado!")

#Sistema
class SistemaClinica:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Clínica")
        self.root.geometry("1100x600")

        self.criar_layout()
        self.mostrar_dashboard()

    def criar_layout(self):
        self.menu = tk.Frame(self.root, bg="#2c3e50", width=220)
        self.menu.pack(side="left", fill="y")

        self.main = tk.Frame(self.root, bg="#ecf0f1")
        self.main.pack(side="right", expand=True, fill="both")

        tk.Label(self.menu, text="CLÍNICA",
                 bg="#2c3e50", fg="white",
                 font=("Arial", 16, "bold")).pack(pady=20)

        tk.Button(self.menu, text="Dashboard", width=20,
                  command=self.mostrar_dashboard).pack(pady=5)

        tk.Button(self.menu, text="Lista de Pacientes", width=20,
                  command=self.mostrar_pacientes).pack(pady=5)

        tk.Button(self.menu, text="Cadastrar Paciente", width=20,
                  command=self.novo_paciente).pack(pady=5)

        tk.Button(self.menu, text="Atendimentos", width=20,
                  command=self.mostrar_atendimentos).pack(pady=5)

        tk.Button(self.menu, text="Novo Atendimento", width=20,
                  command=self.novo_atendimento).pack(pady=5)

    def limpar_tela(self):
        for widget in self.main.winfo_children():
            widget.destroy()

    def mostrar_dashboard(self):
        self.limpar_tela()

        tk.Label(self.main, text="Tela Inicial",
                 font=("Arial", 24)).pack(pady=20)

        pacientes = carregar_dados(ARQ_PACIENTES)
        atendimentos = carregar_dados(ARQ_ATENDIMENTOS)

        tk.Label(self.main, text=f"Total Pacientes: {len(pacientes)}").pack()
        tk.Label(self.main, text=f"Total Atendimentos: {len(atendimentos)}").pack()

    #Pacientes
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
                 font=("Arial", 18)).pack(pady=10)

        campos = {}

        for campo in ["Nome Completo", "Data de Nascimento", "Telefone", "Email", "CPF"]:
            tk.Label(self.main, text=campo).pack()
            entry = tk.Entry(self.main)
            entry.pack()
            campos[campo] = entry

        #Adição: Salvar paciente vazio
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
                  command=salvar).pack(pady=10)

    #Atendimentos
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

        tk.Label(self.main, text="Novo Atendimento").pack()

        pacientes = carregar_dados(ARQ_PACIENTES) #Variável para validar se tem paciente cadastrado e 
                                                  #criar lista de nomes, em seguida para criar combo box

        #Validar
        if not pacientes:
            messagebox.showwarning("Aviso", "Cadastre um paciente primeiro")
            return

        #Criar lista de nomes
        nomes = [p["nome"] for p in pacientes]

        tk.Label(self.main, text="Paciente").pack()
        paciente = ttk.Combobox(self.main, values=nomes)
        paciente.pack()

        tk.Label(self.main, text="Procedimento").pack()
        procedimento = tk.Entry(self.main)
        procedimento.pack()

        def salvar(): #Repetição
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
                  command=salvar).pack()


#Abertura do sistema
def abrir_sistema(root_login):
    sistema = tk.Toplevel(root_login)
    SistemaClinica(sistema)


#Inicialização do login
if __name__ == "__main__":
    root = tk.Tk()
    Login(root)
    root.mainloop()
    
'''
Para cada ação de cadastro (usuário, paciente, atendimento), 
o processo deve seguir está estrutura lógica:
# 1. validar
if erro:
    return

# 2. carregar dados
dados = carregar_dados(...)

# 3. verificar regras
if duplicado:
    return

# 4. salvar
dados.append(...)
salvar_dados(...)

# 5. feedback
messagebox.showinfo(...)
'''

'''
Um plano de ação é um documento estruturado que transforma metas em etapas concretas, 
definindo o que será feito, quem será o responsável, prazos (cronograma) e recursos 
necessários. Essencial para gestão de projetos, ele garante foco e eficiência, sendo 
frequentemente estruturado pela metodologia de validação com regular expression.

(Expressões regulares para validar email e data)

self é uma propriedade da classe utilizada para acessar atributos e métodos dentro da própria classe.
'''
