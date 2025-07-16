# Flask 서버 실행과 로컬 접근 설정

## 🍑 VSCode에서의 Flask 서버 실행 방식

- **Run Without Debugging** <span style="color: #CDBBA7">(Ctrl+F5)</span>

  - 단순 실행 모드
  - 디버깅 도구 없이 코드를 실행
  - 빠르게 실행 결과만 확인하고 싶을 때 사용

- **Start Debugging** <span style="color: #CDBBA7">(F5)</span>
  - 디버깅 모드
  - 중단점(Breakpoint)을 걸고, 변수 상태를 추적하며 코드 흐름을 분석 가능
  - 오류 원인을 파악하거나 로직을 자세히 확인할 때 유용

---

<br>

## 🍑 Flask의 역할

- **라우팅 처리** <span style="color: #CDBBA7">(<span style="background-color: #F0EBE3">`@app.route`</span>)</span>

  - 사용자의 URL 요청에 따라 적절한 함수를 연결해줌
  - <span style="background-color: #F0EBE3">`/home`</span>, <span style="background-color: #F0EBE3">`/about`</span> 등 URL 경로별로 응답 페이지를 다르게 설정 가능

- **HTTP 요청/응답 처리**

  - 브라우저의 <span style="background-color: #F0EBE3">`GET`</span>, <span style="background-color: #F0EBE3">`POST`</span> 요청을 받아 데이터를 처리하고, HTML이나 JSON 등을 응답으로 반환

- **템플릿 렌더링**

  - <span style="background-color: #F0EBE3">`render_template()`</span>를 이용해 HTML 파일과 서버 데이터를 동적으로 연결
  - 사용자에게 보이는 웹 페이지를 유연하게 구성할 수 있음

- **서버 실행** <span style="color: #CDBBA7">(<span style="background-color: #F0EBE3">`app.run()`</span>)</span>

  - Flask 애플리케이션을 로컬 서버에서 실행
  - 이때 host, port, debug 등 다양한 옵션을 통해 실행 방식을 설정할 수 있음

- **세션/쿠키 관리**: 사용자별 상태 저장 및 인증 등에 활용

- **폼 처리 및 검증**: 사용자 입력 데이터를 서버에서 처리하고 검증 가능

- **RESTful API 제작**: 외부 시스템과 데이터를 주고받는 API 서버 개발 가능 <span style="color: #CDBBA7">(간단한 경우 Flask만으로 가능)</span>

---

<br>

## 🍑 Flask 서버 접근 설정

<span style="color: #CDBBA7">→ <span style="background-color: #F0EBE3">`app.run()`</span> 내부에서 host, port 등을 설정하여 서버 접근 방식 제어</span>

### <span style="background-color: #F6A19A">Host 설정</span>: 0.0.0.0 설정의 의미와 장단점

- **Host**: 서버 프로그램이 어떤 IP에서 요청을 받을지 설정하는 옵션

- **Host 설정값**: IP 주소 입력 → 이에 따라 외부 기기의 서버 접근 가능 여부가 달라짐

- **<span style="background-color: #F0EBE3">`host='0.0.0.0'`</span> 설정**
  - 모든 IP 주소에서 들어오는 요청을 수락
  - 같은 와이파이 내 다른 기기에서도 접속 가능 → 크로스 디바이스 테스트 시 유용
  - 외부 네트워크에서도 접속이 가능해져 보안상 외부 노출 위험

### <span style="background-color: #F6A19A">IP 주소 설정</span>: 127.0.0.1 접속 vs 내부 IP 접속 방식 비교

- **IP 주소**

  - 네트워크 상에서 컴퓨터를 식별하기 위해 기기마다 부여되는 고유한 주소
  - 일반적으로 내부 IP 또는 공인 IP를 의미함

- **로컬 접속** <span style="color: #CDBBA7">(<span style="background-color: #F0EBE3">`127.0.0.1`</span> / <span style="background-color: #F0EBE3">`localhost`</span>)</span>

  - 루프백 주소: 내 컴퓨터 자신을 가리키는 특수한 IP 주소 (모든 기기에서 동일, 고유하지 않음)
  - 서버와 클라이언트가 같은 컴퓨터일 때만 사용 가능
  - Flask 설정: <span style="background-color: #F0EBE3">`host='127.0.0.1'`</span><span style="color: #CDBBA7">(기본값으로 생략 시 자동 적용됨)</span> → 다른 기기에서는 이 주소로 접속 불가
  - 개인 개발 환경, 혼자 테스트할 때 주로 사용

- **내부 IP 접속** <span style="color: #CDBBA7">(ex. <span style="background-color: #F0EBE3">`192.168.x.x`</span> 등)</span>
  - 내부 IP: 같은 와이파이(로컬 네트워크)에 연결된 각 기기에 부여되는 고유 주소
  - 다른 기기에서 내 서버에 접속할 때 필요
  - Flask 설정: 반드시 <span style="background-color: #F0EBE3">`host='0.0.0.0'`</span>으로 설정 → Flask가 외부에서 오는 요청을 받아들일 수 있도록
  - 스마트폰·태블릿 등 다른 기기에서도 웹 앱을 테스트할 때 주로 사용

### <span style="background-color: #F6A19A">Port 설정</span>: 포트 번호의 역할과 충돌 시 해결 방안

- **Port**

  - 하나의 컴퓨터 안에서 여러 네트워크 프로그램을 구분하는 통로
  - 같은 IP 주소에서도 서로 다른 포트를 사용해 각기 다른 서비스를 운영할 수 있음
  - 동일한 포트는 동시에 두개 이상 사용할 수 없음
  - 포트 번호: 0~65535 사이에서 지정 가능 (표준 포트 번호: 웹 서버 5000, DB 5432, SSH 원격 접속 프로토콜 22) <span style="color: #CDBBA7">→ Flask는 기본적으로 5000번 포트를 사용</span>

- **포트 충돌**: 해당 포트를 이미 다른 프로그램이 사용 중이거나, 같은 서버가 중복 실행된 경우 발생
  ⇨ 다른 포트로 변경 <span style="color: #CDBBA7">(ex. <span style="background-color: #F0EBE3">`app.run(port=5001)`</span>)</span>
  ⇨ 기존에 해당 포트를 점유 중인 프로세스 종료 <span style="color: #CDBBA7">(ex. <span style="background-color: #F0EBE3">`netstat -ano | findstr :5000`</span>, <span style="background-color: #F0EBE3">`taskkill /PID PID /F`</span> 등의 명령어 사용)</span>
