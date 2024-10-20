
FROM python:3.10-slim
WORKDIR /app
COPY chatbot/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY chatbot .

EXPOSE 3000

CMD ["python", "main.py"]
