class ContaBancaria:
    
    def __init__(self, agencia, numero_conta, cliente):
        self.agencia = agencia
        self.numero_conta = numero_conta
        self.cliente = cliente
        self.saldo = 0
        self.historico = ""
        self.num_saques = 0

    def depositar(self, valor):
        if valor <= 0:
            print("\nFalha! Valor inválido.")
            return
        self.saldo += valor
        self.historico += f"Depósito: R$ {valor:.2f}\n"
        print("\n=== Depósito realizado! ===")

    def sacar(self, valor):
        if valor <= 0:
            print("\nFalha! Valor inválido.")
            return
        saldo_insuficiente = valor > self.saldo

        if saldo_insuficiente:
            print("\nFalha! Saldo insuficiente.")
        else:
            self.saldo -= valor
            self.historico += f"Saque: R$ {valor:.2f}\n"
            self.num_saques += 1
            print("\n=== Saque realizado! ===")

    def ver_historico(self):
        print("\n=========== HISTÓRICO ===========")
        print("Nenhuma transação realizada." if not self.historico else self.historico)
        print(f"\nSaldo: R$ {self.saldo:.2f}")
        print("=================================")

    def calcular_juros(self):
        taxa_anual = float(input("Informe a taxa de juros anual (%): "))
        anos = int(input("Informe o número de anos para simulação: "))
        taxa_mensal = taxa_anual / 12 / 100
        saldo_final = self.saldo * ((1 + taxa_mensal) ** (anos * 12))
        print(f"\nSimulação de juros após {anos} anos:")
        print(f"Saldo inicial: R$ {self.saldo:.2f}")
        print(f"Saldo após {anos} anos: R$ {saldo_final:.2f}")
        return saldo_final

    def listar_informacoes_conta(self):
        print("\n=========== INFORMAÇÕES DA CONTA ===========")
        print(f"Número da Conta: {self.numero_conta:05d}")
        print(f"CPF: {self.cliente.cpf}")
        print(f"Nome do Titular: {self.cliente.nome}")
        print(f"Data de Nascimento: {self.cliente.data_nascimento}")
        print(f"Endereço: {self.cliente.endereco}")
        print("=============================================")

    def encerrar_conta(self, contas):
        contas.remove(self)
        print("\n=== Conta encerrada com sucesso! ===")


class Cliente:
    
    def __init__(self, nome, data_nascimento, cpf, endereco):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        self.endereco = endereco

    def atualizar_informacoes(self, contas):
        print("\n=== Atualização de informações pessoais ===")
        print("Opções de atualização:")
        print("1. Endereço")
        opcao = input("Escolha a opção desejada: ")

        if opcao == "1":
            novo_endereco = input("Novo endereço: ")
            self.endereco = novo_endereco
            print("\n=== Informações atualizadas! ===")
            
            for conta in contas:
                if conta.cliente == self:
                    conta.cliente.endereco = novo_endereco


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
[d]\tDepositar
[h]\tHistórico
[j]\tAplicar Juros
[ai]\tAtualizar Informações
[ec]\tEncerrar conta
[li]\tListar informações da conta
[mi]\tVoltar para o Menu Inicial
[q]\tSair
=> """
    return input(menu_texto)


def depositar_valor(conta):
    while True:
        valor_deposito_str = input("Informe o valor a depositar: ")
        if not valor_deposito_str.replace('.', '', 1).isdigit():
            print("Valor inválido. Por favor, insira um número válido.")
            continue
        valor_deposito = float(valor_deposito_str)
        conta.depositar(valor_deposito)
        break


def criar_cliente():
    while True:
        cpf = input("CPF (somente números): ")
        if not cpf.isdigit() or len(cpf) != 11:
            print("CPF inválido. Deve conter 11 dígitos numéricos.")
            continue
        nome = input("Nome completo: ")
        if not nome.replace(' ', '').isalpha():
            print("Nome inválido. Deve conter apenas letras e espaços.")
            continue
        data_nascimento = input("Data de nascimento (dd-mm-aaaa): ")
        if len(data_nascimento) != 10 or data_nascimento[2] != '-' or data_nascimento[5] != '-':
            print("Data de nascimento inválida. Deve estar no formato dd-mm-aaaa.")
            continue
        endereco = input("Endereço (logradouro, nro - bairro - cidade/sigla estado): ")
        return Cliente(nome, data_nascimento, cpf, endereco)


def criar_conta(clientes):
    while True:
        cpf = input("CPF do cliente: ")
        if not cpf.isdigit() or len(cpf) != 11:
            print("CPF inválido. Deve conter 11 dígitos numéricos.")
            continue
        cliente = next((c for c in clientes if c.cpf == cpf), None)
        if cliente:
            print("\n=== Conta criada com sucesso! ===")
            return ContaBancaria("0001", len(clientes) + 1, cliente)
        print("\nCliente não encontrado!")
        print("Por favor, crie um cliente antes de criar uma conta.")


def login_cliente(clientes, contas):
    while True:
        cpf = input("CPF (somente números): ")
        if not cpf.isdigit() or len(cpf) != 11:
            print("CPF inválido. Deve conter 11 dígitos numéricos.")
            continue
        cliente = next((c for c in clientes if c.cpf == cpf), None)
        if cliente:
            conta_cliente = next((conta for conta in contas if conta.cliente == cliente), None)
            if conta_cliente:
                print("\n=== Login bem-sucedido! ===")
                return cliente, conta_cliente
            else:
                print("\nCliente sem conta associada!")
                print("Por favor, crie uma conta para este cliente antes de fazer login.")
        else:
            print("\nCliente não encontrado!")
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
                        valor_saque = float(input("Informe o valor a sacar: "))
                        conta_logada.sacar(valor_saque)
                    elif opcao_principal == "d":
                        depositar_valor(conta_logada)
                    elif opcao_principal == "h":
                        conta_logada.ver_historico()
                    elif opcao_principal == "j":
                        conta_logada.calcular_juros()
                    elif opcao_principal == "ai":
                        conta_logada.cliente.atualizar_informacoes(contas)
                    elif opcao_principal == "ec":
                        conta_logada.encerrar_conta(contas)
                        break
                    elif opcao_principal == "li":
                        conta_logada.listar_informacoes_conta()
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
