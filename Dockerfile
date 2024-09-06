FROM python:3.12

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["uvicorn", "ai_server:app", "--reload"]
