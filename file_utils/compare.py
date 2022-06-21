import time

from utils.properties import FileProperty


class CompareFile:
    '''
    1차적으로 크기 비교, 크기가 같다면 해시값을 비교한다.
    '''
    def __init__(self, file_list) -> None:
        self.file_list: list[str] = file_list

        self.count = len(file_list)
        self.repeat = 2.5
        self.status = 0

    def lazy_init(self):
        self.file_dict: dict[str,FileProperty] = self._touch_file()

        cmp_size = self._compare_size()
        cmp_hash = self._compare_hash(cmp_size)
        self.result: list[tuple[str]] = cmp_hash

    def _touch_file(self):
        res: dict[str,FileProperty] = {}

        for file_path in self.file_list:
            res[file_path] = FileProperty(file_path)
            self.status += 1 # 현황 기록용

        return res

    def _compare_size(self):
        cmp_size: dict[int,list] = {} 
        for file_path, file_prop in self.file_dict.items():
            if file_prop.size in cmp_size:
                cmp_size.get(file_prop.size).append(file_path)
                continue
            
            cmp_size[file_prop.size] = [file_path, ]
            self.status += 1 

        return cmp_size
            
    def _compare_hash(self, size_res: dict):
        identical_file_list: list[tuple[str]] = []
        for size, file_list in size_res.items():
            if len(file_list) == 1: continue
            self._load_hash_value(file_list)

            # 해시값이 같은 파일들 분류
            hash_dict: dict[int,list] = {}
            for file_dir in file_list:
                hash_value = self.file_dict[file_dir].hash
                if hash_value in hash_dict:
                    hash_dict[hash_value].append(file_dir)
                    continue

                hash_dict[hash_value] = [file_dir, ]

            # 분류된 것 확인 후 하나 이상이면 리스트 추가
            identical_file_list.extend(
                tuple(sorted_file_list) 
                for sorted_file_list in hash_dict.values() 
                if len(sorted_file_list) > 1
            )
            self.status += 1
                        
        return identical_file_list

    def _load_hash_value(self, file_list):
        for file_dir in file_list:
            try:
                self.file_dict[file_dir].init_hash()
            except AttributeError:
                continue