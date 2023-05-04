ingles = [0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015,
           0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749,
           0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758,
           0.00978, 0.02360, 0.00150, 0.01974, 0.00074]

portugues = [0.1463, 0.0104, 0.0388, 0.0499, 0.1257, 0.0102, 0.0130, 0.0128,
              0.0618, 0.0040, 0.0002, 0.0278, 0.0474, 0.0505, 0.1073, 0.0252,
              0.012, 0.0653, 0.0781, 0.0434, 0.0463, 0.0167, 0.0001, 0.0021,
              0.0001, 0.0047]

alfabeto = 'abcdefghijklmnopqrstuvwxyz'


def tamanho_possivel(cifra):
    coincidencia_ordenada = {}

    if op1 == '1':
        print("Em ordem crescente para ajudar a achar o número mais próximo de 1,73:")
        print("A esquerda é o tamanho da chave e a direita é o número de frequência do tamanho da chave\n")
    else:
        print("Em ordem crescente para ajudar a achar o número mais próximo de 1,94:")
        print("A esquerda é o tamanho da chave e a direita é o número de frequência do tamanho da chave\n")

    for i in range(21):
        c_sum = 0.0

        for j in range(i):
            sequencia_letra = ""

            for k in range(0, len(cifra[j:]), i):
                sequencia_letra += cifra[j + k]

            c_sum = get_coincidencias(sequencia_letra)

        coincidencia.append(c_sum)

    for i, c in enumerate(coincidencia):
        coincidencia_ordenada[c] = i

    for x in sorted(coincidencia_ordenada.keys()):
        print(f"{coincidencia_ordenada[x]}: {x:.3f}")

    print()


def get_coincidencias(sequencia):
    n = float(len(sequencia))
    f_sum = 0.0

    for letra in alfabeto:
        f_sum += sequencia.count(letra) * (sequencia.count(letra) - 1)

    if n * (n - 1) <= 0:
        index = f_sum / 1

    else:
        index = f_sum / (n * (n - 1))

    return index * 26


def get_chave(cifra, tamanho):
    p_key = ''
    for i in range(int(tamanho)):
        sequence = ""
        for j in range(0, len(cifra[i:]), int(tamanho)):
            sequence += cifra[i + j]
        p_key += frequencia(sequence)
    return p_key


def frequencia(seq):
    chi2_array = [0.0] * 26

    if op1 == '1':
        l_frequencia = ingles
    else:
        l_frequencia = portugues

    for i in range(26):
        sum_sq = 0.0
        sequence_offset = [chr(((ord(seq[j]) - 97 - i) % 26) + 97) for j in range(len(seq))]
        c = [0] * 26

        for j in sequence_offset:
            c[ord(j) - ord('a')] += 1

        for j in range(26):
            c[j] *= (1.0 / float(len(seq)))

        for j in range(26):
            sum_sq += ((c[j] - float(l_frequencia[j])) ** 2) / float(l_frequencia[j])

        chi2_array[i] = sum_sq

    shift = chi2_array.index(min(chi2_array)) + 97
    return chr(shift)


if __name__ == '__main__':
    coincidencia = []

    while True:
        op1 = input("1 - Ingles\n2 - Portugues\n3 - Sair\n")

        if op1 != '1' and op1 != '2' and op1 != '3':
            print("insira uma opção válida!")

        if op1 == '3':
            break

        msg = input("Insira texto cifrado:\n")
        msg = ''.join(x.lower() for x in msg if x.isalpha())

        tamanho_possivel(msg)
        attempt = input("Insira o tamanho provavel da chave:\n")
        print(f"chave provavel:\n{get_chave(msg, attempt)}\n")
