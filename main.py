from datetime import datetime

saldo = 0
saques_diarios = 3
limite_valor_saque = 500


def verifica_limite_saques():
    global saldo, saques_diarios
    cont_saques = 0
    data_operacao = datetime.now()
    str_data_operacao = data_operacao.strftime('%d-%m-%Y')
    consulta_extrato = open('historico.txt', 'r')
    arquivo = consulta_extrato.readlines()
    for linha in arquivo:
        if str_data_operacao in linha and 'Saque' in linha:
            cont_saques += 1
    print(cont_saques)
    if saques_diarios > cont_saques:
        return True
    print('Limite de saques diarios atingidos!')
    return False


def verifica_saldo():
    global saldo, saques_diarios
    soma_depositos = 0
    soma_saques = 0
    consulta_extrato = open('historico.txt', 'r')
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
        registra_operacao = open('historico.txt', 'a+')
        registra_operacao.write(f'Deposito:   R$ {valor:.2f} | Realizado em: {str_data_operacao}\n')
        print(f'Seu saldo agora é de {saldo:.2f}')
        registra_operacao.close()


def saque(valor):
    global saldo, saques_diarios
    limite_saques = verifica_limite_saques()
    print(limite_saques)
    if limite_saques is False:
        print(f'Não foi possivel realizar a operação de saque. Limite diario de {saques_diarios} saques atingido!')
    if saldo - valor <= 0 and limite_saques is True:
        confirma_operacao = input(f'Você deseja retirar {valor:.2f}? [S/N]').upper()
        if confirma_operacao == 'N':
            print('Operação de saque cancelada!')
            return None
        saldo -= valor
        saques_diarios -= 1
        data_operacao = datetime.now()
        str_data_operacao = data_operacao.strftime('%d-%m-%Y, %H:%M:%S')
        registra_operacao = open('historico.txt', 'a+')
        registra_operacao.write(f'Saque:   R$ {valor:.2f} | Realizado em: {str_data_operacao}\n')
        print('Operação de deposito realizada com sucesso!')
        print(f'Seu saldo agora é de R$ {saldo:.2f}')
        registra_operacao.close()
        print(f'{saques_diarios} saque(s) restante(s).')


def extrato():
    consulta_extrato = open('historico.txt', 'r')
    arquivo = consulta_extrato.readlines()
    if arquivo == '':
        print('Não foram realizadas movimentações')
    for linha in arquivo:
        print(f'| {linha.center(30)} |')
    consulta_extrato.close()


saldo = verifica_saldo()
print(saldo)
while True:
    menu = f'''
    Menu principal

[1] - Depositar
[2] - Sacar
[3] - Extrato
[0] - Sair
    '''
    print(menu)
    opcao = input(f'Selecione uma opcao: ')
    if opcao not in ['0', '1', '2', '3']:
        print(f'A opcao {opcao} é invalida!')
    if opcao == '0':
        print('Obrigado até a proxima!')
        break
    elif opcao == '3':
        print('Consulta de extrato')
        extrato()
    elif opcao == '1' or opcao == '2':
        quantia = float(input('Informe o valor: '))
        if opcao == '1':
            deposito(quantia)
        elif opcao == '2':
            if quantia > limite_valor_saque:
                print(f'O limite de Saque é de R$ {limite_valor_saque:.2f}')
            if quantia - saldo > 0:
                print(f'Saldo Insuficiente! O seu saldo atual é de R$ {saldo:.2f}')
            else:
                saque(quantia)
