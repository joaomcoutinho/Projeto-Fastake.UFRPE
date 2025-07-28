
import mysql.connector
import time
from random import randint
import funcoes_fastake as fk
from email_validator import EmailNotValidError, validate_email
from rich.panel import Panel
from rich import print
from rich.console import Console
from rich.progress import track
from rich.table import Table
from rich.layout import Layout

conexao = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '2710',
    database = 'fastake'
)
cursor = conexao.cursor()
console = Console()


class Admin:
    def __init__(self, email, senha, codigo, id):
        self.email = email
        self.senha = senha
        self.codigo = codigo
        self.id = id
    def validar_email(self, email_checagem):
        cursor.execute(f"SELECT email FROM adm WHERE email = %s", (email_checagem,))
        resultado = cursor.fetchone()
        return bool(resultado)
        
    def checar_senha_adm(self, senha):
        while True:
            if not senha.isdigit():
                console.print('[bold]Escreva apenas números, no formato (1234)[/]')
                continue
            if not len(senha) == 4:
                console.print('[bold]Escreva exatamente 4 números, no formato (1234)[/]')
                continue
            break
        return senha
    @classmethod
    def cadastro_adm(cls):
        email = True
        console.print(Panel('[bold] == Bem-vindo à aba de Cadastro para Administradores == [/]'))
        while email:
            console.print('[green]Vamos realizar seu cadastro!\nPor favor preencha os dados abaixo[/]')
            email_checagem = console.input("[bold]Defina seu email: [/]") 
            if not cls.validar_modelo_email(email_checagem):
                console.print("[red]Digite seu email corretamente[/]")
                continue
            break
        senha_check = True
        while senha_check:
            senha = console.input("[bold]Defina sua senha (a senha deve conter 4 números EX: 1234 ): [/]")
            if not cls.checar_senha_adm(cls, senha):
                console.print('[red]Digite sua senha corretamente![/]')
                time.sleep(1)
                continue
            while True:
                if cls.validar_email(cls, email_checagem):
                    console.print("[red]Esse email já está cadastrado, digite o email correto[/]")
                    #adicionar função para levar para o login caso queira
                    continue
                break
            console.print("[bold]Vai ser gerado um [red]código aleatório de segurança[/]\nNÃO O PERCA! ELE SERÁ UTILIZADO CASO ESQUEÇA A SENHA[/]")
            codigo = randint(1000, 9999)
            console.print(f'[bold]Seu código : [red]{codigo}[/][/]')
            time.sleep(2)
            try:
                cursor.execute("INSERT INTO adm (email, senha, codigo) VALUES (%s, %s, %s)", (email_checagem, senha, codigo))
                conexao.commit()
            except Exception as e : 
                console.print(f"[red]Erro ao inserir no banco: {e}[/]")

                #console.print(f"[red]Houve um erro, por favor reporte aos administradores do programa\nCódigo do erro: [bold]{type(e).__name__}[/][/]")
                time.sleep(1) #type(e).__name__
                cls.cadastro_adm()

            cls.email = email_checagem
            cls.senha = senha
            cls.codigo = codigo
            senha_check = False
            console.print(Panel("[blue]Parabéns, você agora está cadastrado no sistema\n" \
            "Você será redirecionado à página de  login[/]"))
            cls.login_adm()
    @classmethod
    def login_adm(cls):
        console.print(Panel('[bold] Bem-vindo à aba de Login para Administradores[/]'))
        email = True
        while email:
            email_checagem = console.input("[green]Qual é o seu email ?[/]")
            if not cls.validar_modelo_email(email_checagem):
                console.print("[red]Digite seu email corretamente[/]")
                continue

            while True:
                senha_digitada = console.input('[green]Digite sua senha: [/]')
                if not cls.checar_senha_adm(cls, senha_digitada):
                    console.print('[red]Digite sua senha corretamente![/]')
                    continue
                cursor.execute(f"SELECT senha FROM adm WHERE email = %s", (email_checagem,))
                senha_banco = cursor.fetchone()
                senha_banco = senha_banco[0] if senha_banco else None
                if not cls.validar_email(cls, email_checagem) or senha_digitada != str(senha_banco):
                    console.print("[red]Seu email, senha ou ambos estão incorretos[/]")
                    while True:
                        escolha = console.input("[bold]Se você deseja digitar novamente, digite 1\n" \
                        "Se você deseja ir para a página de cadastro, digite 2: [/]")
                        if escolha == 2: 
                            console.print("[bold]Você irá para o cadastro[/]")
                            time.sleep(1)
                            cls.cadastro_adm()
                            break
                        if escolha == 1:
                            break
                    continue
                email = False
                break

            cursor.execute(f"SELECT codigo FROM adm WHERE email = %s", (email_checagem,))
            codigo = cursor.fetchone()[0]

            cursor.execute(f"SELECT id FROM adm WHERE email = %s", (email_checagem,))
            id = cursor.fetchone()[0]

            cls.email = email_checagem
            cls.senha = senha_banco
            cls.codigo = codigo
            cls.id = id
            with console.status('[bold]Validando informações...[/]'):
                time.sleep(3)
            console.print(Panel('[green]Login realizado com sucesso! Estamos lhe redirecionando para o menu...'))
            time.sleep(2)
            cls.menu_adm(cls)
            
    def menu_adm(self):
        while True:
                console.print(Panel('[bold]Você está no Menu! Confira as opções disponíveis: [/]'))
                opcoes = ('[bold]1 - :eyes: Ver Meu Restaurante\n[/]'
                          '[bold]2 - :wrench: Gerenciar meu Restaurante\n[/]'
                          '[bold]3 - :moneybag: Ver Meus Créditos\n[/]'
                          '[bold]4 - :key: Trocar Senha\n[/]' \
                          '[bold]5 - :door: Ir para a página inicial\n[/]'
                )
                panel = Panel(
                opcoes,
                title="[bold green]Menu Interativo [/]",
                subtitle="Fastake 1.0",
                border_style="bright_blue"
                )
                console.print(panel)
                escolha = console.input("[bold]Digite aqui a opção que você deseja: [/]")

                if escolha == '1':
                    self.ver_restaurantes_adm(self)

                elif escolha == '2':
                    self.gerenciar_restaurante(self)

                elif escolha == '3':
                    self.ver_creditos(self)

                elif escolha == '4':
                    self.trocar_senha_adm(self)
                
                elif escolha == '5':
                    from usuario import inicio
                    inicio()
                    return
                else:
                    console.print("[red]Escolha uma opção válida[/]")
                    time.sleep(1)
                    continue

    def validar_modelo_email(email):
        try:
            validate_email(email)
            return True
        except EmailNotValidError:
            return False
      
    def ver_restaurantes_adm(self):

        # Buscar restaurantes do ADM
        cursor.execute("SELECT id, restaurante FROM restaurantes WHERE id_adm = %s", (self.id,))
        restaurantes = cursor.fetchall()
        if restaurantes:
            for restaurante in restaurantes:
                id_restaurante, nome_restaurante = restaurante
                console.print(f"[bold]\nRestaurante: [green]{nome_restaurante}[/]")

                # Buscar pratos desse restaurante
                cursor.execute("SELECT nome, valor FROM pratos WHERE id_restaurante = %s", (id_restaurante,))
                pratos = cursor.fetchall()

                if not pratos:
                    console.print("[red]Nenhum prato cadastrado.[/]")
                else:
                    for nome, valor in pratos:
                        console.print(f"[bold]  Prato: {nome} |Valor: [/][green]R${valor:.2f}[/]")
            while True:
                voltar_menu = console.input("[bold]Digite [green]'SIM'[/] para voltar ao menu: [/]")
                if voltar_menu.upper() == 'SIM':
                    console.print('[bold]Estamos lhe redirecionando para o menu...[/]')
                    time.sleep(1)
                    break
                else:
                    console.print('[bold]Digite [green]"SIM"[/]![/]')
                    time.sleep(1)
                    continue
        else:
            console.print('[red]Você ainda não tem restaurantes cadastrados!')
            time.sleep(1)

    def trocar_senha_adm(self):

        tentativas = int(3)
        while True:
            if tentativas > 0:
                try:
                    entrada = int(console.input("[red]Digite o seu código: [/]"))
                except ValueError:
                    console.print("[bold]Digite apenas números.[/]")
                    tentativas -= 1
                    continue

                if entrada != self.codigo:
                    console.print("[red]Código incorreto[/]")
                    tentativas -= 1
                    continue

                if entrada == self.codigo:
                    break
            else:
                console.print("[red]O número de tentativas foi excedido, você retornará à página de início[/]")
                from usuario import inicio
                inicio()
                ''' Ver a função inicio para aplicar aqui!! '''
                break
        tentativas = int(3)
        while tentativas > 0:
            nova_senha = console.input("[green]Digite sua nova senha (4 dígitos numéricos): [/]")
            if not nova_senha.isdigit() or len(nova_senha) != 4:
                console.print("[red]Senha inválida. Digite novamente.[/]")
                tentativas -= 1
                continue
            break
        else:
            console.print("[bold]Número de tentativas excedido. Você será redirecionado ao menu.[/]")
            self.menu_adm()
            return
        try:
            cursor.execute(f"UPDATE adm SET senha = %s WHERE id = %s", (nova_senha, self.id))
            conexao.commit()
        except mysql.connector.Error as erro:
            console.print(f"[red]Erro ao fazer alteração[/]", erro, "\n"
            "[bold]Por favor, informe o erro para os desenvolvedores.\n[/]" \
            "[bold]Você será redirecionado ao menu[/]")
            self.menu_adm(self)
            return

        console.print("[green]Senha alterada com sucesso!\n[/]" \
        "[bold]Você será redirecionado ao menu[/]")
        time.sleep(1)
        self.senha = nova_senha 

        self.menu_adm(self)

    def ver_creditos(self):
        #id = self.ADM.id

        cursor.execute(f"SELECT restaurante, credito FROM restaurantes WHERE id_adm = %s ", (self.id,))
        restaurantes = cursor.fetchall()

        if not restaurantes: console.print("[red]Você não possui restaurantes cadastrados[/]")

        else:
            for restaurante in restaurantes:
                nome_restaurante, credito = restaurante
                with console.status('[green]Carregando seus restaurantes...'):
                    time.sleep(3)
                console.print("[blue] === Meus restaurantes: === [/]")
                console.print(f"[bold]Restaurante: {nome_restaurante} -[/] [green]Crédito: R${credito:2f}[/]")
        while True:

            decisao = console.input("[bold]Digite [green]'SIM'[/] quando quiser retornar ao menu: [/]")
            if decisao.upper() == 'SIM':
                console.print('[bold]Você está sendo redirecionado para o menu...[/]')
                time.sleep(1)
                self.menu_adm(self)
                break
            else:
                console.print('[bold]Digite apenas [green]"SIM"[/]')
                time.sleep(1)
                continue
        
    def gerenciar_restaurante(self):
        while True:
            console.print(Panel("[bold] === :wrench: Bem vindo ao gerenciamento do seu restaurante, veja as opçõe disponíveis: === [/]"))
            opcoes = ('[bold]1 - :pick: Editar / Adicionar restaurantes\n[/]'
                      '[bold]2 - :pick: Editar / Adicionar pratos\n[/]'
                      '[bold]3 - :heavy_dollar_sign: Editar Valores\n[/]'
                      '[bold]4 - :wastebasket: Excluir Restaurantes\n[/]'
                      '[bold]0 - :door: Voltar ao menu[/]'
            )
            panel = Panel(
                opcoes,
                title='Gerenciamento de Restaurantes',
                style='blue',
                subtitle='Fastake 1.0'
            )
            console.print(panel)
            escolha = console.input("[bold]Qual opção você deseja? Digite [red]'NAO'[/] caso queira voltar ao menu: [/]")
            if escolha == '0':
                self.menu_adm(self)
                break
            elif escolha == '1':
                self.opcao_editar_adicionar_restaurantes(self)
            elif escolha == '2':
                self.opcao_editar_adicionar_pratos(self)
            elif escolha == '3':
                self.opcao_editar_valores(self)
            elif escolha == '4':
                self.opcao_excluir_restaurante(self)
            elif escolha.upper() == 'NAO':
                console.print('[bold]Você está sendo redirecionado para o menu...[/]')
                time.sleep(2)
                break
            else:
                console.print('[red]Digite uma opção válida![/]')
                continue

    def opcao_editar_adicionar_restaurantes(self):
        #id = self.ADM.id
        cursor.execute("SELECT id, restaurante FROM restaurantes WHERE id_adm = %s", (self.id,))
        restaurantes = cursor.fetchall()

        console.print("[green]Seus restaurantes:[/]")
        for i, r in enumerate(restaurantes, start=1):
            console.print(f"[bold]{i} - Nome: {r[1]}[/]")

        console.print(Panel("[bold]1 - Editar nome de restaurante existente[/]"))
        console.print(Panel("[bold]2 - Adicionar novo restaurante[/]"))
        subopcao = console.input("[green]Escolha uma opção: [/]")

        if subopcao == "1":
            while True:
                try:
                    indice = int(console.input("[bold]Digite o número do restaurante que deseja editar: [/]")) - 1
                    if 0 <= indice < len(restaurantes):
                        restaurante_id = restaurantes[indice][0]
                        novo_nome = console.input("[green]Digite o novo nome: [/]")
                        confirmar = console.input(f"[red]Tem certeza que deseja renomear o restaurante para [bold]'{novo_nome}'[/]? (s/n): [/]")
                        if confirmar.lower() == 's':
                            with console.status('Renomeando o restaurante...'):
                                time.sleep(2)
                            cursor.execute("UPDATE restaurantes SET restaurante = %s WHERE id = %s AND id_adm = %s", (novo_nome, restaurante_id, self.id))
                            conexao.commit()
                            console.print("[green]Nome atualizado com sucesso![/]")
                            time.sleep(2)
                        else:
                            console.print("[red]Operação cancelada.[/]")
                    else:
                        console.print("[red]Opção inválida[/]")
                except ValueError:
                    console.print('[red]Tipo de dado inconsistente, digite apenas números (INT)')

        elif subopcao == "2":
            nome = console.input("[green]Digite o nome do novo restaurante: [/]")
            cursor.execute("INSERT INTO restaurantes (restaurante, id_adm, credito) VALUES (%s, %s, 0)", (nome, self.id))
            conexao.commit()
            console.print("[green]Restaurante adicionado com sucesso!\n[/][bold]Para adicionar pratos e valores, acesse as opções correspondentes no menu.[/]")
            time.sleep(3)
        self.menu_adm(self)

    def opcao_editar_adicionar_pratos(self):
        #id = self.ADM.id
        cursor.execute("SELECT id, restaurante FROM restaurantes WHERE id_adm = %s", (self.id,))
        restaurantes = cursor.fetchall()

        if not restaurantes:
            console.print("[red]Você não possui restaurantes cadastrados.[/]")
            self.menu_adm()
            return

        console.print("[green]Seus restaurantes:[/]")
        for i, r in enumerate(restaurantes, start=1):
            console.print(f"[blue]{i} - Nome: {r[1]}[/]")
        while True:
            try:
                indice_rest = int(input("Escolha o restaurante: ")) - 1
                if 0 <= indice_rest < len(restaurantes):
                    restaurante_id = restaurantes[indice_rest][0]
                    break
                else:
                    print("Opção inválida")
                    self.menu_adm(self)
                    break
            except ValueError:
                console.print('[red]Tipo de dado incosistente, digite apenas dados númericos (INT)![/]')
                time.sleep(1)
                continue
        console.print(Panel("[bold]1 - Adicionar novo prato[/]"))
        console.print(Panel("[bold]2 - Editar prato existente[/]"))
        console.print(Panel("[bold]3 - Excluir prato[/]"))
        subopcao = console.input("[green]Escolha uma opção: [/]")

        cursor.execute("SELECT id, nome FROM pratos WHERE id_restaurante = %s", (restaurante_id,))
        pratos = cursor.fetchall()

        if subopcao == "1":
            nome = console.input("[bold]Digite o nome do prato: [/]")
            try:
                valor = float(console.input("[green]Digite o valor do prato: [/]"))
                if valor < 0:
                    console.print("[red]Valor não pode ser negativo.[/]")
                    self.menu_adm(self)
                    return
            except ValueError:
                console.print("[red]Valor inválido, digite apenas dados númericos.[/]")
                self.menu_adm(self)
                return
            cursor.execute("INSERT INTO pratos (nome, valor, id_restaurante) VALUES (%s, %s, %s)", (nome, valor, restaurante_id))
            conexao.commit()
            console.print("[green]Prato adicionado com sucesso![/]")

        elif subopcao == "2":
            for i, p in enumerate(pratos, start=1):
                console.print(f"[blue]{i} - Nome: {p[1]}[/]")
            while True:
                try:
                    indice = int(console.input("[bold]Escolha o prato para editar: [/]")) - 1
                    if 0 <= indice < len(pratos):
                        prato_id = pratos[indice][0]
                        novo_nome = console.input("[green]Digite o novo nome do prato: [/]")
                        with console.status('[bold]Atualizando o novo nome do prato...[/]'):
                            time.sleep(2)
                        cursor.execute("UPDATE pratos SET nome = %s WHERE id = %s", (novo_nome, prato_id))
                        conexao.commit()
                        console.print("[green]Prato atualizado com sucesso![/]")
                    else:
                        console.print("[red]Opção inválida[/]")
                        time.sleep(1)
                except ValueError:
                    console.print('[red]Tipo de dado inconsistente, digite apenas dados numéricos (INT) [/]')
                    time.sleep(1)

        elif subopcao == "3":
            for i, p in enumerate(pratos, start=1):
                console.print(f"[blue]{i} - Nome: {p[1]}[/]")
            while True:
                try:
                    indice = int(console.input("[bold]Escolha o prato para excluir: [/]")) - 1
                    if 0 <= indice < len(pratos):
                        prato_id = pratos[indice][0]
                        confirmar = console.input("[bold]Tem certeza que deseja [red]EXCLUIR[/] este prato? (s/n): [/]")
                        if confirmar.lower() == 's':
                            cursor.execute("DELETE FROM pratos WHERE id = %s", (prato_id,))
                            conexao.commit()
                            with console.status('[bold]Excluindo o prato...'):
                                time.sleep(2)
                            console.print("[green]Prato excluído com sucesso![/]")
                        else:
                            console.print("[red]Operação cancelada.[/]")
                    else:
                        console.print("[red]Opção inválida[/]")
                        time.sleep(1)
                except ValueError:
                    console.print('[red]Tipo de dado incosistente, digite apenas valores numéricos![/]')
                    time.sleep(1)

        self.menu_adm(self)

    def opcao_editar_valores(self):
        #id = self.ADM.id
        cursor.execute("SELECT id, restaurante FROM restaurantes WHERE id_adm = %s", (self.id,))
        restaurantes = cursor.fetchall()
        while True:
            for i, r in enumerate(restaurantes, start=1):
                console.print(f"[blue]{i} - Nome: {r[1]}[/]")
        
            try:
                indice = int(console.input("[bold]Escolha o restaurante: [/]")) - 1
                if 0 <= indice < len(restaurantes):
                    restaurante_id = restaurantes[indice][0]
                    break
                else:
                    console.print("[red]Opção inválida, tente novamente![/]")
                    time.sleep(1)
                    continue
            except ValueError:
                console.print('[red]Tipo de dado inconsistente, digite apenas valores numéricos!')
                time.sleep(1)
                continue

        cursor.execute("SELECT id, nome, valor FROM pratos WHERE id_restaurante = %s", (restaurante_id,))
        pratos = cursor.fetchall()
        while True:
            for i, p in enumerate(pratos, start=1):
                console.print(f"[blue]{i} - Nome: {p[1]} - Valor: R${p[2]:.2f}[/]")
            try:
                indice_prato = int(console.input("[green]Escolha o prato para alterar o valor: [/]")) - 1
                if 0 <= indice_prato < len(pratos):
                    prato_id = pratos[indice_prato][0]
                    break
                else:
                    console.print('[red]Opção inválida[/]')
                    time.sleep(1)
                    continue
            except ValueError:
                console.print('[red]Tipo de dado inconsistente, Digite apenas valores numéricos!')
                time.sleep(1)
                continue
        while True:
            try:
                novo_valor = float(console.input("[green]Digite o novo valor ( No formato a seguir: 9.90 ) : [/]"))
                if novo_valor < 0:
                    console.print("[red]Valor não pode ser negativo.[/]")
                    time.sleep(1)
                    continue
            except ValueError:
                console.print("[red]Valor inválido.[/]")
                time.sleep(1)
                continue
            cursor.execute("UPDATE pratos SET valor = %s WHERE id = %s", (novo_valor, prato_id))
            conexao.commit()
            with console.status('[green]Atualizando valor...'):
                time.sleep(2)
            console.print("[green]Valor atualizado com sucesso![/]")
            console.print('[bold]Estamos lhe redirecionando para o menu...[/]')
            break
        self.menu_adm(self)

    def opcao_excluir_restaurante(self):
        #id = self.ADM.id
        cursor.execute("SELECT id, restaurante FROM restaurantes WHERE id_adm = %s", (self.id,))
        restaurantes = cursor.fetchall()

        for i, r in enumerate(restaurantes, start=1):
            console.print(f"[blue]{i} - Nome: {r[1]}[/]")
        while True:
            try:
                indice = int(console.input("[bold]Escolha o restaurante que deseja excluir: [/]")) - 1
                if 0 <= indice < len(restaurantes):
                    restaurante_id = restaurantes[indice][0]
                    break
                else:
                    console.print("[red]Opção inválida[/]")
                    time.sleep(1)
                    continue
            except ValueError:
                console.print('[red]Tipo de dado incorreto, insira um dado do tipo INT![/]')
                time.sleep(1)
                continue
        
        tentativas = 3
        while tentativas > 0:
            try:
                codigo = int(console.input("[red]Digite o código de segurança para confirmar: [/]"))
                if codigo == self.codigo:
                    cursor.execute("DELETE FROM pratos WHERE id_restaurante = %s", (restaurante_id,))
                    cursor.execute("DELETE FROM restaurantes WHERE id = %s AND id_adm = %s", (restaurante_id, self.id))
                    conexao.commit()
                    with console.status('[green]Excluindo restaurantes[/]'):
                        time.sleep(3)
                    console.print("[red]Restaurante e seus pratos excluídos com sucesso![/]")
                    break
                else:
                    console.print("[red]Código incorreto[/]")
                    tentativas -= 1
            except ValueError:
                console.print("[red]Digite apenas números.[/]")
                tentativas -= 1
        else:
            console.print("[bold]Tentativas excedidas. Você será redirecionado ao menu.[/]")
            time.sleep(2)

        self.menu_adm(self)

    def adm():
        while True:
            console.print(Panel('[bold]Bem vindo administrador!\nO que você deseja fazer?\n[/][blue]1 - Cadastrar Usuário\n[/][green]2 - Login\n[/][bold]Escolha entre as opções disponíveis: [/]'))
            escolha = console.input('[bold]Digite aqui: ')
            if escolha == '1':
                console.print('[bold]Você está sendo redirecionado para o cadastro![/]')
                time.sleep(1)
                admin_cadastrado = Admin.cadastro_adm() # Pass conexao and cursor
                break
            elif escolha == '2':
                console.print('[bold]Você está sendo redirecionado para o login![/]')
                time.sleep(1)
                admin_logado = Admin.login_adm() # Pass conexao and cursor
                break
            else:
                console.print('[red]Digite uma opção válida![/]')
                time.sleep(1)
                continue