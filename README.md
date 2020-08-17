# jbnu-macro

## Usage
#### 1. [Chrome Driver](https://chromedriver.chromium.org/downloads) 다운로드
자신의 Chrome과 동일한 버전을 다운받고 프로젝트 폴더에 넣는다.
#### 2. selenium 설치
```
pip install selenium
```
#### 3. 실행
```
python main.py
```

## Troubleshooting
Windows에서 Chrome Driver가 인식되지 않을 경우 macro.py의 11번째 줄을
```
self.driver = webdriver.Chrome('chromedriver.exe')
```
로 바꿔본다.
