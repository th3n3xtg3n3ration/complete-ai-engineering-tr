# Ders 4 — Türev, Kısmi Türev, Zincir Kuralı, Jacobian ve Hessian

**Seviye:** L2 · **Tahmini süre:** 18 saat · **Durum:** Tamamlandı

## Öğrenme hedefleri

Bu dersin sonunda:

- Türevi anlık değişim oranı ve eğim olarak açıklayabileceksin.
- Analitik ve sayısal türev arasındaki farkı yorumlayabileceksin.
- Kısmi türev ve gradient kavramlarını çok değişkenli fonksiyonlarda uygulayabileceksin.
- Zincir kuralını hesaplama grafikleri ve backpropagation ile ilişkilendirebileceksin.
- Directional derivative ve gradient yönünü açıklayabileceksin.
- Jacobian matrisini vektör değerli fonksiyonlar için hesaplayabileceksin.
- Hessian matrisini eğrilik, minimum ve saddle point analiziyle ilişkilendirebileceksin.
- Finite-difference gradient checking uygulayabileceksin.
- Saf Python ile küçük bir otomatik türev motoru geliştirebileceksin.

## Ders dosyaları

1. [Ayrıntılı teori](theory.md)
2. [Uygulama laboratuvarı](lab.md)
3. [Sayısal diferansiyasyon araçları](src/calculus.py)
4. [Mini otomatik türev motoru](src/autodiff.py)
5. [Gradient checking deneyi](src/gradient_check.py)
6. [Alıştırmalar](exercises.md)
7. [Quiz](quiz.md)
8. [Ödev ve rubrik](assignment.md)
9. [Mülakat soruları](interview-questions.md)
10. [Testler](tests/test_calculus_and_autodiff.py)
11. [Metadata](metadata.yml)

## Çalıştırma

```bash
python curriculum/tr/04-ai-mathematics/04-derivatives-chain-rule-jacobian-hessian/src/calculus.py
python curriculum/tr/04-ai-mathematics/04-derivatives-chain-rule-jacobian-hessian/src/autodiff.py
python curriculum/tr/04-ai-mathematics/04-derivatives-chain-rule-jacobian-hessian/src/gradient_check.py
pytest curriculum/tr/04-ai-mathematics/04-derivatives-chain-rule-jacobian-hessian/tests -q
```

## Mini proje

Saf Python ile skaler hesaplama grafiği kuran küçük bir otomatik türev motoru geliştirecek; analitik gradient sonuçlarını finite-difference gradient checking ile doğrulayacak ve basit bir iki değişkenli loss yüzeyinde gradient ile Hessian davranışını teknik bir raporla inceleyeceksin.
