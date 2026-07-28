# Ödev — Güvenilir Veri İşleme Hattı

Bir eğitim platformundan gelen öğrenci kayıtlarını işleyen küçük bir Python paketi geliştir.

## Gereksinimler

- `StudentRecord` adlı bir dataclass kullan.
- Ad, e-posta ve 0–100 arası puan doğrulaması yap.
- Hatalı girdiler için en az iki özel exception tanımla.
- Kayıtları tembel biçimde üreten bir generator yaz.
- Kayıtları istenen boyutta gruplara ayır.
- Ortalama, minimum, maksimum ve başarı oranı hesapla.
- Süre ölçen bir decorator ekle.
- En az 10 otomatik test yaz.
- Kodun tamamında type hint kullan.

## Teslim yapısı

```text
assignment/
├── README.md
├── student_pipeline/
│   ├── __init__.py
│   ├── models.py
│   ├── validation.py
│   └── pipeline.py
└── tests/
    └── test_pipeline.py
```

## Rubrik — 100 puan

- Doğru çalışma: 30
- Modüler tasarım: 20
- Hata yönetimi: 15
- Type hint ve okunabilirlik: 15
- Test kalitesi: 15
- Dokümantasyon: 5

## Ek puan

Komut satırından CSV dosyası kabul eden ve sonuçları JSON olarak yazan bir arayüz ekle.
