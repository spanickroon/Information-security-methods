class EncryptionIntegrityControlAlgorithms:

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


def main():
    algo_obj = EncryptionIntegrityControlAlgorithms(
        'file_read.txt',
        'file_write.txt'
        )


if __name__ == '__main__':
    pass
