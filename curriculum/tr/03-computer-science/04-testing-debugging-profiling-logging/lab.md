# Laboratuvar — Gözlemlenebilir Model Servisi

## Amaç

Test edilebilir, log üreten ve profillenebilen küçük bir inference servisi geliştir.

## Adım 1 — Servisi incele

`src/observable_service.py` içindeki `ModelService` sınıfını çalıştır. Girdi doğrulama, dependency injection ve latency ölçümünün nerede yapıldığını belirle.

## Adım 2 — Unit testleri çalıştır

```bash
pytest tests -q
```

Başarılı tahmin, hatalı girdi, model hatası ve dependency davranışlarını doğrula.

## Adım 3 — Yeni parametrik test ekle

Boş metin, yalnızca boşluk içeren metin ve maksimum sınırı aşan metin için tek bir parametrik test yaz.

## Adım 4 — Hata ayıklama

`predictor` bağımlılığını kasıtlı olarak exception fırlatacak biçimde değiştir. Stack trace'i incele ve servisin hangi log olayını ürettiğini kaydet.

## Adım 5 — Profiling

```bash
python src/profile_service.py
```

Çıktıda cumulative time'a göre en pahalı fonksiyonları belirle. En az bir optimizasyon hipotezi yaz; ölçmeden kodu değiştirme.

## Adım 6 — Structured context

Her tahmine `request_id` ve `model_version` ekle. Hassas girdi içeriğini loglamadan input uzunluğunu kaydet.

## Teslim

- Eklenen testler
- Profiling çıktısının kısa yorumu
- Bir regression testi
- Güvenli log alanları listesi
