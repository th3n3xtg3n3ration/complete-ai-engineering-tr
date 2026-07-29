# Ders 1 — Fonksiyonlar, Logaritmalar ve Grafikler

**Seviye:** L1 · **Tahmini süre:** 14 saat · **Durum:** Tamamlandı

## Öğrenme hedefleri

Bu dersin sonunda:

- Fonksiyon, domain, codomain ve range kavramlarını açıklayabileceksin.
- Doğrusal, polinom, üstel ve logaritmik fonksiyonları karşılaştırabileceksin.
- Bileşke ve ters fonksiyonları uygulayabileceksin.
- Grafiklerden eğim, kesişim, büyüme ve doygunluk davranışını okuyabileceksin.
- Logaritma kurallarını loss, olasılık ve ölçekleme problemlerine bağlayabileceksin.
- Sigmoid, tanh, ReLU, softplus ve softmax fonksiyonlarını güvenli biçimde uygulayabileceksin.
- MSE, binary cross-entropy ve categorical cross-entropy hesaplayabileceksin.
- Sayısal türev ile bir fonksiyonun yerel değişim oranını yaklaşık olarak bulabileceksin.
- Aktivasyon ve loss eğrilerini örnekleyerek AI modellerinin davranışını yorumlayabileceksin.

## Ders dosyaları

1. [Ayrıntılı teori](theory.md)
2. [Uygulama laboratuvarı](lab.md)
3. [Fonksiyon ve loss implementasyonları](src/math_functions.py)
4. [Deney ve veri üretim aracı](src/function_experiment.py)
5. [Alıştırmalar](exercises.md)
6. [Quiz](quiz.md)
7. [Ödev ve rubrik](assignment.md)
8. [Mülakat soruları](interview-questions.md)
9. [Testler](tests/test_math_functions.py)
10. [Metadata](metadata.yml)

## Çalıştırma

```bash
python curriculum/tr/04-ai-mathematics/01-functions-logarithms-graphs/src/math_functions.py
python curriculum/tr/04-ai-mathematics/01-functions-logarithms-graphs/src/function_experiment.py
pytest curriculum/tr/04-ai-mathematics/01-functions-logarithms-graphs/tests -q
```

Deney aracı aktivasyon fonksiyonlarını örnekler ve sonuçları standart kütüphane ile CSV dosyasına yazar. Görselleştirme için üretilen CSV herhangi bir notebook, spreadsheet veya plotting aracıyla kullanılabilir.

## Mini proje

Sigmoid, tanh, ReLU ve softplus aktivasyonlarını; MSE ve cross-entropy loss fonksiyonlarını saf Python ile uygulayan bir matematik laboratuvarı geliştireceksin. Laboratuvar, farklı giriş aralıklarında sayısal kararlılığı kontrol edecek, eğri verisi üretecek ve model davranışı hakkında kısa bir teknik rapor sunacak.
