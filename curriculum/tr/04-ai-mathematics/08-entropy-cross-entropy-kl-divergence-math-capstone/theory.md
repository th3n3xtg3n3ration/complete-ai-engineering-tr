# Teori — Entropi, Cross-Entropy, KL Divergence ve Matematik Capstone

## 1. Bilgi miktarı ve surprisal

Bilgi teorisi belirsizliği sayısallaştırır. Olasılığı yüksek bir olay daha az, düşük bir olay daha fazla bilgi taşır. Bir olayın surprisal değeri:

```text
I(x) = -log p(x)
```

Logaritmanın tabanı 2 ise birim bit, doğal logaritma kullanılırsa nat olur.

## 2. Entropi

Bir ayrık dağılımın entropisi beklenen surprisal değeridir:

```text
H(P) = -sum(p_i * log(p_i))
```

Tek bir sonuca tüm olasılık verildiğinde entropi sıfırdır. Olasılık kütlesi eşit dağıldığında entropi maksimuma çıkar. Binary entropy, iki sonuçlu bir dağılımın belirsizliğini ölçer ve `p = 0.5` değerinde maksimumdur.

## 3. Cross-entropy

Gerçek dağılım `P`, model dağılımı `Q` olsun:

```text
H(P, Q) = -sum(p_i * log(q_i))
```

Cross-entropy, `P` dağılımından gelen veriyi `Q` kullanarak kodlamanın beklenen maliyetidir. One-hot sınıflandırma hedefinde yalnızca doğru sınıfın log olasılığı kalır:

```text
loss = -log(q_true_class)
```

Bu nedenle categorical cross-entropy ve negative log-likelihood aynı temel hedefi ifade eder.

## 4. KL divergence

```text
KL(P || Q) = sum(p_i * log(p_i / q_i))
```

KL divergence, `Q` dağılımını `P` yerine kullanmanın ek kodlama maliyetidir. Negatif değildir ve dağılımlar aynıysa sıfırdır. Simetrik değildir; dolayısıyla gerçek bir uzaklık metriği değildir. `p_i > 0` iken `q_i = 0` olması sonsuz divergence üretir.

Cross-entropy ayrışımı:

```text
H(P, Q) = H(P) + KL(P || Q)
```

Model eğitimi sırasında `H(P)` sabit olduğundan cross-entropy'yi küçültmek KL divergence'ı küçültmekle eşdeğerdir.

## 5. Jensen–Shannon divergence

Jensen–Shannon divergence, KL divergence'ın simetrik bir türevidir:

```text
M = (P + Q) / 2
JS(P, Q) = 0.5 * KL(P || M) + 0.5 * KL(Q || M)
```

Dağılım kayması izleme ve model çıktılarının karşılaştırılmasında daha dengeli bir ölçüm sağlar.

## 6. Mutual information

Mutual information iki değişkenin birbirleri hakkında taşıdığı bilgiyi ölçer:

```text
I(X; Y) = H(X) + H(Y) - H(X, Y)
```

Bağımsız değişkenlerde sıfırdır. Feature selection, representation learning ve bağımlılık analizi için kullanılır.

## 7. Softmax ve sayısal kararlılık

Softmax, logit skorlarını olasılıklara dönüştürür:

```text
softmax(z_i) = exp(z_i) / sum(exp(z_j))
```

Büyük logit değerleri overflow oluşturabilir. Bu nedenle her logit'ten maksimum değer çıkarılır:

```text
m = max(logits)
softmax(z_i) = exp(z_i - m) / sum(exp(z_j - m))
```

Log-sum-exp işlemi de aynı teknikle kararlı hesaplanır. Cross-entropy için önce softmax sonra log almak yerine doğrudan log-softmax kullanmak daha güvenlidir.

## 8. Binary cross-entropy

Binary hedef `y`, tahmin olasılığı `p` için:

```text
BCE = -y * log(p) - (1 - y) * log(1 - p)
```

Logit üzerinden kararlı form:

```text
BCE(y, z) = max(z, 0) - z*y + log(1 + exp(-abs(z)))
```

Bu form, olasılığın sıfıra veya bire yuvarlanmasından doğan `log(0)` sorununu önler.

## 9. Label smoothing

One-hot hedef yerine küçük bir olasılık kütlesi diğer sınıflara dağıtılır:

```text
smoothed_target = (1 - epsilon) * one_hot + epsilon / class_count
```

Label smoothing aşırı güveni azaltabilir, calibration'ı iyileştirebilir ve etiket gürültüsüne karşı dayanıklılık sağlayabilir. Çok yüksek smoothing ise ayırt ediciliği düşürebilir.

## 10. Focal loss

Focal loss kolay örneklerin etkisini azaltarak zor örneklere odaklanır:

```text
focal_loss = -alpha * (1 - p_t)^gamma * log(p_t)
```

Özellikle sınıf dengesizliği ve nadir pozitif örneklerde yararlıdır. Yine de class weighting, sampling ve karar eşiği analiziyle birlikte değerlendirilmelidir.

## 11. Perplexity

Perplexity ortalama negative log-likelihood'in üstelidir:

```text
perplexity = exp(mean_negative_log_likelihood)
```

Dil modeli belirsizliğini özetler. Yalnızca aynı tokenization, veri kümesi ve değerlendirme protokolü altında karşılaştırılmalıdır.

## 12. Calibration

Bir model belirli bir güven aralığında verdiği tahminlerde benzer bir doğruluk oranına sahipse calibrated kabul edilir. Accuracy ile calibration aynı değildir.

Yaygın ölçümler:

- negative log-likelihood,
- Brier score,
- expected calibration error,
- reliability diagram.

## 13. Softmax regression capstone

Girdi vektörü `x`, ağırlık matrisi `W`, bias `b` olsun:

```text
logits = W x + b
probabilities = softmax(logits)
loss = -log(probabilities[target]) + L2_penalty
```

Tek örnek için logit gradient'i:

```text
dL/dlogits = probabilities - one_hot_target
```

Ağırlık gradient'i dış çarpım ve L2 terimiyle, bias gradient'i ise logit gradient'iyle hesaplanır. Bu proje önceki derslerdeki vektörler, türev, gradient descent, olasılık ve istatistik konularını tek sistemde birleştirir.

## 14. Üretim ortamında dikkat edilmesi gerekenler

- Olasılık değerleri negatif olmamalı ve toplamları bire yakın olmalıdır.
- `0 * log(0)` terimi limit gereği sıfır kabul edilmelidir.
- Destek uyuşmazlığında cross-entropy ve KL sonsuz olabilir.
- Loss reduction yöntemi (`sum` veya `mean`) gradient ölçeğini değiştirir.
- Sınıf dengesizliğinde yalnızca accuracy raporlanmamalıdır.
- Düşük eğitim loss'u üretimde calibration garantisi vermez.
- Seed, initialization, veri bölme ve öğrenme oranı kaydedilmelidir.

## 15. Kontrol listesi

1. Girdiler doğrulanıyor mu?
2. Logaritma tabanı belgelenmiş mi?
3. Sıfır olasılıklar doğru ele alınıyor mu?
4. Softmax ve log-sum-exp sayısal kararlı mı?
5. Label smoothing hedefleri bire toplamlanıyor mu?
6. Gradient işaretleri doğru mu?
7. Loss reduction davranışı açık mı?
8. Accuracy yanında loss ve calibration raporlanıyor mu?
9. Deneyler seed ile tekrarlanabilir mi?
10. Distribution shift için entropy veya divergence sinyalleri izleniyor mu?
