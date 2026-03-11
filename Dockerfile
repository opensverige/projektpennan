FROM nikolaik/python-nodejs:python3.11-nodejs20

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./
COPY agents/ /app/agents/
COPY frontend/ /app/frontend/

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
