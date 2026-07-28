# Ödev — Gözlemlenebilir Inference Servisi

## Görev

Küçük bir metin sınıflandırma servisini test edilebilir ve gözlemlenebilir hale getir.

## Zorunlu özellikler

- Girdi doğrulama ve özel exception sınıfları
- Dependency injection ile değiştirilebilir predictor
- En az 8 unit test
- En az 2 parametrik test
- Başarılı ve başarısız akış için log doğrulaması
- Exception chaining
- `cProfile` çıktısı ve kısa darboğaz analizi
- En az bir ölçülmüş optimizasyon
- Hassas veriyi loglamayan alan politikası

## Rubrik

| Ölçüt | Puan |
|---|---:|
| Doğruluk ve hata yönetimi | 20 |
| Test kapsamı ve test kalitesi | 25 |
| Debugging ve regression yaklaşımı | 15 |
| Profiling ve ölçüme dayalı optimizasyon | 15 |
| Logging ve güvenli gözlemlenebilirlik | 15 |
| Kod kalitesi ve dokümantasyon | 10 |
| **Toplam** | **100** |

## Başarı ölçütü

En az 70 puan, tüm testlerin geçmesi ve profiling yorumunun gerçek ölçüme dayanması gerekir.
