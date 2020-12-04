import os

from PIL import Image, ImageDraw
from random import randint
from re import findall


class Steganography:

    def __init__(
            self,
            read_filename: str, write_filename: str,
            image_filename: str, newimage_filename: str, keys_filename: str):
        self.read_filename = read_filename
        self.write_filename = write_filename
        self.image_filename = image_filename
        self.newimage_filename = newimage_filename
        self.keys_filename = keys_filename
        self.data = self.__reading_from_file()

    def __reading_from_file(self) -> str:
        if not os.path.exists(self.read_filename):
            return ''

        with open(self.read_filename) as rf:
            return rf.read()

    def writing_to_file(self, data: str) -> None:
        with open(self.write_filename, 'w+') as wf:
            wf.write(data)

    def steganography_encrypt(self) -> None:
        keys = []
        img = Image.open(self.image_filename)
        draw = ImageDraw.Draw(img)
        width, height = img.size
        pix = img.load()

        with open(self.keys_filename, 'w+') as keys_file:
            for elem in ([ord(elem) for elem in self.data]):
                key = (randint(1, width-10), randint(1, height-10))
                g, b = pix[key][1: 3]
                draw.point(key, (elem, g, b))
                keys_file.write(str(key)+'\n')
            img.save(self.newimage_filename, 'PNG')

    def steganography_decrypt(self) -> str:
        answer = []
        keys = []
        img = Image.open(self.newimage_filename)
        pix = img.load()
        with open(self.keys_filename) as f:
            y = str([line.strip() for line in f])

            for i in range(len(findall(r'\((\d+)\,', y))):
                keys.append(
                    (
                        int(findall(r'\((\d+)\,', y)[i]),
                        int(findall(r'\,\s(\d+)\)', y)[i])
                    ))
            for key in keys:
                answer.append(pix[tuple(key)][0])
        return ''.join([chr(elem) for elem in answer])


def main():
    steg = Steganography(
        'file_read.txt', 'file_write.txt',
        'cyberpunk.jpg', 'newimage.png', 'keys.txt')

    data = []
    data.append(f'Initial text: {steg.data}')
    steg.steganography_encrypt()
    data.append(f'Text from picture: {steg.steganography_decrypt()}')

    data = '\n'.join(data)
    steg.writing_to_file(data)

    print(data)


if __name__ == '__main__':
    main()
