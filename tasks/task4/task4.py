import os
import csv
import itertools
import math
import random

from typing import Tuple
from sympy.ntheory.residue_ntheory import primitive_root


class AlgorithmElGamal:

    def __init__(self, read_filename: str, write_filename: str):
        self.read_filename = read_filename
        self.write_filename = write_filename
        self.data = self.__reading_from_file()

    def __reading_from_file(self) -> str:
        if not os.path.exists(self.read_filename):
            return ''

        with open(self.read_filename) as rf:
            return rf.read()

    def writing_to_file(self, data: str) -> None:
        with open(self.write_filename, 'w+') as wf:
            wf.write(data)

    def get_first_primes(self) -> list:
        primes = []

        with open('numbers.txt') as file:
            reader = csv.reader(
                file,
                delimiter=' ',
                quoting=csv.QUOTE_NONNUMERIC
            )
            for row in reader:
                primes.append([int(e) for e in row if isinstance(e, float)])

        return sum(primes, [])

    def generate_random_prime(self, size: int) -> int:
        p = (random.getrandbits(size) | (1 << size)) | 1
        for i in itertools.count(1):
            if self.is_prime(p):
                return p

            bits = (random.getrandbits(size) | (1 << size) | 1)
            p = bits if i % (size * 2) == 0 else (p + 2)

    def is_prime(self, n: int) -> bool:
        pr = self.is_prime_simple(n, 256)
        return pr if pr is not None else self.is_prime_rabin_miller(n)

    def is_prime_simple(self, number: int, first_primes_number: int) -> bool:
        for p in self.get_first_primes()[:first_primes_number]:
            if number % p == 0:
                return number == p
        return None

    def is_prime_rabin_miller(self, number: int) -> bool:
        rounds = int(math.log2(number))
        t = number - 1
        s = 0

        while t % 2 == 0:
            s += 1
            t //= 2

        generated_numbers = set()

        for _ in range(rounds):
            a = random.randint(2, number - 2)

            while a in generated_numbers:
                a = random.randint(2, number - 2)

            generated_numbers.add(a)
            x = pow(a, t, number)

            if x == 1 or x == number - 1:
                continue

            for _ in range(s - 1):
                x = pow(x, 2, number)
                if x == 1:
                    return False
                elif x == number - 1:
                    break
            else:
                return False
            continue
        return True

    def get_primitive_root(self, modulo: int) -> int:
        return primitive_root(modulo)

    def generate_keys(self, size: int) -> Tuple[Tuple[int, int, int], int]:
        p = self.generate_random_prime(size)
        g = self.get_primitive_root(p)

        while True:
            x = random.randint(1, p - 1)

            if math.gcd(x, p - 1) == 1:
                break

        return (g, p, pow(g, x, p)), x

    def encrypt(self, n: int, key: Tuple[int, int, int]) -> Tuple[int, int]:
        g, p, y = key

        while True:
            k = random.randint(1, p - 1)

            if math.gcd(k, p - 1) == 1:
                break

        return pow(g, k, p), n * pow(y, k, p)

    def decrypt(self, number: int, key: int, p: int) -> int:
        a, b = number
        x = key
        return b * pow(pow(a, x, p), p - 2, p) % p

    def encrypt_text(self, key: Tuple[int, int, int]) -> list:
        return [self.encrypt(ord(a), key) for a in self.data]

    def decrypt_text(self, msg: list, key: int, p: int) -> str:
        return ''.join(chr(a) for a in [self.decrypt(a, key, p) for a in msg])


def main():
    gamal_obj = AlgorithmElGamal('file_read.txt', 'file_write.txt')

    data = []

    public_key, private_key = gamal_obj.generate_keys(128)

    data.append(f'Public key: {public_key}\nPrivate key: {private_key}')
    data.append(f'\nInitial text: {gamal_obj.data}')

    encrypted = gamal_obj.encrypt_text(public_key)
    decrypted = gamal_obj.decrypt_text(encrypted, private_key, public_key[1])

    data.append(f'\nEncrypted array: {encrypted}')
    data.append(f'\nDecrypted text: {decrypted}')

    data = '\n'.join(data)
    gamal_obj.writing_to_file(data)

    print(data)


if __name__ == '__main__':
    main()
