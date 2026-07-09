FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

HEALTHCHECK CMD curl --fail http://localhost:5000/ || exit 1

ENTRYPOINT ["python", "server.py"]
