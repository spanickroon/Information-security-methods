import os
import pyDes

from typing import Tuple


class EncryptionDes:

    def __init__(self, read_filename: str, write_filename: str, iv: str):
        self.read_filename = read_filename
        self.write_filename = write_filename
        self.data = self.__reading_from_file()
        self.IV = iv.encode('UTF-8')

    def __reading_from_file(self) -> str:
        if not os.path.exists(self.read_filename):
            return ''

        with open(self.read_filename) as rf:
            return rf.read()

    def writing_to_file(self, data: str) -> None:
        with open(self.write_filename, 'w+') as wf:
            wf.write(data)

    def des(self) -> Tuple[object, bytes]:
        KEY = b'CRYPTOSE'

        des = pyDes.des(KEY, pyDes.CBC, self.IV, None, pyDes.PAD_PKCS5)
        return (des, des.encrypt(self.data))

    def double_des(self) -> Tuple[object, bytes]:
        KEY = b'DOUBLESECRYPTOSE'

        des = pyDes.triple_des(KEY, pyDes.ECB, self.IV, None, pyDes.PAD_PKCS5)
        return (des, des.encrypt(self.data))

    def triple_des(self) -> Tuple[object, bytes]:
        KEY = b'LMXXRPADALMNCHCAUXLPLSCS'

        des = pyDes.triple_des(KEY, pyDes.CBC, self.IV, None, pyDes.PAD_PKCS5)
        return (des, des.encrypt(self.data))

    def decrypt(self, des: object, encrypt_data: bytes) -> str:
        return des.decrypt(encrypt_data).decode()


def main():
    des_obj = EncryptionDes('file_read.txt', 'file_write.txt', 'BTCXRPVV')

    data = []
    data.append(f'Data from file: {des_obj.data}\n')
    data.append(f'Data after encryption des: {des_obj.des()[1]}')
    data.append(f'Data after encryption double des: {des_obj.double_des()[1]}')
    data.append(f'Data after encryption triple des: {des_obj.triple_des()[1]}')
    data.append(f'Encryption initial value bytes: {des_obj.IV}')
    data.append(f'Data after encryption: {des_obj.decrypt(*des_obj.des())}')

    data = '\n'.join(data)
    des_obj.writing_to_file(data)

    print(data)


if __name__ == '__main__':
    main()
