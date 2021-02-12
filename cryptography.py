"""Different subclasses of ciphers and subclasses of persons"""
import random
import crypto_utils

english_alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L",
                    "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X",
                    "Y", "Z"]

ascii_alphabet = [" ", "!", '"', "#", "$", "%", "&", "'", "(", ")", "*", "+",
                  ",", "-", ".", "/", "0", "1", "2", "3", "4", "5", "6", "7",
                  "8", "9", ":", ";", "<", "=", ">", "?", "@",
                  "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L",
                  "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X",
                  "Y", "Z",
                  "[", "]", "^", "_", "`", "a", "b", "c", "d", "e", "f", "g", "h",
                  "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
                  "u", "v", "w", "x", "y", "z", "{", "|", "}", "~"]


class Cipher:
    """Has implementations of various ciphers as subclass"""

    def __init__(self, alphabet):
        self.alphabet = alphabet

    def encode(self, text):
        return text

    def decode(self, text):
        return text

    def verify(self):
        if not self.decode(self.encode("CODE")) == "CODE":
            raise Exception


class Caesar(Cipher):
    """Substitutes letters with a static integer"""

    def __init__(self, alphabet, integer):
        super().__init__(alphabet)
        self.integer = integer
        self.name = "Caesar"

    def get_name(self):
        return self.name

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
    """Multiplies index of letters"""

    def __init__(self, alphabet, integer):
        super().__init__(alphabet)
        self.integer = integer
        self.name = "Multiplication"

    def get_name(self):
        return self.name

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
                    index = (letter * crypto_utils.modular_inverse(self.integer,
                                                                   len(self.alphabet))) % len(self.alphabet)
                    decoded_text += self.alphabet[index]

        return decoded_text

    def verify(self):
        if not self.decode(self.encode("CODE")) == "CODE":
            raise Exception


class Affine(Cipher):
    """Combines Caesar and Multiplication"""

    def __init__(self, alphabet, integer1, integer2):
        super().__init__(alphabet)
        self.integers = [integer1, integer2]
        self.name = "Affine"

    def get_name(self):
        return self.name

    def encode(self, text):
        return Multiplication(self.alphabet,
                              self.integers[1]).encode(Caesar(self.alphabet,
                                                              self.integers[0]).encode(text))

    def decode(self, text):
        return Caesar(self.alphabet,
                      self.integers[0]).decode(Multiplication(self.alphabet,
                                                              self.integers[1]).decode(text))

    def verify(self):
        if not self.decode(self.encode("CODE")) == "CODE":
            raise Exception


class Unbreakable(Cipher):
    """uses indexes of a keyword to encode different words"""

    def __init__(self, alphabet, keyword):
        super().__init__(alphabet)
        self.keyword = keyword
        self.name = "Unbreakable"

    def get_name(self):
        return self.name

    def encode(self, text):
        new_keyword = ""
        for index in range(len(text)):
            new_keyword += self.keyword[index % len(self.keyword)]

        encoded_text = ""
        keyword_count = 0
        for character in new_keyword:
            for letter in range(len(self.alphabet)):
                if character == self.alphabet[letter]:
                    encoded_text += Caesar(self.alphabet, letter).encode(text[keyword_count])
                    keyword_count += 1

        return encoded_text

    def decode(self, text):
        new_keyword = ""
        for index in range(len(text)):
            new_keyword += self.keyword[index % len(self.keyword)]

        decoded_text = ""
        keyword_count = 0
        for character in new_keyword:
            for letter in range(len(self.alphabet)):
                if character == self.alphabet[letter]:
                    decoded_text += Caesar(self.alphabet, letter).decode(text[keyword_count])
                    keyword_count += 1

        return decoded_text

    def verify(self):
        if not self.decode(self.encode("CODE")) == "CODE":
            raise Exception


class RSA(Cipher):
    """encodes and decodes integers and text"""
    """did not have time to finish"""

    def generate_key(self):
        p = crypto_utils.generate_random_prime(5)
        q = crypto_utils.generate_random_prime(5)
        while p == q:
            q = crypto_utils.generate_random_prime(5)
        self.n = p * q
        o = (p-1) * (q-1)
        self.e = random.randint(3, o-1)
        self.d = crypto_utils.modular_inverse(self.e, o)
        return self.n, self.e, self.d

    def encode_integer(self, t):
        self.encoded_integer = (t ^ self.e) % self.n
        return self.encoded_integer

    def decode_integer(self):
        return (self.encoded_integer ^ self.d) % self.n

    def encode_text(self, text):
        letter_indexes = ""
        for letter in text:
            for index in range(len(ascii_alphabet)):
                if letter == ascii_alphabet[index]:
                    letter_indexes += '{0:08b}'.format(index)

        return letter_indexes

    def decode_text(self, text):
        decoded_text = ""
        decoded_bits = 0

        for integer in range(len(text)):
            if integer % 8 == 0:
                split = text.split()
                map_object = map(int, split)
                list_of_bits = list(map_object)
                print(list_of_bits)

