import textwrap

# De acordo com o PEP 8, constantes são nomeadas em maiúsculo
AGENCIA = '0001'
LIMITE_SAQUES = 3
LIMITE_VALOR_SAQUE = 500

def menu():
    """Exibe o menu de opções e retorna a escolha do usuário."""
    menu_texto = """\n
    ============== MENU ==============
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nu]\tNovo usuário
    [nc]\tNova conta
    [lc]\tListar contas
    [q]\tSair
    => """
    return  input(textwrap.dedent(menu_texto))

# Funções Bancárias

def depositar(saldo, valor, extrato, /):
    """
    Esta função realiza um depósito na conta.
    Todos os argumentos são do tipo positional only

    Argumentos:
        saldo (float): Saldo atual da conta
        valor (float): Valor a ser depositado
        extrato (str): Histórico de transações

    Retorna:
        tupla: (Novo saldo, Novo extrato
    """

    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print("\n Depósito realizado com sucesso!")
    else:
        print("\n OPERAÇÃO FALHOU! O valor informado é inválido.")

    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    """
    Esta função realiza um saque na conta.
    Todos os argumentos são do tipo keyword only.

    Argumentos:
        saldo (float): Saldo atual
        valor (float): Valor do saque
        extrato (str): Histórico de transações
        limite (float): Limite máximo por saque (R$ 500)
        numero_saques (int): Limite total de saques por dia (3).

    Retorna:
        tupla: (Novo saldo, Novo extrato, Novo número de saques)
    """
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\n OPERAÇÃO FALHOU! Saldo insuficiente.")
    elif excedeu_limite:
        print(f"\n OPERAÇÃO FALHOU! O valor do saque excedeu o limite de R${limite:.2f}.")
    elif excedeu_saques:
        print(f"\n OPERAÇÃO FALHOU! O número máximo de {limite_saques} saques foi excedido.")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:\t\tR$ {valor:.2f}\n"
        numero_saques += 1
        print("\n Saque realizado com sucesso!")
    else:
        print("\n OPERAÇÃO FALHOU! O valor informado é inválido.")
    return saldo, extrato, numero_saques

def exibir_extrato(saldo, /, *, extrato):
    """
    Esta função exibe o extrato da conta.
    Os argumentos são positional ou keyword only.

    Argumentos:
        saldo (float): Saldo atual (Positional only)
        extrato (str): Histórico de transações (Keyword only)
    """

    print("\n============== EXTRATO ==============")
    print(f"\nSaldo>\t\tR$ {saldo:.2f}")
    print("=====================================")

# Funções de cadastro

def filtrar_usuario(cpf, usuarios):
    #Busca um usuário na lista pelo CPF
    cpf = ''.join(filter(str.isdigit, cpf)) # Garante que só há números
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_usuario(usuarios):
    """
    Esta função cadastra um novo usuário (cliente)

    Argumentos: 
        usuarios (list): Lista de dicionários de usuários cadastrados
    """

    cpf = input("Informe o CPF (somente números): ")
    cpf = ''.join(filter(str.isdigit, cpf))

    if filtrar_usuario(cpf, usuarios):
        print("\n Já existe um usuário com este CPF!")
        return
    
    nome = input("Informe o seu nome completo: ")
    data_nascimento =  input("Informe a sua data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (Logradouro, nº, Bairro, Cidade/UF): ")

    usuarios.append({
        "nome": nome,
        "data_nascimento": data_nascimento,
        "cpf": cpf,
        "endereco": endereco
    })

    print("\n Usuário cadastrado com sucesso!")

def criar_conta(agencia, numero_conta, usuarios):
    """
    Esta função cria uma nova conta corrente vinculada a um usuário existente.

    Argumentos:
        agencia (str): Número fixo da agência (0001)
        numero_conta (int): Próximo número sequencial da conta
        usuarios (list): Lista de usuários cadastrados
    
    Retorna:
        Um dicionário ou None: A nova conta criada ou None se o usuário não for encontrado.
    """

    cpf = input("Informe o CPF do usuário: ")
    cpf = ''.join(filter(str.isdigit, cpf))
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("Conta criada com sucesso!")
        return {
            "agencia": agencia,
            "numero_conta": numero_conta,
            "usuario": usuario
        }
    
    print("Usuário não encontrado, criação de conta cancelada!")
    return None

def listar_contas(contas):
    # Exibe a lista de contas correntes cadastradas.

    if not contas:
        print("\n Nenhuma conta cadastrada.")
        return
    print("\n============== LISTA DE CONTAS ==============")
    for conta in contas:
        linha = f"""\
                Agência:\t{conta['agencia']}
                C/C:\t\t{conta['numero_conta']}
                Titular:\t{conta['usuario']['nome']}
                """
        print("-" * 40)
        print(textwrap.dedent(linha))
    print("=============================================")

# Função principal
def main():
    # Função principal para execução do sistema bancário
    saldo = 0
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []
    numero_conta = 1
    
    while True:
        opcao = menu()

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))
            #Chamada do tipo Positional Only
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))
            #Chamada do tipo Keyword Only
            saldo, extrato, numero_saques = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=LIMITE_VALOR_SAQUE,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == "e":
            #Chamada do tipo Positional e Keyword Only
            exibir_extrato(saldo, extrato=extrato)
        
        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            conta = criar_conta(AGENCIA, numero_conta, usuarios)
            if conta:
                contas.append(conta)
                numero_conta += 1 # Incrementa o identificador do número da conta

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            print("\n Tchau. Até breve!")
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

if __name__ == "__main__":
    main()