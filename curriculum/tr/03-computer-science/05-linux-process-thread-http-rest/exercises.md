# Alıştırmalar — Linux, Process, Thread, HTTP ve REST

## Seviye A — Temel kavramlar

### 1. Dosya yolu güvenliği

Aşağıdaki kodun çalışma dizinine neden bağımlı olduğunu açıklayıp `pathlib.Path` ile düzelt:

```python
with open("models/model.json") as file:
    model = file.read()
```

### 2. Exit code

`run_command` kullanarak başarılı ve `4` exit code'u ile başarısız olan iki child process çalıştır. Sonucu `CommandResult` olarak raporla.

### 3. Environment doğrulama

`APP_PORT` değerini okuyan bir `read_port()` fonksiyonu yaz. Değer yoksa `8080` kullan; sayı değilse veya `1..65535` aralığında değilse anlaşılır `ValueError` üret.

### 4. HTTP durum kodu eşleştirme

Aşağıdaki durumları uygun kodlarla eşleştir:

- Geçersiz JSON
- Kimlik doğrulama bilgisi yok
- Model henüz yüklenmedi
- İstek rate limit'i aştı
- Async job kabul edildi
- Kaynak bulunamadı

Her seçim için bir cümle gerekçe yaz.

## Seviye B — Uygulama

### 5. Timeout politikası

`run_command` için üç test yaz:

1. Timeout aşılmıyor.
2. Timeout aşılıyor.
3. Komut başarısız oluyor ama timeout olmuyor.

Timeout ile non-zero exit code arasındaki farkı açıklayan kısa not ekle.

### 6. Thread-safe metrik

Aşağıdaki sayaçları lock ile koruyan `ServiceMetrics` sınıfını geliştir:

- `requests_total`
- `requests_failed`
- `predictions_total`

Snapshot metodu mutable iç durumu dışarı sızdırmayan bir dictionary dönsün. En az 1.000 paralel güncelleme içeren test yaz.

### 7. Bounded concurrency

`BoundedSemaphore` kullanarak aynı anda en fazla üç görevin kritik inference bölümüne girdiğini kanıtlayan test yaz. Aktif görev sayısının gözlemlenen maksimumunu kaydet.

### 8. Yeni endpoint

`GET /ready` endpoint'i ekle. `InferenceState` içine `model_loaded: bool` alanı koy. Model hazırsa `200`, değilse `503` dön.

Cevap sözleşmesi:

```json
{"status":"ready","model_version":"demo-v1"}
```

veya:

```json
{
  "error": {
    "code": "MODEL_NOT_READY",
    "message": "model is not ready",
    "request_id": "..."
  }
}
```

### 9. Payload sınırı

`MAX_BODY_BYTES` sınırını aşan bir isteğin `413` döndürdüğünü integration test ile doğrula. Test verisini gereksiz büyütmeden `Content-Length` header'ını kontrollü biçimde kullan.

### 10. Method not allowed

Bilinen bir kaynakta desteklenmeyen HTTP metodu için `405 Method Not Allowed` ve `Allow` header'ı döndür. Örneğin `PUT /health`.

## Seviye C — Tasarım

### 11. Async prediction job

Uzun süren model işlemi için aşağıdaki akışı tasarla:

```text
POST /v1/prediction-jobs
GET  /v1/prediction-jobs/{job_id}
DELETE /v1/prediction-jobs/{job_id}
```

Şunları belirt:

- Request/response şemaları
- `202`, `200`, `404`, `409` ve `422` kullanımları
- Job durum makinesi
- Idempotency key davranışı
- Retention süresi
- Pagination yaklaşımı

### 12. Retry kararı

Aşağıdaki kodlar için istemcinin retry edip etmemesi gerektiğini değerlendir:

- `400`
- `409`
- `422`
- `429`
- `500`
- `503`

Kararı yalnızca koda göre değil, idempotency ve `Retry-After` gibi bağlama göre açıkla.

### 13. Process mi thread mi?

Şu işleri process, thread veya async I/O seçenekleriyle eşleştir:

- Büyük saf Python matris ön işleme
- 500 uzak URL'den metadata çekme
- GPU inference çağrısını bekleme
- Birden fazla bağımsız CPU-bound feature extraction görevi
- Tek process içinde paylaşılan cache ile kısa I/O işleri

Her seçimde GIL, bellek izolasyonu ve hata etkisini tartış.

### 14. Güvenlik incelemesi

Aşağıdaki kodu değerlendir:

```python
subprocess.run(f"cat {user_path}", shell=True)
```

En az dört risk veya tasarım kusuru bul ve argüman listesi, izin kontrolü, path doğrulama ve çıktı sınırı içeren güvenli yaklaşım öner.

### 15. Production geçiş planı

Dersin standart kütüphane HTTP sunucusunu bir production stack'e taşımak için plan yaz. Şunları kapsa:

- ASGI/WSGI framework seçimi
- Process worker modeli
- Reverse proxy
- TLS
- Authentication/authorization
- Metrics, tracing ve logging
- Timeout, retry ve circuit breaker
- Container resource limit'leri
- Health/readiness/liveness
