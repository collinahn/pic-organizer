from PyQt6.QtCore import pyqtSignal

from utils.properties import FileProperty
from folder_utils.file_list import FileList


class CompareFile:
    '''
    1차적으로 크기 비교, 크기가 같다면 해시값을 비교한다.
    '''
    def __init__(self, file_obj) -> None:
        self.file_obj: FileList = file_obj

    def lazy_init(self, progress_hint: pyqtSignal, progress_int: pyqtSignal):
        self.progress_hint = progress_hint
        self.progress_int = progress_int
        
        self.file_list = self.file_obj.contents # 이 시점에 초기화가 완료된다
        self.file_dict: dict[str,FileProperty] = self._touch_file()

        cmp_size = self._compare_size()
        cmp_hash = self._compare_hash(cmp_size)
        self.result: list[tuple[str]] = cmp_hash

    def _touch_file(self):
        self.progress_hint.emit('파일 검색 중(1/3)')
        res: dict[str,FileProperty] = {}

        for idx, file_path in enumerate(self.file_list):
            res[file_path] = FileProperty(file_path)
            
            complete_rate = int((idx+1)/len(self.file_list)*100)
            self.progress_int.emit(complete_rate)

        return res

    def _compare_size(self):
        self.progress_hint.emit('파일 크기 비교 중(2/3)')
        cmp_size: dict[int,list] = {} 
        for idx, (file_path, file_prop) in enumerate(self.file_dict.items()):
            if file_prop.size in cmp_size:
                cmp_size.get(file_prop.size).append(file_path)
                continue
            
            cmp_size[file_prop.size] = [file_path, ]
            complete_rate = int((idx+1)/len(self.file_dict)*100)
            self.progress_int.emit(complete_rate)

        return cmp_size
            
    def _compare_hash(self, size_res: dict):
        self.progress_hint.emit('파일 해시값 비교 중(3/3)')
        identical_file_list: list[tuple[str]] = []
        for idx, (size, file_list) in enumerate(size_res.items()):
            if len(file_list) == 1: continue

            try:
                self._load_hash_value(file_list)
            except OSError:
                self.progress_hint.emit('네트워크 폴더는 미리 동기화를 진행해주세요.')
                continue

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
            complete_rate = int((idx+1)/len(size_res)*100)
            self.progress_int.emit(complete_rate)
                        
        return identical_file_list

    def _load_hash_value(self, file_list):
        for file_dir in file_list:
            try:
                self.file_dict[file_dir].init_hash()
            except AttributeError:
                continue