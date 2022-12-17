from time import sleep

lista_cadastros = []

def verifica_cadastro():
    consulta_cliente = open('./clientes/registro_clientes.txt', 'r')
    arquivo = consulta_cliente.readlines()
    vizualizar_cadastros = input('Deseja verificar cadastros? [S/N]').upper()
    if vizualizar_cadastros == 'S':
        print(f'{"CPF":^11}|{"Nome":^32}|{"Data de Nascimento":^20}|  Endereco')
        for linha in arquivo:
            split_linha = linha.split('|')
            print(f'{split_linha[0]:^11}|{split_linha[1]:^32}|{split_linha[2]:^20}|  {split_linha[3]}')
    for str_cpf in arquivo:
        str_cpf = str_cpf.split('|')
        lista_cadastros.append(str_cpf[0])
        lista_cadastros.append(str_cpf[1])
    return lista_cadastros


def cadastrar_cliente():
    cpf = input('Informe o CPF: ')
    cadastros = verifica_cadastro()
    if cpf in cadastros:
        print(f'O CPF de número {cpf} já existe!')
        return None
    elif len(cpf) != 11:
        print(f'CPF invalido!')
        return None

    nome = input('Nome do cliente: ').title()
    if len(nome) <= 0:
        print('O nome não pode estar vazio!')
        return None

    dia = int(input('Dia da data de nascimento: '))
    mes = int(input('Mes da data de nascimento: '))
    ano = int(input('Ano da data de nascimento: '))
    if (dia > 31 or dia < 0) or (mes not in range(1, 12)) or (ano < 1900):
        print('Data invalida')
        return None
    if len(dia) == 1:
        dia = f'0{dia}'
    if len(mes) == 1:
        mes = f'0{mes}'

    logadouro = input('Logadouro/rua: ').title()
    numero = input('Numero: ')
    bairro = input('Bairro: ').title()
    cidade = input('Cidade: ').title()
    estado = input('Sigla do Estado: ').upper()

    if len(logadouro) < 1 or len(bairro) < 1 or len(cidade) < 1 or len(numero) < 1 or len(estado) < 2:
        print('Informações de Endereço invalidas')
        return None
    
    cadastra_cliente = open('./clientes/registro_clientes.txt', 'a+')
    cadastra_cliente.write(f'{cpf}|{nome}|{dia}-{mes}-{ano}|{logadouro}, {numero} - {bairro} - {cidade}/{estado}\n')
    print('Cadastro realizado com sucesso!')
    sleep(0.5)
    cadastra_cliente.close()



def verifica_contas_corrente():
    num_conta = 0
    arquivo = open('./contas/contas.txt', 'r')
    listar_contas = input('Deseja verificar contas? [S/N]').upper()
    if listar_contas == 'S':
        print('  Conta  | Agencia |  Usuario  |  Nome')
    for linha in arquivo:
        split_linha = linha.split('|')
        if listar_contas == 'S':
            print(f'{split_linha[0]:^9}|{split_linha[1]:^9}|{split_linha[2]:^11}|  {split_linha[3]}')
        if split_linha == split_linha[-1]:
            num_conta = int(split_linha)
    return num_conta


def criar_conta_corrente():
    conta = verifica_contas_corrente() + 1
    cadastros = verifica_cadastro()

    numero_agencia = '0001'
    usuario = input('Usuario (CPF): ')
    if usuario not in cadastros:
        print('Usuario não foi encontrado! Primeiro faça o cadastro.')
        return None
    print(f'Usuario {usuario} encontado!')
    arquivo = open('./contas/contas.txt', 'a+')
    arquivo.write(f'{conta}|{numero_agencia}|{usuario}|{lista_cadastros[1]}\n')
    print('Conta realizada com sucesso!')
    arquivo.close()
