# Ders 4 — Dosya, Paket ve Bağımlılık Yönetimi

**Seviye:** L1 · **Tahmini süre:** 9 saat · **Durum:** Tamamlandı

## Öğrenme hedefleri

Bu dersin sonunda:

- `pathlib` ile taşınabilir dosya yolları oluşturabileceksin.
- Metin, JSON ve CSV dosyalarını güvenli biçimde okuyup yazabileceksin.
- Bir Python projesini paket ve modüllere ayırabileceksin.
- `pyproject.toml` ile proje metadata ve bağımlılıklarını tanımlayabileceksin.
- Sanal ortam, sürüm sabitleme ve yeniden üretilebilir kurulum ilkelerini açıklayabileceksin.
- Dosya tabanlı küçük bir veri hattını test edebileceksin.

## Ders dosyaları

1. [Ayrıntılı teori](theory.md)
2. [Örnek paket](src/data_toolkit/)
3. [Proje yapılandırması](pyproject.toml)
4. [Alıştırmalar](exercises.md)
5. [Quiz](quiz.md)
6. [Ödev ve rubrik](assignment.md)
7. [Mülakat soruları](interview-questions.md)
8. [Otomatik testler](tests/test_storage.py)
9. [Metadata](metadata.yml)

## Çalıştırma

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install -e .[dev]
pytest
```

## Mini proje

Örnek paket, JSON kayıtlarını doğrular, diske atomik biçimde yazar ve tekrar okuyarak özet üretir. Uygulama kodu ile dosya sistemi ayrıldığı için testlerde geçici dizin kullanılabilir.