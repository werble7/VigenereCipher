# Alunos: PEDRO LÍSIAS VIANA ARCOVERDE ALVES 19/0036559
#         MARCELO PIANO PATUSCO SANTIAGO     20/0049496 

# Cifra de Vigenère

#   Parte I: cifrador/decifrador
#     O cifrador recebe uma senha e uma mensagem que é cifrada segundo a cifra de Vigenère,
#     gerando um criptograma, enquanto o decifrador recebe uma senha e um criptograma que é
#     decifrado segundo a cifra de Vigenère, recuperando uma mensagem.

from unicodedata import normalize
import string

alfabeto = 'abcdefghijklmnopqrstuvwxyz'

letra_para_numero = dict(zip(alfabeto, range(len(alfabeto))))
numero_para_letra = dict(zip(range(len(alfabeto)), alfabeto))


def remove_punctuation(self, text, filter='[^A-Z]'):
    return re.sub(filter, '', text.upper())


def cifra(msg, chave):
    # limpa a mensagem (retira acentos, pontuação e coloca em maiscula)

    msg_rslt = []
    msg = normalize('NFKD', msg).encode('ASCII', 'ignore').decode('ASCII')  # tira acentos
    msg = remove_punctuation(msg)

    # retira espaços e números
    for letra in msg:
        if letra in '0123456789 ':
            continue
        else:
            msg_rslt.append(letra.lower)

    # separa a mensagem em partes do tamanho da chave
    msg_cifrada = ''
    split_msg = [msg[i:i + len(chave)] for i in range(0, len(msg), len(chave))]

    # converte a mensagem e a chave em numeros, cifra por Vigenère a mensagem
    for each_split in split_msg:
        i = 0
        for letra in each_split:
            numero = (letra_para_numero[letra] + letra_para_numero[chave[i]]) % len(alfabeto)
            msg_cifrada += numero_para_letra[numero]
            i += 1

    return msg_cifrada


def decifra(msg_cifrada: str, chave):
    # formatando a mensagem cifrada para facilitar a analise
    msg_cifrada = str(msg_cifrada).replace(' ', '').lower()  # tira espaços e coloca em minuscula
    msg_cifrada = ''.join([i for i in msg_cifrada if not i.isdigit()])  # tira numeros
    msg_cifrada = normalize('NFKD', str(msg_cifrada)).encode('ASCII', 'ignore').decode('ASCII')  # tira acentos
    msg_cifrada = msg_cifrada.translate(str.maketrans('', '', string.punctuation))  # tira pontuação

    # separa a cifra em partes do tamanho da chave
    msg = ''
    split_msg_cifrada = [msg_cifrada[i:i + len(chave)] for i in range(0, len(msg_cifrada), len(chave))]

    # converte a mensagem e a chave em numeros
    for each_split in split_msg_cifrada:
        i = 0
        for letra in each_split:
            numero = (letra_para_numero[letra] - letra_para_numero[chave[i]]) % len(alfabeto)
            msg += numero_para_letra[numero]
            i += 1

    # retorna a mensagem decifrada
    return msg


###############################################################################################

#   Parte II: ataque de recuperação de senha por análise de frequência
#     Serão fornecidas duas mensagens cifradas (uma em português e outra em inglês) com senhas
#     diferentes. Cada uma das mensagens deve ser utilizada para recuperar a senha geradora do
#     keystream usado na cifração e então decifradas. 

