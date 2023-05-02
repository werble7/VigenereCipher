# Alunos: Henrique Valente Lima 211055380
#         Gabriel Brito Franca  211020867

# Lista contendo a frequência de cada letra do alfabeto em português 
pt_frequencies = [0.1463, 0.0104, 0.0388, 0.0499, 0.1257, 0.0102, 0.0130, 0.0128,
                  0.0618, 0.0040, 0.0002, 0.0278, 0.0474, 0.0505, 0.1073, 0.0252,
                  0.012, 0.0653, 0.0781, 0.0434, 0.0463, 0.0167, 0.0001, 0.0021,
                  0.0001, 0.0047]

letters = 'abcdefghijklmnopqrstuvwxyz'
coincidences = []


# Retorna um índice de coincidencias para a "seção" da cifra recebida.
def get_index_coincidence(ciphermsg):
    x = float(len(ciphermsg))
    frequency_sum: float = 0.0

    # Usando o índice da formula da coincidencia 
    for a in letters:
        frequency_sum += ciphermsg.count(a) * (ciphermsg.count(a) - 1)

   
    try:
        indexCoincidence = frequency_sum / (x * (x - 1))
        return indexCoincidence
    except ZeroDivisionError:
        return frequency_sum


# Retorna o tamanho da chave com o índice médio de coincidencia 
def get_key_length(ciphertext):
    index_coincidence_table = []

    # Divide o texto cifrado em sequências com base no tamanho da chave adivinhada de 0 até a estimativa de comprimento máximo da chave (20)
    # Ex: adivinha um comprimento de chave de 2 divide o "12345678" em "1357" e "2468"
    # O comprimento de chave estimado com o maior índice de coincidência é o comprimento de chave mais provável

    for guess_len in range(20):
        index_coincidence_sum = 0.0
        avg_index_coincidence = 0.0
        for i in range(guess_len):
            sequence = ""
            # divide o texto cifrado em sequências
            for j in range(0, len(ciphertext[i:]), guess_len):
                sequence += ciphertext[i + j]
            index_coincidence_sum += get_index_coincidence(sequence)
        # impede que divida por 0
        if not guess_len == 0:
            avg_index_coincidence = index_coincidence_sum / guess_len
        index_coincidence_table.append(avg_index_coincidence)

    # retorna o índice do maior Índice de Coincidência (comprimento de chave mais provável)
    best_guess = index_coincidence_table.index(sorted(index_coincidence_table, reverse=True)[0])
    second_best_guess = index_coincidence_table.index(sorted(index_coincidence_table, reverse=True)[1])

    # Uma vez que este programa às vezes pode pensar que uma chave é literalmente duas vezes ela mesma, ou três vezes ela mesma,

    # é melhor devolver o valor menor.
    # Ex. a chave real é "gato", mas o programa acha que a chave é "gatoga" ou "gatogato"
    # (A razão deste erro é que a distribuição de frequência para a chave "dog" vs "dogdog" seria quase igual)
    if best_guess % second_best_guess == 0:
        return second_best_guess
    else:
        return best_guess


# Executa a análise de frequência na "sequência" do texto cifrado para retornar a letra dessa parte da chave
# Usa a estatística Qui-quadrado para medir o quão semelhantes são duas distribuições de probabilidade.
# (Os dois sendo o texto cifrado e a distribuição regular em português)
def frequency_analysis(sequence):
    all_chi_squareds = [0.0] * 26

    i: int
    for i in range(26):

        chi_squared_sum = 0.0

        sequence_offset = [chr(((ord(sequence[j]) - 97 - i) % 26) + 97) for j in range(len(sequence))]
        v = [0] * 26
        # conte os números de cada letra no sequence_offset já em ascii
        for x in sequence_offset:
            v[ord(x) - ord('a')] += 1
        # divida a lista pelo comprimento da sequência para obter as porcentagens de frequência

        for y in range(26):
            v[y] *= (1.0 / float(len(sequence)))

        # agora você pode comparar com as frequências em português
        for z in range(26):
            chi_squared_sum += ((v[z] - float(pt_frequencies[z])) ** 2) / float(pt_frequencies[z])

        # adicioná-lo à grande tabela de qui-quadrado
        all_chi_squareds.append(chi_squared_sum)

    # retornar a letra-chave que precisa ser deslocada
    # isso é encontrado pela menor diferença entre distribuição de sequência e distribuição portuguesa
    shift = all_chi_squareds.index(min(all_chi_squareds))

    # retorna a letra
    return chr(shift + 97)


