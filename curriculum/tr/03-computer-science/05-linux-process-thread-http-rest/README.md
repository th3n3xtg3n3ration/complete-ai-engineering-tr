# Ders 5 — Linux, Process, Thread, HTTP ve REST Temelleri

**Seviye:** L2 · **Tahmini süre:** 16 saat · **Durum:** Tamamlandı

## Öğrenme hedefleri

Bu dersin sonunda:

- Linux dosya sistemi, izinler, environment variable ve temel shell araçlarını kullanabileceksin.
- Process, thread, concurrency ve parallelism kavramlarını ayırt edebileceksin.
- Python'da `subprocess`, `threading` ve `concurrent.futures` ile güvenli iş akışları kurabileceksin.
- Race condition, lock, deadlock ve graceful shutdown risklerini açıklayabileceksin.
- HTTP request/response yapısını, metotları, durum kodlarını ve header'ları okuyabileceksin.
- REST kaynak modelleme, idempotency, pagination, versioning ve hata sözleşmeleri tasarlayabileceksin.
- AI inference servisleri için küçük, test edilebilir bir HTTP API geliştirebileceksin.

## Ders dosyaları

1. [Ayrıntılı teori](theory.md)
2. [Uygulama laboratuvarı](lab.md)
3. [Linux ve concurrency yardımcıları](src/system_inspector.py)
4. [Standart kütüphane ile inference HTTP API](src/http_api.py)
5. [Alıştırmalar](exercises.md)
6. [Quiz](quiz.md)
7. [Ödev ve rubrik](assignment.md)
8. [Mülakat soruları](interview-questions.md)
9. [Testler](tests/test_systems_and_http.py)
10. [Metadata](metadata.yml)

## Çalıştırma

```bash
python curriculum/tr/03-computer-science/05-linux-process-thread-http-rest/src/system_inspector.py
python curriculum/tr/03-computer-science/05-linux-process-thread-http-rest/src/http_api.py
pytest curriculum/tr/03-computer-science/05-linux-process-thread-http-rest/tests -q
```

API varsayılan olarak `127.0.0.1:8080` üzerinde çalışır:

```bash
curl -s http://127.0.0.1:8080/health
curl -s -X POST http://127.0.0.1:8080/v1/predictions \
  -H 'Content-Type: application/json' \
  -d '{"features": [0.2, 0.7, 0.1]}'
```

## Mini proje

Linux üzerinde çalışan, kontrollü concurrency kullanan ve `/health` ile `/v1/predictions` uç noktalarını sunan küçük bir AI inference servisi geliştireceksin. Servis; doğrulama, tutarlı JSON hata cevapları, request ID, timeout yaklaşımı ve graceful shutdown ilkelerini uygulayacak.
