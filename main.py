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

def exibir_menu():
    menu_texto = """\n
=============== MENU ================
[d]\tDepositar
[s]\tSacar
[t]\tTransferir
[h]\tHistórico
[j]\tAplicar Juros
[ai]\tAtualizar Informações
[nc]\tNova conta
[ec]\tEncerrar conta
[lc]\tListar contas
[nu]\tNovo cliente
[q]\tSair
=> """
    return input(menu_texto)

def criar_cliente():
    cpf = input("CPF (somente números): ")
    nome = input("Nome completo: ")
    data_nascimento = input("Data de nascimento (dd-mm-aaaa): ")
    endereco = input("Endereço (logradouro, nro - bairro - cidade/sigla estado): ")
    return Cliente(nome, data_nascimento, cpf, endereco)

def criar_conta(clientes):
    cpf = input("CPF do cliente: ")
    cliente = next((c for c in clientes if c.cpf == cpf), None)
    if cliente:
        print("\n=== Conta criada com sucesso! ===")
        return ContaBancaria("0001", len(clientes) + 1, cliente)
    print("\n@@@ Cliente não encontrado! @@@")
    return None

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

def main():
    clientes = []
    contas = []

    while True:
        opcao = exibir_menu()

        if opcao == "d":
            try:
                valor = float(input("Valor do depósito: "))
                contas[-1].depositar(valor)
            except ValueError:
                print("\n@@@ Falha! Valor inválido. Informe um número válido. @@@")
                continue

        elif opcao == "s":
            try:
                valor = float(input("Valor do saque: "))
                contas[-1].sacar(valor)
            except ValueError:
                print("\n@@@ Falha! Valor inválido. Informe um número válido. @@@")
                continue

        elif opcao == "t":
            try:
                conta_destino = int(input("Digite o número da conta de destino: "))
                valor_transferencia = float(input("Digite o valor da transferência: "))
                conta_destino -= 1  # Ajuste para índice de lista
                if 0 <= conta_destino < len(contas):
                    contas[-1].transferir(contas[conta_destino], valor_transferencia)
                else:
                    print("\n@@@ Conta de destino inválida! @@@")
            except ValueError:
                print("\n@@@ Falha! Valor inválido. Informe um número válido. @@@")
                continue

        elif opcao == "h":
            contas[-1].ver_historico()

        elif opcao == "j":
            taxa_juros = float(input("Digite a taxa de juros a ser aplicada (%): "))
            contas[-1].calcular_juros(taxa_juros)

        elif opcao == "ai":
            clientes[-1].atualizar_informacoes()

        elif opcao == "nc":
            conta = criar_conta(clientes)
            if conta:
                contas.append(conta)

        elif opcao == "ec":
            contas.pop()
            print("\n=== Conta encerrada com sucesso! ===")

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "nu":
            clientes.append(criar_cliente())

        elif opcao == "q":
            break

        elif opcao == "ee":
            if contas:
                exportar_extrato(contas[-1])
            else:
                print("\n@@@ Nenhuma conta disponível para exportar extrato! @@@")
        
        else:
            print("Opção inválida. Selecione novamente.")

    main()