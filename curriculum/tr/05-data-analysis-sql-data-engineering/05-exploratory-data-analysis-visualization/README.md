# Ders 5 — Keşifsel Veri Analizi ve Görselleştirme

**Seviye:** L2 · **Tahmini süre:** 20 saat · **Durum:** Tamamlandı

## Öğrenme hedefleri

Bu dersin sonunda:

- EDA sürecini iş sorusu, veri sözleşmesi ve karar ihtiyacıyla ilişkilendirebileceksin.
- Satır, kolon, dtype, eksiklik, duplicate ve bellek profilini otomatik çıkarabileceksin.
- Sayısal değişkenleri merkez, yayılım, çarpıklık, kuantil ve IQR üzerinden inceleyebileceksin.
- Kategorik değişkenlerde kardinalite, seyrek sınıf, missing kategori ve oran analizi yapabileceksin.
- Korelasyon değerlerini nedensellik iddiasına dönüştürmeden yorumlayabileceksin.
- Segment, hedef ve zaman ekseninde karşılaştırmalı özetler üretebileceksin.
- Histogram, bar chart, scatter plot, missingness grafiği ve korelasyon heatmap'i oluşturabileceksin.
- Grafiklerde eksen, ölçek, örneklem büyüklüğü ve seçim yanlılığından doğan yanıltıcı örüntüleri teşhis edebileceksin.
- EDA kodunu notebook'a bağımlı bırakmadan test edilen fonksiyonlar ve rapor artefaktları olarak paketleyebileceksin.
- Tek komutla yeniden üretilebilen Markdown, CSV ve PNG çıktılarından oluşan bir EDA raporu geliştirebileceksin.

## Ders dosyaları

1. [Ayrıntılı teori](theory.md)
2. [Uygulama laboratuvarı](lab.md)
3. [EDA temel araçları](src/eda_foundations.py)
4. [Matplotlib görselleştirme araçları](src/visualization.py)
5. [Tekrarlanabilir EDA rapor üreticisi](src/eda_report.py)
6. [Alıştırmalar](exercises.md)
7. [Quiz](quiz.md)
8. [Ödev ve rubrik](assignment.md)
9. [Mülakat soruları](interview-questions.md)
10. [Testler](tests/test_eda.py)
11. [Metadata](metadata.yml)

## Kurulum ve çalıştırma

```bash
python -m pip install numpy pandas matplotlib pytest
python curriculum/tr/05-data-analysis-sql-data-engineering/05-exploratory-data-analysis-visualization/src/eda_foundations.py
python curriculum/tr/05-data-analysis-sql-data-engineering/05-exploratory-data-analysis-visualization/src/eda_report.py
pytest curriculum/tr/05-data-analysis-sql-data-engineering/05-exploratory-data-analysis-visualization/tests -q
```

## Mini proje

Müşteri davranışı verisi için tekrarlanabilir bir EDA paketi geliştireceksin. Paket; veri profili, sayısal ve kategorik özetler, IQR aykırı değer raporu, korelasyon çiftleri, segment metrikleri, hedef incelemesi ve Matplotlib grafiklerini otomatik üretecek. Tüm tablolar CSV, yapı bilgisi JSON, anlatı Markdown ve grafikler PNG olarak yayımlanacak. Aynı girdi ve konfigürasyonla aynı artefaktların üretildiği testlerle doğrulanacak.
