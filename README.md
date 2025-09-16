## 실시간으로 가져오는 기상청 정보

## 강사님 추천

주소 : https://data.kma.go.kr/cmmn/main.do
경로 : API>>예특보>>1. 동네예보(초단기실황·초단기예보·단기예보) 조회

브랜치명 : 1.최남회 - choinamhoe 2.조창제 - changjecho 3.전하늘 - jeonhaneul 4.박한비 - parkhanbee 5.윤수진 - sujinyun

내 ip : 192.168.0.38
db정보 :
user_id = "root"
password = "15932!miniprojectdb"
host = "192.168.0.38"
port = 30000
database_name = "miniproject"

git주소 : https://github.com/choinamhoe/humanminiproject

구글 스프레드시트를 활용한 주소 -> 좌표계로 변환
https://velog.io/@syh0397/%EA%B5%AC%EA%B8%80-%EC%8A%A4%ED%94%84%EB%A0%88%EB%93%9C-%EC%8B%9C%ED%8A%B8%EC%97%90%EC%84%9C-%EC%A7%80%EC%98%A4%EC%BD%94%EB%94%A9%EC%A3%BC%EC%86%8C-%EC%A2%8C%ED%91%9C-%EB%B3%80%ED%99%98%ED%95%98%EA%B8%B0

https://www.perplexity.ai/ 링크 같은거 찾아주는 LLM 서비스입니다.

# 주제: 골프장별 맞춤형 실시간 날씨와 플레이 가능성 예측

- 조 이름: swing sky

# 골프장 목록 조회시 날씨 정보 설명

      STN : 관측소 번호 (Station ID, 기상청 고유 식별자)
      LON : 관측소 경도 (Longitude, WGS84 좌표계)
      LAT : 관측소 위도 (Latitude, WGS84 좌표계)
      TM : 관측 시각 (Timestamp, YYYY-MM-DD HH:MM:SS)
      TA : 기온 (Temperature, ℃)
      PR : 기압 (Pressure, hPa)
      HM : 상대습도 (Humidity, %)
      WS : 풍속 (Wind Speed, m/s)
      WD : 풍향 (Wind Direction, degree, 0~360°)
      RN : 강수량 (Precipitation, mm, 해당 시각까지의 누적 혹은 시강수 depending on KMA 제공값)
      geometry : Shapely Point 객체 (위치 좌표, EPSG:4326)

# 골프장 상세 조회시 날씨 정보 설명

      id                : int   -> 순번 (1부터 시작)
      time              : datetime -> 예측 시간 (한국 시간, tz=Asia/Seoul)
      temperature       : float -> 기온(℃)
      humidity          : float -> 상대습도(%)
      wind_speed        : float -> 풍속(m/s)
      visibility        : float -> 가시거리(m), 기본 10000m
      precip_prob       : float    -> 강수 확률(%), 초단기예보에는 0.0
      precipitation     : float    -> 1시간 강수량(mm), RN1 기준
      precip_type       : int      -> 강수 형태, PTY 기준 (0=없음, 1=비, 2=비/눈, 3=눈, 4=소나기)
      fog_index         : float -> 안개 지수(0~100, 높을수록 안개 심함)
      playable_rule     : int   -> Rule 기반 골프 가능 여부 (0=불가,1=가능)
      playable_prob_ml  : float -> ML(RandomForest) 예측 확률(0~1)
      playable_ml       : int   -> ML(RandomForest) 예측 결과 (0=불가,1=가능)
      playable_prob_dl  : float -> DL(NeuralNetwork) 예측 확률(0~1)
      playable_dl       : int   -> DL(NeuralNetwork) 예측 결과 (0=불가,1=가능)
      final_playable    : int   -> 최종 골프 가능 여부 (0=불가,1=가능), playable_rule OR playable_ml
      summary           : str   -> 사람이 읽기 좋은 요약 문자열
                              (HTML 출력 대응 위해 줄바꿈은 <br> 로 변환됨)
                              예시:
                              "2025-09-13 14:00:00 — 기온 25.0°C, 습도 65%, 풍속 4.0m/s, 강수량 2.5mm, 안개지수 12.0 → 골프장: 가능 (ML:0.92)<br>👉 기온 적당, 바람 약함"

## 도커 실행 순서

docker-compose down
docker-compose build --no-cache
docker-compose up -d

## 기상청 API키 발급

data.go.kr - 로그인 해야 하는 사이트 - 네이버 로그인(cnh665@naver.com) - 휴대폰 인증 필요
로그인 하고 기상청 단기예보 조회 서비스 검색 - https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15084084
활용신청 버튼 클릭
API키 발급
현재일자 - 2025-09-13
만료일자 - 2027-09-13
일반 인증키 : 3b8dcb53f1ccdd05fb434481223a53ff8fe1a47df3860abbb1a315ddf2637338

