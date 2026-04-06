import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

#Banco de dados
conn = sqlite3.connect("clinica.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT UNIQUE,
    senha TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS pacientes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    nascimento TEXT,
    telefone TEXT,
    email TEXT,
    cpf TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS atendimentos(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    paciente TEXT,
    procedimento TEXT,
    data TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS prontuario(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    paciente TEXT,
    descricao TEXT,
    data TEXT
)
""")

conn.commit()

#App
class App:
    def _init_(self, root):
        self.root = root
        self.root.title("Sistema Clínica")
        self.root.geometry("1200x650")

        self.frame_login = tk.Frame(root)
        self.frame_sistema = tk.Frame(root)

        self.tela_login()

    #Login
    def tela_login(self):
        for widget in self.frame_login.winfo_children():
            widget.destroy

        self.frame_sistema.pack_forget()
        self.frame_login.pack(expand=True)

        tk.Label(self.frame_login, text="Sistema Clínica",
                 font=("Arial", 22)).pack(pady=20)

        tk.Label(self.frame_login, text="Usuário").pack()
        self.usuario = tk.Entry(self.frame_login)
        self.usuario.pack()

        tk.Label(self.frame_login, text="Senha").pack()
        self.senha = tk.Entry(self.frame_login, show="*")
        self.senha.pack()

        tk.Button(self.frame_login, text="Login",
                  command=self.login).pack(pady=10)

        tk.Button(self.frame_login, text="Cadastrar",
                  command=self.cadastrar).pack()

    def login(self):
        if self.usuario.get() == "" or self.senha.get() == "":
            messagebox.showerror("Erro", "Preencha usuário e senha")
            return

        cursor.execute("SELECT * FROM usuarios WHERE usuario=? AND senha=?",
                       (self.usuario.get(), self.senha.get()))
        user = cursor.fetchone()

        if user:
            self.abrir_sistema()
        else:
            messagebox.showerror("Erro", "Login inválido")

    def cadastrar(self):
        if self.usuario.get() == "" or self.senha.get() == "":
            messagebox.showerror("Erro", "Preencha usuário e senha")
            return

        try:
            cursor.execute("INSERT INTO usuarios(usuario, senha) VALUES(?,?)",
                           (self.usuario.get(), self.senha.get()))
            conn.commit()
            messagebox.showinfo("Sucesso", "Usuário cadastrado")
        except:
            messagebox.showerror("Erro", "Usuário já existe")

    #Sistema
    def abrir_sistema(self):
        self.frame_login.pack_forget()
        self.frame_sistema.pack(fill="both", expand=True)

        self.menu = tk.Frame(self.frame_sistema, bg="#2c3e50", width=200)
        self.menu.pack(side="left", fill="y")

        self.main = tk.Frame(self.frame_sistema, bg="#ecf0f1")
        self.main.pack(side="right", expand=True, fill="both")

        tk.Button(self.menu, text="Dashboard", width=20,
                  command=self.dashboard).pack(pady=5)

        tk.Button(self.menu, text="Pacientes", width=20,
                  command=self.tela_pacientes).pack(pady=5)

        tk.Button(self.menu, text="Cadastrar Paciente", width=20,
                  command=self.cadastrar_paciente).pack(pady=5)

        tk.Button(self.menu, text="Atendimentos", width=20,
                  command=self.tela_atendimentos).pack(pady=5)

        tk.Button(self.menu, text="Novo Atendimento", width=20,
                  command=self.novo_atendimento).pack(pady=5)

        tk.Button(self.menu, text="Prontuário", width=20,
                  command=self.tela_prontuario).pack(pady=5)

        tk.Button(self.menu, text="Logout", width=20,
                  command=self.logout).pack(pady=20)

        self.dashboard()

    def limpar_tela(self):
        for widget in self.main.winfo_children():
            widget.destroy()

    def logout(self):
        self.frame_sistema.pack_forget()
        self.tela_login() #(expand=True)
        self.usuario.delete(0, tk.END)
        self.senha.delete(0, tk.END)

    #Dashboard
    def dashboard(self):
        self.limpar_tela()

        cursor.execute("SELECT COUNT(*) FROM pacientes")
        pacientes = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM atendimentos")
        atendimentos = cursor.fetchone()[0]

        tk.Label(self.main, text="Dashboard",
                 font=("Arial", 24)).pack(pady=20)

        tk.Label(self.main, text=f"Pacientes cadastrados: {pacientes}").pack()
        tk.Label(self.main, text=f"Atendimentos realizados: {atendimentos}").pack()

    #Pacientes
    def tela_pacientes(self):
        self.limpar_tela()

        tk.Label(self.main, text="Pacientes",
                 font=("Arial", 18)).pack(pady=10)

        busca = tk.Entry(self.main)
        busca.pack()

        tabela = ttk.Treeview(self.main,
                              columns=("ID", "Nome", "Telefone", "CPF"),
                              show="headings")

        for col in ("ID", "Nome", "Telefone", "CPF"):
            tabela.heading(col, text=col)

        tabela.pack(expand=True, fill="both")

        def carregar():
            for i in tabela.get_children():
                tabela.delete(i)

            cursor.execute("SELECT id, nome, telefone, cpf FROM pacientes WHERE nome LIKE ?",
                           ('%' + busca.get() + '%',))

            for p in cursor.fetchall():
                tabela.insert("", "end", values=p)

        carregar()

        tk.Button(self.main, text="Buscar", command=carregar).pack()

        def excluir():
            item = tabela.selection()
            if not item:
                return
            id_p = tabela.item(item)["values"][0]
            cursor.execute("DELETE FROM pacientes WHERE id=?", (id_p,))
            conn.commit()
            carregar()

        tk.Button(self.main, text="Excluir", command=excluir).pack()

    def cadastrar_paciente(self):
        self.limpar_tela()

        campos = {}

        for campo in ["Nome", "Nascimento", "Telefone", "Email", "CPF"]:
            tk.Label(self.main, text=campo).pack()
            entry = tk.Entry(self.main)
            entry.pack()
            campos[campo] = entry

        def salvar():
            if campos["Nome"].get() == "":
                messagebox.showerror("Erro", "Nome obrigatório")
                return

            cursor.execute("""
            INSERT INTO pacientes(nome, nascimento, telefone, email, cpf)
            VALUES(?,?,?,?,?)
            """, (
                campos["Nome"].get(),
                campos["Nascimento"].get(),
                campos["Telefone"].get(),
                campos["Email"].get(),
                campos["CPF"].get()
            ))
            conn.commit()
            messagebox.showinfo("Sucesso", "Paciente cadastrado")

        tk.Button(self.main, text="Salvar", command=salvar).pack(pady=10)

    #tendimentos
    def tela_atendimentos(self):
        self.limpar_tela()

        tabela = ttk.Treeview(self.main,
                              columns=("Paciente", "Procedimento", "Data"),
                              show="headings")

        for col in ("Paciente", "Procedimento", "Data"):
            tabela.heading(col, text=col)

        tabela.pack(expand=True, fill="both")

        cursor.execute("SELECT paciente, procedimento, data FROM atendimentos")
        for a in cursor.fetchall():
            tabela.insert("", "end", values=a)

    def novo_atendimento(self):
        self.limpar_tela()

        cursor.execute("SELECT nome FROM pacientes")
        nomes = [n[0] for n in cursor.fetchall()]

        tk.Label(self.main, text="Paciente").pack()
        paciente = ttk.Combobox(self.main, values=nomes)
        paciente.pack()

        tk.Label(self.main, text="Procedimento").pack()
        procedimento = tk.Entry(self.main)
        procedimento.pack()

        def salvar():
            if paciente.get() == "" or procedimento.get() == "":
                messagebox.showerror("Erro", "Preencha os campos")
                return

            cursor.execute("""
            INSERT INTO atendimentos(paciente, procedimento, data)
            VALUES(?,?,?)
            """, (
                paciente.get(),
                procedimento.get(),
                datetime.now().strftime("%d/%m/%Y")
            ))
            conn.commit()
            messagebox.showinfo("Sucesso", "Atendimento cadastrado")

        tk.Button(self.main, text="Salvar", command=salvar).pack()

    
#Prontuário
    def tela_prontuario(self):
        self.limpar_tela()

        cursor.execute("SELECT nome FROM pacientes")
        nomes = [n[0] for n in cursor.fetchall()]

        tk.Label(self.main, text="Paciente").pack()
        paciente = ttk.Combobox(self.main, values=nomes)
        paciente.pack()

        tk.Label(self.main, text="Descrição").pack()
        descricao = tk.Entry(self.main, width=50)
        descricao.pack()

        def salvar():
            if paciente.get() == "" or descricao.get() == "":
                messagebox.showerror("Erro", "Preencha os campos")
                return

            cursor.execute("""
            INSERT INTO prontuario(paciente, descricao, data)
            VALUES(?,?,?)
            """, (
                paciente.get(),
                descricao.get(),
                datetime.now().strftime("%d/%m/%Y")
            ))
            conn.commit()
            messagebox.showinfo("Sucesso", "Registro salvo")

        tk.Button(self.main, text="Salvar", command=salvar).pack()


#Fechar Banco de dados
def fechar():
    conn.comit()
    conn.close()
    root.destroy()


#Main
root = tk.Tk()
app = App(root)
root.protocol("WM_DELETE_WINDOW", fechar)
root.mainloop()