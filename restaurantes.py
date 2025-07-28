
import mysql.connector
import time
from usuario import Usuario
from usuario import Checagem
from random import randint
from unidecode import unidecode
import sessao
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
check = Checagem()

class Restaurantes:

    ''' Classe que se associa aos restaurantes e as ações disponíveis dentro desse contexto, bem como a armazenagem de dados importantes no processo
    de compra do usuário ( como o nome do prato escolhido ) '''


    def __init__(self, nome_prato, prato_escolhido):
        self.nome_prato = nome_prato
        self.prato_escolhido = prato_escolhido
        self.cpf = sessao.usuario_logado.cpf # QUANDO QUISER USAR O CPF EM OUTRA CLASSE, SÓ FAZER ISSO !!!

    def ver_restaurantes(self):

        ''' Método para ver a lista de restaurantes disponíveis no sistema'''

        # === VER LISTA DE RESTAURANTES ===
        console.print(Panel('[bold]:fork_and_knife: Estamos lhe redirecionando para a página de restaurantes participantes![/]'))
        time.sleep(1)
        opcoes = 'SELECT id, restaurante FROM restaurantes' # == LEITURA ( READ ) DOS RESTAURANTES CADASTRADOS NO BANCO DE DADOS ==
        cursor.execute(opcoes)
        resultado = cursor.fetchall()
        rest = True
        while rest:
            console.print('[bold]----Restaurantes disponiveis----[/]')
            for i, lista_restaurantes in enumerate(resultado, start=1):
                num_restaurante = lista_restaurantes[0]
                nome_restaurante = lista_restaurantes[1]
                console.print(f'[bold]Restaurante : {nome_restaurante} - {num_restaurante}[/]') # == IMPRESSÃO DOS RESTAURANTES PARTICIPANTES ==
            option = True
            while option:
                escolha = console.input('[green]Escolha entre as opções disponíveis (o número ao lado do restaurante): [/]')
                
                if not escolha.isdigit():
                    console.print('[bold]Digite apenas números[/]')
                    continue
                escolha = int(escolha)
                if not 1 <= escolha <= len(resultado): 
                    console.print(f'[bold]A opção escolhida não é válida, escolha uma opção entre 1 e {len(lista_restaurantes)}[/]')
                    continue
                cursor.execute(f"SELECT restaurante FROM restaurantes WHERE id = {escolha}")
                nome = cursor.fetchone()
                console.print(Panel(f"[bold] == Bem vindo(a) ao restaurante {nome[0]} == [/]"))
                
                dec = True
                while dec:
                    decisao = console.input(f'[bold]Você escolheu o restaurante {nome[0]}, digite [green]SIM[/] caso deseje continuar para realizar o pedido\nDigite [red]NÃO[/] caso deseje retornar ao menu: [/]')
                    if not decisao.isalpha():
                        console.print('[bold]Digite apenas [green]SIM[/] ou [red]NÃO[/][/]')
                        continue
                    elif unidecode(decisao.lower()) == 'nao':
                        console.print('[bold]Você será redirecionado para o menu![/]')
                        time.sleep(1) # FUNCIONANDO !!!
                        dec = False
                        option = False
                        rest = False
                    elif decisao.lower() == 'sim':
                        Restaurantes.ver_pratos_disponíveis(escolha)
                        dec = False
                        option = False
                        rest = False

    @classmethod
    def ver_pratos_disponíveis(cls, escolha):

        ''' A partir da escolha realizada dos restaurantes participantes, o usuário poderá analisar o cardápio do restaurante escolhido e ser
        redirecionado para a finalização da compra '''

        cursor.execute(f"SELECT nome, valor FROM pratos WHERE id_restaurante = {escolha}")
        pratos = cursor.fetchall()
        for i, (nome, valor) in enumerate(pratos, start=1):
            console.print(f"[bold]{nome}, [green]R${valor:.2f}[/] - {i}[/]")
        prato = True
        while prato:
            selecao_prato = console.input('[bold]Escolha entre as opções disponíveis (o número ao lado do prato): [/]')
            if not selecao_prato.isdigit():
                console.print('[red]Digite apenas números[/]')
                continue
            selecao_prato = int(selecao_prato)#-1
            if not 1 <= selecao_prato <= len(pratos):
                console.print(f'[red]A opção escolhida não é válida, escolha uma opção entre 1 e {len(pratos)}[/]')
                continue
            nome_prato = pratos[selecao_prato-1][0]
            cursor.execute(f"SELECT id FROM pratos WHERE nome = %s", (nome_prato,))
            prato_escolhido = cursor.fetchone()
            instancia = cls(nome_prato, prato_escolhido)
             # === Instanciar os self.nome_prato e self.prato_escolhido para serem usados posteriormente ===
            while True:
                decisao = console.input(f"[bold]Você escolheu o prato [green]{nome_prato}[/]\nDigite [green]SIM[/] caso deseje realizar o pedido\nDigite [red]NÃO[/] caso deseje cancelar o pedido e voltar ao menu\n: [/]")
                if not decisao.isalpha():
                    console.print("[bold]Digite apenas SIM ou NÃO[/]")
                    continue
                if unidecode(decisao.lower()) == "nao":
                    console.print("[bold]Você será redirecionado ao menu[/]")
                    time.sleep(1) 
                    prato = False
                    return None
                    break
                if decisao.lower() == "sim":
                    instancia.finalizar_compra()
                    prato = False
                    return instancia
                    break # === Método para finalizar compra ===
                else:
                    return
            
    def finalizar_compra(self):

        ''' Finalização da compra a partir da escolha de produto realizada pelo usuário, havendo um gasto de créditos de acordo com o preço do
        produto '''

        final = True
        while final:
            cursor.execute(f"SELECT valor FROM pratos WHERE id = %s", (self.prato_escolhido)) # == LEITURA DO VALOR ==
            valor_prato = cursor.fetchone()
            time.sleep(1)
            console.print(Panel('[green] == Finalizando sua compra ==[/]'))
            time.sleep(1)
            console.print(f'[bold]O valor do seu pedido é de: [green]R${valor_prato[0]:.2f}[/][/]') 
            
            if Checagem.checar_senha_compra(conexao, self.cpf): 

                cursor.execute(f'SELECT credito FROM cadastros WHERE cpf = %s', (self.cpf, ))
                resultado = cursor.fetchone()
                if float(resultado[0]) >= float(valor_prato[0]): # == VERIFICAR SE O USUÁRIO POSSUI CRÉDITOS SUFICIENTES ATRAVÉS DE UMA CONSULTA AO BANCO DE DADOS ==
                    with console.status('[bold]Estamos processando sua compra...[/]'):
                        time.sleep(3)
                    credito_desconto = float(resultado[0]) -  float(valor_prato[0])
                    cursor.execute(f'UPDATE cadastros SET credito = %s WHERE cpf = %s', (credito_desconto, self.cpf)) # == UPDATE DOS CRÉDITOS SUBTRAIDOS PELO VALOR DO PRATO ==
                    conexao.commit()
                    console.print(Panel('[green]Compra realizada com sucesso e Ticket gerado\nEstamos lhe redirecionando para o menu..[/]'))
                    self.gerar_ticket(self.prato_escolhido, self.cpf, conexao)
                    final = False 
                else:
                    add_credito = True
                    while add_credito: # == PERGUNTAR AO USUÁRIO SE ELE QUER ADICIONAR CRÉDITOS OU RETORNAR AO MENU ==
                        decisao_credito = console.input('[red]Você não tem créditos para realizar essa compra!\nDigite [bold]1[/] para adicionar créditos ou [bold]2[/] para retornar ao menu: [/]')
                        if decisao_credito == '1':
                            add_credito = False
                            Usuario.creditos_ver(self)
                            return
                        
                        elif decisao_credito == '2':
                            console.print('[bold]Você está sendo redirecionado para o menu...[/]')
                            time.sleep(1)
                            add_credito = False
                            final = False 
                        else:
                            console.print('[red]Tente uma opção válida![/]')
                            continue
    
            else:
                console.print('[red]Senha não válida, tente novamente[/]')
                continue

    def gerar_ticket(self, prato_escolhido, cpf, conexao):

        ''' Gerador de ticket de acordo com o prato escolhido, o id do usuário ( lido através do seu CPF ) e de um código gerado aleatoriamente '''
        cursor = conexao.cursor()
        cursor.execute(f'SELECT id FROM cadastros WHERE cpf = %s', (cpf,))
        id_usuario = cursor.fetchone()[0]
        id_prato = prato_escolhido[0]
        codigo_ticket = randint(10000, 99999)
        cursor.execute(f'INSERT INTO tickets (id_usuario, id_prato, codigo) VALUES (%s, %s, %s)', (id_usuario, id_prato, codigo_ticket))
        conexao.commit()
        cursor.close()
        
        cursor = conexao.cursor()
        time.sleep(1)
        return