def ataque(msg_cifrada: str, idioma, max_chave=20, tolerancia=10):
    # formatando a mensagem cifrada para facilitar a analise
    msg_cifrada = str(msg_cifrada).replace(' ', '').lower()  # tira espaços e coloca em minuscula
    msg_cifrada = ''.join([i for i in msg_cifrada if not i.isdigit()])  # tira numeros
    msg_cifrada = normalize('NFKD', msg_cifrada).encode('ASCII', 'ignore').decode('ASCII')  # tira acentos
    msg_cifrada = msg_cifrada.translate(str.maketrans('', '', string.punctuation))  # tira pontuação

    # frequencias em cada idioma para análise
    en_freq = [
        ('a', 8.167), ('b', 1.492), ('c', 2.782), ('d', 4.253),
        ('e', 12.702), ('f', 2.228), ('g', 2.015), ('h', 6.094),
        ('i', 6.966), ('j', 0.153), ('k', 0.772), ('l', 4.025),
        ('m', 2.406), ('n', 6.749), ('o', 7.507), ('p', 1.929),
        ('q', 0.095), ('r', 5.987), ('s', 6.327), ('t', 9.056),
        ('u', 2.758), ('v', 0.978), ('w', 2.360), ('x', 0.150),
        ('y', 1.974), ('z', 0.074)]

    pt_freq = [
        ('a', 14.63), ('b', 1.04), ('c', 3.88), ('d', 4.99),
        ('e', 12.57), ('f', 1.02), ('g', 1.30), ('h', 1.28),
        ('i', 6.18), ('j', 0.40), ('k', 0.02), ('l', 2.78),
        ('m', 4.74), ('n', 5.05), ('o', 10.73), ('p', 2.52),
        ('q', 1.20), ('r', 6.53), ('s', 7.81), ('t', 4.34),
        ('u', 4.63), ('v', 1.67), ('w', 0.01), ('x', 0.47),
        ('y', 0.01), ('z', 0.47)]

    # encontrar o comprimento provavel da chave
    espacamento = []

    for i in range(len(msg_cifrada) - 2):
        tmp = msg_cifrada[i] + msg_cifrada[i + 1] + msg_cifrada[i + 2]
        for j in range(3, len(msg_cifrada) - 2 - i):
            if tmp == msg_cifrada[i + j] + msg_cifrada[i + j + 1] + msg_cifrada[i + j + 2]:
                espacamento.append(j)
                break

    if max_chave > len(msg_cifrada): max_chave = len(msg_cifrada)
    max_mmc = 0
    tam_chave = 0
    for i in range(2, max_chave + 1):
        counter = 0
        for n in espacamento:
            if n % i == 0:
                counter += 1
        if counter + tolerancia > max_mmc:
            tam_chave = i
            max_mmc = counter

    print('\nTAMANHO PROVAVEL DA CHAVE: ' + str(tam_chave))

    # separar a cifra em grupos do tamanho da chave provavel
    # tabela é uma matriz q contem os grupos para analise
    tabela = []

    for i in range(tam_chave):
        grupo = []
        j = 0
        while (j * tam_chave + i < len(msg_cifrada)):
            grupo.append(msg_cifrada[j * tam_chave + i])
            j += 1
        tabela.append(grupo)

    # análise de frequencia de cada grupo utilizando as rfequecias fornecidas pela wikipedia
    freq = en_freq if idioma == 0 else pt_freq
    chave_provavel = []

    for grupo in tabela:
        chave_atual = ''
        min_dif = 10000
        for i in range(26):
            aux = []
            for c in grupo:
                if ord(c) - i >= ord('a'):
                    aux.append(chr(ord(c) - i))
                else:
                    aux.append(chr(ord('a') + 26 - i + (ord(c) % ord('a'))))
            dif = 0
            for c in aux:
                prob = [letra for letra in freq if letra[0] == c][0][1] / 100
                dif += abs(prob - (aux.count(c) / len(aux)))
            dif = dif / len(aux)
            if dif < min_dif:
                min_dif = dif
                chave_atual = chr(ord('a') + i)
        chave_provavel.append(chave_atual)

    # retorna a chave provavel
    return chave_provavel


if __name__ == "__main__":

    while True:
        op = int(input("ESCOLHA UMA OPÇÃO:\n 1 - CIFRAR\n 2 - DECIFRAR\n 3 - ATACAR\n 4 - SAIR\n"))

        if ((op == 1) or (op == 2)):
            chave = list(input('\nDIGITE A CHAVE\n'))
            if (op == 1):
                cifra_gerada = cifra(input('\nDIGITE A MENSAGEM A SER CIFRADA\n'), chave)
                print("\nCIFRA GERADA:\n" + cifra_gerada)
                input()

            elif (op == 2):
                msg_obtida = decifra(list(input('\nDIGITE A MENSAGEM CIFRADA\n')), chave)
                print("\nMENSAGEM OBTIDA:\n" + msg_obtida)
                input()

        elif (op == 3):
            idioma = int(input('\nESCOLHA QUAL IDIOMA:\n 1 - INGLÊS\n 2 - PORTUGUÊS\n'))
            if ((idioma == 1) or (idioma == 2)):

                op1 = int(input('\nESCOLHER PARAMETROS DE ANALISE AVANÇADOS?\n1 - SIM\n2 - NÃO\n'))
                if op1 == 1:
                    max_chave = int(input('\nESCOLHA UM TAMANHO MÁXIMO PARA A CHAVE:\n'))
                    tolerancia = int(input(
                        '\nESCOLHA QUAL A TOLERANCIA PARA OS ESPAÇAMENTOS DA BUSCA:\n(escolha valores maiores quanto maior for o texto, valores entre 10 e 30)\n'))
                    msg_cifrada_ataque = input('\nDIGITE A MENSAGEM CIFRADA\n')
                    chave_provavel = ataque(msg_cifrada_ataque, idioma, max_chave, tolerancia)
                else:
                    msg_cifrada_ataque = input('\nDIGITE A MENSAGEM CIFRADA\n')
                    chave_provavel = ataque(msg_cifrada_ataque, idioma)

                print("\nCHAVE PROVAVEL:")
                for x in chave_provavel: print(x, end='')
                print()
                msg_obtida_ataque = decifra(list(msg_cifrada_ataque), chave_provavel)
                print("\nMENSAGEM OBTIDA:\n" + msg_obtida_ataque)
                input()

        elif (op == 4):
            break
