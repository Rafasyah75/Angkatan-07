FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Port wajib Hugging Face
EXPOSE 7860
CMD ["flet", "run", "main.py", "--web", "--port", "7860"]
