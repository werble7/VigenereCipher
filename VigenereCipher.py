# Alunos: Henrique Valente Lima 211055380
#         Gabriel Brito Franca  211020867

def encrypt(e_msg, e_key):
    e_ascii = [ord(letter) for letter in e_msg]
    chave_ascii = [ord(letter) for letter in e_key]
    cifra_ascii = []

    for i in range(len(e_ascii)):
        cifra_ascii.append(((e_ascii[i] + chave_ascii[i % len(e_key)] - 194) % 26) + 97)

    e_msg = ''.join(chr(i) for i in cifra_ascii)
    return e_msg


def decrypt(d_msg, d_key):
    d_ascii = []
    cipher_ascii = [ord(letter) for letter in d_msg]
    key_ascii = [ord(letter) for letter in d_key]

    for i in range(len(cipher_ascii)):
        d_ascii.append(((cipher_ascii[i] - key_ascii[i % len(d_key)]) % 26) + 97)

    d_msg = ''.join(chr(i) for i in d_ascii)
    return d_msg


if __name__ == '__main__':
    while True:
        op1 = int(input("1- Criptografar\n2- descriptografar\n3- Sair\n"))

        if op1 == 1:
            msg = input("Insira a mensagem que serar cifrada:\n")
            key = input("Insira chave: \n")

            msg = ''.join(x.lower() for x in msg if x.isalpha())
            key = ''.join(x.lower() for x in key if x.isalpha())

            msg = encrypt(msg, key)
            print(f"resultado: {msg}\n")

        elif op1 == 2:
            msg = input("Insira mensagem cifrada: \n")
            key = input("Insira a chave: ")\

            msg = ''.join(x.lower() for x in msg if x.isalpha())
            key = ''.join(x.lower() for x in key if x.isalpha())

            msg = decrypt(msg, key)
            print(f"Menssagem: {msg}\n")

        elif op1 == 3:
            break
