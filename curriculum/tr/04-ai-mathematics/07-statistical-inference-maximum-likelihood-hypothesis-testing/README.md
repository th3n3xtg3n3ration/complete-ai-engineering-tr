# Ders 7 — İstatistiksel Çıkarım, Maximum Likelihood ve Hipotez Testi

**Seviye:** L2 · **Tahmini süre:** 22 saat · **Durum:** Tamamlandı

## Öğrenme hedefleri

Bu dersin sonunda:

- Evren, örneklem, parametre, istatistik ve sampling distribution kavramlarını ayırt edebileceksin.
- Tahmin edicileri bias, variance, consistency ve efficiency açısından değerlendirebileceksin.
- Standard error ve confidence interval hesaplayıp doğru yorumlayabileceksin.
- Bootstrap ile belirsizlik tahmini ve güven aralığı üretebileceksin.
- Likelihood ve log-likelihood fonksiyonlarını model parametreleri için kurabileceksin.
- Bernoulli ve Gaussian modellerinde maximum likelihood estimation uygulayabileceksin.
- MLE ile MAP tahminini karşılaştırabileceksin.
- Null hypothesis, alternative hypothesis, test statistic, p-value ve significance level kavramlarını açıklayabileceksin.
- Type I/II error, statistical power, effect size ve sample size ilişkisini yorumlayabileceksin.
- Tek örneklem ve iki örneklem testleri ile permutation test uygulayabileceksin.
- Multiple testing problemine Bonferroni ve Benjamini–Hochberg düzeltmeleri uygulayabileceksin.
- A/B testlerinde peeking, selection bias, leakage ve pratik anlamlılık hatalarını teşhis edebileceksin.

## Ders dosyaları

1. [Ayrıntılı teori](theory.md)
2. [Uygulama laboratuvarı](lab.md)
3. [İstatistiksel çıkarım araçları](src/statistical_inference.py)
4. [Maximum likelihood uygulamaları](src/maximum_likelihood.py)
5. [Hipotez testi ve A/B test araçları](src/hypothesis_testing.py)
6. [Alıştırmalar](exercises.md)
7. [Quiz](quiz.md)
8. [Ödev ve rubrik](assignment.md)
9. [Mülakat soruları](interview-questions.md)
10. [Testler](tests/test_statistical_inference.py)
11. [Metadata](metadata.yml)

## Çalıştırma

```bash
python curriculum/tr/04-ai-mathematics/07-statistical-inference-maximum-likelihood-hypothesis-testing/src/statistical_inference.py
python curriculum/tr/04-ai-mathematics/07-statistical-inference-maximum-likelihood-hypothesis-testing/src/maximum_likelihood.py
python curriculum/tr/04-ai-mathematics/07-statistical-inference-maximum-likelihood-hypothesis-testing/src/hypothesis_testing.py
pytest curriculum/tr/04-ai-mathematics/07-statistical-inference-maximum-likelihood-hypothesis-testing/tests -q
```

## Mini proje

Saf Python ile yeniden kullanılabilir bir A/B test analiz paketi geliştirecek; dönüşüm oranı ve sürekli metrikler için etki büyüklüğü, güven aralığı, p-value, statistical power, permutation test ve multiple-testing düzeltmelerini raporlayacaksın. Aynı deney üzerinde erken bakma, dengesiz örneklem ve yalnızca p-value odaklı kararların nasıl hatalı sonuç üretebildiğini teknik bir raporla göstereceksin.
