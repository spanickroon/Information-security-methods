import os

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from typing import Tuple


class ElectronicSignature:

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

    def signature_creation(self) -> Tuple[object, bytes]:
        key = RSA.generate(1024, os.urandom)
        hash_signature = SHA256.new()

        with open(self.read_filename, 'rb') as rf:
            for chunk in iter(lambda: rf.read(4096), b''):
                hash_signature.update(chunk)

        signature = pkcs1_15.new(key).sign(hash_signature)
        pubkey = key.publickey()
        pkcs1_15.new(pubkey).verify(hash_signature, signature)

        return pubkey, signature

    def signature_verification(
            self, pubkey: object, signature: bytes, msg: str) -> bool:
        try:
            pkcs1_15.new(pubkey).verify(
                SHA256.new(msg.encode('UTF-8')),
                signature
            )
        except ValueError:
            return False

        return True


def main():
    es = ElectronicSignature('file_read.txt', 'file_write.txt')

    data = []
    data.append(f'Initial text: {es.data}')

    pubkey, signature = es.signature_creation()
    data.append(f'\nPublic key: {pubkey}')
    data.append(f'Signature: {signature}')

    msg = 'Hello'
    checker = es.signature_verification(pubkey, signature, msg)
    data.append(f'\nVerify signature with text "{msg}": {checker}')

    msg = es.data
    checker = es.signature_verification(pubkey, signature, msg)
    data.append(f'Verify signature with text "{msg}": {checker}')

    data = '\n'.join(data)
    es.writing_to_file(data)

    print(data)


if __name__ == '__main__':
    main()
