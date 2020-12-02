import os
import rsa


class AlgorithmRSA:

    def __init__(self, read_filename: str, write_filename: str):
        self.read_filename = read_filename
        self.write_filename = write_filename
        self.data = self.__reading_from_file()
        self.public_key, self.private_key = rsa.key.newkeys(256)

    def __reading_from_file(self) -> str:
        if not os.path.exists(self.read_filename):
            return ''

        with open(self.read_filename) as rf:
            return rf.read()

    def writing_to_file(self, data: str) -> None:
        with open(self.write_filename, 'w+') as wf:
            wf.write(data)

    def rsa_encrypt(self):
        return rsa.encrypt(self.data.encode('UTF-8'), self.public_key)

    def rsa_decrypt(self, data):
        return rsa.decrypt(data, self.private_key)


def main():
    rsa_obj = AlgorithmRSA('file_read.txt', 'file_write.txt')

    data = []
    data.append(f'Data from file: {rsa_obj.data}\n')
    data.append(f'Public RSA key: {rsa_obj.public_key}')
    data.append(f'Private RSA key: {rsa_obj.private_key}\n')

    rsa_data = rsa_obj.rsa_encrypt()
    data.append(f'Data after encryption RSA: {rsa_data}')
    data.append(f'Data after encryption: {rsa_obj.rsa_decrypt(rsa_data)}')

    data = '\n'.join(data)
    rsa_obj.writing_to_file(data)

    print(data)


if __name__ == '__main__':
    main()
