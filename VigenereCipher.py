# Alunos: Henrique Valente Lima 211055380
#         ...

# Cifra de Vigenère

#   Parte I: cifrador/decifrador
#     O cifrador recebe uma senha e uma mensagem que é cifrada segundo a cifra de Vigenère,
#     gerando um criptograma, enquanto o decifrador recebe uma senha e um criptograma que é
#     decifrado segundo a cifra de Vigenère, recuperando uma mensagem.

import re


class Vigenere():

    def a2int(self, ch):
        ch = ch.upper()
        arr = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9, 'K': 10,
               'L': 11, 'M': 12, 'N': 13, 'O': 14, 'P': 15, 'Q': 16, 'R': 17, 'S': 18, 'T': 19, 'U': 20,
               'V': 21, 'W': 22, 'X': 23, 'Y': 24, 'Z': 25}
        return arr[ch]

    def int2a(self, i):
        i = i % 26
        arr = (
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
        'W', 'X', 'Y', 'Z')
        return arr[i]

    def filter_msg(self, text, filter='[^A-Z]'):
        return re.sub(filter, '', text.upper())

    def __init__(self, key='fortification'):
        self.key = [k.upper() for k in key]

    def encipher(self, string):
        string = self.filter_msg(str(string))
        ret = ''
        for (i, c) in enumerate(string):
            i = i % len(self.key)
            ret += self.int2a(self.a2int(c) + self.a2int(self.key[i]))
        return ret

    def decipher(self, string):
        string = self.filter_msg(str(string))
        ret = ''
        for (i, c) in enumerate(string):
            i = i % len(self.key)
            ret += self.int2a(self.a2int(c) - self.a2int(self.key[i]))
        return ret


if __name__ == "__main__":

    vig = Vigenere()

    while True:
        op = int(input("Select an option:\n 1 - Cipher\n 2 - Decipher\n 3 - Attack\n 4 - Exit\n"))

        if op == 1:
            vig.key = input('\nInsert a key: \n')
            cifra_gerada = vig.encipher(input('\nInsert a message to be ciphed: \n'))
            print("\ngenerated message:\n" + cifra_gerada + "\n")

        elif op == 2:
            vig.key = input('\nInsert a key: \n')
            msg_obtida = vig.decipher(list(input('\nInsert a ciphed message to be deciphed\n')))
            print("\nObtained message:\n" + msg_obtida + "\n")

        elif op == 3:
            continue

        elif op == 4:
            break

    print("Thanks for using me!")
