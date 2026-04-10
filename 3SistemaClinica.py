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

    #Dashboard
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

    #Pacientes
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

    #Novo Paciente
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

    #Atendimentos
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

    #Novo Atendimento
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
        
#Abertura do Sistema
def abrir_sistema(root_login):
    sistema = tk.Toplevel(root_login)
    SistemaClinica(sistema)

#Start na Tela de Login
if __name__ == "__main__":
    root = tk.Tk()
    Login(root)
    root.mainloop()