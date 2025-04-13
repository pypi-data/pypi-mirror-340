import struct

class bmp:
    def __init__(self, file_name):
        try:
            self._File = open(file_name, "rb")
            self._FileName = file_name
        except FileNotFoundError:
            raise FileNotFoundError(f"{file_name} not found")

        self._Info = self.readInfo()
        self._Image = self.readImage()

    def readInfo(self):
        '''
        Read the BMP file and DIB header, supporting variable DIB header sizes.
        '''
        self._File.seek(0)

        file_header = self._File.read(14)
        bfType, bfSize, bfReserved1, bfReserved2, bfOffBits = struct.unpack('<2sIHHI', file_header)

        if bfType != b'BM':
            raise ValueError("Not a valid BMP file")

        dib_header_start = self._File.read(4)
        biSize = struct.unpack('<I', dib_header_start)[0]

        remaining_dib = self._File.read(biSize - 4)
        full_dib_header = dib_header_start + remaining_dib

        info = {
            "bfType": bfType.decode(),
            "bfSize": bfSize,
            "bfReserved1": bfReserved1,
            "bfReserved2": bfReserved2,
            "bfOffBits": bfOffBits,
            "biSize": biSize,
            "biWidth": None,
            "biHeight": None,
            "biPlanes": None,
            "biBitCount": None,
            "biCompression": None,
            "biSizeImage": None,
        }

        if biSize >= 12:

            if biSize == 12:
                biWidth, biHeight, biPlanes, biBitCount = struct.unpack('<HHHH', remaining_dib[:8])
                info.update({
                    "biWidth": biWidth,
                    "biHeight": biHeight,
                    "biPlanes": biPlanes,
                    "biBitCount": biBitCount,
                    "biCompression": 0,
                    "biSizeImage": 0,
                })
            elif biSize >= 40:

                biWidth, biHeight, biPlanes, biBitCount, biCompression, biSizeImage = struct.unpack('<iiHHII', remaining_dib[:20])
                info.update({
                    "biWidth": biWidth,
                    "biHeight": biHeight,
                    "biPlanes": biPlanes,
                    "biBitCount": biBitCount,
                    "biCompression": biCompression,
                    "biSizeImage": biSizeImage
                })

        return info

    def readImage(self):
        '''
        Reads pixel data from the BMP file.
        '''
        offset = self._Info['bfOffBits']
        width = self._Info['biWidth']
        height = self._Info['biHeight']
        bit_count = self._Info['biBitCount']
        compression = self._Info['biCompression']

        if bit_count != 24 or compression != 0:
            raise NotImplementedError("Only uncompressed 24-bit BMP is supported.")

        row_size = (width * 3 + 3) & ~3  
        image = []

        self._File.seek(offset)

        for y in range(abs(height)):
            row_data = self._File.read(row_size)
            row = []
            for x in range(width):
                b, g, r = struct.unpack_from('BBB', row_data, x * 3)
                row.append((r, g, b))
            
            if height > 0:
                image.insert(0, row)
            else:
                image.append(row)

        return image

    def showInfo(self):
        '''
        Nicely formatted print of all header info stored in self._Info.
        '''
        if not self._Info:
            print("No header info available.")
            return

        print("=" * 40)
        print(f"{'BMP FILE INFO':^40}")
        print("=" * 40)

        max_key_len = max(len(key) for key in self._Info.keys())

        for key, value in self._Info.items():
            if isinstance(value, int):
                print(f"{key:<{max_key_len}} : {value:,}")
            else:
                print(f"{key:<{max_key_len}} : {value}")

        print("=" * 40)

    def __del__(self):
        if hasattr(self, '_File') and self._File:
            self._File.close()


def showInfo(file_name):
    bmp(file_name).showInfo()
