FROM python:3.12

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 Python 모듈 설치
COPY ./app /app
RUN pip install --no-cache-dir -r latest.txt

# Uvicorn 서버 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]