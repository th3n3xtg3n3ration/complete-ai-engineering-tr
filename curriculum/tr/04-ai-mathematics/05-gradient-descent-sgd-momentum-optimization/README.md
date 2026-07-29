# Ders 5 — Gradient Descent, SGD, Momentum ve Optimizasyon

**Seviye:** L2 · **Tahmini süre:** 20 saat · **Durum:** Tamamlandı

## Öğrenme hedefleri

Bu dersin sonunda:

- Optimizasyon problemini amaç fonksiyonu, parametreler ve kısıtlar üzerinden tanımlayabileceksin.
- Gradient descent güncelleme kuralını türev ve zincir kuralıyla ilişkilendirebileceksin.
- Batch, stochastic ve mini-batch gradient descent yaklaşımlarını karşılaştırabileceksin.
- Learning rate, batch size ve initialization seçiminin eğitim dinamiklerine etkisini yorumlayabileceksin.
- Momentum ve Nesterov momentum algoritmalarını saf Python ile uygulayabileceksin.
- AdaGrad, RMSProp ve Adam optimizasyon algoritmalarının temel fikirlerini açıklayabileceksin.
- Gradient clipping, early stopping ve learning-rate schedule uygulayabileceksin.
- Convex, non-convex, ill-conditioned ve saddle-point loss yüzeylerini analiz edebileceksin.
- Linear regression modelini farklı optimizer'larla eğitip yakınsama davranışlarını karşılaştırabileceksin.
- Eğitim günlüklerinden divergence, oscillation, vanishing update ve overfitting belirtilerini teşhis edebileceksin.

## Ders dosyaları

1. [Ayrıntılı teori](theory.md)
2. [Uygulama laboratuvarı](lab.md)
3. [Optimizer implementasyonları](src/optimizers.py)
4. [Linear regression deneyi](src/regression_experiment.py)
5. [Optimizasyon tanılama araçları](src/optimization_diagnostics.py)
6. [Alıştırmalar](exercises.md)
7. [Quiz](quiz.md)
8. [Ödev ve rubrik](assignment.md)
9. [Mülakat soruları](interview-questions.md)
10. [Testler](tests/test_optimizers.py)
11. [Metadata](metadata.yml)

## Çalıştırma

```bash
python curriculum/tr/04-ai-mathematics/05-gradient-descent-sgd-momentum-optimization/src/optimizers.py
python curriculum/tr/04-ai-mathematics/05-gradient-descent-sgd-momentum-optimization/src/regression_experiment.py
python curriculum/tr/04-ai-mathematics/05-gradient-descent-sgd-momentum-optimization/src/optimization_diagnostics.py
pytest curriculum/tr/04-ai-mathematics/05-gradient-descent-sgd-momentum-optimization/tests -q
```

## Mini proje

Saf Python ile modüler bir optimizer kütüphanesi geliştirecek; sentetik bir linear regression problemini Gradient Descent, SGD, Momentum, RMSProp ve Adam ile eğitecek; convergence speed, final loss, gradient norm, update norm ve kararlılık ölçümlerini teknik bir raporda karşılaştıracaksın.
