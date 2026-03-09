FROM python:3.10-slim

WORKDIR /app

# Langsung copy semua file sekaligus
COPY . .

# Install library
RUN pip install --no-cache-dir flet supabase

# Port wajib
EXPOSE 7860

# Jalankan aplikasi
CMD ["flet", "run", "main.py", "--web", "--port", "7860"]
