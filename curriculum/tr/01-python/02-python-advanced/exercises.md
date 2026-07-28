# İleri Python Alıştırmaları

1. 1–100 arasındaki çift sayıların karelerini comprehension ile üret.
2. Bir kelime listesini uzunluklarına göre sözlüğe dönüştür.
3. Büyük bir sayı akışından yalnızca asal sayıları üreten generator yaz.
4. Bir iterable'ı sabit boyutlu parçalara ayıran `batch` fonksiyonunu geliştir.
5. Fonksiyon çağrı sayısını ölçen decorator yaz.
6. Süre ölçen decorator'ın fonksiyon adını korumasını `functools.wraps` ile sağla.
7. `@dataclass` ile `ModelMetric` sınıfı oluştur.
8. Negatif metrik değerlerinde özel exception yükselt.
9. Dosya açıp güvenli kapatan bir context manager yaz.
10. Ham veri doğrulama, dönüştürme ve özetleme adımlarını ayrı saf fonksiyonlara böl.
11. Generator ile liste yaklaşımının bellek farkını `sys.getsizeof` kullanarak incele.
12. `mypy` veya benzeri bir statik analiz aracıyla type hint hatalarını bul.

## Meydan okuma

CSV benzeri sözlük kayıtlarını doğrulayan, hatalı satırları raporlayan ve geçerli kayıtları gruplar halinde işleyen bir mini ETL hattı tasarla. Çözümün en az üç saf fonksiyon, bir generator, bir dataclass ve bir özel exception içermelidir.
