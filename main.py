from datetime import datetime
import cadastro

saldo = 0
limite_valor_saque = 500


def selecionar_conta():
    global dados_conta
    dados_conta = []
    arquivo = open('./contas/contas.txt', 'r')
    selecionar_conta = input('Selecione a conta: ')
    for linha in arquivo:
        str_conta = linha.split('|')
        if selecionar_conta == str_conta[0]:
            cod_conta = selecionar_conta
            dados_conta = str_conta.copy()
            return cod_conta
    print('Numero de conta não encontrado!')


def verifica_limite_saques():
    global saldo, saques_diarios
    cont_saques = 0
    saques_diarios = 3
    data_operacao = datetime.now()
    str_data_operacao = data_operacao.strftime('%d-%m-%Y')
    consulta_extrato = open(f'./historico_contas/conta_cod{cod_conta_historico}.txt', 'r')
    arquivo = consulta_extrato.readlines()
    for linha in arquivo:
        if str_data_operacao in linha and 'Saque' in linha:
            cont_saques += 1
    print(f'{saques_diarios - cont_saques} saque(s) restante(s).')
    if saques_diarios > cont_saques:
        return True
    print('Limite de saques diarios atingidos!')
    return False


def verifica_saldo():
    global saldo, saques_diarios
    soma_depositos = 0
    soma_saques = 0
    consulta_extrato = open(f'./historico_contas/conta_cod{cod_conta_historico}.txt', 'r')
    arquivo = consulta_extrato.readlines()
    for linha in arquivo:
        valor_operacao = float(linha.split()[2])
        if 'Saque' in linha:
            soma_saques += valor_operacao
        elif 'Deposito' in linha:
            soma_depositos += valor_operacao
    saldo = soma_depositos - soma_saques
    return saldo


def deposito(valor):
    global saldo
    if valor > 0:
        confirma_operacao = input(f'Você deseja depositar {valor:.2f}?')
        if confirma_operacao == 'N':
            print('Operação de deposito cancelada!')
            return None
        saldo += valor
        data_operacao = datetime.now()
        str_data_operacao = data_operacao.strftime('%d-%m-%Y, %H:%M:%S')
        registra_operacao = open(f'./historico_contas/conta_cod{cod_conta_historico}.txt', 'a+')
        registra_operacao.write(f'Deposito:   R$ {valor:.2f} | Realizado em: {str_data_operacao}\n')
        print(f'Seu saldo agora é de {saldo:.2f}')
        registra_operacao.close()


def saque(valor):
    global saldo, saques_diarios
    limite_saques = verifica_limite_saques()
    if limite_saques is False:
        print(f'Não foi possivel realizar a operação de saque. Limite diario de {saques_diarios} saques atingido!')
    if saldo - valor >= 0 and limite_saques is True:
        confirma_operacao = input(f'Você deseja retirar {valor:.2f}? [S/N]').upper()
        if confirma_operacao == 'N':
            print('Operação de saque cancelada!')
            return None
        saldo -= valor
        saques_diarios -= 1
        data_operacao = datetime.now()
        str_data_operacao = data_operacao.strftime('%d-%m-%Y, %H:%M:%S')
        registra_operacao = open(f'./historico_contas/conta_cod{cod_conta_historico}.txt', 'a+')
        registra_operacao.write(f'Saque:   R$ {valor:.2f} | Realizado em: {str_data_operacao}\n')
        print('Operação de deposito realizada com sucesso!')
        print(f'Seu saldo agora é de R$ {saldo:.2f}')
        registra_operacao.close()


def extrato():
    consulta_extrato = open(f'./historico_contas/conta_cod{cod_conta_historico}.txt', 'r')
    arquivo = consulta_extrato.readlines()
    print(f'\n{"Consulta de Extrato Bancario":^20}')
    print(f'''Dados do conta:
Numero da Conta: {dados_conta[0]}
Agencia: {dados_conta[1]}
CPF: {dados_conta[2]}
Nome do titular: {dados_conta[3]}''')
    print(f'{"Historico de Operações":^30}\n')
    if arquivo == '':
        print('Não foram realizadas movimentações')
    for linha in arquivo:
        linha = linha.split('|')
        print(f'|{linha[0]}|{linha[1]}|')

    consulta_extrato.close()


while True:
    menu_principal = '''
Menu principal

[1] - Saques, Depositos e Extratos
[2] - Cadastros e Criar Conta 
[0] - Sair'''

    print(menu_principal)
    opcao1 = input(f'Selecione uma opcao: ')

    if opcao1 not in ['0', '1', '2']:
        print(f'A opcao {opcao1} é invalida!')
    if opcao1 == '0':
        print('Obrigado até a proxima!')
        break

    if opcao1 == '1':
        print(f'\n{"Operações Bancarias":^20}')
        cod_conta_historico = selecionar_conta()
        saldo = verifica_saldo()
        print(f'\n{"Operacoes Bancarias":^20}')

        print('''
[0] - Sair
[1] - Voltar
[2] - Depositar
[3] - Sacar
[4] - Extrato''')

    elif opcao1 == '2':
        print(f'\n{"Contas e Cadastros":^20}')
        print('''
[0] - Sair
[1] - Voltar
[2] - Cadastro Cliente
[3] - Criar Conta Corrente
[4] - Listar Contas
[5] - Listar Cadastros''')

    opcao2 = input(f'Selecione uma opcao: ')
    if opcao2 not in ['0', '1', '2', '3', '4']:
        print(f'A opcao {opcao2} é invalida!')
    if opcao2 == '0':
        print('Obrigado até a proxima!')
        break
    elif opcao2 == '1':
        print('\nVoltando ao menu anterior,,,')
        saldo = 0
    
    # opcao contas
    if str(f'{opcao1}{opcao2}') == '14':
        print('Consulta de extrato')
        extrato()
    elif str(f'{opcao1}{opcao2}') == '12' or str(f'{opcao1}{opcao2}') == '13':
        quantia = float(input('Informe o valor: '))
        if str(f'{opcao1}{opcao2}') == '12':
            deposito(quantia)
        elif str(f'{opcao1}{opcao2}') == '13':
            if quantia > limite_valor_saque:
                print(f'O limite de Saque é de R$ {limite_valor_saque:.2f}')
            if quantia - saldo > 0:
                print(f'Saldo Insuficiente! O seu saldo atual é de R$ {saldo:.2f}')
            else:
                saque(quantia)
    elif str(f'{opcao1}{opcao2}') == '15':
        print('\nOpção invalida!')
        


    # opcao cadastros e criar conta
    elif str(f'{opcao1}{opcao2}') == '22':
        print('\nCadatro de Cliente')
        cadastro.cadastrar_cliente()
    elif str(f'{opcao1}{opcao2}') == '23':
        print('\nCriar Conta')
        cadastro.criar_conta_corrente()
    elif str(f'{opcao1}{opcao2}') == '24':
        print('\nLista de Contas')
        cadastro.verifica_contas_corrente()
    elif str(f'{opcao1}{opcao2}') == '25':
        print('\nLista de Cadastros')
        cadastro.verifica_cadastro()

