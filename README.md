# jbnu-macro

## Usage
#### 1. [Chrome Driver](https://chromedriver.chromium.org/downloads) 다운로드
자신의 Chrome과 동일한 버전을 다운받고 프로젝트 경로에 넣는다.  
[Chrome 버전 확인 방법](https://support.google.com/chrome/answer/95414?hl=ko&co=GENIE.Platform%3DDesktop)
#### 2. 라이브러리 설치
```
cd [프로젝트 경로]
pip install -r requirements.txt
```
#### 3. 실행
```
# 전공 신청
python main.py -n [학번] -p [비밀번호] -g [학년] -i [과목 인덱스 (맨 위에서 0부터 시작)] -m 0

# 장바구니 신청
python main.py -n [학번] -p [비밀번호] -i [과목 인덱스 (맨 위에서 0부터 시작)] -m 1
```

## Troubleshooting
Windows에서 Chrome Driver가 인식되지 않을 경우 macro.py의 11번째 줄을
```
self.__driver = webdriver.Chrome('chromedriver.exe')
```
로 바꿔본다.
