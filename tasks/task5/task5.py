import os
import hashlib
from typing import Tuple


class MD5Hash:

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

    def md_hash(self) -> Tuple[object, bytes, str]:
        md = hashlib.md5(self.data.encode('UTF-8'))
        return md, md.digest(), md.hexdigest()


def main():
    md = MD5Hash('file_read.txt', 'file_write.txt')

    data = []
    data.append(f'Initial text: {md.data}')
    data.append(f'\nMD5 object: {md.md_hash()[0]}')
    data.append(f'Encoded data in byte forma: {md.md_hash()[1]}')
    data.append(f'Encoded data in hexadecimal format: {md.md_hash()[2]}')

    data = '\n'.join(data)
    md.writing_to_file(data)

    print(data)


if __name__ == '__main__':
    main()
