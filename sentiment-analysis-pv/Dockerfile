FROM python:3.8-slim-buster
WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["python", "sentiment_analysis.py"]
