import re
import textwrap
import csv

class ContaBancaria:
    def __init__(self, agencia, numero_conta, cliente):
        self.agencia = agencia
        self.numero_conta = numero_conta
        self.cliente = cliente
        self.saldo = 0
        self.limite = 500
        self.historico = ""
        self.num_saques = 0
        self.LIM_SAQUES = 3

    def depositar(self, valor):
        if valor <= 0:
            print("\n@@@ Falha! Valor inválido. @@@")
            return
        self.saldo += valor
        self.historico += f"Depósito: R$ {valor:.2f}\n"
        print("\n=== Depósito realizado! ===")

    def sacar(self, valor):
        if valor <= 0:
            print("\n@@@ Falha! Valor inválido. @@@")
            return
        saldo_insuf = valor > self.saldo
        limite_excedido = valor > self.limite
        saques_excedidos = self.num_saques >= self.LIM_SAQUES

        if saldo_insuf:
            print("\n@@@ Falha! Saldo insuficiente. @@@")
        elif limite_excedido:
            print("\n@@@ Falha! Limite de saque excedido. @@@")
        elif saques_excedidos:
            print("\n@@@ Falha! Número máximo de saques atingido. @@@")
        else:
            self.saldo -= valor
            self.historico += f"Saque: R$ {valor:.2f}\n"
            self.num_saques += 1
            print("\n=== Saque realizado! ===")

    def transferir(self, outra_conta, valor):
        if valor <= 0:
            print("\n@@@ Falha! Valor inválido. @@@")
            return
        if valor > self.saldo:
            print("\n@@@ Falha! Saldo insuficiente. @@@")
            return

        self.saldo -= valor
        outra_conta.depositar(valor)
        self.historico += f"Transferência enviada para {outra_conta.cliente.nome}: R$ {valor:.2f}\n"
        outra_conta.historico += f"Transferência recebida de {self.cliente.nome}: R$ {valor:.2f}\n"

    def ver_historico(self):
        print("\n=========== HISTÓRICO ===========")
        print("Nenhuma transação realizada." if not self.historico else self.historico)
        print(f"\nSaldo: R$ {self.saldo:.2f}")
        print("=================================")

    def calcular_juros(self, taxa):
        juros = self.saldo * (taxa / 100)
        self.saldo += juros
        self.historico += f"Juros aplicados: R$ {juros:.2f}\n"
        print("\n=== Juros aplicados! ===")

class Cliente:
    def __init__(self, nome, data_nascimento, cpf, endereco):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        self.endereco = endereco

    def atualizar_informacoes(self):
        print("\n=== Atualização de informações pessoais ===")
        print("Opções de atualização:")
        print("1. Endereço")
        opcao = input("Escolha a opção desejada: ")

        if opcao == "1":
            novo_endereco = input("Novo endereço: ")
            self.endereco = novo_endereco
            print("\n=== Informações atualizadas! ===")

def exibir_menu_inicial():
    menu_texto = """\n
=============== MENU INICIAL ================
[nc]\tNovo Cliente
[nco]\tNova Conta
[l]\tLogin
[q]\tSair
=> """
    return input(menu_texto)

def exibir_menu_principal():
    menu_texto = """\n
=============== MENU PRINCIPAL ================
[s]\tSacar
[t]\tTransferir
[h]\tHistórico
[j]\tAplicar Juros
[ai]\tAtualizar Informações
[ec]\tEncerrar conta
[lc]\tListar contas
[mi]\tVoltar para o Menu Inicial
[q]\tSair
=> """
    return input(menu_texto)

def criar_cliente():
    cpf_pattern = re.compile(r'^\d{11}$')
    data_nascimento_pattern = re.compile(r'^\d{2}[-/]\d{2}[-/]\d{4}$')
    nome_pattern = re.compile(r'^[a-zA-Z\s]+$')
    endereco_pattern = re.compile(r'^[a-zA-Z0-9\s,.-]+$')

    while True:
        cpf = input("CPF (somente números): ")
        if not cpf_pattern.match(cpf):
            print("CPF inválido. Deve conter 11 dígitos.")
            continue
        nome = input("Nome completo: ")
        if not nome_pattern.match(nome):
            print("Nome inválido. Deve conter apenas letras e espaços.")
            continue
        data_nascimento = input("Data de nascimento (dd-mm-aaaa): ")
        if not data_nascimento_pattern.match(data_nascimento):
            print("Data de nascimento inválida. Deve estar no formato dd-mm-aaaa ou dd/mm/aaaa.")
            continue
        endereco = input("Endereço (logradouro, nro - bairro - cidade/sigla estado): ")
        if not endereco_pattern.match(endereco):
            print("Endereço inválido. Deve conter apenas letras, números e os caracteres ,.-.")
            continue
        return Cliente(nome, data_nascimento, cpf, endereco)

