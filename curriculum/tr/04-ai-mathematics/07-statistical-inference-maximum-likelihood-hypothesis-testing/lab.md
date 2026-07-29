# Laboratuvar — İstatistiksel Çıkarım ve A/B Test Analizi

Bu laboratuvarda tüm hesaplamaları standart Python kütüphanesiyle yapacaksın. Amaç hazır bir istatistik paketini çağırmak değil; belirsizlik, likelihood ve hipotez testi akışını adım adım kurmaktır.

## 1. Hazırlık

Repository kök dizininden çalış:

```bash
LESSON=curriculum/tr/04-ai-mathematics/07-statistical-inference-maximum-likelihood-hypothesis-testing
python "$LESSON/src/statistical_inference.py"
python "$LESSON/src/maximum_likelihood.py"
python "$LESSON/src/hypothesis_testing.py"
pytest "$LESSON/tests" -q
```

## 2. Point estimate ile uncertainty ayrımı

Aşağıdaki iki örneklemin ortalaması benzerdir fakat belirsizlikleri farklıdır:

```python
small_sample = [9.2, 10.4, 8.8, 11.1, 10.5]
large_sample = small_sample * 20
```

Görevler:

1. Her iki örneklem için mean ve sample variance hesapla.
2. Standard error değerlerini karşılaştır.
3. Yüzde 95 normal-approximation confidence interval üret.
4. Neden aynı ortalamanın farklı güven seviyeleri verebildiğini açıkla.

## 3. Sampling distribution deneyi

Gerçek ortalaması 50, standard deviation değeri 10 olan bir Gaussian dağılımdan tekrar tekrar örneklem çek.

- `n=10`, `n=50`, `n=200` için 2.000 sample mean üret.
- Her sampling distribution için mean ve standard deviation hesapla.
- Gözlenen standard deviation değerini `sigma / sqrt(n)` ile karşılaştır.
- Sample size arttıkça dağılımın nasıl daraldığını yorumla.

Deney seed değerini sabitlemelidir.

## 4. Bootstrap confidence interval

Aşağıdaki latency verisini kullan:

```python
latencies_ms = [91, 87, 95, 101, 89, 110, 93, 96, 88, 105, 99, 92]
```

Görevler:

1. Mean için 5.000 bootstrap resample üret.
2. Bootstrap standard error hesapla.
3. Percentile yüzde 95 confidence interval üret.
4. Aynı işlemi median için tekrarla.
5. Mean ve median belirsizliklerini karşılaştır.

## 5. Bernoulli likelihood yüzeyi

Aşağıdaki conversion gözlemleri için Bernoulli log-likelihood hesapla:

```python
conversions = [1, 0, 0, 1, 1, 0, 1, 0, 0, 1]
```

`p=0.05` ile `p=0.95` arasında 0.01 adımlarla grid search yap.

- En yüksek log-likelihood değerini veren `p` değerini bul.
- Sonucu sample mean ile karşılaştır.
- `p=0` ve `p=1` sınırlarında log-likelihood davranışını açıkla.
- Probability çarpımı yerine log-likelihood toplamının neden güvenli olduğunu göster.

## 6. Gaussian MLE ve unbiased variance

Bir Gaussian örneklemi için:

1. MLE mean hesapla.
2. MLE variance değerini paydaya `n` yazarak hesapla.
3. Unbiased sample variance değerini paydaya `n-1` yazarak hesapla.
4. Küçük örneklemde iki değerin neden farklı olduğunu açıkla.
5. Veri büyüdükçe farkın nasıl küçüldüğünü simülasyonla göster.

## 7. MLE ile MAP karşılaştırması

Beta prior kullanarak Bernoulli parametresinin MAP tahminini hesapla.

Senaryolar:

- Veri yok denecek kadar az: 1 success, 1 failure.
- Orta veri: 12 success, 8 failure.
- Büyük veri: 1.200 success, 800 failure.

Aşağıdaki prior'ları karşılaştır:

- `Beta(1, 1)` uniform prior.
- `Beta(2, 8)` düşük conversion beklentisi.
- `Beta(20, 20)` güçlü ve simetrik prior.

Prior etkisinin sample size ile nasıl değiştiğini raporla.

## 8. Tek örneklem z testi

Bir servis değişikliğinden sonra ortalama latency'nin 100 ms baseline değerinden farklı olup olmadığını test et.

- Null: `mu = 100`
- Alternative: `mu != 100`
- Önceden belirlenmiş alpha: `0.05`

Rapor:

