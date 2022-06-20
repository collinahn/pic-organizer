import os

from file_utils.hash import HashFile

class MultiGlobalMeta(type):
    _instances = {}
    def __call__(self, file_path: str, *args, **kwargs):
        if file_path not in self._instances:
            self._instances[file_path] = super().__call__(file_path, *args, **kwargs)
        return self._instances[file_path]



class FileProperty(metaclass=MultiGlobalMeta):
    def __init__(self, file_path) -> None:
        self.file_path = file_path
        self.name = os.path.basename(file_path)
        self.size = os.path.getsize(self.file_path)
        self.hash = 0

        print(f'{file_path} FileProperty object initiated')

    def init_hash(self):
        '''나중에 비교하기 위함'''
        hf = HashFile(path=self.file_path)
        self.hash = hf.value

if __name__ == '__main__':

    props2 = FileProperty('02')
    props1 = FileProperty('01')
    props01 = FileProperty('01')
    print(props2 == props1)
    print(props01 == props1)

    