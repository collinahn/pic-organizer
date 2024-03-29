import os
import re
import webbrowser


class Browser(object):
    @classmethod
    def open_file(cls, *, file_name):
        '''
        opens file.
        then returns exit code.
        '''
        return bool(webbrowser.open(f'file://{file_name}'))

    @classmethod
    def open_folder(cls, *, path):
        '''
        opens folder.
        then returns exit code.
        '''
        target = path
        if os.path.isfile(path):
            target = os.path.dirname(path)

        return bool(webbrowser.open(f'file://{target}'))

    @staticmethod
    def korean_included_for_mac(dir):
        cnt = len(re.findall(u'[\u3130-\u318F\uAC00-\uD7A3]+', dir))
        return cnt > 0
