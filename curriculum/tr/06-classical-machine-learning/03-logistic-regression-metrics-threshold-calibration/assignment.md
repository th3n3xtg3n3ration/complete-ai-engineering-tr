# Ödev — Kalibre Edilmiş ve Maliyet Duyarlı Churn Sistemi

## Senaryo

Bir abonelik şirketi, gelecek 30 gün içinde churn edecek müşterilere retention teklifi gönderecek. Teklif maliyeti vardır; churn eden müşteriyi kaçırmanın maliyeti ise daha yüksektir.

## Görev

Üretim öncesi binary classification ve karar sistemi geliştir.

Teslimat şunları içermelidir:

1. Positive class ve karar zamanı tanımı
2. Train/validation/test split
3. Majority ve class-prior baseline
4. Leakage-safe preprocessing pipeline
5. L1 ve L2 logistic regression karşılaştırması
6. Class weight deneyi
7. ROC-AUC, average precision, log loss ve Brier score
8. En az 51 threshold içeren değerlendirme tablosu
9. İş maliyetlerine dayalı threshold seçimi
10. Precision veya recall guardrail'i
11. Sigmoid ve isotonic calibration karşılaştırması
12. Reliability tablosu ve expected calibration error
13. Segment bazlı hata ve calibration analizi
14. Model konfigürasyonu ve değerlendirme raporu
15. En az 20 otomatik test

## Maliyet varsayımı

Retention teklifinin gereksiz gönderim maliyeti **₺40**, churn eden müşteriyi kaçırmanın beklenen maliyeti **₺600** olarak kullanılacaktır. Bu değerler threshold seçiminde açıkça yer almalıdır.

## Rubrik

| Boyut | Puan |
|---|---:|
| Problem, positive class ve split | 10 |
| Leakage-safe preprocessing | 15 |
| Logistic regression ve regularization | 15 |
| Dengesizlik ve class weight | 10 |
| Metrik doğruluğu | 15 |
| Threshold ve maliyet optimizasyonu | 15 |
| Calibration analizi | 10 |
| Test ve tekrarlanabilirlik | 5 |
| Teknik rapor | 5 |
| **Toplam** | **100** |

## Ek kredi

- Segment bazlı farklı threshold stratejisini etik ve operasyonel riskleriyle tartışmak
- Bootstrap ile threshold metrikleri için güven aralığı üretmek
- Calibration drift izleme planı hazırlamak