def criar_conta(clientes):
    cpf_pattern = re.compile(r'^\d{11}$')
    while True:
        cpf = input("CPF do cliente: ")
        if not cpf_pattern.match(cpf):
            print("CPF inválido. Deve conter 11 dígitos.")
            continue
        cliente = next((c for c in clientes if c.cpf == cpf), None)
        if cliente:
            print("\n=== Conta criada com sucesso! ===")
            return ContaBancaria("0001", len(clientes) + 1, cliente)
        print("\n@@@ Cliente não encontrado! @@@")
        print("Por favor, crie um cliente antes de criar uma conta.")

def listar_contas(contas):
    if not contas:
        print("\n@@@ Nenhuma conta disponível. @@@")
        return

    for conta in contas:
        print("=" * 35)
        print(f"Agência:\t{conta.agencia}")
        print(f"C/C:\t\t{conta.numero_conta}")
        print(f"Titular:\t{conta.cliente.nome}")

def exportar_extrato(conta):
    nome_arquivo = f"extrato_conta_{conta.numero_conta}.csv"
    with open(nome_arquivo, mode='w', newline='') as arquivo:
        writer = csv.writer(arquivo)
        writer.writerow(['Transação', 'Valor'])
        for transacao in conta.historico.split('\n'):
            if transacao:
                tipo, valor = transacao.split(':')
                writer.writerow([tipo.strip(), float(valor.strip()[3:])])
    print(f"\n=== Extrato exportado para '{nome_arquivo}'! ===")

def login_cliente(clientes, contas):
    cpf_pattern = re.compile(r'^\d{11}$')
    while True:
        cpf = input("CPF (somente números): ")
        if not cpf_pattern.match(cpf):
            print("CPF inválido. Deve conter 11 dígitos.")
            continue
        cliente = next((c for c in clientes if c.cpf == cpf), None)
        if cliente:
            conta_cliente = next((conta for conta in contas if conta.cliente == cliente), None)
            if conta_cliente:
                print("\n=== Login bem-sucedido! ===")
                return cliente, conta_cliente
            else:
                print("\n@@@ Cliente sem conta associada! @@@")
                print("Por favor, crie uma conta para este cliente antes de fazer login.")
        else:
            print("\n@@@ Cliente não encontrado! @@@")
            print("Por favor, crie um cliente antes de fazer login.")

def main():
    clientes = []
    contas = []
    cliente_logado = None

    while True:
        opcao_inicial = exibir_menu_inicial()

        if opcao_inicial == "nc":
            novo_cliente = criar_cliente()
            clientes.append(novo_cliente)
            print("\n=== Cliente criado com sucesso! ===")
        elif opcao_inicial == "nco":
            if not clientes:
                print("Por favor, crie um cliente antes de criar uma conta.")
                continue
            nova_conta = criar_conta(clientes)
            if nova_conta:
                contas.append(nova_conta)
        elif opcao_inicial == "l":
            if not clientes or not contas:
                print("Por favor, crie um cliente e uma conta antes de fazer login.")
                continue
            cliente_logado, conta_logada = login_cliente(clientes, contas)
            if cliente_logado and conta_logada:
                while True:
                    opcao_principal = exibir_menu_principal()
                    if opcao_principal == "s":
                        pass
                    elif opcao_principal == "t":
                        pass
                    elif opcao_principal == "h":
                        pass
                    elif opcao_principal == "j":
                        pass
                    elif opcao_principal == "ai":
                        pass
                    elif opcao_principal == "ec":
                        pass
                    elif opcao_principal == "lc":
                        pass
                    elif opcao_principal == "mi":
                        cliente_logado = None
                        break
                    elif opcao_principal == "q":
                        return
                    else:
                        print("Opção inválida. Selecione novamente.")
        elif opcao_inicial == "q":
            return
        else:
            print("Opção inválida. Selecione novamente.")

main()
