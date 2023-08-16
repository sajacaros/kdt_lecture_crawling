# kdt_lecture_crawling
## 프로젝트 최상위 폴더에 'config.ini' 파일을 만들고 아래 규격에 맞혀서 설정값 입력
```
[chrome-driver]
path=C:\tools\Webdriver\chromedriver-win64\chromedriver.exe

[auth]
id=kdt_id
passwd=kdt_passwd
```

## 크롬 driver 다운로드
* 셀레니움 크롬 드라이버가 최신 버전의 크롬을 자동으로 지원하지 않음 
* 크롬 드라이버를 수동으로 다운로드
  * [최신 크롬 드라이버 다운로드](https://googlechromelabs.github.io/chrome-for-testing/)
* 향후 크롬 드라이버 지원시 자동 다운로드를 통해 실행 가능

## 설치
``` 
pip install bs4 # 4.12.2
pip install selenium # 4.11.2
pip install openpyxl # 3.1.2
```

## 실행 방법
``` 
python kdt.py
```