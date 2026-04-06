'''Um plano de ação é um documento estruturado que transforma metas em 
etapas concretas, definindo o que será feito, quem será o responsável, 
prazos (cronograma) e recursos necessários. Essencial para gestão de projetos, 
ele garante foco e eficiência, sendo frequentemente estruturado pela metodologia
validação com regular expression (Expressões regulares para validar email e data)

self é uma propriedade da classe
'''

import tkinter as tk
from tkinter import ttk messagebox
import json
from datetime import datetime

ARQ_USUARIOS = "usuarios.jason"
ARQ_PACIENTES = "pacientes.json"
ARQ_ATENDIMENTOS = "atendimentos.jason"

def carregar_dados(arquivo):
    if not os.path.exists(arquivo):
        with open(arquivo, "w") as f:
            json.dumb([], f) #Para não abrir arquivo vazio

    try:
        with open(arquivo,"r") as f:
            return json.load(f)
    except:
        return []

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
            messagebox.showerror("Erro", "Login inválido")

    def cadastrar(self):
        usuarios = carregar_dados(ARQ_USUARIOS)

        usuarios.append({
            "usuario": self.usuario.get(), 
            "senha": self.senha.get()"
            })
        
        salvar_dados(ARQ_USUARIOS, usuarios)

messagebox.showinfo("Sucesso", "Usuário cadastrado!")
        
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

        tk.Label(self.main, text=f"Total de Pacientes: {len(pacientes)}").pack()
        tk.Label(self.main, text=f"Total de Atendimentos: {len(atendimentos)}").pack()

    def mostrar_pacientes(self):
        self.impar_tela()

        tabela = ttk.Treeview(self.main, 
                              columns=("Nome", "Nascimento", "Telefone", "Email", "CPF"), show="headings")
        
        tabela.heading("Nome", text="Nome")
        tabela.heading("Nascimento", text="Nascimento")
        tabela.heading("Telefone", text="Telefone")
        tabela.heading("Email", text="Email")
        tabela.heading("CPF", text="CPF")

        tabela.pack(spand=True, fill="both")

        pacientes = carregar_dados(ARQ_PACIENTES)

        for p in pacientes:
            tabela.insert("", "end" #Imprimir print sem adicionar linha em cada chamada da função 
                          values=(p["Nome"],
                                  p["Nascimento"],
                                  p["Telefone"],
                                  p["Email"],
                                  p["CPF"]))
            
        def excluir():
            item = tabela.selection()
            if item:
                index = tabela.index(item)
                pacientes.pop(index)

    salvar_dados(ARQ_PACIENTES, pacientes)
            self.mostrar_pacientes()
    
            tk.Button(self.main,
                        text="Excluir",
                        command=excluir).pack(pady=10)
    
    def novo_paciente(self):
        self.impar_tela()

        tk.Label(self.main,
                 text="Cadastro de Paciente",
                 font="Arial", 18)).pack(pady=10)

        tk.Label(self.main,
                 text="Nome Completo").pack()
        nome = tk.Entry(self.main)
        nome.pack()

        tk.Label(self.main,
                 text="Data de Nascimento").pack()
        nascimento = tk.Entry(self.main)
        nascimento.pack()

        tk.Label(self.main,
                 text="Telefone").pack()
        telefone = tk.Entry(self.main)
        telefone.pack()

        tk.Label(self.main,
                 text="Email").pack()
        email = tk.Entry(self.main)
        email.pack()

        tk.Label(self.main,
                 text="CPF").pack()
        cpf = tk.Entry(self.main)
        cpf.pack()

        def salvar():
            if nome.get() == "":

    messagebox.showwarning("Erro", "preencha o nome")
            return

        pacientes = carregar_dados(ARQ_PACIENTES)
    
        pacientes.append({"nome":nome.get(),
                          "nascimento": nascimento.get(),
                          "telefone": telefone.get(),
                          "email": email.get(),
                          "cpf": cpf.get()
                          })
    
    salvar_dados(ARQ_PACIENTES, pacientes)

    messagebox.showinfo("Sucesso", "Paciente cadastrado!")
        self.mostrar_pacientes()
    
    tk.Button(self.main,
            text="Salvar",
            command=salvar).pack(pady=10)
    
    def mostrar_atendimentos(self):
        self.impar_tela()

        tabela = ttk.Treeview(self.main,
                              columns=("Paciente", "Procedimento", "Data"),
                              show="headings")
        
        tabela.heading("Paciente",
                       text="Paciente")
        tabela.heading("Procedimento",
                       text="Procedimento")
        tabela.heading("Data",
                       text="Data")
        tabela.pack(expand=True, fill="both")

        atendimento = carregar_dados(ARQ_ATENDIMENTOS)

        for a in atendimentos:
            tabela.insert("", "end",
                          values=(a["paciente"], a["procedimento"], a["data"]))
            
        def novo_atendimento(self):
            self.limpar_tela()

        tk.Label(self.main, 
                 text="Novo Atendimento").pack()
        
        pacientes = carregar_dados(ARQ_PACIENTES)
        nomes = [p["nome"] for p in pacientes]

        tk.Label(self.main, 
                 text="Paciente").pack()
        paciente = ttk.Combobox(self.main,
                                values=nomes).pack()
        
        tk.Label(self.main,
                 text="Procedimento").pack()
        procedimento = tk.Entry(self.main)
        procedimento.pack()

        def salvar():
            atendimentos = carregar_dados(ARQ_ATENDIMENTOS)
            atendimentos.append({"paciente": paciente.get(),
                                 "procedimento:" procedimento.get(),
                                 "data": data.datetime.now().strtime("%d/%m/%Y")
                                 })
            
        salvar_dados(ARQ_ATENDIMENTOS, atendimentos)

        messagebox.showinfo("Sucesso", "Atendimento cadastrado")
        self.mostar_atendimentos()

            tk.Button(self.main,
                      text="Salvar",
                      command=salvar).pack()
    
'''
def abrir_sistema()
app = SistemaClinica(root)
root.mainloop()

root = tk.Tk()
Login(root)
root.mainloop()
'''




