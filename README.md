# 사진 중복 정리 앱 Thanos

### Description
* 파일 중복을 찾아 중복된 파일을 하나 남기고 모두 삭제한다.
* 먼저 크기가 같은 파일들을 하위 폴더들을 모두 포함하여 탐색한 뒤 크기가 같으면 파일의 일부를 읽어들여 해쉬값을 비교한다.
* 파일의 크기와 해쉬값이 같으면 같은 파일로 인식함.
* 폴더 명이 "\_" 혹은 "."으로 시작하거나 파일명이 "._"(썸네일 파일)으로 시작한다면 탐색하지 않는다.

### Usage
* 첫 실행 화면\
![image](https://user-images.githubusercontent.com/87699755/175552995-9641d8fc-22a1-4287-a2c2-ccc8ca86efb5.png)

* 폴더를 선택하고 분석하기를 누른다\
![image](https://user-images.githubusercontent.com/87699755/175554294-537e80f6-9e32-48aa-8edf-dd1eeb7e3588.png)![image](https://user-images.githubusercontent.com/87699755/175556261-5e74ca4c-984e-4b60-b086-7234416730c8.png)

* 탐색을 다 하면 목록 보기 버튼이 활성화되는데, \
그 버튼을 눌러서 열리는 창으로 사진을 확인할 수 있고, 제외할 사진을 선택할 수 있다. \
![image](https://user-images.githubusercontent.com/87699755/175554954-91cd7964-e977-4c6b-a414-248f7586c403.png)

* 하단의 정리하기 버튼을 눌러서 선택한 사진을 정리한다. \
목록을 확인하지 않아도 중복된 사진들은 전부 정리된다. \
![image](https://user-images.githubusercontent.com/87699755/175555771-71d27c24-80f5-40cb-bac1-0339c8c9b8c5.png)![image](https://user-images.githubusercontent.com/87699755/175556576-5bae0172-713b-43af-bbeb-d3f7cd13521e.png)


### Environment
* Windows 11 
* macOS 12.4

### Prerequisite
* python==3.10.4
* altgraph==0.17.2
* macholib==1.16
* pyinstaller==5.1
* pyinstaller-hooks-contrib==2022.7
* PyQt6==6.3.0
* PyQt6-Qt6==6.3.0
* PyQt6-sip==13.3.1
* Send2Trash==1.8.0 (macOS)

### Files
* strategy패턴을 통해 os마다 다른 삭제 방식을 결정한다. (file_utils/delete.py)
```python
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
```

### Build

* Windows 빌드(pyinstaller)
```
pyinstaller --onefile --noconsole --icon=./icons/thanos.ico --add-data "icons/thanos.ico;./icons" --add-data "icons/thanos.png;./icons" --add-data "icons/guntlet.png;./icons" --add-data "icons/mind_stone.png;./icons" --add-data "icons/power_stone.png;./icons" --add-data "icons/reality_stone.png;./icons" --add-data "icons/space_stone.png;./icons" --add-data "icons/time_stone.png;./icons" -n Thanos app.py
```

* macOS 빌드(pyinstaller + create-dmg)
```
pyinstaller --windowed --noconfirm --hiddenimport=PyQt6.sip --icon=./icons/thanos.ico --add-data "icons/thanos.ico:./icons" --add-data "icons/thanos.png:./icons" --add-data "icons/guntlet.png:./icons" --add-data "icons/mind_stone.png:./icons" --add-data "icons/power_stone.png:./icons" --add-data "icons/reality_stone.png:./icons" --add-data "icons/space_stone.png:./icons" --add-data "icons/time_stone.png:./icons" -n Thanos app.py 

./builddmg.sh
```
요구사항: Apple Silicon Mac에서는 rosetta2로 연 터미널에서 가상환경을 생성하고 가상환경에서 빌드한다.
