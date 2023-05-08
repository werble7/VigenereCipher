english = [0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015,
           0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749,
           0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758,
           0.00978, 0.02360, 0.00150, 0.01974, 0.00074]

portuguese = [0.1463, 0.0104, 0.0388, 0.0499, 0.1257, 0.0102, 0.0130, 0.0128,
              0.0618, 0.0040, 0.0002, 0.0278, 0.0474, 0.0505, 0.1073, 0.0252,
              0.012, 0.0653, 0.0781, 0.0434, 0.0463, 0.0167, 0.0001, 0.0021,
              0.0001, 0.0047]

alphabet = 'abcdefghijklmnopqrstuvwxyz'


def probable_length(cipher):
    sorted_coincidences = {}

    if op1 == '1':
        print("In crescent order to help finding the closest number to 1.73:")
        print("On the left is the key length and on the right is the frequency number for this key length\n")
    else:
        print("In crescent order to help finding the closest number to 1.94:")
        print("On the left is the key length and on the right is the frequency number for this key length\n")

    for i in range(len(cipher)):
        c_sum = 0.0

        for j in range(i):
            letter_sequence = ""

            for k in range(0, len(cipher[j:]), i):
                letter_sequence += cipher[j + k]

            c_sum = get_coincidences(letter_sequence)

        coincidences.append(c_sum)

    for i, c in enumerate(coincidences):
        sorted_coincidences[c] = i

    for x in sorted(sorted_coincidences.keys()):
        print(f"{sorted_coincidences[x]}: {x:.3f}")

    print()


def get_coincidences(sequence):
    n = float(len(sequence))
    f_sum = 0.0

    if n == 1:
        return 0

    for letter in alphabet:
        f_sum += sequence.count(letter) * (sequence.count(letter) - 1)

    return (f_sum / (n * (n - 1))) * 26


def get_key(cipher, length):
    p_key = ''
    for i in range(int(length)):
        sequence = ""
        for j in range(0, len(cipher[i:]), int(length)):
            sequence += cipher[i + j]
        p_key += frequencies(sequence)
    return p_key


def frequencies(seq):
    chi2_array = [0.0] * 26

    if op1 == '1':
        l_frequencies = english
    else:
        l_frequencies = portuguese

    for i in range(26):
        sum_sq = 0.0
        sequence_offset = [chr(((ord(seq[j]) - 97 - i) % 26) + 97) for j in range(len(seq))]
        c = [0] * 26

        for j in sequence_offset:
            c[ord(j) - 97] += 1

        for k in range(26):
            c[k] /= len(seq)
            sum_sq += ((c[k] - l_frequencies[k]) ** 2) / l_frequencies[k]

        chi2_array[i] = sum_sq

    shift = chi2_array.index(min(chi2_array)) + 97
    return chr(shift)


if __name__ == '__main__':
    coincidences = []

    while True:
        op1 = input("1 - English\n2 - Portuguese\n3 - Exit\n")

        if op1 != '1' and op1 != '2' and op1 != '3':
            print("Insert a valid option!")

        if op1 == '3':
            break

        msg = input("Insert cipher text:\n")
        msg = ''.join(x.lower() for x in msg if x.isalpha())

        probable_length(msg)
        attempt = input("Insert the possible key length:\n")
        print(f"Possible key:\n{get_key(msg, attempt)}\n")
