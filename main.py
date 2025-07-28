
import mysql.connector
import time
from usuario import Usuario
from restaurantes import Restaurantes
import sessao

from adm import Admin
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
while True:
        
    console.print(Panel('Bem-Vindo à Fastake, Para onde quer ser redirecionado?', style='bold'))
    console.print(Panel('1 - Ir para a aba de Administrador', style='green'))
    console.print(Panel('2 - Ir para a aba de Usuário', style='green'))
    escolha = console.input('[bold]Digite aqui: [/]')
    if escolha == '1':
        console.print('[bold]Você está sendo redirecionado para a página de administrador![/]')
        time.sleep(1)
        Admin.adm() # Pass conexao and cursor
        break
    elif escolha == '2':
        console.print('[bold]Você está sendo redirecionado para a página de usuário![/]')
        time.sleep(1)
        user = True
        while user:
            console.print(Panel('O que deseja fazer?', style='bold'))
            console.print(Panel('1 - Ir para o cadastro', style='blue'))
            console.print(Panel('2 - Ir para o login', style='green'))

            escolha = console.input('[bold]Digite aqui: [/]')
            if escolha == '1':
                console.print('[bold]Você está sendo redirecionado para o cadastro![/]')
                time.sleep(1)
                sessao.usuario_cadastrado = Usuario.cadastrar() # Pass conexao and cursor
                continue
            elif escolha == '2':
                console.print('[bold]Você está sendo redirecionado para o login![/]')
                time.sleep(1)
                sessao.usuario_logado = Usuario.fazer_login(conexao, cursor) # Pass conexao and cursor
                break
            else:
                console.print('[bold]Digite uma opção válida![/]')
                time.sleep(1)
                continue
        
    
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
                sessao.usuario_logado.trocar_senha()

            # == VER CRÉDITO ==
            elif opcao_menu == '2': 
                sessao.usuario_logado.creditos_ver()
                
            # == VER RESTAURANTES ==

            elif opcao_menu == '3':
                r = Restaurantes("placeholder", "placeholder")  # Instância qualquer para acessar o método
                r.ver_restaurantes()

                #Restaurantes.ver_restaurantes()
                #usuario_logado.ver_restaurantes(conexao, cursor)
                

            # == VER TICKET ==
            elif opcao_menu == '4': # EM DESENVOLVIMENTO
                sessao.usuario_logado.ver_tickets()
                time.sleep(1)
                #menu

            # == DELETAR CONTA ==

            elif opcao_menu == '5':
                sessao.usuario_logado.deletar_conta()
                
            elif opcao_menu == '6':
                time.sleep(1)
                break
            elif opcao_menu == '7':
                from usuario import inicio
                inicio()
                user = False
                break
            else:
                console.print('[bold]Digite uma opção válida![/]')
                time.sleep(1)
                continue
    else:
        console.print('[bold]Digite uma opção válida![/]')
        time.sleep(1)
        continue
