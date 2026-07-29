# Ders 6 — Olasılık, Dağılımlar, Beklenti, Varyans ve Bayes

**Seviye:** L2 · **Tahmini süre:** 20 saat · **Durum:** Tamamlandı

## Öğrenme hedefleri

Bu dersin sonunda:

- Örnek uzay, olay, birleşim, kesişim ve tümleyen kavramlarını modelleyebileceksin.
- Koşullu olasılık, bağımsızlık ve toplam olasılık kuralını uygulayabileceksin.
- Ayrık ve sürekli rassal değişkenleri ayırt edebileceksin.
- Bernoulli, Binomial, Categorical, Uniform, Normal, Exponential ve Poisson dağılımlarını AI problemleriyle ilişkilendirebileceksin.
- Beklenti, varyans, standart sapma, covariance ve correlation hesaplayabileceksin.
- Law of Large Numbers ve Central Limit Theorem davranışını simülasyonla gözlemleyebileceksin.
- Bayes teoremini prior, likelihood, evidence ve posterior bileşenleriyle kurabileceksin.
- Naive Bayes sınıflandırıcısını log-olasılıklarla saf Python kullanarak geliştirebileceksin.
- Monte Carlo tahmini, sampling ve calibration kavramlarını yorumlayabileceksin.
- Sayısal kararlılık, veri sızıntısı ve yanlış bağımsızlık varsayımlarını teşhis edebileceksin.

## Ders dosyaları

1. [Ayrıntılı teori](theory.md)
2. [Uygulama laboratuvarı](lab.md)
3. [Olasılık ve dağılım araçları](src/probability.py)
4. [Bayes ve Naive Bayes](src/bayes.py)
5. [Simülasyon deneyleri](src/simulation_experiment.py)
6. [Alıştırmalar](exercises.md)
7. [Quiz](quiz.md)
8. [Ödev ve rubrik](assignment.md)
9. [Mülakat soruları](interview-questions.md)
10. [Testler](tests/test_probability_and_bayes.py)
11. [Metadata](metadata.yml)

## Çalıştırma

```bash
python curriculum/tr/04-ai-mathematics/06-probability-distributions-expectation-variance-bayes/src/probability.py
python curriculum/tr/04-ai-mathematics/06-probability-distributions-expectation-variance-bayes/src/bayes.py
python curriculum/tr/04-ai-mathematics/06-probability-distributions-expectation-variance-bayes/src/simulation_experiment.py
pytest curriculum/tr/04-ai-mathematics/06-probability-distributions-expectation-variance-bayes/tests -q
```

## Mini proje

Saf Python ile log-uzayında çalışan bir Gaussian Naive Bayes sınıflandırıcısı geliştirecek; sentetik veri üzerinde prior seçimi, sınıf dengesizliği, calibration ve karar eşiği etkilerini inceleyecek; sonuçları accuracy, log-loss, confusion matrix ve posterior güvenilirliği üzerinden teknik bir raporda karşılaştıracaksın.
