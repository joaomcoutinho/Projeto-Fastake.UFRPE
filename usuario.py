
import mysql.connector
import time
from random import randint
from unidecode import unidecode
from adm import Admin
from rich.panel import Panel
from rich import print
from rich.console import Console
from rich.progress import track
from rich.table import Table
from rich.layout import Layout
console = Console()
conexao = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '2710',
    database = 'fastake'
)
cursor = conexao.cursor()

class Checagem:

    ''' Classe para armarzenar os métodos de checagem de dados ( cpf, senha e código ) existentes ao longo do sistema, através de restrições e validações '''


    def checar_cpf(self, cpf):

        ''' Checar o CPF no processo de logi/cadastro, antes de outras possibilidades do usuário, como , ao rrar, ter a possibilidade de tentar
        novamente ou ir para a aba inicial '''

        
            
        if not cpf.isdigit():
            console.print('[bold]Digite apenas números, no formato (12345678912)[/]')
            return False # == VERIFICAR SE HÁ APENAS NÚMEROS ==
        #cpf = int(cpf)
        if not len(str(cpf)) == 11: # == VERIFICAÇÃO DA QUANTIDADE DE DÍGITOS DO CPF ==
            console.print('[bold]Digite exatamente 11 números[/]')
            return False
        return True    
                
    def checar_codigo(self, codigo, cpf):

        ''' Checagem do código de acordo com certos critérios, como tamanho do mesmo e se possui apenas dígitos '''

        cod = True
        while cod:
            
                if not str(codigo).isdigit() or len(str(codigo)) != 4:
                    console.print('[bold]Código inválido, tente novamente[/]!')
                    while True:
                        try:
                            codigo = console.input('[red]Digite aqui novamente: [/]')
                            if not str(codigo).isdigit() or len(str(codigo)) != 4:
                                console.print('[bold]Código inválido, tente novamente[/]!')
                            codigo = int(codigo)
                            cursor.execute('SELECT * FROM cadastros WHERE cpf = %s AND codigo = %s', (cpf, codigo))
                            if not cursor.fetchone():
                                console.print('[bold]Código incorreto.[/]')
                                continue
                            cod = False
                            break
                        except ValueError:
                            console.print('[red]Tipo de dado incorreto, insira apenas dados númericos (INT)[/]')
                            continue
                
                codigo = int(codigo)
                cursor.execute('SELECT * FROM cadastros WHERE cpf = %s AND codigo = %s', (cpf, codigo))
                while True:
                    try:
                        if not cursor.fetchone():
                            console.print('[bold]Código incorreto, tente novamente![/]')
                            codigo = console.input('[red]Digite aqui: [/]')
                            codigo = int(codigo)
                            cursor.execute('SELECT * FROM cadastros WHERE cpf = %s AND codigo = %s', (cpf, codigo))
                            if not cursor.fetchone():
                                console.print('[bold]Tente novamente![/]')
                                continue
                        cod = False
                        break   
                    except ValueError:
                        console.print('Tipo de dado incosistente, digite dados númericos (INT)')
                        continue

    def checar_senha_login(self, senha):

        ''' Checar a senha no ato de login, para verificar se há apenas dígitos e analisar o tamanho da senha '''

        while True:
            if not str(senha).isdigit() or len(str(senha)) != 4:
                    console.print('[bold]Senha inválida. Tente novamente![/]')
                    while True:
                        senha = console.input('[green]Digite aqui: [/]')
                        if not str(senha).isdigit() or len(str(senha)) != 4:
                            console.print('[bold]Tente novamente![/]')
                            continue
                        break
            senha = int(senha)
            break

    def checar_senha_cadastro(self, senha):

        ''' Checar as restrições de uma senha no ato de cadastro, para analisar se estão de acordo '''

        while True:
            if not str(senha).isdigit() or len(str(senha)) != 4:
                    console.print('[bold]Senha inválida! Deve conter exatamente 4 dígitos numéricos.[/]')
                    return False
            senha = int(senha)
            return True
            

    def checar_senha_compra(conexao, cpf):

        ''' Checagem de senha realizada no ato da compra de um produto em certo restaurante '''

        while True:
            senha_checagem = console.input('[green]Digite sua senha para continuar: [/]')
            if not str(senha_checagem).isdigit():
                console.print('[bold]Escreva apenas números, no formato (1234)[/]')
                continue
            if not len(str(senha_checagem)) == 4:
                console.print('[bold]Escreva exatamente 4 números, no formato (1234)[/]')
                continue
            break
        cursor.execute(f'SELECT senha FROM cadastros WHERE cpf = %s', (cpf,))
        senha_certa = cursor.fetchone()
        if senha_checagem == str(senha_certa[0]):
            return True
        else: 
            return False

