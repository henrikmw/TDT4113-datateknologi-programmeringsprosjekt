import crypto_utils

english_alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L",
                    "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X",
                    "Y", "Z"]


class Cipher:
    #has implementations of various encryption algorithms as subclasses

    def __init__(self, alphabet):
        self.alphabet = alphabet

    def encode(self, text):
        return 0

    def decode(self, text):
        return 0

    def verify(self):
        #encodes and decodes for itself, to check that it has been done correctly
        return 0

    #method for generating encryption and decryption keys


class Caesar(Cipher):

    def __init__(self, alphabet, integer):
        super().__init__(alphabet)
        self.integer = integer

    def encode(self, text):
        encoded_text = ""
        for character in text:
            for letter in range(len(self.alphabet)):
                if character == self.alphabet[letter]:
                    index = (letter + self.integer) % len(self.alphabet)
                    encoded_text += self.alphabet[index]
        return encoded_text

    def decode(self, text):
        decoded_text = ""
        for character in text:
            for letter in range(len(self.alphabet)):
                if character == self.alphabet[letter]:
                    index = (letter - self.integer) % len(self.alphabet)
                    decoded_text += self.alphabet[index]

        return decoded_text

    def verify(self):
        if not self.decode(self.encode("CODE")) == "CODE":
            raise Exception


class Multiplication(Cipher):

    def __init__(self, alphabet, integer):
        super().__init__(alphabet)
        self.integer = integer

    def encode(self, text):
        encoded_text = ""
        for character in text:
            for letter in range(len(self.alphabet)):
                if character == self.alphabet[letter]:
                    index = (letter * self.integer) % len(self.alphabet)
                    encoded_text += self.alphabet[index]
        return encoded_text

    def decode(self, text):
        decoded_text = ""
        for character in text:
            for letter in range(len(self.alphabet)):
                if character == self.alphabet[letter]:
                    index = letter * self.alphabet / self.integer
                    decoded_text += self.alphabet[index]

        return decoded_text

    def verify(self):
        if not self.decode(self.encode("CODE")) == "CODE":
            raise Exception


class Person:

    def __init__(self, key, cipher):
        self.key = key
        self.cipher = cipher

    def set_key(self, key):
        self.key = key

    def get_key(self):
        return self.key

    def operate_cipher(self):
        return self.cipher.verify()


class Sender(Person):

    def __init__(self, key, cipher, text):
        super().__init__(key, cipher)
        self.text = text

    def operate_cipher(self):
        return self.cipher.encode(self.text)


class Receiver(Person):

    def __init__(self, key, cipher, text):
        super().__init__(key, cipher)
        self.text = text

    def operate_cipher(self):
        return self.cipher.decode(self.text)


class Hacker(Person):

    def __init__(self, key, cipher):
        super().__init__(key, cipher)


def main():
    """the main function"""
    sender = Sender(2, Caesar(english_alphabet, 23), "HMMMM")
    encoded_text = sender.operate_cipher()

    receiver = Receiver(2, Caesar(english_alphabet, 23), encoded_text)
    decoded_text = receiver.operate_cipher()
    print(encoded_text)
    print(decoded_text)

    """verifies that the Caesar cipher works"""
    Caesar(english_alphabet, 23).verify()




if __name__ == "__main__":
    main()
