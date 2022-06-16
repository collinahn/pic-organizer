import os
from pprint import pprint

from utils.constants import VALID_EXT

class FileList:
    def __init__(self, path: str) -> None:
        self.walk_path = tuple(os.walk(path))
        # pprint(f'{self.walk_path = }')
        self.walk_path_filtered = self.filter_forbidden()
        self.contents = self.only_media()
        self.count = len(self.contents)

    def filter_forbidden(self) -> tuple:
        return tuple( 
            pack for pack in self.walk_path 
            if not os.path.basename(pack[0]).startswith(('.', '_')) 
        )

    def only_media(self):
        res = []
        for pack in self.walk_path_filtered:
            res.extend(os.path.join(pack[0], file_name) for file_name in pack[2] if file_name.endswith(VALID_EXT))

        return res
        
if __name__ == '__main__':
    print(*os.walk(os.getcwd()), sep='\n')

    fl = FileList(os.getcwd())
    print(len(fl.walk_path))
    print(fl.walk_path)
    print(len(fl.walk_path_filtered))
    print(fl.walk_path_filtered)
    print(fl.contents)

    from PIL import Image
    img = Image.open(fl.contents[1])
