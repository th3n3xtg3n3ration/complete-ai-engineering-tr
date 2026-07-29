# Teori — Logistic Regression, Threshold ve Calibration

## 1. Sınıflandırma problemi

Binary classification, her gözlem için `0` veya `1` hedefini tahmin eder. Model yalnızca sınıf etiketi değil, karar vermede kullanılabilecek bir olasılık üretmelidir. Olasılık ile son karar birbirinden ayrıdır: model `p(y=1|x)` üretir, iş sistemi bu olasılığı bir threshold ile etikete dönüştürür.

## 2. Odds, log-odds ve sigmoid

Bir olayın olasılığı `p` ise odds değeri `p / (1-p)` olur. Logistic regression, özelliklerin doğrusal kombinasyonunu log-odds olarak modeller:

`log(p / (1-p)) = b + w₁x₁ + ... + wₙxₙ`

Sigmoid fonksiyonu doğrusal skoru `[0, 1]` aralığına taşır:

`σ(z) = 1 / (1 + exp(-z))`

Katsayının işareti log-odds yönünü, `exp(w)` değeri ise diğer değişkenler sabitken odds ratio'yu ifade eder.

## 3. Maximum likelihood ve log loss

Model parametreleri gözlenen etiketlerin olasılığını en yüksek yapan değerler olarak seçilir. Bu hedefi minimize edilen binary cross-entropy biçiminde yazabiliriz:

`L = -mean[y log(p) + (1-y) log(1-p)]`

Log loss, yanlış ve aşırı güvenli tahminleri güçlü biçimde cezalandırır. Probability clipping sayısal taşmayı önler.

## 4. Gradient descent

Gradient descent, katsayıları loss gradyanının ters yönünde günceller. Learning rate çok yüksekse optimizasyon salınır; çok düşükse eğitim gereksiz uzar. Convergence tolerance ve maksimum iterasyon birlikte kullanılmalıdır.

## 5. Regularization

L2 regularization katsayıları küçültür ve yüksek varyansı azaltır. L1 regularization bazı katsayıları tam sıfıra iterek seyrek çözümler üretebilir. scikit-learn'deki `C`, regularization gücünün tersidir: küçük `C`, daha güçlü regularization demektir.

Ölçeklenmemiş özellikler regularization cezasını adaletsiz dağıtır. Bu nedenle sayısal kolonlar eğitim fold'u içinde ölçeklenmelidir.

## 6. Sınıf dengesizliği

Accuracy, çoğunluk sınıfını sürekli tahmin eden bir modelde yanıltıcı olabilir. Balanced accuracy sınıf başına recall ortalamasını alır. Precision, pozitif tahminlerin doğruluğunu; recall, gerçek pozitiflerin yakalanma oranını ölçer. F1, precision ve recall'ın harmonik ortalamasıdır.

`class_weight="balanced"`, azınlık sınıfının loss içindeki etkisini yükseltir. Bu yöntem threshold seçiminin yerine geçmez; eğitim hedefini değiştirir.

## 7. ROC-AUC ve average precision

ROC-AUC, rastgele seçilen pozitif örneğin negatif örnekten daha yüksek skor alma olasılığı olarak yorumlanabilir. Average precision, özellikle pozitif sınıf seyrekken precision-recall eğrisini özetler. Bu metrikler ranking kalitesini ölçer; tek başına üretim threshold'unu belirlemez.

## 8. Threshold seçimi

Varsayılan `0.5` eşiği, iş maliyetlerinin simetrik olduğunu varsayar. Fraud kaçırmanın maliyeti yanlış alarmdan daha yüksekse eşik düşürülebilir. Threshold seçimi yalnızca validation verisinde yapılmalı, test verisi son doğrulama için saklanmalıdır.

Yaygın stratejiler:

- F1 veya balanced accuracy maksimumu
- Minimum recall altında en yüksek precision
- Minimum precision altında en yüksek recall
- Yanlış pozitif ve yanlış negatif maliyetlerinin minimumu
- Operasyon kapasitesine göre maksimum pozitif hacmi

## 9. Probability calibration

İyi kalibre edilmiş bir modelin `0.8` olasılık verdiği örneklerin yaklaşık yüzde 80'i pozitif olmalıdır. ROC-AUC yüksek olsa bile olasılıklar kötü kalibre edilmiş olabilir.

Brier score, olasılık ile etiket arasındaki karesel hatadır. Reliability diagram tahmin olasılığı ile gözlenen event rate'i karşılaştırır. Expected calibration error, bin bazlı mutlak farkların ağırlıklı ortalamasıdır.

## 10. Platt scaling ve isotonic regression

Platt scaling, model skorları üzerinde ikinci bir logistic regression fit eder ve düşük veri hacminde daha kararlıdır. Isotonic regression monoton ancak parametrik olmayan bir dönüşüm öğrenir; daha esnektir fakat küçük calibration setlerinde overfit olabilir.

Calibration modeli training verisinin aynısında fit edilmemelidir. `CalibratedClassifierCV`, fold tabanlı out-of-fold skorlarla bu riski azaltır.

## 11. Leakage-safe pipeline

İmputation, scaling ve encoding yalnızca training fold'unda öğrenilmelidir. `ColumnTransformer` ve `Pipeline`, preprocessing adımlarını model ve cross-validation ile birlikte paketler. Calibration da pipeline'ın dışından, clone edilmiş estimator ve CV ile uygulanmalıdır.

## 12. Üretim raporu

Bir binary classification raporu en az şunları içermelidir:

- veri ve split sürümü,
- positive class tanımı,
- prevalence,
- ROC-AUC ve average precision,
- seçilen threshold ve seçim kuralı,
- confusion matrix,
- precision, recall, F1 ve balanced accuracy,
- yanlış karar maliyeti,
- log loss, Brier score ve calibration error,
- slice bazlı performans,
- model ve preprocessing konfigürasyonu.
