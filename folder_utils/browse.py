# 파일/폴더를 오픈해주는 클래스
import os
import webbrowser

class Browser(object):
    @classmethod
    def open_file(cls, *, file_name):
        '''
        파일을 연다
        '''
        return bool(webbrowser.open(f'file://{file_name}'))
    
    @classmethod
    def open_folder(cls, *, path):
        '''
        폴더를 연다
        '''
        target = path
        if os.path.isfile(path):
            target = os.path.dirname(path)
        
        return bool(webbrowser.open(f'file://{target}'))
