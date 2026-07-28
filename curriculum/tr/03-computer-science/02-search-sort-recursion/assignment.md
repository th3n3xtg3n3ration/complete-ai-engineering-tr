# Ödev — Algoritma Benchmark Paketi

## Görev

Arama ve sıralama algoritmalarını karşılaştıran tekrar üretilebilir bir Python paketi geliştir.

Paket şu özellikleri içermelidir:

- Linear ve binary search implementasyonu
- Insertion, merge ve quick sort implementasyonu
- Rastgele, sıralı, ters sıralı ve tekrar eden değerlerden oluşan veri üretimi
- Birden fazla tekrar üzerinden süre ölçümü
- Sonuç doğrulama
- CSV veya Markdown raporu
- Pytest testleri
- Kısa karmaşıklık analizi

## Zorunlu senaryolar

1. En az üç farklı veri boyutu kullan.
2. Her algoritma için doğru sonuç üretildiğini kontrol et.
3. Binary search öncesinde sıralama maliyetini ayrı değerlendir.
4. Küçük veri ile büyük veri sonuçlarını ayrı yorumla.
5. Recursive çözümün call-stack maliyetini açıkla.

## Rubrik

| Ölçüt | Puan |
|---|---:|
| Algoritmaların doğruluğu | 30 |
| Test kapsamı ve kenar durumları | 20 |
| Benchmark tasarımı | 20 |
| Karmaşıklık analizi | 15 |
| Kod kalitesi ve type hints | 10 |
| Raporlama | 5 |
| **Toplam** | **100** |
