FROM nikolaik/python-nodejs:python3.11-nodejs20

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY web/package.json web/package-lock.json /app/web/
WORKDIR /app/web
RUN npm ci
COPY web/ /app/web/
RUN npm run build

WORKDIR /app
COPY backend/ ./
COPY agents/ /app/agents/
COPY skooli_buddy/ /app/skooli_buddy/

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
