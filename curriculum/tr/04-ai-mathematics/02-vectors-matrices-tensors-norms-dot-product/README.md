# Ders 2 — Vektörler, Matrisler, Tensörler, Normlar ve Dot Product

**Seviye:** L1–L2 · **Tahmini süre:** 16 saat · **Durum:** Tamamlandı

## Öğrenme hedefleri

Bu dersin sonunda:

- Skaler, vektör, matris ve tensör kavramlarını birbirinden ayırabileceksin.
- Shape, rank, axis ve broadcasting kavramlarını açıklayabileceksin.
- Vektör toplama, skaler çarpma, dot product ve outer product işlemlerini uygulayabileceksin.
- Matris toplama, transpose ve matrix multiplication işlemlerini boyut kontrolüyle gerçekleştirebileceksin.
- L1, L2 ve infinity normlarını hesaplayıp kullanım farklarını yorumlayabileceksin.
- Euclidean distance ve cosine similarity metriklerini karşılaştırabileceksin.
- Vektör normalizasyonunun embedding araması ve model eğitimindeki etkisini açıklayabileceksin.
- Saf Python ile küçük bir lineer cebir yardımcı kütüphanesi geliştirebileceksin.
- AI verilerinde batch, feature, sequence ve channel eksenlerini okuyabileceksin.

## Ders dosyaları

1. [Ayrıntılı teori](theory.md)
2. [Uygulama laboratuvarı](lab.md)
3. [Saf Python lineer cebir kütüphanesi](src/linear_algebra.py)
4. [Embedding benzerlik deneyi](src/embedding_experiment.py)
5. [Alıştırmalar](exercises.md)
6. [Quiz](quiz.md)
7. [Ödev ve rubrik](assignment.md)
8. [Mülakat soruları](interview-questions.md)
9. [Testler](tests/test_linear_algebra.py)
10. [Metadata](metadata.yml)

## Çalıştırma

```bash
python curriculum/tr/04-ai-mathematics/02-vectors-matrices-tensors-norms-dot-product/src/linear_algebra.py
python curriculum/tr/04-ai-mathematics/02-vectors-matrices-tensors-norms-dot-product/src/embedding_experiment.py
pytest curriculum/tr/04-ai-mathematics/02-vectors-matrices-tensors-norms-dot-product/tests -q
```

Embedding deneyi, sorgu vektörü ile aday doküman vektörlerini cosine similarity ve Euclidean distance kullanarak sıralar ve sonuçları CSV dosyasına yazar.

## Mini proje

Saf Python ile shape doğrulaması yapan küçük bir lineer cebir kütüphanesi geliştirecek; ardından bu kütüphaneyi kullanarak embedding tabanlı bir benzerlik arama sistemi kuracaksın. Sistem, farklı normalizasyon stratejilerinin sıralama sonuçlarına etkisini teknik bir raporla karşılaştıracak.
