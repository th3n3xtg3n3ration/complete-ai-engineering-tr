# Ödev — Production'a Hazır Mini Inference Servisi

## Amaç

Standart Python kütüphanesi veya seçtiğin hafif bir web framework ile Linux üzerinde çalışabilen, test edilebilir ve gözlemlenebilir küçük bir inference servisi geliştir.

Model matematiksel olarak basit olabilir. Değerlendirme; sistem davranışı, API sözleşmesi, concurrency kontrolü ve hata yönetimine odaklanır.

## Zorunlu gereksinimler

### 1. API

Aşağıdaki endpoint'leri geliştir:

```text
GET  /health
GET  /ready
POST /v1/predictions
GET  /v1/metrics
```

`POST /v1/predictions` en az şu girdiyi kabul etsin:

```json
{"features":[0.3,0.7,0.2]}
```

Başarılı cevap:

```json
{
  "prediction": {
    "label": 0,
    "score": 0.4,
    "model_version": "demo-v1"
  },
  "request_id": "..."
}
```

### 2. Doğrulama ve hata sözleşmesi

- Yalnızca `application/json` kabul et.
- Payload boyutunu sınırla.
- Boş, sayı olmayan, boolean veya finite olmayan feature değerlerini reddet.
- Tüm hataları tutarlı JSON sözleşmesiyle dön.
- Beklenmeyen hatalarda stack trace'i istemciye gönderme.

### 3. Concurrency

- Aktif inference sayısını açık bir sınırla kontrol et.
- Kapasite dolduğunda `503` dön.
- Paylaşılan metrikleri thread-safe biçimde güncelle.
- Sınır ve timeout değerlerini environment variable ile yapılandır.

### 4. Process yaşam döngüsü

- `SIGTERM` veya `KeyboardInterrupt` ile kontrollü kapan.
- Yeni trafiği durdurma ve kaynakları kapatma yaklaşımını README'de açıkla.
- Process'in anlamlı exit code kullanmasını sağla.

### 5. Gözlemlenebilirlik

Her request için en az şu alanları logla:

- request ID
- path
- method
- status code
- latency
- model version

Authorization token, ham feature listesi veya kişisel veri loglama.

`GET /v1/metrics` en az şu sayaçları dönsün:

```json
{
  "requests_total": 10,
  "requests_failed": 2,
  "predictions_total": 7,
  "inflight_predictions": 1
}
```

### 6. Testler

En az 15 otomatik test yaz. Şunları kapsa:

- Health ve readiness
- Başarılı prediction
- Geçersiz JSON
- Yanlış media type
- Boş feature listesi
- Boolean ve `NaN` reddi
- Payload sınırı
- Request ID üretimi ve korunması
- Concurrency limiti
- Thread-safe metrics
- Bilinmeyen route
- Beklenmeyen model hatası
- Graceful shutdown'a ait test edilebilir core davranış

Testler dış internete ihtiyaç duymamalıdır.

## Teslim yapısı

```text
inference-service/
├── README.md
├── pyproject.toml
├── src/
│   └── inference_service/
│       ├── __init__.py
│       ├── api.py
│       ├── config.py
│       ├── model.py
│       ├── metrics.py
│       └── server.py
└── tests/
    ├── test_api.py
    ├── test_config.py
    ├── test_metrics.py
    └── test_model.py
```

## README beklentileri

- Mimari kararlar
- Local çalıştırma komutları
- Environment variable tablosu
- Örnek `curl` çağrıları
- HTTP durum kodları ve hata sözleşmesi
- Concurrency ve backpressure yaklaşımı
- Graceful shutdown açıklaması
- Güvenlik sınırlamaları
- Production'a geçiş için sonraki adımlar

## Bonus görevler

- Idempotency key desteği
- `/v1/prediction-jobs` async iş modeli
- Cursor pagination
- OpenAPI dokümanı
- Containerfile/Dockerfile
- Non-root container kullanıcısı
- Prometheus uyumlu metrics
- Structured JSON logging
- Load test scripti

## Değerlendirme rubriği

| Alan | Puan |
|---|---:|
| API ve REST sözleşmesi | 20 |
| Doğrulama ve hata yönetimi | 15 |
| Concurrency ve thread safety | 20 |
| Process yaşam döngüsü | 10 |
| Test kalitesi | 20 |
| Gözlemlenebilirlik ve güvenlik | 10 |
| Dokümantasyon | 5 |
| **Toplam** | **100** |

## Başarı ölçütü

- **90–100:** Üretim düşüncesi güçlü, kapsamlı ve güvenilir
- **75–89:** Temel gereksinimler doğru, küçük eksikler var
- **60–74:** Çalışıyor fakat concurrency, test veya hata sözleşmesinde önemli eksikler var
- **0–59:** Ana endpoint'ler ya da güvenilirlik gereksinimleri tamamlanmamış