#        for integer in text.split().:
#            decoded_bits += int(text[integer:integer+8], 2)

        for integer in decoded_bits:
            decoded_text += ascii_alphabet[integer]

        return decoded_text


class Person:
    """Superclass person who sends, receives or hacks ciphertext"""

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
    """Person who sends ciphertext"""

    def __init__(self, key, cipher, text):
        super().__init__(key, cipher)
        self.text = text

    def operate_cipher(self):
        return self.cipher.encode(self.text)


class Receiver(Person):
    """Person who receives ciphertext, and decodes it to plaintext"""

    def __init__(self, key, cipher, text):
        super().__init__(key, cipher)
        self.text = text

    def operate_cipher(self):
        return self.cipher.decode(self.text)


class Hacker(Person):
    """Brute force hacker who tries to gain plaintext"""

    def __init__(self, key, cipher, text, alphabet):
        super().__init__(key, cipher)
        self.text = text
        self.alphabet = alphabet
        file = open('english_words.txt', 'r')
        self.english_words = file.read().split()
        file.close()

    def hack(self):

        english_words_count = 0
        final_shift1 = 0
        final_shift2 = 0

        if self.cipher.get_name() == "Caesar":
            for shift in range(len(self.alphabet)):
                word_count = 0
                decoded_text = Caesar(self.alphabet, shift).decode(self.text).split(" ")
                for decoded_word in decoded_text:
                    for word in self.english_words:
                        if word == decoded_word:
                            word_count += 1
                if word_count > english_words_count:
                    final_shift1 = shift
                    english_words_count = word_count
            return Caesar(self.alphabet, final_shift1).decode(self.text)
        elif self.cipher.get_name() == "Multiplication":
            for shift in range(len(self.alphabet)):
                word_count = 0
                decoded_text = Multiplication(self.alphabet, shift).decode(self.text).split(" ")
                for decoded_word in decoded_text:
                    if self.english_words.__contains__(decoded_word.lower().replace(".", "")):
                        word_count += 1
                if word_count > english_words_count:
                    final_shift1 = shift
                    english_words_count = word_count
            return Multiplication(self.alphabet, final_shift1).decode(self.text)
        elif self.cipher.get_name() == "Affine":
            for shift in range(len(self.alphabet)):
                for shift2 in range(len(self.alphabet)):
                    word_count = 0
                    decoded_text = Caesar(self.alphabet, shift).decode(Multiplication(self.alphabet, shift2).decode(self.text)).split(" ")
                    for decoded_word in decoded_text:
                        if self.english_words.__contains__(decoded_word.lower().replace(".", "")):
                            word_count += 1
                    if word_count > english_words_count:
                        final_shift1 = shift
                        final_shift2 = shift2
                        english_words_count = word_count
            return Caesar(self.alphabet, final_shift1).decode(Multiplication(self.alphabet, final_shift2).decode(self.text))
        else:
            final_keyword = ""
            for word in self.english_words:
                count = 0

                """Create keyword as long as the text"""
                new_keyword = ""
                for index in range(len(self.text)):
                    new_keyword += word[index % len(word)]

                decoded_text = Unbreakable(self.alphabet, new_keyword).decode(self.text)
                decoded_text = decoded_text.split(" ")
                for decoded_word in decoded_text:
                    if self.english_words.__contains__(decoded_word.lower().replace(".", "")):
                        count += 1
                if count > english_words_count:
                    english_words_count = count
                    final_keyword = new_keyword

                """breakpoint so that the code doesn't run too long"""
                if english_words_count > len(self.text)/5:
                    return Unbreakable(self.alphabet, final_keyword).decode(self.text)

            return Unbreakable(self.alphabet, final_keyword).decode(self.text)


