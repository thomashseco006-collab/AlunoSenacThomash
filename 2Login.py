class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("Login do Sistema")
        self.root.geometry("700x400")
        self.root.configure(bg=COR_VERDE_CLARO)
        self.root.resizable(False, False)

        #Esquerda Dinâmica
        self.esquerda = tk.Frame(root, bg=COR_VERDE_CLARO, width=350)
        self.esquerda.pack(side="left", fill="both")

        #Esquerda Login
        frame = tk.Frame(root, bg=COR_VERDE_MEDIO, width=350, height=400)
        frame.pack(side="right", fill="y")

        tk.Label(frame, text="Sistema de Login",
                 bg=COR_VERDE_MEDIO, fg=COR_TEXTO_ESCURO,
                 font=("Arial", 20)).pack(pady=20)

        #Campo Usuário (placeholder discreto)
        self.usuario = tk.Entry(frame, width=30, fg=COR_MARROM)
        self.usuario.insert(0, "Nome ou Email")
        self.usuario.pack(pady=10)

        #Campo Senha com botão de mostrar (mantido)
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

    #Login-
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

    #Cadastro
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

    #Recuperar Senha
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