check = Checagem()


class Usuario:

    ''' Classe para armazenar os objetos do usuário instanciado, bem como as suas possibilidades de ações dentro do programa
    como fazer login ; cadastrar ou até mesmo deletar a conta, abrangendo um CRUD completo '''

    def __init__(self, cpf, senha, codigo):
        self.cpf = cpf
        self.senha = senha
        self.codigo = codigo

    @classmethod
    def fazer_login(cls, conexao, cursor):

        ''' Login de um usuário já cadastrado '''

        console.print(Panel('Bem-vindo ao Login', style='bold'))
        login = True
        while login: 
            while True:
                cpf = console.input('[green]Digite aqui seu CPF: [/]')
                check.checar_cpf(cpf)
                try:
                    cursor.fetchall()
                except:
                    pass
                checagem_cpf = "SELECT cpf FROM cadastros WHERE cpf = %s" # == CHECAR EXISTÊNCIA DO CPF NO BANCO DE DADOS ==
                cursor.execute(checagem_cpf, (cpf,))
                resultado = cursor.fetchall()
                if resultado:
                    console.print(f'[green]CPF validado![/]')
                else:
                    while True:
                        decisao = console.input(f'[bold]CPF não existente, digite 1 para ir até a aba inicial:[/] ')
                        if decisao == '1':
                            inicio()
                            login = False
                            break
                        else:
                            console.print('[bold]Digite apenas "1"![/]')
                            continue
                break

            while True:
                senha = console.input('[green]Digite aqui sua senha (4 dígitos): [/]')
                check.checar_senha_login(senha)
                try:
                    cursor.fetchall()
                except:
                    pass
                cursor.execute('SELECT * FROM cadastros WHERE cpf = %s AND senha = %s', (cpf, senha))
                verify = cursor.fetchone()
                if not verify:
                    decisao = True
                    while decisao: 
                        console.print('[bold]Senha incorreta, você esqueceu sua senha? Digite 1 para recupera-la ou 2 para tentar novamente: [/]')
                        decisao_senha = int(console.input('[bold]Digite aqui: [/]'))
                        if decisao_senha == 1:
                            cls.recuperar_senha(cls)
                            decisao = False
                            break
                        elif decisao_senha == 2:
                            tentativa = True
                            while tentativa:
                                senha = console.input('[bold]Digite aqui: [/]')
                                senha = int(senha)
                                cursor.execute('SELECT * FROM cadastros WHERE cpf = %s AND senha = %s', (cpf, senha))
                                if not cursor.fetchone():
                                    continue
                                tentativa = False
                                decisao = False
                        else:
                            console.print('[red]Digite uma opção válida![/]')
                            time.sleep(1)
                            continue
                else:
                    verify = cursor.fetchone()
                break
            try:
                cursor.fetchall()
            except:
                pass
            cursor = conexao.cursor()
            cursor.execute(f'SELECT codigo FROM cadastros WHERE cpf = %s', (cpf,))
            codigo = cursor.fetchone()[0]
            with console.status('[bold]Processando as informações...[/]'):
                time.sleep(3)
            console.print('[green]Login realizado com sucesso!, estamos lhe redirecionando para o menu![/]')
            menu()
            login = False
            return cls(cpf, senha, codigo)
    
    @classmethod
    def cadastrar(cls):

        ''' Cadastro do usuário'''
        console.print(Panel('Bem-vindo ao Cadastro', style='bold'))

        time.sleep(1)
        cadastro = True
        while cadastro:
            while True:
                cpf = console.input('[green]Digite aqui seu CPF (No formato 11133344455): [/]')
                if check.checar_cpf(cpf):
                    console.print('[bold]Formato válido[/]')
                else:
                    console.print('[red]Formato inválido[/]')
                    time.sleep(1)
                    continue
                # Verificar se CPF já existe
                
                cursor.execute('SELECT * FROM cadastros WHERE cpf = %s', (cpf,))
                if cursor.fetchone():
                    console.print('[bold]Este CPF já está cadastrado. Tente fazer login.\nEstamos lhe redirecionando para a página inicial...[/]')
                    time.sleep(1)
                    inicio()
                    return
                break

            while True:
                senha = console.input('[green]Digite aqui sua senha (4 dígitos): [/]')
                if check.checar_senha_cadastro(senha):
                    console.print('[green]Senha validada com sucesso[/]')
                    time.sleep(1)
                    break
                else:
                    console.print('[red]Digite a senha no formato correto![/]')
                    time.sleep(1)
                    continue

            codigo = randint(999, 10000)
            console.print(f'[bold]Aqui está seu código gerado aleatoriamente: [red]{codigo}[/]\nGuarde-o de forma segura para utilizá-lo no nosso sistema[/]')
            time.sleep(1)
            # Inserir no banco
            cursor.execute(
                'INSERT INTO cadastros (cpf, senha, codigo) VALUES (%s, %s, %s)',
                (cpf, senha, codigo)
            )
            conexao.commit()
            console.print('[bold]Cadastro finalizado com sucesso! Estamos lhe redirecionando para a página inicial para o login[/]')

            # Retorna a instância de Usuario
            return cls(cpf, senha, codigo)
    
    def trocar_senha(self):

        ''' Método específico para a troca de senha pelo usuário através de seu código de segurança gerado no cadastro '''
        console.print(Panel('[bold]:lock: Vamos ao processo de troca de senha![/]'))
        codigo_trocar = console.input('[red]Digite aqui seu código de segurança: [/]')
        Checagem.checar_codigo(self, codigo_trocar, self.cpf)
        try:
            nova_senha = console.input('[green]Digite sua nova senha aqui: [/]')
            if len(nova_senha) == 4 and nova_senha.isdigit(): # == VERIFICAÇÃO PARA SENHA DE 4 DÍGITOS ==
                comando_novasenha = f'UPDATE cadastros SET senha = %s WHERE codigo = %s' # == UPDATE DA SENHA NO BANCO DE DADOS ==
                cursor.execute(comando_novasenha, (nova_senha, codigo_trocar))
                conexao.commit()
                time.sleep(1)
                with console.status('[green]Salvando senha...[/]'):
                    time.sleep(3)
                self.senha = nova_senha
                console.print('[green]Senha salva com sucesso!\nVocê está sendo redirecionado para o menu[/]')
                time.sleep(1)
            else:
                raise ValueError
        except ValueError: # == ERRO TRATÁVEL PARA SENHA QUE CONTER CARACTERES ( STRINGS ) ==
                console.print('[bold]Senha inválida, tente novamente utilizando os padrões corretos! (1234)')
                time.sleep(1)
                senha_invalida = True
                while senha_invalida: # == LOOP PARA, ENQUANTO A SENHA NÃO CONTER AS RESTRIÇÕES, SOLICITAR AO USUÁRIO NOVAMENTE A SENHA ==
                    try:
                        nova_senha = console.input('[bold]Tente novamente: [/]')
                        if len(nova_senha) == 4 and nova_senha.isdigit():
                            time.sleep(1)
                            comando_novasenha = f'UPDATE cadastros SET senha = {nova_senha} WHERE codigo = %s' # == UPDATE NO BANCO DE DADOS ==
                            cursor.execute(comando_novasenha, (codigo_trocar,))
                            conexao.commit()
                            with console.status('[green]Salvando senha...[/]'):
                                time.sleep(3)
                            console.print('[green]Senha salva com sucesso![/]')
                            self.senha = nova_senha
                            time.sleep(1)
                            console.print('[bold]Você está sendo redirecionado para o menu![/]')
                            time.sleep(1)
                            senha_invalida = False
                        else:
                            console.print('[red]Senha deve ter 4 dígitos![/]')
                            senha_invalida = True
                    except ValueError:
                        console.print('[red]Você deve digitar apenas números[/]')

    def deletar_conta(self):

        ''' Deletar a conta do usuário do sistema a partir de uma verificação de CPF '''
        console.print(Panel('[bold]:wastebasket: Vamos ao processo de exclusão da conta[/]'))
        time.sleep(1)
        cpf = str((console.input('[bold]Digite o CPF da conta a ser apagada: [/]'))) # == VERIFICAÇÃO POR CPF ==
        consulta2 = 'SELECT * FROM cadastros WHERE cpf = %s'
        cursor.execute(consulta2, (cpf,))
        resultado = cursor.fetchone()
        if resultado:
            console.print('[green]CPF validado![/]')
            time.sleep(1)
        else:
            while True: # == LOOP PARA SOLICITAR UM CPF VÁLIDO ATÉ O USUÁRIO ACERTAR ==
                cpf = str((console.input('[bold]Digite novamente um CPF válido![/]')))
                consulta3 = 'SELECT * FROM cadastros WHERE cpf = %s'
                cursor.execute(consulta3, (cpf,))
                resultado = cursor.fetchone()
                if resultado:
                    console.print('[green]CPF validado![/]')
                    time.sleep(1)
                    False
                else:
                    console.print('[bold]Escreva seu CPF correto: [/]')
                    time.sleep(1) 
                    continue  
        decisao_delete = str(console.input('[bold]Digite [green]SIM[/] para confirmar a exclusão da conta ou [red]NAO[/] para retornar ao menu: [/]')) # == CONFIRMAÇÃO DE EXCLUSÃO ==
        decisao_invalida = True
        if decisao_delete.upper() == 'SIM':
            comando = 'DELETE FROM cadastros WHERE cpf = %s ' # == DELETE DA CONTA NO BANCO DE DADOS ==
            cursor.execute(comando, (cpf,))
            conexao.commit()
            with console.status('[green]Deletando a conta...'):
                time.sleep(3)
            console.print('[red]Conta deletada com sucesso!\nVocê está sendo redirecionado para a página inicial[/]')
            time.sleep(1)
            inicio()
        elif decisao_delete.upper() == 'NAO':
            console.print('[bold]Você está sendo redirecionado para o menu![/]')
            time.sleep(1)
        else:
            console.print('[bold]Tente novamente uma opção válida![/]')
            time.sleep(1)
            while decisao_invalida:
                decisao_delete2 = str(console.input('[green]Digite SIM para confirmar a exclusão da conta ou [red]NAO[/] para retornar ao menu! [/]'))
                if decisao_delete2.upper() == 'SIM':
                    comando = 'DELETE FROM cadastros WHERE cpf = %s'
                    cursor.execute(comando, (cpf,)) # == DELETE DA CONTA NO BANCO DE DADOS ==
                    conexao.commit()
                    with console.status('[green]Deletando a conta...[/]'):
                        time.sleep(3)
                    console.print('[red]Conta deletada com sucesso!\nVocê está sendo redirecionado para a página inicial [/]')
                    inicio()
                    time.sleep(1)
                    decisao_invalida = False
                    break
                elif decisao_delete2.upper() == 'NAO':
                    console.print('[bold]Você está sendo redirecionado para o menu![/]')
                    time.sleep(1)
                    decisao_invalida = False
                    break
                else:
                    console.print('[bold]Tente novamente uma opção válida![/]')
                    time.sleep(1)

    def creditos_ver(self):
            
            ''' Carregamento e impressão dos créditos do usuário, bem como a possível adição de créditos caso  o mesmo deseje '''
            console.print(Panel('[bold]:money_with_wings: Indo para a aba de créditos[/]'))
            time.sleep(1)
            console.print('[bold]Estamos carregando seu saldo de créditos...[/]')
            time.sleep(1)
            consulta_credito = 'SELECT credito FROM cadastros WHERE cpf = %s' # == ANÁLISE DO CRÉDITO QUE O USUÁRIO POSSUI NO BANCO DE DADOS ==
            cursor.execute(consulta_credito, (self.cpf,))
            resultado = cursor.fetchone()
            credito_atual = float(resultado[0]) # == IMPRIME O NÚMERO DE CRÉDITOS ==
            console.print(f'[bold]Você tem [green]{credito_atual}[/] créditos[/]')
            time.sleep(1)

            add = console.input('[bold]Você deseja adicionar mais créditos? Digite [green]SIM[/] para adicionar, caso contrário será redirecionado para o menu: [/]')
            if add.upper() == 'SIM':
                quantia = float(console.input('[green]Digite a quantia desejada, em R$: \n[/]'))
                quantia_nova = credito_atual + quantia
                while True: # == SIMULAÇÃO DE PAGAMENTO AO ADICIONAR CRÉDITOS ==
                    console.print(Panel('[bold]=== FORMAS DE PAGAMENTO ===\n[/]' \
                    ' [bold]1 - :moneybag: PIX\n[/]' \
                    ' [bold]2 - :credit_card: Cartão de crédito\n[/]' \
                    ' [bold]3 - :credit_card: Cartão de débito\n [/]'
                    ))
                    forma_pagamento = console.input('[green]Qual será a forma de pagamento? Digite entre 1, 2 ou 3:  [/]')
                    if forma_pagamento == '1':
                        with console.status('[bold]Estamos processando sua solicitação de pagamento via PIX[/]'):
                            time.sleep(3)
                        break
                    elif forma_pagamento == '2':
                        with console.status('[bold]Estamos processando sua solicitação de pagamento via Cartão de Crédito[/]'):
                            time.sleep(3)
                        break
                    elif forma_pagamento == '3':
                        with console.status('[bold]Estamos processando sua solicitação de pagamento via Cartão de Débito[/]'):
                            time.sleep(3)
                        break
                    else:
                        console.print('[red]Escolha uma forma de pagamento válida[/]')
                time.sleep(1)
                adicionar_quantia = 'UPDATE cadastros SET credito = %s WHERE cpf = %s' # == UPDATE DE CRÉDITOS NO BANCO DE DADOS ==
                cursor.execute(adicionar_quantia, (quantia_nova, self.cpf))
                conexao.commit()
                console.print('[green]Processo finalizado com sucesso![/]')
                time.sleep(1)
            else:
                console.print('[bold]Você está sendo redirecionado para o menu...[/]')
                time.sleep(1)

    def recuperar_senha(self):

        ''' Recuperação de senha realizada no processo de login, caso o usuário se esqueça de sua credencial '''

        while True: # == RECUPERAÇÃO DE SENHA ATRAVÉS DO CÓDIGO PESSOAL ==
            codigo = console.input('[red]Informe seu código pessoal para recuperar sua senha: [/]')
            if not codigo.isdigit(): # == VERIFICAÇÃO SE HÁ APENAS NÚMEROS ==
                console.print('[bold]Digite apenas números, com 5 digitos EX: (12345)[/]')
                continue
            codigo = int(codigo)
            if not len(str(codigo)) == 4: # == VERIFICAÇÃO DA QUANTIDADE DE DÍGITOS ==
                console.print('[bold]Digite apenas números, com 4 digitos EX: (1234)[/]')
            checagem_codigo = "SELECT * FROM cadastros WHERE codigo = %s"
            cursor.execute(checagem_codigo, (codigo,))
            resultado = cursor.fetchone()
            if not resultado:
                console.print('[bold]Seu código está incorreto, tente novamente[/]')
                continue
            senha = randint (1000, 10000) # == GERAÇÃO DE SENHA ALEATÓRIA PARA O USUÁRIO APÓS VALIDAÇÃO DE CÓDIGO ==
            atualizar = "UPDATE cadastros SET senha = %s WHERE codigo = %s" # == UPDATE NO BANCO DE DADOS ==
            cursor.execute(atualizar, (senha, codigo))
            conexao.commit()
            print(f'[bold]Agora sua nova senha é [green]{senha}[/]\nGuarde sua senha\nAgora você será direcionado ao login[/]')
            time.sleep(1)
            #self.fazer_login()
            inicio()
            break

    def ver_tickets(self):
        cursor = conexao.cursor()
        conexao.commit()
        ''' Impressão dos tickets de forma organizada e relacionada com o usuário, o ID do prato e o código gerado aleatoriamente '''
        console.print(Panel('[bold]:ticket: Bem-Vindo à aba de Tickets[/]'))
        time.sleep(1)
        with console.status('[green] === Estamos carregando seus tickets... ===\n'):
            time.sleep(3)
        cursor.execute('SELECT id FROM cadastros WHERE cpf = %s', (self.cpf,))
        id_usuario = cursor.fetchone()[0] # Recebimento do id do usuário
        cursor.execute('SELECT tickets.codigo, pratos.nome FROM tickets JOIN pratos ON tickets.id_prato = pratos.id WHERE tickets.id_usuario = %s', (id_usuario,))
        tickets = cursor.fetchall()
        if tickets:
            console.print('[green] === Seus Tickets Gerados === [/]')
            for codigo, nome_prato in tickets:
                console.print(f'[bold]Ticket: [green]{codigo}[/] | Prato:[/] [green]{nome_prato}[/]')
                
            while True:
                decisao = console.input('[bold]Digite 1 quando quiser retornar ao menu: [/]')
                if decisao == '1':
                    console.print('[bold]Estamos lhe redirecionando para o menu![/]')
                    time.sleep(1)
                    break
                else:
                    console.print('[red]Digite apenas "1"![/]')
                    continue

        else:
            console.print('[red]Você ainda não possui tickets registrados.[/]')
            return


