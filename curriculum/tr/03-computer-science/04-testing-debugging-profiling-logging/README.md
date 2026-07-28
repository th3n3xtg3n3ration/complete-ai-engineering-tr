# Ders 4 — Test, Debugging, Profiling ve Logging

**Seviye:** L2 · **Tahmini süre:** 14 saat · **Durum:** Tamamlandı

## Öğrenme hedefleri

Bu dersin sonunda:

- Unit, integration ve regression testlerini ayırt edebileceksin.
- pytest ile fixture, parametrization ve exception testleri yazabileceksin.
- Mock ve dependency injection ile dış bağımlılıkları izole edebileceksin.
- Sistematik debugging yapabileceksin.
- `timeit`, `cProfile` ve `pstats` ile performans darboğazlarını inceleyebileceksin.
- Python logging seviyeleri, handler ve structured logging yaklaşımını uygulayabileceksin.
- AI servislerinde gözlemlenebilirlik ve hata teşhisi için temel bir çalışma akışı kurabileceksin.

## Ders dosyaları

1. [Ayrıntılı teori](theory.md)
2. [Uygulama laboratuvarı](lab.md)
3. [Gözlemlenebilir örnek servis](src/observable_service.py)
4. [Profiling aracı](src/profile_service.py)
5. [Alıştırmalar](exercises.md)
6. [Quiz](quiz.md)
7. [Ödev ve rubrik](assignment.md)
8. [Mülakat soruları](interview-questions.md)
9. [Testler](tests/test_observable_service.py)
10. [Metadata](metadata.yml)

## Çalıştırma

```bash
python curriculum/tr/03-computer-science/04-testing-debugging-profiling-logging/src/observable_service.py
python curriculum/tr/03-computer-science/04-testing-debugging-profiling-logging/src/profile_service.py
pytest curriculum/tr/03-computer-science/04-testing-debugging-profiling-logging/tests -q
```

## Mini proje

Bir model inference servisinin tahmin, doğrulama, hata yönetimi, structured logging, test ve profiling katmanlarını geliştirerek sorun teşhis edilebilir küçük bir servis oluşturacaksın.
