# 나홀로메모장
## 1. alonememo 폴더 안에 가상환경 만들기
파워쉘에서 alonememo로 이동  

py -3 -m venv .venv
- 만들어졋나 VSCODE에서 보임

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
- 윈도우는 이거 해야 가상환경 활성화 가능

.venv\Scripts\activate
- 활성화

VSCODE에서 좌측하단 클릭해 인터프리터 바꾸기  

```
pip list
pip install requests
pip install beautifulsoup4
pip install pymongo
pip install flask

```

## 2. static, templates 폴더, app.py 파일 만들기
## 3. 요구사항 보기
### 3.1 요구사항
> 완성작을 보면서 어떤 기능이 필요한지 생각해봅시다! [링크](http://spartacodingclub.shop/)  

1. 페이지가 로딩되고 나면 DB에 저장되어 있는 기사 정보를 받아와 카드로 만들어 붙여준다.
    - 페이지 로딩 후 함수가 실행되게 한다.
    - 서버로 추가 정보 없이 GET 요청을 보낸다.
    - 서버는 DB에서 모든 기사의 제목, 설명, URL, 이미지URL, 코멘트 받아와 넘겨준다.
    - 받아온 정보로 각 기사에 대하여 카드를 만들어 붙인다.
2. 포스팅 버튼을 누르면 입력한 url과 코멘트를 받아 DB에 제목, 설명, 이미지 URL까지 다 저장하고 페이지 새로고침한다. → 페이지 새로 로딩되면서 추가된 카드까지 나온다.
    - 포스팅 버튼을 눌러 함수가 실행되게 한다.
    - url과 코멘트를 잘 입력했는지 확인한다.
    - 입력 받은 url과 코멘트를 서버로 POST 요청을 보내준다.
    - 서버에서 url과 코멘트를 받아 제목, 설명 이미지 URL을 크롤링한다.
    - 5개 정보를 DB에 도큐먼트로 저장한다.
    - 성공 메시지를 반환하면 페이지를 새로고침한다.

## 4. 프로젝트 설계
- 메모 저장
- 전체 메모 목록

### 4.1 포스팅API: Create. 카드생성. (기사 저장)
1. 요청 정보
    - 요청 URL = `/memo`, 요청 방식 = `POST`
        - 조회 이외에는 전부 POST
    - 요청 데이터 : 사용자가 메모 작성해서 서버에 날리는거
        - URL(url_give), 코멘트(comment_give)
2. 서버가 제공할 기능
    - URL의 meta태그 정보를 바탕으로 제목, 설명, 이미지URL 스크래핑
    - (제목, 설명, URL, 이미지URL, 코멘트) 정보를 모두 DB에 저장
3. 응답 데이터
    - API가 정상적으로 작동하는지 클라이언트에게 알려주기 위해서 성공메시지 보내기
    - (JSON 형식) 'result'='success'


### 4.2 리스팅API: Read. 저장된 카드 보여주기. (전체 카드 목록)
1. 요청 정보
    - 요청 URL = `/memo`, 요청 방식 = `GET`
        - 당연히 조회니까 GET
    - 요청 데이터 : 없음
2. 서버가 제공할 기능
    - DB에 저장돼 있는 모든 (제목, 설명, URL, 이미지URL, 코멘트) 정보를 가져오기
3. 응답 데이터
    - API 동작 잘했다는 성공 메시지, 아티클(기사)들의 정보(제목, 설명, URL, 이미지URL, 코멘트)
    - (JSON 형식) 'result'='success', 'article': 아티클 정보

## 5. 프로젝트 준비
### 5.1 URL로부터 페이지 정보 받아오는 기능 구현
사용자가 URL과 코멘트만 줬을뿐인데.