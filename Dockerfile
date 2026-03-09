FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir flet supabase
EXPOSE 7860
CMD ["flet", "run", "main.py", "--web", "--port", "7860"]
