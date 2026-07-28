# Ödev — AI Pipeline Scheduler

Bir AI pipeline scheduler geliştir.

## Gereksinimler

- Görev bağımlılıklarını directed graph ile modelle.
- Topological sort ile çalışma sırası üret.
- Cycle olduğunda açıklayıcı hata döndür.
- Görevleri öncelik kuyruğuna aktar.
- Aynı öncelikte kararlı sıra sağla.
- En az 12 unit test yaz.
- Type hint, docstring ve hata yönetimi kullan.

## Teslim çıktıları

- `scheduler.py`
- `test_scheduler.py`
- Mimari kararları açıklayan kısa `README.md`
- Zaman ve alan karmaşıklığı analizi

## Rubrik

| Ölçüt | Puan |
|---|---:|
| Graph ve bağımlılık modeli | 25 |
| Topological sort ve cycle detection | 25 |
| Priority queue entegrasyonu | 20 |
| Test kalitesi ve kenar durumları | 20 |
| Kod kalitesi ve dokümantasyon | 10 |
| **Toplam** | **100** |
