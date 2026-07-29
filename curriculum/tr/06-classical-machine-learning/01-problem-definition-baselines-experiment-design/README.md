# Ders 1 — Problem Tanımı, Baseline ve Deney Tasarımı

**Seviye:** L2 · **Tahmini süre:** 22 saat · **Durum:** Tamamlandı

## Öğrenme hedefleri

Bu dersin sonunda:

- Bir ML problemini tahmin birimi, hedef, özellik kullanılabilirliği ve karar zamanı üzerinden tanımlayabileceksin.
- Regresyon, binary classification ve multiclass classification görevlerini doğru biçimde ayırabileceksin.
- Random, temporal ve entity-level split stratejilerini veri üretim sürecine göre seçebileceksin.
- Target leakage, temporal leakage ve entity overlap risklerini deney başlamadan teşhis edebileceksin.
- Mean, median, majority-class ve class-prior baseline modelleri kurabileceksin.
- MAE, RMSE, R², accuracy, balanced accuracy, precision, recall, F1, ROC-AUC ve log loss metriklerini yorumlayabileceksin.
- Birincil metrik, guardrail metrik, başarı eşiği ve metric direction tanımlayabileceksin.
- Bootstrap güven aralığı ve paired bootstrap ile metrik belirsizliğini ölçebileceksin.
- Random seed, split tanımı ve deney kaydıyla tekrarlanabilir deneyler geliştirebileceksin.
- Model geliştirmeye başlamadan önce ölçülebilir ve test edilen bir baseline raporu yayımlayabileceksin.

## Ders dosyaları

1. [Ayrıntılı teori](theory.md)
2. [Uygulama laboratuvarı](lab.md)
3. [Problem tanımı ve split araçları](src/problem_definition.py)
4. [Baseline modeller ve metrikler](src/baselines.py)
5. [Deney konfigürasyonu ve belirsizlik araçları](src/experiment_design.py)
6. [Alıştırmalar](exercises.md)
7. [Quiz](quiz.md)
8. [Ödev ve rubrik](assignment.md)
9. [Mülakat soruları](interview-questions.md)
10. [Testler](tests/test_ml_foundations.py)
11. [Metadata](metadata.yml)

## Kurulum ve çalıştırma

```bash
python -m pip install numpy pandas scikit-learn pytest
python curriculum/tr/06-classical-machine-learning/01-problem-definition-baselines-experiment-design/src/experiment_design.py
pytest curriculum/tr/06-classical-machine-learning/01-problem-definition-baselines-experiment-design/tests -q
```

## Mini proje

Bir müşteri kaybı veya gelir tahmini problemi için üretim öncesi deney paketi geliştireceksin. Paket; açık problem sözleşmesi, random/temporal/entity split seçenekleri, leakage kontrolleri, regresyon ve sınıflandırma baseline'ları, birincil ve guardrail metrikler, bootstrap güven aralığı ve JSON deney kaydı üretecek. Başarı kriteri, geliştirilecek modelin yalnızca yüksek skor vermesi değil; doğru veri bölünmesinde güvenilir biçimde baseline'ı aşması olacak.
