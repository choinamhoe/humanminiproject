# 🐾 골프 날씨 예측 웹 서비스

본 프로젝트는 현재 기상 및 기상 예측 정보를 고려한 **골프 플레이 가능성**과 관련된 예측 정보 제공하는 서비스입니다.(AI 부분 수정 필요)

---

<div style="display: flex; align-items: center; gap: 8px;">
  <div>
    <img src="https://img.shields.io/badge/Licence-GPL-1177AA.svg?style=flat-round" />
    <img src="https://img.shields.io/badge/Version-0.0.1-1177AA.svg?style=flat-round" />
    <img
        src="https://img.shields.io/badge/HTML-%23E34F26.svg?logo=html5&logoColor=white" alt="HTML" />
    <img
      src="https://img.shields.io/badge/CSS-1572B6?style=flat&logo=CSS&logoColor=white" alt="CSS Badge" />
    <img
    src="https://img.shields.io/badge/JavaScript-%23F7DF1E.svg?logo=javascript&logoColor=black" alt="JavaScript" />
    <img src="https://img.shields.io/badge/react-1177AA?logo=react&logoColor=%2361DAFB" alt="React" />
    <br/>
    <img src="https://img.shields.io/badge/python-3.10.0-1177AA.svg?style=flat-round" alt="Python" />
    <img src="https://img.shields.io/badge/FastAPI-02569B?logo=FastAPI&logoColor=white" alt="FastAPI" />
    <img src="https://img.shields.io/badge/github-%23121011?logo=github&logoColor=white" alt="GitHub" />
    <img src="https://img.shields.io/badge/Docker-1572B6?logo=docker&logoColor=fff" />
    <img src="https://img.shields.io/badge/Docker--Compose-000000?logo=docker&logoColor=white" />
    <img src="https://img.shields.io/badge/MySQL-1572B6?logo=mysql&logoColor=fff" />
<img src="https://img.shields.io/badge/Geocode-Awesome_Table-4A90E2?logo=googlemaps&logoColor=white" />
<img src="https://img.shields.io/badge/Cron-4CAF50?style=flat&logo=clock&logoColor=white" alt="Cron" />

  </div>
</div>

![시연](./Animation.gif)

## 💡 개발 배경 및 목적

본 프로젝트는 현재 기상 및 기상 예측 정보를 고려한 **골프 플레이 가능성**과 관련된 예측 정보 제공하는 서비스입니다.

## ⚙️ 서비스 핵심 기능

**[주요기능]**

- 기상 정보를 바탕으로 한 골프 가능성 예측 정보 제공

## 📆 개발 과정

- 개발 기간은 9월 8일부터 9월 16일까지 진행(팀 배정 및 주제선정, 발표 자료 작성 기간 포함)
- 개발 과정은 오전 회의 진행, 및 오전/오후 일정 파악 수행

## 📦 설치 및 실행

### cron

```bash
cd backend

docker-compose up -d
```

### python backend

```bash
# python backend는 python 3.10.0 버전 환경에서 진행
# conda env create -f conda-env-cpu.yml 로 생성 가능
conda env create -f conda-env-cpu.yml

conda activate golf_310
cd  py_backend
```

### frontend

```bash
cd frontend
npm install
npm run start

depcheck # 코드에서 안쓰는 패키지 목록 확인
SET PORT=3001 && npm run start # 다른 포트로 시작(Windows)
```

### DataBase

```bash
cd DB
docker-compose up -d
# db관련 툴 활용하여 init.sql 실행
# dump 파일 삽입
```

## 🚧 향후 개발 계획

## ©️License

본 프로젝트의 코드는 비상업적 용도로 자유롭게 사용하실 수 있습니다.
상업적 이용이나 수정, 재배포 시에는 사전 연락을 부탁드립니다.

문의는 이메일()로 해주시기 바랍니다.

## 📖 Reference

데이터 출처 :

- [기상청 단기예보 조회 서비스](https://www.data.go.kr/data/15084084/openapi.do)
- [기상청 API허브](https://apihub.kma.go.kr/)

## 👨‍💻👩‍💻 Collaborator

- 프론트 개발
  - [윤수진(M), 전하늘, 박한비](https://github.com/choinamhoe/humanminiproject)
- DB, AI 및 백엔드 개발
  - [최남회(S)](https://github.com/choinamhoe/humanminiproject)
