FROM python:3.12

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 Python 모듈 설치
COPY ./app /app
COPY ./favicon.ico /favicon.ico

# 패키지 목록 업데이트 및 Vim 설치
RUN apt-get update && \
    apt-get install -y vim && \
    pip install --no-cache-dir -r latest.txt && \
    # 불필요한 패키지 목록 캐시 삭제
    rm -rf /var/lib/apt/lists/*

# Uvicorn 서버 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]