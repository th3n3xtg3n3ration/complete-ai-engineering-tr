# Ders 5 — SVM, Margin, Kernel ve Ölçekleme

**Seviye:** L2–L3 · **Tahmini süre:** 30 saat · **Durum:** Tamamlandı

Bu ders, destek vektör makinelerini yalnızca scikit-learn API düzeyinde değil; geometrik sezgi, primal–dual optimizasyon, kernel trick, ölçekleme, model seçimi ve üretim kararlarıyla birlikte ele alır.

## Öğrenme çıktıları

Bu dersin sonunda:

- Hiper-düzlem, functional margin ve geometric margin kavramlarını ayırabileceksin.
- Hard-margin ve soft-margin SVM problemlerini formüle edebileceksin.
- Slack variable, hinge loss ve `C` hiperparametresi arasındaki ilişkiyi açıklayabileceksin.
- Lagrangian, dual problem ve KKT koşullarının support vector kavramına nasıl yol açtığını yorumlayabileceksin.
- Linear, polynomial ve RBF kernel fonksiyonlarını hem matematiksel hem kod düzeyinde uygulayabileceksin.
- Gram matrix, positive semidefinite kernel ve Mercer koşulu hakkında doğru sezgi kurabileceksin.
- `C`, `gamma`, degree ve `coef0` parametrelerinin bias–variance dengesi üzerindeki etkisini analiz edebileceksin.
- Feature scaling'in LinearSVC ve kernel SVM üzerindeki etkisini leakage oluşturmadan gösterebileceksin.
- OvR ve OvO çok sınıflı stratejileri, class weight, calibration ve threshold tuning kararlarını ayırabileceksin.
- Grid search, validation curve ve nested cross-validation içeren güvenilir bir SVM pipeline geliştirebileceksin.

## Konu haritası

1. Sınıflandırma geometrisi ve hiper-düzlemler
2. Functional ve geometric margin
3. Hard margin ve soft margin
4. Slack variables, hinge loss ve regularization
5. Primal problem, Lagrangian, dual problem ve KKT
6. Support vectors ve karar fonksiyonu
7. Kernel trick, Gram matrix ve Mercer sezgisi
8. Linear, polynomial ve RBF kernel
9. `C`, `gamma`, degree ve `coef0`
10. Feature scaling ve sparse veri
11. LinearSVC, SVC ve SGDClassifier karşılaştırması
12. OvR ve OvO çok sınıflı stratejiler
13. Class imbalance ve class weight
14. Probability calibration ve threshold tuning
15. Grid search, validation curve ve nested CV
16. Hesaplama maliyeti, hata analizi ve üretim sınırları

## Ders dosyaları

1. [Ayrıntılı teori](theory.md)
2. [Uygulama laboratuvarı](lab.md)
3. [Kernel ve margin araçları](src/kernel_functions.py)
4. [SVM model araçları](src/svm_models.py)
5. [Leakage-safe SVM pipeline](src/svm_pipeline.py)
6. [Alıştırmalar](exercises.md)
7. [Quiz](quiz.md)
8. [Ödev ve rubrik](assignment.md)
9. [Mülakat soruları](interview-questions.md)
10. [Otomatik testler](tests/test_svm.py)
11. [Metadata](metadata.yml)

## Mini proje

Bir dolandırıcılık veya kalite kontrol problemi için linear ve RBF SVM modellerini karşılaştır. Proje şu bileşenleri içermelidir:

- leakage-safe preprocessing,
- scaling ablation,
- `C` ve `gamma` araması,
- class weight karşılaştırması,
- ROC-AUC ve average precision,
- sigmoid veya isotonic calibration,
- validation üzerinde threshold seçimi,
- support vector oranı,
- segment bazlı hata analizi,
- üretim maliyeti ve ölçeklenebilirlik değerlendirmesi.

## Çalıştırma

```bash
python -m pip install numpy pandas scikit-learn pytest
pytest curriculum/tr/06-classical-machine-learning/05-svm-margin-kernel-scaling/tests -q
```

## Başarı ölçütü

Ders tamamlandığında öğrenci yalnızca bir `SVC` nesnesi kurmamalı; seçilen kernel ve hiperparametrelerin matematiksel, istatistiksel ve operasyonel sonuçlarını gerekçelendirebilmelidir.
