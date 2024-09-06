# 베이스 이미지 선택
FROM python:3.12.4-slim

# 필요한 파일 복사
COPY . .

# 필요 패키지 설치
RUN pip install --upgrade pip
RUN pip install --use-pep517 --no-cache-dir -r requirements.txt

ENTRYPOINT ["uvicorn", "ai_server.py:app", "--host", "0.0.0.0", "--port", "8000"]
