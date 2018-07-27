import string
import re
import random
from unidecode import unidecode

class PolybiusSquare:
    def __init__(self, width=0, height=0, cipher=None, ij=True):
        if not ((width and height) or cipher):
            raise ValueError('Either choose the size of the square (width/height) or the encrypted cypher.')

        if cipher:
            cipher = cipher.lower()
            match = re.search(r'(\d+)x(\d+)#(?:\d+-\d+;?)+', cipher)
            if not match:
                raise ValueError('Can\'t find square size within the cipher, please specify with width and height parameters')

        self.width = width if width else int(match.group(1))
        self.height = height if height else int(match.group(2))

        self.abc = string.ascii_uppercase
        self.abc = self.abc.replace('J', '') if ij else self.abc

        if width * height < len(self.abc):
            raise ValueError('This square is not large enough to comprehend the whole alphabet.\nPlease increase width or height.')

        self.mount_square()

        if cipher:
            print(self.decrypt(match.group(0)))

    def mount_square(self):
        self.square_area = self.width * self.height
        self.abc_square = (self.abc * (self.square_area // len(self.abc) + 1))[:self.square_area]
        self.square = [self.abc_square[i:i+self.width] for i in range(0, len(self.abc_square), self.width)]

        self.abc_to_pos = {letter:[] for letter in self.abc}
        for line_index, line in enumerate(self.square):
            for col_index, letter in enumerate(line):
                self.abc_to_pos[letter].append('{}-{}'.format(col_index + 1, line_index + 1))
        
        self.pos_to_abc = {}
        for letter in self.abc:
            for pos in self.abc_to_pos[letter]:
                self.pos_to_abc[pos] = letter
        self.pos_to_abc['0-0'] = '�'

    def encrypt(self, text):
        text = unidecode(text).upper()
        text = text.replace('J', 'I') if len(self.abc) == 25 else text
        cipher = '{}x{}#'.format(self.width, self.height)
        positions = [random.choice(self.abc_to_pos.get(letter, ['0-0'])) for letter in text]
        cipher += ';'.join(positions)
        return cipher

    def decrypt(self, cipher):
        cipher = cipher.lower()
        match = re.search(r'(?:\d+x\d+#)?((?:\d+-\d+;?)+)', cipher)
        if match:
            positions = match.group(1).split(';')
            text = ''.join([self.pos_to_abc.get(pos, '0-0') for pos in positions])
            return text
        else:
            raise ValueError('Cipher doesn\'t match the Polybius Square pattern.')

class Atbash:
    def __init__(self, abc=string.ascii_uppercase):
        self.abc = abc
        self.cba = abc[::-1]
        self.convertion_dict = dict(zip(self.abc, self.cba))

    def encrypt(self, text, decode_unicode=True):
        text = unidecode(text).upper() if decode_unicode else text.upper()
        cipher = ''.join([self.convertion_dict.get(character, character) for character in text])
        return cipher

    decrypt = encrypt

class Caesar:
    def __init__(self, abc=string.ascii_uppercase, key=1):
        self.abc = abc
        self.max_value = len(abc) - 1
        self.key = abs(key)
        self.caesar_dict = dict(enumerate(abc, 1))

    def encrypt(self, text, decode_unicode=True, key=0):
        key = key if key else self.key
        text = unidecode(text).upper() if decode_unicode else text.upper()
        cipher = ''
        for letter in text:
            if letter in self.abc:
                letter_index = self.abc.index(letter) + key
                if letter_index > self.max_value:
                    letter_index = letter_index - self.max_value - 1
                if letter_index < 0:
                    letter_index = letter_index + self.max_value + 1

                cipher += self.abc[letter_index]
            else:
                cipher += letter
        return cipher

    def decrypt(self, cipher, decode_unicode=True, key=0):
        key = key if key else self.key
        text = self.encrypt(cipher, decode_unicode, -key)
        return text

    def brute_force(self, cipher, decode_unicode=True):
        for try_number in range(1, self.max_value + 1):
            text = self.encrypt(cipher, decode_unicode, try_number)
            print(text)

ROT13 = Caesar(key=13)

class Morse:
    def __init__(self, word_splitter='/'):
        self.word_splitter = word_splitter
        self.char_to_morse = {
        ' ': word_splitter,
        'A': '.-',
        'B': '-...',
        'C': '-.-.',
        'D': '-..',
        'E': '.',
        'F': '..-.',
        'G': '--.',
        'H': '....',
        'I': '..',
        'J': '.---',
        'K': '-.-',
        'L': '.-..',
        'M': '--',
        'N': '-.',
        'O': '---',
        'P': '.--.',
        'Q': '--.-',
        'R': '.-.',
        'S': '...',
        'T': '-',
        'U': '..-',
        'V': '...-',
        'W': '.--',
        'X': '-..-',
        'Y': '-.--',
        'Z': '--..',
        '0': '-----',
        '1': '.----',
        '2': '..---',
        '3': '...--',
        '4': '....-',
        '5': '.....',
        '6': '-....',
        '7': '--...',
        '8': '---..',
        '9': '----.',
        '.': '.-.-.-',
        ',': '--..--',
        '?': '..--..',
        '\'': '.----.',
        '!': '-.-.--',
        '/': '-..-.',
        '(': '-.--.',
        ')': '-.--.-',
        '&': '.-...',
        ':': '---...',
        ';': '-.-.-.',
        '=': '-...-',
        '+': '.-.-.',
        '-': '-....-',
        '_': '..--.-',
        '"': '.-..-.',
        '$': '...-..-',
        '@': '.--.-.',
        }

        self.morse_to_char = {v:k for k, v in self.char_to_morse.items()}
 
    def encrypt(self, text):
        text = unidecode(text).upper()
        cipher = ' '.join([self.char_to_morse.get(character, character) for character in text]).strip()
        return cipher

    def decrypt(self, cipher):
        text = ''
        for word in cipher.split(self.word_splitter):
            text += ''.join([self.morse_to_char.get(character, '�') for character in word.split()])
            text += ' '
        return text.strip()