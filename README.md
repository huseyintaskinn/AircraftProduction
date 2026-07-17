# BAYKAR Hava Aracı Üretim Uygulaması

Bu proje, BAYKAR Arka Uç Yazılım Uzmanı pozisyonu için özel olarak geliştirilmiş, iş kuralları ve takımların kısıtlamalarını dinamik olarak yöneten modern bir hava aracı üretim portalıdır.

---

## 🌟 Önemli Özellikler & Çözümler

- **Decoupled Architecture**: Django REST Framework (DRF) tabanlı güvenli bir API katmanı ve modern React + Tailwind CSS tabanlı bir tek sayfa uygulaması (SPA).
- **Service Layer Pattern**: İş mantığı modellerin veya serializer'ların içine yığılmak yerine `services.py` altında bağımsız servislerde (`PartService`, `AssemblyService`, `InventoryService`) kurgulanmıştır.
- **Dynamic Team Enforcement**: `TeamBasedPartPermission` ve `PartService` yardımıyla her takımın (Kanat, Gövde vb.) sadece kendi parçalarını üretip yönetebilmesi sağlanmıştır.
- **Transactional Assembly**: Uçak montajı sırasında parçaların uçağa ait olması, daha önce kullanılmamış olması ve tek seferde `is_used=True` durumuna geçmesi Django'nun `transaction.atomic` mekanizması ile güvenceye alınmıştır.
- **Soft Delete / Recycle**: İsterler doğrultusunda silme (delete) işlemi "Geri Dönüşüme Gönderme" (`is_recycled=True`) olarak modellenmiş ve kullanılmış parçaların geri dönüşümü kısıtlanmıştır.
- **Eksik Parça Uyarısı**: Envanterdeki anlık stok durumuna göre montaj için eksik olan parçalar listelenir ve uyarı panellerinde gösterilir.
- **11/11 Unit Test Coverage**: Model, servis ve API düzeyinde tüm senaryoları kapsayan otomatik testler mevcuttur.

---

## ⚙️ Teknolojiler

- **Backend**: Python 3.9+, Django 4.2+, Django REST Framework, SimpleJWT (OAuth2/JWT Auth), Django Filter, DRF-Spectacular (Swagger/OpenAPI).
- **Database**: PostgreSQL (Docker üzerinde) / SQLite (Yerel).
- **Frontend**: React 19, Vite, Tailwind CSS, Lucide Icons.
- **DevOps**: Docker, Docker Compose, Multi-stage Dockerfile.

---

## 📸 Arayüz Ekran Görüntüleri

Projenin modern, responsive ve glassmorphism tasarımlı web arayüzünden örnek ekran görüntüleri:

### 1. Giriş Ekranı
![Giriş Ekranı](docs/images/login.png)

### 2. Envanter & Stok Takip Paneli
![Envanter & Stok Takip Paneli](docs/images/inventory.png)

### 3. Parça Üretim İstasyonu
![Parça Üretim İstasyonu](docs/images/production.png)

### 4. Uçak Montaj İstasyonu
![Uçak Montaj İstasyonu](docs/images/assembly.png)

---

## 🚀 Yerel Kurulum & Çalıştırma

### 1. Backend Kurulumu
Proje klasöründe terminal açın:
```bash
# Bağımlılıkları yükleyin
pip install -r requirements.txt

# Veritabanını göçürün (Migrate)
python manage.py migrate

# Takım gruplarını oluşturun
python manage.py create_groups

# Test kullanıcılarını oluşturun (Seed)
python manage.py seed_users
```

### 2. Backend Sunucusunu Başlatma
```bash
python manage.py runserver
```
API sunucusu default olarak `http://127.0.0.1:8000` adresinde çalışacaktır.
- **API Dokümantasyonu (Swagger)**: `http://127.0.0.1:8000/swagger/` adresinden tüm endpoint'leri görüntüleyip test edebilirsiniz.

### 3. Frontend Kurulumu & Başlatma
Yeni bir terminalde `frontend` klasörüne geçin:
```bash
cd frontend

# Bağımlılıkları yükleyin
npm install

# Geliştirici sunucusunu başlatın
npm run dev
```
Frontend default olarak `http://localhost:5173` adresinde çalışacaktır.

---

## 👥 Test Personel Bilgileri

Sistemde her departman için otomatik olarak oluşturulmuş hazır test kullanıcıları mevcuttur. 

**Tüm kullanıcıların şifresi:** `testpassword`

| Kullanıcı Adı | Ait Olduğu Takım | Üretebileceği Parçalar |
|---|---|---|
| `wing_worker` | Kanat Takımı | Kanat (`wing`) |
| `fuselage_worker` | Gövde Takımı | Gövde (`fuselage`) |
| `tail_worker` | Kuyruk Takımı | Kuyruk (`tail`) |
| `avionics_worker` | Aviyonik Takımı | Aviyonik (`avionics`) |
| `assembly_worker` | Montaj Takımı | Sadece Montaj Yapabilir |

---

## 🧪 Birim Testlerini Çalıştırma

Tüm unit testleri çalıştırmak için projenin kök dizininde:
```bash
python manage.py test
```

---

## 🐳 Docker ile Ayağa Kaldırma (Alternatif)

Docker Compose ile postgres ve django sunucularını tek komutla çalıştırabilirsiniz:
```bash
docker-compose up --build
```
`docker-compose` otomatik olarak veritabanını oluşturur, göçleri uygular ve test personellerini yükler.
