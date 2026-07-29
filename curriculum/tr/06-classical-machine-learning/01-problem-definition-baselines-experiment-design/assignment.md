# Ödev — Modelden Önce Deney Sözleşmesi

## Senaryo

Bir abonelik şirketi, gelecek 30 gün içinde churn edecek müşterileri önceden belirlemek istiyor. Veri setinde müşteri profili, ödeme geçmişi, destek kayıtları ve abonelik durumu bulunuyor.

## Görev

Üretime alınabilir bir ML deneyinin model öncesi katmanını geliştir.

Teslimat şunları içermelidir:

1. Problem statement ve karar akışı
2. Prediction unit, observation window ve prediction horizon
3. Target ve positive class tanımı
4. Feature availability tablosu
5. Leakage risk kaydı
6. Random, temporal ve entity split karşılaştırması
7. Majority ve class-prior baseline
8. Birincil ve guardrail metrikler
9. Bootstrap güven aralığı
10. JSON deney kaydı
11. En az 15 otomatik test
12. Sonraki model için açık başarı kriteri

## Zorunlu başarı kriteri

Önerilecek sonraki model:

- temporal veya entity-safe evaluation üzerinde baseline'ı aşmalı,
- guardrail eşiğini ihlal etmemeli,
- iyileşmenin belirsizliği raporlanmalı,
- aynı seed ve dataset sürümüyle tekrar üretilebilmelidir.

## Rubrik

| Boyut | Puan |
|---|---:|
| Problem ve karar tanımı | 15 |
| Hedef, horizon ve feature availability | 15 |
| Split ve leakage güvenliği | 20 |
| Baseline ve metrik doğruluğu | 15 |
| Belirsizlik analizi | 10 |
| Tekrarlanabilirlik ve deney kaydı | 10 |
| Test kalitesi | 10 |
| Teknik rapor | 5 |
| **Toplam** | **100** |

## Ek kredi

- Mevcut iş kuralı baseline'ı eklemek
- Slice bazlı baseline performansı raporlamak
- Metrik farkı için paired bootstrap kullanmak
- Dataset fingerprint veya commit SHA kaydetmek
