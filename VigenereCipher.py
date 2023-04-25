# Alunos: Henrique Valente Lima 211055380
#         Gabriel Brito Franca  211020867

# array containing the frequencies of each letter in portuguese
pt_frequencies = [0.1463, 0.0104, 0.0388, 0.0499, 0.1257, 0.0102, 0.0130, 0.0128,
                  0.0618, 0.0040, 0.0002, 0.0278, 0.0474, 0.0505, 0.1073, 0.0252,
                  0.012, 0.0653, 0.0781, 0.0434, 0.0463, 0.0167, 0.0001, 0.0021,
                  0.0001, 0.0047]

letters = 'abcdefghijklmnopqrstuvwxyz'
coincidences = []


# Returns the Index of Coincidence for the "section" of the given cipher message
def get_index_coincidence(ciphermsg):
    x = float(len(ciphermsg))
    frequency_sum: float = 0.0

    # Using Index of Coincidence formula
    for a in letters:
        frequency_sum += ciphermsg.count(a) * (ciphermsg.count(a) - 1)

    # Using Index of Coincidence formula
    try:
        indexCoincidence = frequency_sum / (x * (x - 1))
        return indexCoincidence
    except ZeroDivisionError:
        return frequency_sum


# Returns the key length with the highest average Index of Coincidence
def get_key_length(ciphertext):
    index_coincidence_table = []

    # Splits the ciphertext into sequences based on the guessed key length from 0 until the max key length guess (20)
    # Ex. guessing a key length of 2 splits the "12345678" into "1357" and "2468"
    # This procedure of breaking cipher message into sequences and sorting it by the Index of Coincidence
    # The guessed key length with the highest index of coincidence is the most probable key length
    for guess_len in range(20):
        index_coincidence_sum = 0.0
        avg_index_coincidence = 0.0
        for i in range(guess_len):
            sequence = ""
            # breaks the ciphertext into sequences
            for j in range(0, len(ciphertext[i:]), guess_len):
                sequence += ciphertext[i + j]
            index_coincidence_sum += get_index_coincidence(sequence)
        # obviously don't want to divide by zero
        if not guess_len == 0:
            avg_index_coincidence = index_coincidence_sum / guess_len
        index_coincidence_table.append(avg_index_coincidence)

    # returns the index of the highest Index of Coincidence (most probable key length)
    best_guess = index_coincidence_table.index(sorted(index_coincidence_table, reverse=True)[0])
    second_best_guess = index_coincidence_table.index(sorted(index_coincidence_table, reverse=True)[1])

    # Since this program can sometimes think that a key is literally twice itself, or three times itself,
    # it's best to return the smaller amount.
    # Ex. the actual key is "dog", but the program thinks the key is "dogdog" or "dogdogdog"
    # (The reason for this error is that the frequency distribution for the key "dog" vs "dogdog" would be nearly equal)
    if best_guess % second_best_guess == 0:
        return second_best_guess
    else:
        return best_guess


# Performs frequency analysis on the "sequence" of the ciphertext to return the letter for that part of the key
# Uses the Chi-Squared Statistic to measure how similar two probability distributions are.
# (The two being the ciphertext and regular english distribution)
def frequency_analysis(sequence):
    all_chi_squareds = [0.0] * 26

    i: int
    for i in range(26):

        chi_squared_sum = 0.0

        sequence_offset = [chr(((ord(sequence[j]) - 97 - i) % 26) + 97) for j in range(len(sequence))]
        v = [0] * 26
        # count the numbers of each letter in the sequence_offset already in ascii
        for x in sequence_offset:
            v[ord(x) - ord('a')] += 1
        # divide the array by the length of the sequence to get the frequency percentages
        for y in range(26):
            v[y] *= (1.0 / float(len(sequence)))

        # now you can compare to the english frequencies
        for z in range(26):
            chi_squared_sum += ((v[z] - float(pt_frequencies[z])) ** 2) / float(pt_frequencies[z])

        # add it to the big table of chi squareds
        all_chi_squareds.append(chi_squared_sum)

    # return the key letter that it needs to be shifted by
    # this is found by the smallest difference between sequence distribution and portuguese distribution
    shift = all_chi_squareds.index(min(all_chi_squareds))

    # return the letter
    return chr(shift + 97)


def get_key(ciphertext, kl):
    k = ''

    # Calculates the letter frequency table for each letter of the key
    for i in range(kl):
        sequence = ""
        # breaks the cipher message into sequences
        for j in range(0, len(ciphertext[i:]), key_length):
            sequence += ciphertext[i + j]
        k += frequency_analysis(sequence)

    return k


# Returns the message given the cipher message and a key
def decrypt(ciphermsg, key):
    msg_ascii = []
    # Creates an ascii array values of the cipher message and the key
    cipher_ascii = [ord(letter) for letter in ciphermsg]
    key_ascii = [ord(letter) for letter in key]

    # Turns each ascii value of the cipher message into the ascii value of the message
    for i in range(len(cipher_ascii)):
        msg_ascii.append(((cipher_ascii[i] - key_ascii[i % len(key)]) % 26) + 97)

    # Turns the ascii array values into characters
    msg = ''.join(chr(i) for i in msg_ascii)
    return msg


def encrypt(msg, key):
    # Creates an ascii array values of the message and the key
    msg_ascii = [ord(letter) for letter in msg]
    key_ascii = [ord(letter) for letter in key]
    cipher_ascii = []

    # Turns each ascii value of the message into the ascii value of the cipher message
    for i in range(len(msg_ascii)):

        temp = msg_ascii[i] - 97 + key_ascii[i % len(key)]
        if temp <= 122:
            cipher_ascii.append(temp)
        else:
            # Go from the start
            cipher_ascii.append(temp - 26)

    # Turns the ascii array values into letters
    ciphermsg = ''.join(chr(i) for i in cipher_ascii)
    return ciphermsg


if __name__ == '__main__':
    while True:
        op1 = int(input("1- Encrypt\n2- Decrypt\n3- Exit\n"))
        if op1 == 1:
            msg = input("Insert message to be encrypted: \n")
            key = input("Insert key to encrypt with: \n")

            # Remove all that is not in lowercase alphabet
            msg = ''.join(x.lower() for x in msg if x.isalpha())
            key = ''.join(x.lower() for x in key if x.isalpha())

            cipher = encrypt(msg, key)
            print(f"result: {cipher}\n")

        elif op1 == 2:
            msg = input("Insert ciphed message to decrypted: \n")

            # Remove all that is not in lowercase alphabet
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

    print("Thanks for using me!")