- sample mean,
- standard error,
- z statistic,
- two-sided p-value,
- yüzde 95 confidence interval,
- karar,
- practical significance değerlendirmesi.

## 9. İki örneklem testi

Kontrol ve treatment için bağımsız latency örnekleri oluştur. Grupların variance değerlerini eşit kabul etmeden Welch yaklaşımını kullan.

Görevler:

1. Mean difference hesapla.
2. Standard error hesapla.
3. Approximate z/t statistic ve p-value üret.
4. Confidence interval hesapla.
5. Cohen's d hesapla.
6. “Anlamlı” sonuç ile “ürün açısından değerli” sonuç arasındaki farkı açıkla.

## 10. Conversion A/B testi

Örnek deney:

- Control: 12.000 kullanıcı, 1.080 conversion.
- Treatment: 12.100 kullanıcı, 1.150 conversion.

Şunları raporla:

- control rate,
- treatment rate,
- absolute lift,
- relative lift,
- pooled standard error,
- z statistic,
- two-sided p-value,
- confidence interval,
- minimum business effect ile karşılaştırma.

## 11. Permutation test

Aynı continuous metric verisi üzerinde 10.000 permutation kullan.

- Gözlenen mean difference değerini hesapla.
- Grup etiketlerini seed kontrollü karıştır.
- Two-sided p-value üret.
- Parametrik test sonucu ile karşılaştır.
- Exchangeability varsayımını tartış.

## 12. Type I error simülasyonu

Gerçekte aynı dağılımdan gelen iki grup oluştur ve 2.000 sahte A/B testi çalıştır.

- Her testte alpha `0.05` kullan.
- Null reddedilen deney oranını hesapla.
- Sonucun yaklaşık olarak alpha seviyesine neden yaklaşması gerektiğini açıkla.

Daha sonra her deneyde 20 metric test edip en küçük p-value değerini seç. False-positive oranının nasıl yükseldiğini gözlemle.

## 13. Multiple-testing düzeltmeleri

Aşağıdaki p-value listesini kullan:

```python
p_values = [0.001, 0.009, 0.013, 0.031, 0.049, 0.08, 0.21, 0.50]
```

- Bonferroni adjusted threshold hesapla.
- Düzeltilmiş p-value değerlerini üret.
- Benjamini–Hochberg prosedürüyle FDR kontrolü yap.
- İki yöntemin reddettiği hipotezleri karşılaştır.

## 14. Peeking deneyi

Null doğru olacak şekilde günlük control/treatment dönüşümleri üret. Her gün p-value hesapla ve ilk kez `p < 0.05` olduğunda deneyi durdur.

Bu süreci 1.000 kez tekrarla.

- En az bir noktada “anlamlı” görünen deney oranını hesapla.
- Nominal yüzde 5 false-positive oranıyla karşılaştır.
- Fixed-horizon ve sequential testing arasındaki farkı açıkla.

## 15. Sample ratio mismatch

Beklenen trafik dağılımı yüzde 50/50 iken 20.000 kullanıcının 11.300'ünün control grubuna düştüğünü varsay.

- Gözlenen oranları hesapla.
- Bunun yalnızca rastlantıyla açıklanıp açıklanamayacağını değerlendir.
- Assignment, logging ve eligibility katmanlarında hangi kontrolleri yapacağını yaz.

## 16. Mini proje teslimi

Aşağıdaki arayüzü sağlayan küçük bir paket geliştir:

```python
report = analyze_ab_test(
    control=control_values,
    treatment=treatment_values,
    alpha=0.05,
    minimum_practical_effect=0.02,
    permutations=10_000,
    seed=42,
)
```

Rapor en az şu alanları içermelidir:

- sample sizes,
- point estimates,
- absolute ve relative difference,
- standard error,
- confidence interval,
- parametric p-value,
- permutation p-value,
- effect size,
- statistical decision,
- practical decision,
- assumptions,
- warnings.

## 17. Kalite kapıları

Teslimden önce:

```bash
python -m compileall "$LESSON/src" "$LESSON/tests"
pytest "$LESSON/tests" -q
```

Kontrol listesi:

- Random seed dışarıdan verilebiliyor.
- Empty input ve invalid probability durumları açık hata üretiyor.
- NaN ve infinity kabul edilmiyor.
- Test yönü açıkça belirtiliyor.
- p-value ile effect size karıştırılmıyor.
- Confidence interval yorumu doğru.
- Multiple testing yaklaşımı belgeleniyor.
- Fonksiyonlar type hint ve docstring içeriyor.
