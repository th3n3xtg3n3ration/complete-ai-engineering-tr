# Ödev — Güvenilir Kernel SVM Sistemi

## Senaryo

Bir üretim hattında kusurlu ürünleri sevkiyattan önce tespit eden ikili sınıflandırma sistemi geliştiriyorsun. Veri; sensör ölçümleri, ürün tipi, vardiya, operatör grubu ve makine kimliği gibi sayısal ve kategorik özellikler içeriyor.

Pozitif sınıf **kusurlu ürün**dür. Kusurlu ürünü kaçırmanın beklenen maliyeti **₺400**, kusursuz ürünü gereksiz manuel incelemeye göndermenin maliyeti **₺25** olarak kabul edilecektir.

Amaç yalnızca yüksek skor elde etmek değil; veri sızıntısı olmayan, maliyet duyarlı, kalibre edilmiş ve yeniden üretilebilir bir SVM sistemi geliştirmektir.

## Zorunlu teslimatlar

### 1. Problem tanımı

- Prediction unit'i açıkça tanımla.
- Tahminin hangi anda üretileceğini belirt.
- Target etiketinin nasıl ve ne zaman oluştuğunu açıkla.
- Kullanılamayacak post-outcome feature'ları listele.
- False positive ve false negative sonuçlarını iş diliyle tanımla.

### 2. Veri bölme stratejisi

- Train, validation ve test kümeleri oluştur.
- Aynı makine veya ürün partisinin farklı split'lere dağılması leakage yaratıyorsa group-aware split kullan.
- Zaman etkisi varsa temporal split tercih et.
- Seçimini gerekçelendir ve sınıf dağılımlarını raporla.

### 3. Baseline modeller

Aşağıdaki baseline'ları kur:

1. majority-class baseline,
2. stratified random baseline,
3. leakage-safe logistic regression pipeline.

Her baseline için ROC-AUC, average precision, F1, balanced accuracy ve maliyet metriğini raporla.

### 4. Leakage-safe preprocessing

Tek bir `Pipeline`/`ColumnTransformer` içinde:

- sayısal eksikleri median ile doldur,
- kategorik eksikleri most-frequent ile doldur,
- sayısal feature'ları ölçekle,
- kategorik feature'ları unknown kategoriye dayanıklı encode et,
- model fit işlemlerinin yalnızca training fold üzerinde gerçekleşmesini sağla.

Pipeline dışında fit edilmiş scaler veya encoder kullanma.

### 5. SVM modelleri

En az şu modelleri karşılaştır:

- `LinearSVC`,
- `SVC(kernel="linear")`,
- `SVC(kernel="rbf")`.

Aşağıdakileri raporla:

- training süresi,
- inference süresi,
- validation metrikleri,
- support vector sayısı ve oranı,
- model boyutu veya serialize edilmiş artefakt boyutu.

### 6. Hiperparametre seçimi

- Linear model için en az beş `C` değeri dene.
- RBF model için en az beş `C` ve beş `gamma` değeri dene.
- Stratified veya group-aware cross-validation kullan.
- Ana seçim metriği olarak average precision veya iş maliyetini kullan.
- Test kümesini hiçbir seçim adımında kullanma.
- En az bir `C`–`gamma` validation heatmap'i üret.

### 7. Dengesiz sınıf analizi

Şunları karşılaştır:

- `class_weight=None`,
- `class_weight="balanced"`,
- iş maliyetlerinden türetilen özel class weight.

Minority precision, recall, PR-AUC ve confusion matrix üzerindeki etkileri yorumla.

### 8. Probability calibration

En iyi karar skoru modeline:

- sigmoid calibration,
- isotonic calibration

uygula. Calibration işlemini validation/test bilgisini sızdırmayacak biçimde kur.

Şunları karşılaştır:

- Brier score,
- log loss,
- reliability diagram,
- calibration öncesi ve sonrası ROC-AUC.

Calibration'ın ranking metriğini büyük ölçüde korurken probability quality'yi neden değiştirdiğini açıkla.

### 9. Maliyet duyarlı threshold

Validation kümesinde her threshold için:

```text
Toplam maliyet = 400 × false_negative + 25 × false_positive
```

hesapla.

- Maliyeti minimize eden threshold'u seç.
- Varsayılan threshold ile karşılaştır.
- Seçilen threshold'u test kümesine yalnızca bir kez uygula.
- Test maliyeti, confusion matrix ve iş etkisini raporla.

### 10. Hata ve segment analizi

En az üç segment seç:

- ürün tipi,
- makine,
- vardiya veya operatör grubu.

Her segment için sample count, positive rate, recall, precision ve maliyet raporla. En kötü segment için olası veri, süreç veya model kaynaklı nedenleri tartış.

### 11. Üretim paketi

Aşağıdaki artefaktları teslim et:

- eğitilmiş pipeline,
- feature şeması,
- seçilen threshold,
- sınıf etiketi eşlemesi,
- dependency sürümleri,
- eğitim ve test veri dönemleri,
- model card,
- rollback planı.

## Otomatik test gereksinimleri

En az 20 test yaz. Test paketi şunları kapsamalıdır:

- kernel fonksiyonlarının bilinen değerleri,
- invalid parametre kontrolleri,
- bilinmeyen kategori davranışı,
- eksik değer işleme,
- leakage-safe pipeline yapısı,
- probability aralığı,
- threshold boundary durumları,
- cost fonksiyonu,
- support vector oranı,
- serialize/deserialize sonrası tahmin eşitliği.

## Beklenen rapor yapısı

1. Yönetici özeti
2. Problem ve karar bağlamı
3. Veri ve split tasarımı
4. Baseline sonuçları
5. Model seçimi
6. Calibration ve threshold
7. Segment analizi
8. Üretim riskleri
9. Sonuç ve öneri

## Değerlendirme rubriği

| Boyut | Puan |
|---|---:|
| Problem, target ve leakage analizi | 10 |
| Split ve deney tasarımı | 10 |
| Leakage-safe preprocessing | 15 |
| Linear ve kernel SVM karşılaştırması | 15 |
| Hiperparametre seçimi | 10 |
| Class imbalance ve maliyet duyarlılığı | 10 |
| Calibration ve threshold seçimi | 10 |
| Hata/segment analizi | 8 |
| Otomatik testler | 7 |
| Üretim paketi ve teknik rapor | 5 |
| **Toplam** | **100** |

## Başarı ölçütü

Başarılı teslimat yalnızca en yüksek validation skoruna sahip model değildir. Seçilen sistemin:

- bağımsız test performansı,
- toplam iş maliyeti,
- calibration kalitesi,
- segmentler arası güvenilirliği,
- eğitim ve inference maliyeti

birlikte savunulmalıdır.
