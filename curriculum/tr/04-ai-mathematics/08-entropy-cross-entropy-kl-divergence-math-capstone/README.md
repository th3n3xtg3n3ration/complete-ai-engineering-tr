# Ders 8 — Entropi, Cross-Entropy, KL Divergence ve Matematik Capstone

**Seviye:** L2 · **Tahmini süre:** 24 saat · **Durum:** Tamamlandı

## Öğrenme hedefleri

Bu dersin sonunda:

- Bilgi miktarı, surprisal ve entropi kavramlarını olasılık dağılımları üzerinden açıklayabileceksin.
- Binary ve categorical entropy hesaplayabileceksin.
- Cross-entropy ile negative log-likelihood arasındaki ilişkiyi kurabileceksin.
- KL divergence'ın yönlü olduğunu ve bir uzaklık metriği olmadığını açıklayabileceksin.
- Jensen–Shannon divergence ve mutual information hesaplayabileceksin.
- Softmax, log-softmax ve log-sum-exp işlemlerini sayısal kararlı biçimde uygulayabileceksin.
- Binary ve multiclass classification loss fonksiyonlarını saf Python ile geliştirebileceksin.
- Label smoothing, focal loss, class weighting ve calibration kavramlarını yorumlayabileceksin.
- Perplexity değerini dil modeli belirsizliğiyle ilişkilendirebileceksin.
- Lineer cebir, türev, olasılık, optimizasyon ve bilgi teorisini bir softmax regression capstone projesinde birleştirebileceksin.

## Ders dosyaları

1. [Ayrıntılı teori](theory.md)
2. [Uygulama laboratuvarı](lab.md)
3. [Bilgi teorisi araçları](src/information_theory.py)
4. [Classification loss fonksiyonları](src/classification_losses.py)
5. [Matematik capstone uygulaması](src/math_capstone.py)
6. [Alıştırmalar](exercises.md)
7. [Quiz](quiz.md)
8. [Ödev ve rubrik](assignment.md)
9. [Mülakat soruları](interview-questions.md)
10. [Testler](tests/test_information_theory.py)
11. [Metadata](metadata.yml)

## Çalıştırma

```bash
python curriculum/tr/04-ai-mathematics/08-entropy-cross-entropy-kl-divergence-math-capstone/src/information_theory.py
python curriculum/tr/04-ai-mathematics/08-entropy-cross-entropy-kl-divergence-math-capstone/src/classification_losses.py
python curriculum/tr/04-ai-mathematics/08-entropy-cross-entropy-kl-divergence-math-capstone/src/math_capstone.py
pytest curriculum/tr/04-ai-mathematics/08-entropy-cross-entropy-kl-divergence-math-capstone/tests -q
```

## Mini proje

Saf Python ile çok sınıflı bir softmax regression sistemi geliştirecek; modeli cross-entropy ve L2 regularization ile eğitecek; gradient descent, sayısal kararlılık, calibration, entropy, KL divergence ve confusion matrix ölçümlerini tek bir teknik raporda birleştireceksin. Deneylerde learning rate, label smoothing ve class imbalance ayarlarının loss, accuracy, confidence ve calibration üzerindeki etkisini karşılaştıracaksın.
