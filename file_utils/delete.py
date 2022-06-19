import os 
import send2trash
import abc

class DeleteFile(metaclass=abc.ABCMeta):
    '''
    하나를 제외하고 나머지를 휴지통으로 보낸다.
    '''
    def __init__(self, overlap_list, valid_flag) -> None:
        self.files2handle = overlap_list
        self.delete_flag = valid_flag
    
    def run(self):
        for idx, overlaps in enumerate(self.files2handle):
            if self.delete_flag[idx]:
                print(f'deleting {overlaps[1:]}')
                self._delete(list(overlaps[1:]))
                continue
            print('not deleting due to user choices')

    @abc.abstractmethod
    def _delete(self, file_list: list):
        ...

class DeleteFileWindows(DeleteFile):
    def _delete(self, file_list: list):
        for file in file_list:
            try:
                os.remove(file)
            except Exception as e:
                print(f'{e} / an error occurred while deleting {file}')

class DeleteFileMac(DeleteFile):
    def _delete(self, file_list: list):
        for file in file_list:
            try:
                send2trash.send2trash(file)
            except Exception as e:
                print(f'{e} / an error occurred while sending {file} to trash')

class DeleteFileStrategy:
    def __init__(self, *args, **kwargs) -> None:
        self.delete = DeleteFileWindows(*args, **kwargs) if os.name == 'nt' else DeleteFileMac(*args, **kwargs)