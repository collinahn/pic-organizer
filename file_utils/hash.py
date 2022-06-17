import hashlib

class HashFile:
    '''
    파일의 동일성을 체크하기 위한 값을 계산한다.
    '''
    def __init__(self, path) -> None:
        self._block_size = 65536
        self._file_path = path

        self.value = self._get_hash()

    def _get_hash(self):
        '''파일의 일정 부분을 바이너리로 불러와 비교'''
        with open(self._file_path, 'rb') as f:
            hashd = hashlib.md5()
            buf = f.read(self._block_size)

            while len(buf): # 현재는 전체를 다 본다
                hashd.update(buf)
                buf = f.read(self._block_size)

        return hashd.hexdigest()

if __name__ == '__main__':

    hf = HashFile('123.jpg')
    print(hf.value)

    print(HashFile('123.jpg').value == HashFile('1234.jpg').value)