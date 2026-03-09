FROM python:3.10-slim

WORKDIR /app

# Salin semua file dari repositori ke dalam folder /app di server
COPY . .

# Install library utama (Flet untuk tampilan, Supabase untuk database)
RUN pip install --no-cache-dir flet supabase

# Port 7860 adalah port wajib yang dibuka oleh Hugging Face
EXPOSE 7860

# Menjalankan aplikasi sebagai web app di port yang ditentukan
CMD ["flet", "run", "main.py", "--web", "--port", "7860"]
