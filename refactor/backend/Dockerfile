from python:3.8-slim

# 리눅스 패키지 설치
RUN apt-get update && apt-get install -y cron vim dos2unix
RUN /usr/local/bin/pip install numpy pandas geopandas dotenv  shapely  sqlalchemy requests pymysql

# 작업 경로 변경
WORKDIR /app

# 로컬 파일 도커 환경으로 복사
# COPY ./crontab /etc/cron.d/crontab
# # 윈도우에서 생성된 ^M 제거
# RUN dos2unix /etc/cron.d/crontab \
#     && chmod 0644 /etc/cron.d/crontab
# # crontab 실행
# RUN crontab /etc/cron.d/crontab

COPY ./crontab /tmp/crontab
RUN dos2unix /tmp/crontab || true
RUN crontab /tmp/crontab
# 디렉토리 생성
RUN mkdir -p /var/log/cron

# cron 실행 (foreground)
CMD ["cron","-f"]