# docker를 로그오프에도 자동으로 실행되게 하는 방법

nssm (Non-Sucking Service Manager) 설치 -https://nssm.cc/download 에서 nssm 2.24 (2014-08-31) 설치 -자료 폴더에 여기서 받은 nssm 2.24.zip파일 넣어둠 -압축을 푼 후 C:\nssm\nssm.exe 에 64bit폴더에 있는 파일을 옮겨놓음 -보통 도커 설치 경로를 확인 - C:\Program Files\Docker\Docker\Docker Desktop.exe

# 도커 설치 경로 확인 방법

1)시작 메뉴 - 파일 위치 열기 - Docker Desktop 마우스 오른쪽버튼 - 파일 위치 열기 - 파일 경로 확인

-nssm으로 서비스 등록 1)관리자 권한 PowerShell 또는 CMD 실행 후 아래 입력:
-C:\nssm\nssm.exe install DockerDesktopService 하면 GUI 창이 뜸
-Application Path: C:\Program Files\Docker\Docker\Docker Desktop.exe
-Startup directory:C:\Program Files\Docker\Docker -나머지칸은 공백으로 넣고 적용
2)Win + R → services.msc 입력 → DockerDesktopService 찾아서 -시작 유형(Start type) → Automatic (자동) 으로 변경 -서비스 시작(Start) -자동이 안될 경우 수동에 있는 건도 실행중

-확인 방법
-docker version,docker ps 했을때 컨테이너 실행 안해도 실행되면 정상 작동

# 도커를 작업스케줄러로 등록 방법

-window키 + R
-taskschd.msc 실행 -오른쪽버튼 + 작업만들기

# 일반탭 :

- 사용자가 로그인할때만 실행체크 + 가장높은 수준의 권한으로 실행 + windows 10

# 트리거탭 :

- 로그온할때로 선택

# 동작탭 :

프로그램시작
프로그램/스크립트 : "C:\Program Files\Docker\Docker\Docker Desktop.exe"
시작위치(옵션)(T) : C:\Program Files\Docker\Docker

# 조건탭 :

- 전원쪽에 체크되어 있는거 해제

# 설정탭 :

- 요청시 작업이 실행되도록 허용,요청할 때 실행중인 작업이 끝나지 않으면 강제로 작업 중지만 체크

# 작업표시줄

- 위로 향해있는 버튼 클릭
- 백그라운드 버튼 중 Docker Desktop running 오른쪽 버튼 선택
- change settings 버튼 클릭
- General에서 Open Docker Dashboard when Docker Desktop starts 체크 되어 있는 것을 해제

# docker 현황 조회

- docker ps

# 컨테이너 중지 (ID 또는 이름 사용)

docker stop 6cd2ec6fdf20

# 컨테이너 삭제

docker rm 6cd2ec6fdf20

# 재시작 정책을 적용하여 컨테이너 새로 실행

docker run -d --name weathercron --restart unless-stopped cron_test:latest

# 화면 보호기 설정

1. 화면보호기 + 잠금 설정
   윈도우 키 + S → 화면 보호기 검색 → 화면 보호기 변경 클릭
   (또는 제어판 → 모양 및 개인 설정 → 개인 설정 → 화면 보호기)

화면 보호기 드롭다운에서 원하는 화면보호기 선택 (예: 공백, 3D 텍스트 등).

대기 시간 입력 (예: 10분 → 10분 동안 입력이 없으면 실행).

✅ "다시 시작할 때 로그온 화면 표시" 체크
→ 화면보호기 해제 시 자동으로 잠금 화면으로 전환됨.
적용 → 확인 클릭.

# 전원 관리(대기 모드/절전)와 분리

위 방법은 화면보호기 → 잠금이고, PC는 계속 켜져 있습니다.

만약 절전 모드로 들어가면 Docker 컨테이너도 멈추니까,
👉 설정 → 시스템 → 전원 및 절전에서 절전 모드 안 들어가게 설정해두는 게 좋아요.

# 추후 개발 방향

📍 확장 방향 (기능적 측면)

골프장 예약 기능
→ 지도에서 골프장 선택 → 상세 정보 확인 → 바로 예약까지 연결

공유하기 기능
→ 원하는 골프장 정보를 간단히 지인과 공유 가능

골프장 리뷰 작성/조회
→ 실제 이용자들의 후기를 통해 선택에 도움

추천 골프장 서비스
→ 오늘의 추천 골프장 제공
→ 현재 시간 기준, 가장 가까운 티업 가능한 골프장 추천
→ 날씨·티업 시간 조건을 함께 고려해 자동 추천

대체 골프장 안내
→ 날씨 영향으로 예약이 취소될 경우
→ 근처 날씨가 좋은 골프장 + 가장 빠른 티업 시간대 추천
→ 사용자가 즉시 다른 곳에서 플레이 가능

# --- 파일/환경 준비 ---