def user(): # Add cursor as an argument
    user = True
    while user:
        console.print(Panel('[bold]Bem-vindo usuário, o que você deseja fazer?[/]'))
        console.print(Panel('[blue]1 - Cadastro[/]'))
        console.print(Panel('[green]2 - Login[/]'))
        escolha = console.input('[bold]Digite aqui: [/]')
        if escolha == '1':
            console.print('[bold]Você está sendo redirecionado para o cadastro![/]')
            time.sleep(1)
            Usuario.cadastrar() # Pass conexao and cursor
            break
        elif escolha == '2':
            console.print('[bold]Você está sendo redirecionado para o login![/]')
            time.sleep(1)
            Usuario.fazer_login(conexao, cursor) # Pass conexao and cursor
            break
        else:
            console.print('[red]Digite uma opção válida![/]')
            time.sleep(1)
            continue


def inicio():
    while True:
        console.print(Panel("[bold]Bem vindo à Fastake![/]"))
        console.print(Panel("[green]Se deseja ir para a parte de adiministradores: digite 1[/]"))
        console.print(Panel("[green]Se deseja ir para a parte de usuários: digite 2[/]"))
        escolha = console.input('[bold]Digite aqui: [/]')
        if escolha == '1':
            console.print('[green]Você está sendo redirecionado para a página de administrador![/]')
            time.sleep(1)
            Admin.adm() # Pass conexao and cursor
            break
        elif escolha == '2':
            console.print('[green]Você está sendo redirecionado para a página de usuário![/]')
            time.sleep(1)
            user() # Pass conexao and cursor
            break
        else:
            console.print('[bold]Digite uma opção válida![/]')
            time.sleep(1)
            continue

