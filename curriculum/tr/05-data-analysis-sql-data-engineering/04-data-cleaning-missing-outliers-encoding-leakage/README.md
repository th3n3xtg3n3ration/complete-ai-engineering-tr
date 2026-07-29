# Ders 4 — Veri Temizleme, Eksik Değer, Aykırı Değer, Encoding ve Veri Sızıntısı

**Seviye:** L2 · **Tahmini süre:** 22 saat · **Durum:** Tamamlandı

## Öğrenme hedefleri

Bu dersin sonunda:

- Veri kalitesini eksiklik, geçerlilik, tutarlılık, benzersizlik ve güncellik boyutlarıyla değerlendirebileceksin.
- Eksik değer mekanizmalarını MCAR, MAR ve MNAR çerçevesinde yorumlayabileceksin.
- Sayısal ve kategorik kolonlarda açık iş kurallarına dayalı temizleme uygulayabileceksin.
- IQR ve robust z-score yöntemleriyle aykırı değerleri teşhis edebileceksin.
- Silme, clipping, winsorization ve robust dönüşüm seçeneklerini karşılaştırabileceksin.
- One-hot encoding, ordinal encoding, rare-category grouping ve bilinmeyen kategori yönetimini uygulayabileceksin.
- İmputation, clipping ve kategori sözlüklerini yalnızca eğitim verisinde fit edebileceksin.
- Target leakage, temporal leakage, entity overlap ve post-outcome feature risklerini denetleyebileceksin.
- Zaman tabanlı ve grup tabanlı veri bölme stratejilerini doğru problem bağlamında seçebileceksin.
- Tekrarlanabilir ve test edilen bir tabular preprocessing paketi geliştirebileceksin.

## Ders dosyaları

1. [Ayrıntılı teori](theory.md)
2. [Uygulama laboratuvarı](lab.md)
3. [Veri kalitesi araçları](src/data_quality.py)
4. [Sızıntısız preprocessing pipeline'ı](src/preprocessing_pipeline.py)
5. [Leakage denetim araçları](src/leakage_audit.py)
6. [Alıştırmalar](exercises.md)
7. [Quiz](quiz.md)
8. [Ödev ve rubrik](assignment.md)
9. [Mülakat soruları](interview-questions.md)
10. [Testler](tests/test_data_cleaning.py)
11. [Metadata](metadata.yml)

## Kurulum ve çalıştırma

```bash
python -m pip install numpy pandas pytest
python curriculum/tr/05-data-analysis-sql-data-engineering/04-data-cleaning-missing-outliers-encoding-leakage/src/data_quality.py
python curriculum/tr/05-data-analysis-sql-data-engineering/04-data-cleaning-missing-outliers-encoding-leakage/src/preprocessing_pipeline.py
python curriculum/tr/05-data-analysis-sql-data-engineering/04-data-cleaning-missing-outliers-encoding-leakage/src/leakage_audit.py
pytest curriculum/tr/05-data-analysis-sql-data-engineering/04-data-cleaning-missing-outliers-encoding-leakage/tests -q
```

## Mini proje

Ham müşteri ve işlem verisini alan, şema ve iş kuralı kontrolleri uygulayan, sayısal kolonlarda eğitim medyanı ile imputation ve IQR clipping yapan, kategorik kolonlarda missing/rare/unknown ayrımını koruyan ve deterministik one-hot özellikler üreten bir preprocessing paketi geliştireceksin. Sistem ayrıca target proxy, post-outcome kolon, temporal split ihlali ve train/evaluation satır çakışmalarını raporlayacak. Tüm fit istatistiklerinin yalnızca eğitim verisinden öğrenildiği otomatik testlerle kanıtlanacak.