def get_key(ciphertext, kl):
    k = ''

    # Calcula a tabela de frequência de letras para cada letra da tecla
    for i in range(kl):
        sequence = ""
        # quebra a mensagem cifrada em sequências
        for j in range(0, len(ciphertext[i:]), key_length):
            sequence += ciphertext[i + j]
        k += frequency_analysis(sequence)

    return k


# Retorna a mensagem dada a mensagem cifrada e uma chave
def decrypt(ciphermsg, key):
    msg_ascii = []
    # Cria uma lista de valores ascii da mensagem cifrada e a chave
    cipher_ascii = [ord(letter) for letter in ciphermsg]
    key_ascii = [ord(letter) for letter in key]

    # Transforma cada valor ascii da mensagem cifrada no valor ascii da mensagem
    for i in range(len(cipher_ascii)):
        msg_ascii.append(((cipher_ascii[i] - key_ascii[i % len(key)]) % 26) + 97)

    # Transforma os valores da lista ascii em caracteres
    msg = ''.join(chr(i) for i in msg_ascii)
    return msg


def encrypt(msg, key):
    # Cria uma lista de valores ascii da mensagem e a chave
    msg_ascii = [ord(letter) for letter in msg]
    key_ascii = [ord(letter) for letter in key]
    cipher_ascii = []

    # Transforma cada valor ascii da mensagem no valor ascii da mensagem cifrada
    for i in range(len(msg_ascii)):

        temp = msg_ascii[i] - 97 + key_ascii[i % len(key)]
        if temp <= 122:
            cipher_ascii.append(temp)
        else:

            cipher_ascii.append(temp - 26)

    # Transforma os valores da lista ASCII em letras
    ciphermsg = ''.join(chr(i) for i in cipher_ascii)
    return ciphermsg


if __name__ == '__main__':
    while True:
        op1 = int(input("1- Encrypt\n2- Decrypt\n3- Exit\n"))
        if op1 == 1:
            msg = input("Insert message to be encrypted: \n")
            key = input("Insert key to encrypt with: \n")

            # Remova tudo o que não estiver no alfabeto minúsculo
            msg = ''.join(x.lower() for x in msg if x.isalpha())
            key = ''.join(x.lower() for x in key if x.isalpha())

            cipher = encrypt(msg, key)
            print(f"result: {cipher}\n")

        elif op1 == 2:
            msg = input("Insert ciphed message to decrypted: \n")

            # Remova tudo o que não estiver no alfabeto minúsculo
            msg = ''.join(x.lower() for x in msg if x.isalpha())

            while True:
                op2 = int(input("Insert 1 to break, 2 to decrypt or 3 to go back: \n"))
                if op2 == 1:

                    key_length = get_key_length(msg)
                    print(f"Most probable key lenght {key_length}")

                    key = get_key(msg, key_length)
                    msg = decrypt(msg, key)

                    print(f"Key: {key}")
                    print(f"Message: {msg}")
                    break
                elif op2 == 2:

                    key = input("Enter key to decrypt with: ")
                    key = ''.join(x.lower() for x in key if x.isalpha())
                    msg = decrypt(msg, key)

                    print(f"Message: {msg}")
                    break
                elif op2 == 3:
                    break

        elif op1 == 3:
            break

    print("Volte sempre")
