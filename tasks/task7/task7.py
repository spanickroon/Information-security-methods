import os
from ecdsa import SigningKey
from ecdsa import BadSignatureError
from typing import Tuple


class EllipticCurves:

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

    def signature_creation(self) -> Tuple[object, object, bytes]:
        sk = SigningKey.generate()
        vk = sk.verifying_key
        signature = sk.sign(self.data.encode('UTF-8'))

        return sk, vk, signature

    def signature_verification(
            self,  sk: object, vk: object, signature: bytes, msg: str) -> bool:
        try:
            return vk.verify(signature, msg.encode('UTF-8'))
        except BadSignatureError:
            return False


def main():
    ec = EllipticCurves('file_read.txt', 'file_write.txt')

    data = []
    data.append(f'Initial text: {ec.data}')

    sk, vk, signature = ec.signature_creation()
    data.append(f'\nSigningKey: {sk}')
    data.append(f'VerifyingKey: {vk}')
    data.append(f'Signature: {signature}')

    msg = 'Hello'
    checker = ec.signature_verification(sk, vk, signature, msg)
    data.append(f'\nVerify signature with text "{msg}": {checker}')

    msg = ec.data
    checker = ec.signature_verification(sk, vk, signature, msg)
    data.append(f'Verify signature with text "{msg}": {checker}')

    data = '\n'.join(data)
    ec.writing_to_file(data)

    print(data)


if __name__ == '__main__':
    main()
