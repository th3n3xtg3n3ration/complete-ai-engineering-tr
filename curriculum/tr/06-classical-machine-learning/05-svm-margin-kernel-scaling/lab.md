# Laboratuvar — SVM'i Geometriden Üretim Pipeline'ına Taşımak

## Amaç

Bu laboratuvarda aynı problemi farklı SVM yaklaşımlarıyla çözüp, matematiksel sezgiyi ölçülebilir deneylere bağlayacaksın.

## Bölüm A — Margin geometrisi

1. `make_blobs` ile iki boyutlu, doğrusal ayrılabilir veri üret.
2. `SVC(kernel="linear", C=1e6)` eğit.
3. `coef_` ve `intercept_` kullanarak `f(x)=0`, `f(x)=1` ve `f(x)=-1` doğrularını çiz.
4. `support_vectors_` noktalarını farklı işaretle göster.
5. `2 / ||w||` ile margin genişliğini hesapla.
6. `C` değerlerini `0.01, 0.1, 1, 10, 100` olarak değiştir; margin genişliği, eğitim hatası ve support vector oranını tabloya yaz.

## Bölüm B — Hinge loss ve support vectors

1. Her örnek için `y_i f(x_i)` değerini hesapla.
2. Hinge loss değerlerini bul.
3. Örnekleri şu gruplara ayır:
   - margin dışında,
   - margin üzerinde,
   - margin içinde,
   - yanlış sınıflandırılmış.
4. Dual coefficient ve support vector indekslerini incele.
5. `0 < alpha < C` ve `alpha = C` yorumlarını deney üzerinden doğrula.

## Bölüm C — Kernel karşılaştırması

1. `make_moons` ile doğrusal olmayan veri üret.
2. Aynı train/test split üzerinde şu modelleri kur:
   - linear SVM,
   - polynomial SVM,
   - RBF SVM.
3. Her model için decision boundary çiz.
4. Accuracy yanında ROC-AUC, average precision ve support vector oranını raporla.
5. Polynomial kernel için degree ve `coef0` etkisini incele.

## Bölüm D — C–gamma etkileşimi

1. RBF SVM için aşağıdaki aralığı kullan:

```python
C_VALUES = [0.01, 0.1, 1, 10, 100]
GAMMA_VALUES = [0.001, 0.01, 0.1, 1, 10]
```

2. Her kombinasyon için train ve validation skorlarını kaydet.
3. Validation skorlarını heatmap veya pivot tablo ile göster.
4. Underfitting ve overfitting bölgelerini yorumla.
5. En iyi kombinasyonu test kümesinde yalnızca bir kez değerlendir.

## Bölüm E — Scaling ablation

1. Bir feature'ı 0–1, diğerini 0–100000 aralığında üret.
2. Scaling olmadan linear ve RBF SVM eğit.
3. `StandardScaler` pipeline'ı ile modelleri tekrar eğit.
4. Şunları karşılaştır:
   - cross-validation skoru,
   - eğitim süresi,
   - support vector oranı,
   - decision boundary,
   - seçilen `C` ve `gamma`.
5. Tüm veriyi önceden scale edip CV çalıştırmanın neden leakage olduğunu yazılı açıkla.

## Bölüm F — Karışık tipte leakage-safe pipeline

1. Sayısal ve kategorik özellikler içeren bir `DataFrame` oluştur.
2. Sayısal kolonda median imputation ve `StandardScaler` kullan.
3. Kategorik kolonda most-frequent imputation ve `OneHotEncoder(handle_unknown="ignore")` kullan.
4. Preprocessor ile `SVC` modelini tek `Pipeline` içinde birleştir.
5. Bilinmeyen kategori ve eksik değer içeren yeni örnekte tahmin al.

## Bölüm G — Dengesiz sınıf ve threshold

1. `make_classification(weights=[0.95, 0.05])` ile dengesiz veri üret.
2. `class_weight=None` ve `class_weight="balanced"` modellerini karşılaştır.
3. ROC-AUC, average precision, minority recall ve balanced accuracy raporla.
4. Calibrated probability üzerinde farklı threshold değerleri dene.
5. Aşağıdaki maliyet fonksiyonunu kullan:

```text
Toplam maliyet = 25 TL × false positive + 400 TL × false negative
```

6. Threshold'u validation kümesinde seç; test kümesine sabit olarak uygula.

## Bölüm H — Probability calibration

1. `LinearSVC` veya `SVC(probability=False)` modelini sigmoid calibration ile sar.
2. Aynı modeli isotonic calibration ile tekrar kur.
3. Brier score, log loss ve calibration curve karşılaştır.
4. Küçük validation setinde isotonic yaklaşımının neden kırılgan olabileceğini yorumla.

## Bölüm I — Çok sınıflı SVM

1. Üç sınıflı veri üret.
2. `SVC` ile OvO davranışını incele.
3. `OneVsRestClassifier(LinearSVC(...))` modeli kur.
4. Eğitim süresi, tahmin süresi, macro-F1 ve model sayısını karşılaştır.
5. Sınıf sayısı büyüdüğünde OvO maliyetini hesapla.

## Bölüm J — Nested cross-validation

1. Outer loop için stratified 5-fold CV kullan.
2. Her outer training fold içinde `C`, kernel ve `gamma` seç.
3. Outer validation skorlarını sakla.
4. Basit grid search sonucuyla nested CV sonucunu karşılaştır.
5. Tek CV sonucunun model seçimi iyimserliği yaratabileceğini açıkla.

## Teslimat

- Çalışan notebook veya Python script
- Deney tablosu
- En az dört decision-boundary grafiği
- C–gamma validation tablosu
- Calibration karşılaştırması
- Maliyet duyarlı threshold sonucu
- Segment bazlı hata analizi
- Üretim önerisi

## Doğrulama

```bash
pytest curriculum/tr/06-classical-machine-learning/05-svm-margin-kernel-scaling/tests -q
```

Test sonucunu gerçekten çalıştırmadan rapora yazma.
