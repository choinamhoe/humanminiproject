# 1. docker 와 cron을 활용하여 매 분마다 log.txt 에 시간 출력하기

```bash
cron_test.py
crontab
Dockerfile
docker-compose.yml

```

```bash
# 도커 환경 테스트
docker run -it --name cron_test -v D:/250520/cron/src:/app python:3.8-slim bash
docker run -it --name cron_test -v "D:/250520 경로/cron/src":/app python:3.8-slim bash


docker build -t cron_test:latest -f Dockerfile .
docker save -o cron_test.tar cron_test:latest  #docker 파일 형태로 저장
docker load cron_test.tar cron_test:latest # 파일을 이미지로 불러오기
```

```bash
# 파이썬 패키지 목록 추출
pip freeze > requirement.txt
```
