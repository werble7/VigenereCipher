# Alunos: Henrique Valente Lima 211055380
#         Gabriel Brito Franca  211020867

def decrypt(ciphermsg, key):
    ascii = []
    cipher_ascii = [ord(letter) for letter in ciphermsg]
    key_ascii = [ord(letter) for letter in key]

    for i in range(len(cipher_ascii)):
        ascii.append(((cipher_ascii[i] - key_ascii[i % len(key)]) % 26) + 97)

    msg = ''.join(chr(i) for i in ascii)
    return msg


def encrypt(msg, key):
    ascii = [ord(letter) for letter in msg]
    key_ascii = [ord(letter) for letter in key]
    cipher_ascii = []

    for i in range(len(ascii)):

        temp = ascii[i] - 97 + key_ascii[i % len(key)]
        if temp <= 122:
            cipher_ascii.append(temp)
        else:

            cipher_ascii.append(temp - 26)

    ciphermsg = ''.join(chr(i) for i in cipher_ascii)
    return ciphermsg


if __name__ == '__main__':
    while True:
        op1 = int(input("1- Encrypt\n2- Decrypt\n3- Exit\n"))
        if op1 == 1:
            msg = input("Insert message to be encrypted: \n")
            key = input("Insert key to encrypt with: \n")

            msg = ''.join(x.lower() for x in msg if x.isalpha())
            key = ''.join(x.lower() for x in key if x.isalpha())

            cipher = encrypt(msg, key)
            print(f"result: {cipher}\n")

        elif op1 == 2:
            msg = input("Insert ciphed message to be decrypted: \n")
            key = input("Enter key to decrypt with: ")\

            msg = ''.join(x.lower() for x in msg if x.isalpha())
            key = ''.join(x.lower() for x in key if x.isalpha())

            msg = decrypt(msg, key)
            print(f"Message: {msg}\n")

        elif op1 == 3:
            break
