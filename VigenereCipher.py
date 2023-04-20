# Alunos: Henrique Valente Lima 211055380
#         Gabriel Brito Franca  211020867

# Cifra de Vigenère

#   Parte I: cifrador/decifrador
#     O cifrador recebe uma senha e uma mensagem que é cifrada segundo a cifra de Vigenère,
#     gerando um criptograma, enquanto o decifrador recebe uma senha e um criptograma que é
#     decifrado segundo a cifra de Vigenère, recuperando uma mensagem.

import re

en_frequencies = [0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015,
                  0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749,
                  0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758,
                  0.00978, 0.02360, 0.00150, 0.01974, 0.00074]

pt_frequencies = [0.1463, 0.0104, 0.0388, 0.0499, 0.1257, 0.0102, 0.0130, 0.0128,
                  0.0618, 0.0040, 0.0002, 0.0278, 0.0474, 0.0505, 0.1073, 0.0252,
                  0.012, 0.0653, 0.0781, 0.0434, 0.0463, 0.0167, 0.0001, 0.0021,
                  0.0001, 0.0047]

letters = 'abcdefghijklmnopqrstuvwxyz'
coincidences = []


def filter_string(string):
    string = ''.join(x.lower() for x in string if x.isalpha())
    return string


def show_coincidences(cipherText):
    counter = 0
    cipherLength = len(cipherText)
    copy = cipherText
    for offset in range(1, cipherLength // 2):
        j = 0
        for i in range(offset, cipherLength):
            if cipherText[i] == copy[j]:
                counter += 1
            j += 1
        print(str(offset) + ": " + str(counter))
        counter = 0


def get_c(sequence):
    N = float(len(sequence))
    frequency_sum = 0.0
    for letter in letters:
        frequency_sum += sequence.count(letter) * (sequence.count(letter) - 1)
    if N * (N - 1) <= 0:
        index = frequency_sum / 1
    else:
        index = frequency_sum / (N * (N - 1))
    return index * 26


def probable_key_length(ciphertext, en):
    print("-------------Chances for key lenght-------------")
    for guess in range(21):
        coincidence_sum = 0.0
        for i in range(guess):
            letter_sequence = ""
            for j in range(0, len(ciphertext[i:]), guess):
                letter_sequence += ciphertext[i + j]
            coincidence_sum = get_c(letter_sequence)
        coincidences.append(coincidence_sum)
    print_coincidences(coincidences)


def print_coincidences(coincidences_array):
    for i in range(len(coincidences_array)):
        print(str(i) + ": " + str(coincidences_array[i]))
    print()


def frequencies(seq, en):
    chi_squared_array = [0] * 26
    if en:
        letter_frequencies = en_frequencies
    else:
        letter_frequencies = pt_frequencies
    for i in range(26):
        sum_sq = 0.0
        sequence_offset = [chr(((ord(seq[j]) - 97 - i) % 26) + 97) for j in range(len(seq))]
        c = [0] * 26
        for l in sequence_offset:
            c[ord(l) - ord('a')] += 1
        for j in range(26):
            if len(seq) > 0:
                c[j] *= (1.0 / float(len(seq)))
        for j in range(26):
            sum_sq += ((c[j] - float(letter_frequencies[j])) ** 2) / float(letter_frequencies[j])
        chi_squared_array[i] = sum_sq
    shift = chi_squared_array.index(min(chi_squared_array))
    return chr(shift + 97)


def get_key(ciphertext, key_length, en):
    key = ''
    for i in range(int(key_length)):
        sequence = ""
        for j in range(0, len(ciphertext[i:]), int(key_length)):
            sequence += ciphertext[i + j]
        key += frequencies(sequence, en)
    return key


def attack():
    language = input("Insert 'en' for english or 'pt' for portuguese: ")
    en = True
    if language == 'pt':
        en = False
    ciphertext_unfiltered = input("Insert the ciphed text: ")
    ciphertext = filter_string(ciphertext_unfiltered)
    probable_key_length(ciphertext, en)
    '''
    key_length_guess = input("Insert the key lenght: ")
    vig.key = get_key(ciphertext, key_length_guess, en)
    print("Possible key: " + vig.key)
    print("Possible message:", vig.decipher(ciphertext), "\n")
    '''
    for x in range(len(coincidences)):
        if coincidences[x] > 0:
            print("key lenght:", x)
            vig.key = get_key(ciphertext, x, en)
            print("Possible key: " + vig.key)
            print("Possible message:", vig.decipher(ciphertext), "\n")


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
            cipher = vig.encipher(input('\nInsert a message to be ciphed: \n'))
            print("\ngenerated message:\n" + cipher + "\n")

        elif op == 2:
            vig.key = input('\nInsert a key: \n')
            msg = vig.decipher(list(input('\nInsert a ciphed message to be deciphed\n')))
            print("\nObtained message:\n" + msg + "\n")

        elif op == 3:
            attack()

        elif op == 4:
            break

    print("Thanks for using me!")
