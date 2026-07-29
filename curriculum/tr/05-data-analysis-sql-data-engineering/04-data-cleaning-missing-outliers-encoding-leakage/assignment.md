# Ödev — Leakage-Safe Data Cleaning Package

## Senaryo

Bir abonelik ürününde churn tahmini için müşteri, kullanım ve ödeme verileri hazırlanacaktır. Ham veri eksik değer, duplicate kayıt, uç kullanım miktarı, yeni kategoriler ve tahmin tarihinden sonra oluşan ödeme bilgileri içermektedir.

## Gereksinimler

1. Şema ve required-column doğrulaması
2. Kolon bazlı missingness raporu
3. İş anahtarı duplicate raporu
4. Sayısal kolonlarda train medianı
5. IQR tabanlı train clipping sınırları
6. Missing, rare ve unknown kategorilerin ayrı yönetimi
7. Deterministik one-hot kolonları
8. Zaman tabanlı train/evaluation split
9. Row ID overlap denetimi
10. Target proxy ve post-outcome feature denetimi
11. Girdiyi değiştirmeyen dönüşümler
12. En az 20 otomatik test
13. Teknik karar günlüğü
14. Veri kalite ve leakage raporu

## Teslimatlar

- `src/` altında yeniden kullanılabilir Python paketi
- `tests/` altında testler
- Örnek çalıştırma scripti
- Kalite raporu
- Leakage raporu
- Mimari ve karar dokümanı

## Rubrik

| Boyut | Puan |
|---|---:|
| Şema ve veri kalite kontrolleri | 15 |
| Eksik değer stratejisi | 15 |
| Aykırı değer stratejisi | 15 |
| Encoding ve bilinmeyen kategori | 15 |
| Fit/transform ve leakage güvenliği | 20 |
| Test kapsamı | 10 |
| Dokümantasyon ve açıklanabilirlik | 10 |
| **Toplam** | **100** |

## Kabul ölçütü

En az 70 puan, tüm kritik testlerin geçmesi ve hiçbir preprocessing istatistiğinin evaluation verisinde fit edilmemesi gerekir.