def main():
    """the main function"""

    """Testing Caesar cipher"""

    sender = Sender(2, Caesar(ascii_alphabet, 23), "This is a sentence.")
    encoded_text = sender.operate_cipher()

    receiver = Receiver(2, Caesar(ascii_alphabet, 23), encoded_text)
    decoded_text = receiver.operate_cipher()
    print("Caesar encoded text:", encoded_text)
    print("Caesar decoded text:", decoded_text)
    print("\n")

    """verifies that the Caesar cipher works"""
    Caesar(ascii_alphabet, 23).verify()

    """Testing Multiplication cipher"""

    sender = Sender(2, Multiplication(ascii_alphabet, 5), "This is a sentence.")
    encoded_text = sender.operate_cipher()

    receiver = Receiver(2, Multiplication(ascii_alphabet, 5), encoded_text)
    decoded_text = receiver.operate_cipher()
    print("Multiplication encoded text:", encoded_text)
    print("Multiplication decoded text:", decoded_text)
    print("\n")

    """verifies that the Multiplication cipher works"""
    Multiplication(ascii_alphabet, 23).verify()

    """Testing Affine cipher"""

    sender = Sender(2, Affine(ascii_alphabet, 2, 5), "This is a sentence.")
    encoded_text = sender.operate_cipher()

    receiver = Receiver(2, Affine(ascii_alphabet, 2, 5), encoded_text)
    decoded_text = receiver.operate_cipher()
    print("Affine encoded text:", encoded_text)
    print("Affine decoded text:", decoded_text)
    print("\n")

    """verifies that the Affine cipher works"""
    Affine(ascii_alphabet, 2, 23).verify()

    """Testing Unbreakable cipher"""

    sender = Sender(2, Unbreakable(ascii_alphabet, "aahed"), "This is a sentence.")
    encoded_text = sender.operate_cipher()

    receiver = Receiver(2, Unbreakable(ascii_alphabet, "aahed"), encoded_text)
    decoded_text = receiver.operate_cipher()
    print("Unbreakable encoded text:", encoded_text)
    print("Unbreakable decoded text:", decoded_text)
    print("\n")

    """verifies that the Unbreakable cipher works"""
    Unbreakable(ascii_alphabet, "PIZZA").verify()

    """Testing RSA cipher"""
    rsa = RSA(ascii_alphabet)
    rsa.generate_key()
    encoded_text = rsa.encode_integer(7)
    decoded_text = rsa.decode_integer()
    print("RSA encoded integer:", encoded_text)
    print("RSA decoded integer:", decoded_text)
    print("\n")

#    encoded_text = rsa.encode_text("CODE")
#    print(encoded_text)

#    decoded_text = rsa.decode_text(encoded_text)
#    print(decoded_text)


    """Testing the Hacker with Caesar cipher"""
    sender = Sender(2, Caesar(ascii_alphabet, 22), "This is a sentence.")
    encoded_text = sender.operate_cipher()

    hacker = Hacker(2, Caesar(ascii_alphabet, 22), encoded_text, ascii_alphabet)
    decoded_text = hacker.hack()
    print("Hacker encoded Caesar text:", encoded_text)
    print("Hacker bruteforce decoded Caesar text:", decoded_text)
    print("\n")


    """Testing the Hacker with Multiplication cipher"""
    sender = Sender(2, Multiplication(ascii_alphabet, 3), "This is a sentence.")
    encoded_text = sender.operate_cipher()

    hacker = Hacker(2, Multiplication(ascii_alphabet, 3), encoded_text, ascii_alphabet)
    decoded_text = hacker.hack()
    print("Hacker encoded Multiplication text:", encoded_text)
    print("Hacker bruteforce decoded Multiplication text:", decoded_text)
    print("\n")


    """Testing the Hacker with Affine cipher"""
    sender = Sender(2, Affine(ascii_alphabet, 2, 3), "This is a sentence.")
    encoded_text = sender.operate_cipher()

    hacker = Hacker(2, Affine(ascii_alphabet, 2, 3), encoded_text, ascii_alphabet)
    decoded_text = hacker.hack()
    print("Hacker encoded Affine text:", encoded_text)
    print("Hacker bruteforce decoded Affine text:", decoded_text)
    print("\n")


    """Testing the Hacker with Unbreakable cipher"""
    sender = Sender(2, Unbreakable(ascii_alphabet, "aahed"), "This is a sentence.")
    encoded_text = sender.operate_cipher()

    hacker = Hacker(2, Unbreakable(ascii_alphabet, "aahed"), encoded_text, ascii_alphabet)
    decoded_text = hacker.hack()
    print("Hacker encoded Unbreakable text:", encoded_text)
    print("Hacker bruteforce decoded Unbreakable text:", decoded_text)
    print("\n")


if __name__ == "__main__":
    main()
