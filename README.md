# flight-roster-system-CMPE331-Project
CMPE 331 Project flight-roster-system

Bu proje, CMPE331 dersi kapsamında geliştirilen ve hayali bir havayolu şirketi için uçuş roster'ları (uçuş listeleri) hazırlayan bir web sistemidir. Proje, dört farklı mikroservis API'sinden (Uçuş Bilgileri, Uçuş Ekibi, Kabin Ekibi ve Yolcu Bilgileri) veri çeken bir ana sistemden oluşmaktadır.
--

## 1. Gereksinimler

Projeye başlamadan önce, geliştirme ortamınızın aşağıdaki gereksinimleri karşıladığından emin olmalısınız.
* **Python Sürümü:** Bu projenin sorunsuz çalışabilmesi için **Python 3.14** sürümünün bilgisayarınızda yüklü olması gerekmektedir.

### Python 3.14 Kurulumu

Eğer sisteminizde doğru Python sürümü yüklü değilse, resmi `python.org` sitesinden indirip kurabilirsiniz. Kurulum sırasında **"Add Python 3.14 to PATH"** seçeneğini işaretlediğinizden emin olun.

---

## 2. Kurulum ve Başlatma Adımları

### Adım 1: Projeyi Klonlama (Visual Studio Code ile)

Herkesin projeyi VS Code üzerinden klonlaması beklenmektedir.

1.  **Visual Studio Code'u açın.**
2.  **Command Palette'i Açın:** `Cmd+Shift+P` (macOS) veya `Ctrl+Shift+P` (Windows) tuş kombinasyonunu kullanarak komut paletini açın.
3.  Açılan arama çubuğuna **`Git: Clone`** yazın ve çıkan seçeneğe tıklayın.
4.  **Repository URL'ini Yapıştırın:** Sizden istenen alana projenin GitHub URL'ini yapıştırın ve Enter'a basın.
    `https://github.com/senin-kullanici-adin/proje-repo-adin.git`
5.  **Klasör Seçin:** Projenin bilgisayarınızda nereye kaydedileceğini seçin.
6.  Klonlama tamamlandığında, VS Code sağ altta **"Would you like to open the cloned repository?"** diye soracaktır. **"Open"** butonuna basarak projeyi açın.

### Adım 2: Sanal Ortam (Virtual Environment) Oluşturma

Projeyi VS Code içinde açtıktan sonra, entegre terminali açın

**Windows:**
```bash
# Python 3.14'ü kullanarak sanal ortamı oluştur
py -3.14 -m venv venv
# Sanal ortamı aktive et
.\venv\Scripts\activate
```

**macOS / Linux:**
```bash
# Python 3.14'ü kullanarak sanal ortamı oluştur
python3 -m venv venv
# Sanal ortamı aktive et
source venv/bin/activate
```

### Adım 3: Bağımlılıkları Yükleme
```bash
pip install -r requirements.txt
```

### Adım 4: Veritabanını Oluşturma
```bash
python manage.py migrate
```

### Adım 5: Yönetici (Superuser) Oluşturma
```bash
python manage.py createsuperuser
```

### Adım 6: Geliştirme Sunucusunu Başlatma
```bash
python manage.py runserver
```
Sunucu varsayılan olarak `http://127.0.0.1:8000/` adresinde çalışmaya başlayacaktır.

---

## 3. Takım Çalışması ve Git İş Akışı

Bu proje, takım çalışması gerektirdiği için herkesin aşağıdaki Git kurallarına uyması **zorunludur**.

### Yeni Bir Özellik Geliştirme

1.  Her zaman kendi geliştireceğiniz özellik (örneğin yeni bir API) için yeni bir `branch` oluşturun. **Asla doğrudan `main` branch'ine kod göndermeyin!**
2.  Branch isimleri `feature/` ön eki ile başlamalıdır. (Örn: `feature/flight-crew-api`)

    ```bash
    # Önce main'in en güncel halini al
    git checkout main
    git pull origin main

    # Şimdi kendi yeni branch'ini oluştur ve ona geçiş yap
    git checkout -b feature/senin-api-adin
    ```

### **ÖNEMLİ:** `main` Branch'i Değiştiğinde Ne Yapılmalı?

Bir takım arkadaşınız kendi kodunu `main` branch'ine birleştirdiğinde, projenin ana yapısı değişmiş olur. Kendi kodunuzun bu yeni yapı ile uyumlu kalması için **düzenli olarak** aşağıdaki senkronizasyon adımlarını izlemelisiniz:

1.  **Mevcut İşini Kaydet:** Kendi `feature` branch'indeyken, o anki tüm değişikliklerini commit'le.
    ```bash
    git add .
    git commit -m "Yaptığın değişikliği anlatan bir mesaj"
    ```

2.  **`main` Branch'ine Geçiş Yap:** Projenin ana branch'ine geç.
    ```bash
    git checkout main
    ```

3.  **`main` Branch'ini Güncelle:** GitHub'daki en son değişiklikleri bilgisayarına çek.
    ```bash
    git pull origin main
    ```

4.  **Kendi Branch'ine Geri Dön:** Tekrar kendi çalıştığın `feature` branch'ine dön.
    ```bash
    git checkout feature/senin-api-adin
    ```

5.  **Güncel `main`'i Kendi Branch'ine Birleştir:** `main`'deki yenilikleri kendi branch'ine dahil et.
    ```bash
    git merge main
    ```

Bu adımları, kod yazmaya başlamadan önce veya önemli bir commit yapmadan önce alışkanlık haline getirmek, projenin sonunda yaşanacak büyük birleştirme (merge) sorunlarını engelleyecektir.
