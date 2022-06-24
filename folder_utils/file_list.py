import os
from pprint import pprint

from utils.constants import VALID_EXT
from utils.constants import TEMP_FILE_PREFIX

class FileList:
    def __init__(self, path: str) -> None:
        self.path = path
        self.contents = []

    def lazy_init(self):
        self.walk_path = tuple(os.walk(self.path))
        self.walk_path_filtered = self.filter_forbidden(self.walk_path)
        self.contents = self.only_media(self.walk_path_filtered)
        self.count = len(self.contents)

    @staticmethod
    def filter_forbidden(walk_path) -> tuple:
        return tuple( 
            pack for pack in walk_path 
            if not os.path.basename(pack[0]).startswith(('.', '_')) 
        )

    @staticmethod
    def only_media(walk_path_filtered):
        res = []
        for pack in walk_path_filtered:
            res.extend(
                os.path.join(pack[0], file_name) 
                for file_name in pack[2] 
                if file_name.endswith(VALID_EXT)
                and not file_name.startswith(TEMP_FILE_PREFIX)
            )

        return res
        
if __name__ == '__main__':
    print(*os.walk(os.getcwd()), sep='\n')

    fl = FileList(os.getcwd())
    print(len(fl.walk_path))
    print(fl.walk_path)
    print(len(fl.walk_path_filtered))
    print(fl.walk_path_filtered)
    print(fl.contents)

