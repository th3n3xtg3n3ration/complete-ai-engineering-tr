# Laboratuvar — Olasılık, Dağılımlar ve Bayes

Bu laboratuvarda tüm deneyler sabit random seed ile tekrarlanabilir biçimde yürütülür. Kod dili İngilizcedir; analiz ve yorumlar Türkçe tutulmalıdır.

## Hazırlık

Repository kök dizininde:

```bash
LESSON=curriculum/tr/04-ai-mathematics/06-probability-distributions-expectation-variance-bayes
python "$LESSON/src/probability.py"
python "$LESSON/src/bayes.py"
python "$LESSON/src/simulation_experiment.py"
pytest "$LESSON/tests" -q
```

## Bölüm 1 — Temel olasılık denetimleri

1. Bir zar ve iki yazı-tura deneyi için örnek uzayları yaz.
2. Birleşim ve kesişim olasılıklarını hem sayarak hem fonksiyonlarla hesapla.
3. `conditional_probability` fonksiyonunu kullanarak koşullu olasılığı doğrula.
4. Bağımsız iki olay ve bağımlı iki olay için sonuçları karşılaştır.

Beklenen çıktı: Her olay için teorik değer, hesaplanan değer ve mutlak hata.

## Bölüm 2 — Dağılımların momentleri

1. Bernoulli örnekleri üret ve deneysel ortalama ile varyansı teorik değerlerle karşılaştır.
2. Binomial dağılım için farklı `n` ve `p` değerlerini dene.
3. Poisson dağılımında ortalama ile varyansın yaklaşık eşitliğini incele.
4. Normal dağılımda örnek sayısının moment tahminlerine etkisini ölç.

Her deney için en az `100`, `1_000` ve `10_000` örnek kullan.

## Bölüm 3 — Büyük sayılar yasası

`running_mean` çıktısını kullanarak bir Bernoulli sürecinde örnek ortalamasının gerçek `p` değerine yaklaşmasını incele.

Raporla:

- İlk 10 gözlemdeki hata
- 100 gözlemdeki hata
- 1.000 gözlemdeki hata
- Son gözlemdeki hata

Tek bir koşunun monoton yaklaşmak zorunda olmadığını açıkla.

## Bölüm 4 — Merkezi limit teoremi

`simulate_sample_means` ile normal olmayan bir dağılımdan örnek ortalamaları üret.

Deneyler:

- Örneklem büyüklüğü: `2`, `5`, `30`, `100`
- Tekrar sayısı: en az `5_000`

Her deneyde ortalamaların mean ve standard deviation değerlerini raporla. Teorik standard error ile karşılaştır.

## Bölüm 5 — Bayes güncellemesi

Bir ikili test senaryosu tanımla:

- Ön olasılık
- Sensitivity
- Specificity

Pozitif test sonrası posterior olasılığı `binary_bayes_update` ile hesapla. Base-rate etkisini görmek için prior değerini `0.01`, `0.10` ve `0.50` olarak değiştir.

Sonuçları yalnızca test doğruluğuna bakarak yorumlamanın neden yanıltıcı olabileceğini açıkla.

## Bölüm 6 — Gaussian Naive Bayes

1. `make_gaussian_classification_data` ile veri üret.
2. Veriyi eğitim ve test bölmelerine ayır.
3. `GaussianNaiveBayes` modelini yalnızca eğitim verisine fit et.
4. Accuracy, confusion matrix ve log-loss hesapla.
5. `var_smoothing` değerini değiştirerek sonuçları karşılaştır.

Önemli: Test verisinin istatistiklerini eğitim sırasında kullanma.

## Bölüm 7 — Sınıf dengesizliği

Pozitif sınıf oranını azalt. Aşağıdaki iki yaklaşımı karşılaştır:

- Eğitim verisinden öğrenilen prior
- Domain tarafından verilen özel prior

Accuracy tek başına yeterli mi? Precision, recall ve posterior dağılımını da incele.

## Bölüm 8 — Calibration

Tahmin olasılıklarını 10 eşit aralığa böl. Her aralık için:

- Örnek sayısı
- Ortalama tahmin olasılığı
- Gerçek pozitif oranı

hesapla. Az örnek içeren aralıkların neden güvenilmez olabileceğini belirt.

## Bölüm 9 — Karar eşiği

Yanlış negatif maliyetinin yanlış pozitif maliyetinden daha yüksek olduğu bir senaryo kur. Eşiği `0.1` ile `0.9` arasında tara ve beklenen maliyeti hesapla.

En düşük maliyetli eşik ile en yüksek accuracy sağlayan eşiğin farklı olup olmadığını raporla.

## Bölüm 10 — Teslim formatı

Teslim dizini:

```text
reports/ai-math-06/
├── report.md
├── metrics.json
└── decisions.md
```

`report.md` şu başlıkları içermelidir:

1. Deney düzeni
2. Varsayımlar
3. Teorik beklentiler
4. Ölçülen sonuçlar
5. Sayısal kararlılık gözlemleri
6. Calibration ve eşik analizi
7. Hata kaynakları
8. Sonuç

## Kabul kriterleri

- Tüm deneyler sabit seed ile tekrar üretilebilir.
- Eğitim ve test verisi arasında sızıntı yoktur.
- Olasılık hesapları log-uzayında kararlıdır.
- En az üç farklı örneklem büyüklüğü karşılaştırılır.
- Model yalnızca accuracy ile değerlendirilmez.
- Teknik yorumlar varsayımları açıkça belirtir.
