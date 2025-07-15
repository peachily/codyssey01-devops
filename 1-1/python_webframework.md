# Python의 웹 프레임워크

## 🍑 웹 프레임워크

- <span style="color: #F6A19A">**정의**</span>: 웹 애플리케이션을 쉽게 만들 수 있도록 기본 구조<span style="color: #CDBBA7">(라우팅, 요청 처리, 응답 등)</span>를 미리 제공하는 도구

- <span style="color: #F6A19A">**기능**</span>
  - 클라이언트 요청 처리 <span style="color: #CDBBA7">(ex. <span style="background-color: #F0EBE3">`/login`</span> 주소로 접속 시 로그인 처리)</span>
  - HTML 템플릿 사용
  - 데이터베이스 연결
  - 보안 설정

---

<br>

## 🍑 Python의 웹 프레임워크

### <span style="background-color: #F6A19A">Django</span>

- <span style="color: #F6A19A">**특징**</span>

  - 풀스택 웹 프레임워크: 대부분의 기능이 내장되어 있음
  - MTV 아키텍처: Model, Template, View
  - 관리자 페이지 자동 생성 <span style="color: #CDBBA7">(<span style="background-color: #F0EBE3">`/admin`</span>)</span>
  - ORM, 인증, 세션, 폼 등 거의 모든 기능 제공

- <span style="color: #F6A19A">**장점**</span>

  - 빠르게 개발 가능 <span style="color: #CDBBA7">(기능이 대부분 내장되어 있음)</span>
  - 대규모 프로젝트에 적합
  - 보안 관련 기능이 잘 갖춰져 있음

- <span style="color: #F6A19A">**단점**</span>

  - 무겁고 구조가 복잡함
  - 커스터마이징이 어려울 수 있음

- <span style="color: #F6A19A">**예시 폴더 구조**</span> <span style="color: #CDBBA7">(<span style="background-color: #F0EBE3">`startproject`</span>, <span style="background-color: #F0EBE3">`startapp`</span> 명령어로 자동 생성됨)</span>
  ```markdown
  myproject/
  ├── manage.py
  ├── myproject/
  │ ├── settings.py
  │ ├── urls.py
  │ └── wsgi.py
  └── app/
  ├── models.py
  ├── views.py
  ├── urls.py
  └── templates/
  ```
  <br>
- <span style="color: #F6A19A">**작동 방식**</span>
  1. 프로젝트/앱 생성 : <span style="background-color: #F0EBE3">`django-admin startproject myproject`</span> → <span style="background-color: #F0EBE3">`python manage.py startapp myapp`</span>
  2. 라우팅 설정 : <span style="background-color: #F0EBE3">`myproject/urls.py`</span>에서 URL과 view 함수 연결 (<span style="background-color: #F0EBE3">`path('', views.hello)`</span> 등)
  3. View 함수 작성 : <span style="background-color: #F0EBE3">`myapp/views.py`</span>에 <span style="background-color: #F0EBE3">`def hello(request):`</span> 형태로 작성
  4. 응답 반환 : <span style="background-color: #F0EBE3">`HttpResponse()`</span> 또는 <span style="background-color: #F0EBE3">`render()`</span>로 문자열/HTML 반환
  5. 서버 실행 : <span style="background-color: #F0EBE3">`python manage.py runserver`</span>로 개발 서버 시작

### <span style="background-color: #F6A19A">Flask</span>

- <span style="color: #F6A19A">**특징**</span>

  - 마이크로 웹 프레임워크: 핵심 기능만 제공, 나머지는 개발자가 선택
  - 코드가 직관적이고 단순함
  - 확장성이 뛰어남 <span style="color: #CDBBA7">(필요한 것만 추가)</span>

- <span style="color: #F6A19A">**장점**</span>

  - 배우기 쉽고 간단한 구조
  - 작은 프로젝트나 MVP 제작에 적합
  - 자유도가 높고 유연함

- <span style="color: #F6A19A">**단점**</span>

  - 직접 구현해야 할 부분이 많음 <span style="color: #CDBBA7">(ex. 인증, 폼, ORM 등)</span>
  - 큰 프로젝트에서는 유지보수가 어려울 수 있음

- <span style="color: #F6A19A">**예시 폴더 구조**</span> <span style="color: #CDBBA7">(자유롭게 설계 가능)</span>
  ```markdown
  myflaskapp/
  ├── app.py
  ├── templates/
  │ └── index.html
  └── static/
  └── style.css
  ```
  <br>
- <span style="color: #F6A19A">**작동 방식**</span>
  1. 앱 파일 생성 : <span style="background-color: #F0EBE3">`app.py`</span> 하나로 프로젝트 시작
  2. Flask 객체 생성 : <span style="background-color: #F0EBE3">`app = Flask(__name__)`</span>으로 객체 생성
  3. 라우팅 설정 : <span style="background-color: #F0EBE3">`@app.route('/')`</span> 데코레이터로 URL 지정
  4. View 함수 작성 : 문자열 또는 템플릿을 반환하는 함수 작성
  5. 서버 실행 : <span style="background-color: #F0EBE3">`app.run(debug=True)`</span>으로 로컬 서버 실행

### <span style="background-color: #F6A19A">FastAPI</span>

- <span style="color: #F6A19A">**특징**</span>

  - 비동기(Async) 지원을 중심으로 설계
  - 자동 문서화 <span style="color: #CDBBA7">(Swagger UI 제공)</span>
  - 타입 힌트 기반의 경량 API 개발에 최적화
  - 성능이 매우 우수함

- <span style="color: #F6A19A">**장점**</span>

  - 매우 빠른 성능 <span style="color: #CDBBA7">(Starlette 기반, Uvicorn 사용)</span>
  - 자동 문서화 <span style="color: #CDBBA7">(http://localhost:8000/docs)</span>
  - 타입 안정성 → 에러 감소

- <span style="color: #F6A19A">**단점**</span>

  - 신생 프레임워크로 자료가 Django/Flask보다 적음
  - 초심자에게는 타입 힌트 사용이 다소 어려울 수 있음

- <span style="color: #F6A19A">**예시 폴더 구조**</span> <span style="color: #CDBBA7">(<span style="background-color: #F0EBE3">`main.py`</span>만 있어도 실행 가능, 규모 커지면 나눔)</span>
  ```markdown
  fastapi_app/
  ├── main.py
  ├── routers/
  │ └── user.py
  ├── models.py
  └── requirements.txt
  ```
  <br>
- <span style="color: #F6A19A">**작동 방식**</span>
  1. 앱 파일 생성 : <span style="background-color: #F0EBE3">`main.py`</span> 파일에서 시작
  2. FastAPI 객체 생성 : <span style="background-color: #F0EBE3">`app = FastAPI()`</span>로 객체 생성
  3. 라우팅 설정 : <span style="background-color: #F0EBE3">`@app.get('/')`</span>, <span style="background-color: #F0EBE3">`@app.post()`</span>로 HTTP 메서드별 경로 지정
  4. View 함수 작성 : 함수 인자에 타입 힌트를 작성하면 자동 검증 및 문서화
  5. 서버 실행 : <span style="background-color: #F0EBE3">`uvicorn main:app --reload`</span>로 서버 실행 → <span style="background-color: #F0EBE3">`/docs`</span>에서 Swagger 문서 자동 생성