def menu():
    while True:
            menu = (
                '[bold]\n1 - :lock: Trocar senha[/]'
                '[bold]\n2 - :money_with_wings: Ver crédito[/]'
                '[bold]\n3 - :fork_and_knife: Ver restaurantes[/]'
                '[bold]\n4 - :ticket: Ver tickets[/]'
                '[bold]\n5 - :wastebasket: Deletar conta[/]'
                '[bold]\n6 - :door: Ir para página de login[/]'
                '[bold]\n7 - :door: Ir para o início do sistema[/]')
            mensagem = f'[bold]Escolha uma opção no menu abaixo.[/]\n{menu}'
            panel = Panel(
                mensagem,
                title="[bold green]Menu Interativo[/]",
                subtitle="Fastake 1.0",
                border_style="bright_blue"
            )
            console.print(panel)
            opcao_menu = console.input(str('[bold]Digite aqui uma opção válida: [/]'))
                # == TROCAR SENHA ==
            if opcao_menu == '1':
                Usuario.trocar_senha()

            # == VER CRÉDITO ==
            elif opcao_menu == '2': 
                Usuario.creditos_ver()
                
            # == VER RESTAURANTES ==

            elif opcao_menu == '3':
                from restaurantes import Restaurantes
                r = Restaurantes("placeholder", "placeholder")  # Instância qualquer para acessar o método
                r.ver_restaurantes()

                #Restaurantes.ver_restaurantes()
                #usuario_logado.ver_restaurantes(conexao, cursor)
                

            # == VER TICKET ==
            elif opcao_menu == '4': # EM DESENVOLVIMENTO
                Usuario.ver_tickets()
                time.sleep(1)
                #menu

            # == DELETAR CONTA ==

            elif opcao_menu == '5':
                Usuario.deletar_conta()
                
            elif opcao_menu == '6':
                time.sleep(1)
                break
            elif opcao_menu == '7':
                inicio()
                break
            else:
                console.print('[bold]Digite uma opção válida![/]')
                time.sleep(1)
                continue
