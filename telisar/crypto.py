from collections import defaultdict
import re


class ElethisCipher:
    """
    An implementation of Elethi's Cipher, a cipher created by Madame Elethi and used in her ledger.

    This is an autokey cipher that uses a variant on a tabula recta. Rather than a typical 26x26 matrix with A-Z,
    Elethi's Cipher uses a 10x10 matrix that encodes A-Z0-9:

        0 1 2 3 4 5 6 7 8 9
      +--------------------
    0 | a b c d e f g h i j
    1 | k l m n o p q r s t
    2 | u v w x y z 0 1 2 3
    3 | 4 5 6 7 8 9 a b c d
    4 | e f g h i j k l m n
    5 | o p q r s t u v w x
    6 | y z 0 1 2 3 4 5 6 7
    7 | 8 9 a b c d e f g h
    8 | i j k l m n o p q r
    9 | s t u v w x y z 0 1


    Encrypting Messages
    -------------------

    The encryption algorithm is as follows. Consider the plaintext message

        KILL KEEN FOR HANDSOME HENRY SMALLS

    and the pre-shared key

        SABETHA

    1. Remove all non alpha-numeric characters from both the message and the pre-shared key.

    2. Create an encryption key by prefixing the plaintext message with a short pre-shared key:

        S A B E T H A K I L L K E E N F O ...

    3. Locate each character of the key in the tabula recta and replace it with a two-digit number comprised of the
       row coordinate followed by the column coordinate:

        S  A  B  E  T  H  A  K  I  L  L  K  E  E  N  F  O
        18 00 01 04 19 07 00 10 08 11 11 10 04 04 13 05 14 ...

    4. Convert the characters of the plaintext message in the same way:

        K  I  L  L  K  E  E  N  F  O
        10 08 11 11 10 04 04 13 05 14 ...

    5. Sum the value of each character in the plaintext message with the key:

        K  I  L  L  K  E  E  N  F  O
        10 08 11 11 10 04 04 13 05 14
      + 18 00 01 04 19 07 00 10 08 11
        -----------------------------
        28 08 12 15 29 11 04 23 13 25

    Note that tabula recta has multiple entries for each plaintext character; any valid set of coordinates may be used
    to encode a given character, which can be helpful when encoding repeating characters. From the above example, We
    might choose to encode KEEN as follows:

        K  E  E  N
        10 76 04 13


    Decrypting Messages
    -------------------

    To decrypt the message, the recipient constructs the decryption key one character at a time and subtracts the
    values from the encrypted characters:

    1. Generate the start of the decryption key by converting the pre-shared key into numbers using the tabula recta:

        S  A  B  E  T  H  A
        18 00 01 04 19 07 00

    2. Subtract the first number of the key from the first number in the message:

        28
      - 18
        --
        10

    3. This number is appended to the decryption key:

        S  A  B  E  T  H  A  K
        18 00 01 04 19 07 00 10

    4. To decrypt the first character of the message, look up the number from Step 2 in the tabula recta:

        K

    5. Repeat Steps 2-4 until the message has been decrypted, subtracting the next value in the key from the next value
       in the encrypted message:

        28 08 12 15 29 11 04 23 13 25
      - 18 00 01 04 19 07 00 10 08 11
        -----------------------------
        10 08 11 11 10 04 04 13 05 14
        K  I  L  L  K  E  E  N  F  O

    """

    alphabet = 'abcdefghijklmnopqrstuvwxyz0123456789'
    non_alphanum = re.compile('[^A-Za-z0-9]')

    def __init__(self):
        self._table = []
        self._reversed = defaultdict(list)
        self._reversed_index = defaultdict(list)
        self._generate_tabula_recta()

    def _generate_tabula_recta(self):
        """
        Generate the tabula recta as a two-dimensional array, and a reverse lookup table as a dictionary.
        """
        index = 0
        for offset_y in range(0, 10):
            row = ''
            for offset_x in range(0, 10):
                letter = self.alphabet[index]
                row = row + letter
                self._reversed[letter].append(f'{offset_y}{offset_x}')
                index = index + 1
                if index == len(self.alphabet):
                    index = 0
            self._table.append(row)

    @property
    def tabula_recta(self):
        """
        Return a formatted representation of the tabula recta.
        """
        t = self._table.copy()
        for (i, line) in enumerate(t):
            t[i] = f'{i}|{line}'
        t = '\n'.join([' '.join([col for col in row]) for row in t])
        return f'    0 1 2 3 4 5 6 7 8 9\n  +--------------------\n{t}'

    def forward(self, n):
        """
        Perform a forward lookup of a two digit number in the tabula recta and return the corresponding letter.
        """
        n = int(n)
        if n < 10:
            x = 0
            y = n
        else:
            y = n % 10
            x = int((n - y)/10)
        return self._table[x][y]

    def reverse(self, letter):
        """
        Perform a reverse lookup of a letter in the tabula recta and return a two-digit number corresponding to it.
        """
        return int(self._reversed[letter][0])

    def normalize(self, text):
        """
        Normalize a string so that each character can be encrypted using the tabula recta.
        """
        return self.non_alphanum.sub('', text).lower()

    def encrypt(self, psk, message):
        """
        Encrypt a message using the specified pre-shared key (psk). Returns a list of numbers.
        """
        psk = self.normalize(psk)
        plaintext = self.normalize(message)

        key = [self.reverse(x) for x in psk + plaintext]
        encrypted = []
        for i in range(len(plaintext)):
            a = self.reverse(plaintext[i])
            x = int(a) + key[i]
            encrypted.append(x)
        return encrypted

    def pretty_encrypt(self, psk, message, block_length=5, blocks_per_line=3):
        """
        Encrypt a message using the specified pre-shared key (psk). Returns a formatted string consisting of the
        encrypted message split into blocks of 3-digit numbers, 5 numbers to a block, 3 blocks to a line.
        """
        psk = self.normalize(psk)
        encrypted = [f'{x:03d}' for x in self.encrypt(psk, message)]
        blocks = [encrypted[i:i + block_length] for i in range(0, len(encrypted), block_length)]
        return '\n'.join([
            '    '.join([' '.join(inner) for inner in blocks[outer:outer + blocks_per_line]])
            for outer in range(0, len(blocks), blocks_per_line)
        ])

    def decrypt(self, psk, message):
        """
        Decrypte a message using the specified pre-shared key (psk). Returns a list of characters.
        """
        psk = self.normalize(psk)
        plaintext = []

        numbers = [int(x) for x in message.split()]
        key = [self.reverse(x) for x in psk]

        for (i, n) in enumerate(numbers):
            k = key[0]
            a = n - k
            plaintext.append(self.forward(a).upper())
            key = key[1:] + [a]

        return plaintext

    def pretty_decrypt(self, psk, message, block_length=5, blocks_per_line=3):
        """
        Decryptes a message using the specified pre-shared key (psk). Returns a formatted string consisting of the
        plaintext message split into blocks of single characters, 5 characters to a block, 3 blocks to a line.
        """
        plaintext = self.decrypt(psk, message)
        blocks = [plaintext[i:i + block_length] for i in range(0, len(plaintext), block_length)]
        return '\n'.join([
            '    '.join([' '.join(inner) for inner in blocks[outer:outer + blocks_per_line]])
            for outer in range(0, len(blocks), blocks_per_line)
        ])

    def encrypt_file(self, psk, infile):
        with open(infile) as f:
            return self.pretty_encrypt(psk, f.read())

    def decrypt_file(self, psk, infile):
        with open(infile) as f:
            return self.pretty_decrypt(psk, f.read())
