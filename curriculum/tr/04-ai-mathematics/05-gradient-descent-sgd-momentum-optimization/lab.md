# Laboratuvar — Optimizer Davranışlarını Ölçmek

## Amaç

Bu laboratuvarda aynı linear regression problemini farklı optimizer'larla eğitecek, yalnızca final loss'u değil eğitim dinamiklerini de karşılaştıracaksın.

## Ön koşullar

- Python 3.11+
- `pytest`
- Ders 4'teki gradient ve gradient-checking bilgisi

## 1. Dosyaları çalıştır

Repo kök dizininde:

```bash
python curriculum/tr/04-ai-mathematics/05-gradient-descent-sgd-momentum-optimization/src/optimizers.py
python curriculum/tr/04-ai-mathematics/05-gradient-descent-sgd-momentum-optimization/src/regression_experiment.py
python curriculum/tr/04-ai-mathematics/05-gradient-descent-sgd-momentum-optimization/src/optimization_diagnostics.py
```

Beklenen davranış:

- Quadratic örneğinde loss düzenli olarak azalır.
- Regression deneyinde slope yaklaşık `3.5`, intercept yaklaşık `-1.25` olur.
- Farklı optimizer'lar farklı hız ve dalgalanma davranışı gösterir.

## 2. Batch gradient descent deneyi

`regression_experiment.py` içindeki `train` fonksiyonunu tüm veriyi tek batch olarak kullanacak biçimde çağır:

```python
from optimizers import SGD
from regression_experiment import make_regression_data, train

examples = make_regression_data()
result = train(
    examples,
    SGD(learning_rate=0.03),
    epochs=100,
    batch_size=len(examples),
)
```

Kaydet:

- İlk loss
- Son loss
- Son gradient normu
- Son update normu
- Öğrenilen slope ve intercept

## 3. SGD varyans deneyi

Aynı modeli `batch_size=1` ile eğit. Seed değerlerini `7`, `17` ve `27` yap.

Tartış:

- Final parametreler neden tam olarak aynı değil?
- Loss eğrisi neden daha gürültülü?
- Gürültü yakınsamayı tamamen engelliyor mu?

## 4. Mini-batch karşılaştırması

Aşağıdaki batch size değerlerini dene:

```text
1, 4, 16, 64, full batch
```

Her deney için tablo oluştur:

| Batch size | Final loss | Gradient norm | Update norm | Slope error | Intercept error |
|---:|---:|---:|---:|---:|---:|

Gerçek parametreler:

```text
slope = 3.5
intercept = -1.25
```

## 5. Learning-rate taraması

Vanilla SGD için şu değerleri dene:

```text
0.0001, 0.001, 0.01, 0.03, 0.1, 0.5
```

Her koşuda:

- Eğitimin yakınsayıp yakınsamadığını belirle.
- Loss'un ilk 10 epoch davranışını incele.
- Divergence varsa hangi epoch'ta başladığını kaydet.
- En hızlı kararlı değeri seç.

## 6. Momentum deneyi

Aynı learning rate ile:

```python
SGD(learning_rate=0.02, momentum=0.0)
SGD(learning_rate=0.02, momentum=0.5)
SGD(learning_rate=0.02, momentum=0.9)
SGD(learning_rate=0.02, momentum=0.99)
```

Sorular:

1. Hangi momentum değeri en hızlı ilerledi?
2. Hangi değerde salınım arttı?
3. Büyük momentum neden her zaman daha iyi değildir?

## 7. Nesterov deneyi

```python
optimizer = SGD(
    learning_rate=0.02,
    momentum=0.9,
    nesterov=True,
)
```

Vanilla momentum ile karşılaştır. Nesterov gradient'inin lookahead parametrelerinde hesaplandığını kod üzerinden göster.

## 8. Adaptive optimizer karşılaştırması

Şu optimizer'ları çalıştır:

```python
RMSProp(learning_rate=0.03)
Adam(learning_rate=0.05)
```

Aşağıdaki soruları yanıtla:

- İlk 10 epoch'ta hangisi daha hızlı?
- Final loss açısından fark anlamlı mı?
- Adaptive yöntemlerin update normları nasıl değişiyor?
- Aynı learning rate'i doğrudan karşılaştırmak neden yanıltıcı olabilir?

## 9. Gradient clipping

Yapay olarak büyük gradient oluştur:

```python
from optimizers import clip_by_global_norm, l2_norm

gradient = [300.0, -400.0]
clipped = clip_by_global_norm(gradient, max_norm=10.0)

print(l2_norm(gradient))
print(l2_norm(clipped))
```

Beklenen normlar yaklaşık `500` ve `10` olmalıdır.

Ardından yüksek learning rate kullanılan bir SGD deneyinde clipping açık ve kapalı sonuçları karşılaştır.

## 10. Learning-rate schedule

`step_decay`, `exponential_decay` ve `cosine_decay` fonksiyonlarını 100 adım boyunca örnekle. En az şu adımları tabloya yaz:

```text
0, 1, 10, 25, 50, 75, 100
```

Her schedule için şu yorumu yap:

- Başlangıçta ne kadar agresif?
- Eğitimin sonunda ne kadar küçük?
- Hangi problem türünde tercih edilebilir?

## 11. Early stopping

Validation loss dizisi üzerinde `EarlyStopping` kullan:

```python
validation_losses = [1.0, 0.8, 0.7, 0.69, 0.691, 0.692, 0.693]
```

`patience=3` için durma epoch'unu bul. En iyi epoch ile durma epoch'unun neden farklı olduğunu açıkla.

## 12. Tanılama senaryoları

`diagnose_training` fonksiyonuna şu örüntüleri ver:

1. Düzenli azalan loss
2. Sürekli büyüyen loss
3. Aşağı-yukarı salınan loss
4. Son adımlarda neredeyse değişmeyen loss
5. NaN içeren loss

Her raporun `status` ve mesajlarını değerlendir. Heuristik tanılamanın kesin kanıt olmadığını belirt.

## 13. Küçük veri üzerinde overfit testi

Yalnızca 4 örnek seç ve modeli uzun süre eğit. Model bu küçük veri grubunda çok düşük loss'a ulaşamıyorsa şunları kontrol et:

- Gradient formülü
- Parametre güncelleme işareti
- Learning rate
- Batch oluşturma
- Optimizer state boyutu

Bu test, büyük eğitimden önce pipeline doğrulamasında kullanılır.

## 14. Testleri çalıştır

```bash
pytest curriculum/tr/04-ai-mathematics/05-gradient-descent-sgd-momentum-optimization/tests -q
```

## Teslim çıktısı

Aşağıdakileri içeren kısa bir teknik rapor hazırla:

- Deney yapılandırmaları
- Karşılaştırma tablosu
- En az üç loss eğrisi
- Gradient ve update normu analizi
- Seçtiğin optimizer ve gerekçesi
- Başarısız veya kararsız koşuların kök neden analizi
- Tekrarlanabilirlik için seed ve çalıştırma komutları
