# Resmi Python 3.9 imajını temel al
FROM python:3.9-slim

# Çalışma dizinini oluştur
WORKDIR /app

# Gerekli dosyaları çalışma dizinine kopyala
COPY requirements.txt requirements.txt

# Bağımlılıkları yükle
RUN pip install --no-cache-dir -r requirements.txt

# Proje dosyalarını kopyala
COPY . .

# Django uygulaması için ortam değişkenlerini ayarla
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Uygulamayı çalıştırmak için komut
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "aircraft_production.wsgi:application"]
