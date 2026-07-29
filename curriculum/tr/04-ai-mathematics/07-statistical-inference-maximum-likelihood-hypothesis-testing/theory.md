# Teori — İstatistiksel Çıkarım, MLE ve Hipotez Testi

## 1. Betimlemekten çıkarım yapmaya

Betimsel istatistik, eldeki veriyi özetler. İstatistiksel çıkarım ise sınırlı bir örneklemden daha geniş bir evren hakkında kontrollü belirsizlik altında sonuç üretir.

- **Evren (population):** Hakkında konuşmak istediğimiz tüm birimler.
- **Örneklem (sample):** Evrenden gözlemlediğimiz alt küme.
- **Parametre:** Evrene ait bilinmeyen büyüklük; örneğin gerçek ortalama veya dönüşüm oranı.
- **İstatistik:** Örneklemden hesaplanan büyüklük; örneğin sample mean.
- **Tahmin edici (estimator):** Parametreyi tahmin etmek için kullanılan kural.
- **Tahmin (estimate):** Belirli bir veri kümesi üzerinde elde edilen sayısal sonuç.

Bir örneklem istatistiği rastlantısaldır; farklı örneklemler farklı sonuç verir. Bu değişkenliği modelleyen dağılıma **sampling distribution** denir.

## 2. İyi bir tahmin edici nasıl değerlendirilir?

### Bias

Bir tahmin edicinin beklenen değeri gerçek parametreye eşitse unbiased kabul edilir:

\[
\operatorname{Bias}(\hat{\theta}) = E[\hat{\theta}] - \theta
\]

Düşük bias tek başına yeterli değildir. Çok değişken bir tahmin edici pratikte güvenilmez olabilir.

### Variance

Tahmin edicinin örneklemler arasında ne kadar değiştiğini ölçer:

\[
\operatorname{Var}(\hat{\theta}) = E[(\hat{\theta} - E[\hat{\theta}])^2]
\]

### Mean squared error

Bias ve variance etkisini birlikte özetler:

\[
\operatorname{MSE}(\hat{\theta}) = \operatorname{Var}(\hat{\theta}) + \operatorname{Bias}(\hat{\theta})^2
\]

### Consistency

Örneklem büyüklüğü arttıkça tahmin edici gerçek parametreye yakınsıyorsa consistent kabul edilir.

### Efficiency

Aynı hedefi tahmin eden iki yöntem arasında daha düşük variance üreten yöntem daha efficient olabilir. Bu karşılaştırmanın aynı varsayımlar altında yapılması gerekir.

## 3. Standard error

Standard deviation, bireysel gözlemlerin yayılımını ölçer. **Standard error**, tahmin edicinin örneklemler arasındaki belirsizliğini ölçer.

Sample mean için:

\[
SE(\bar{x}) = \frac{s}{\sqrt{n}}
\]

Örneklem büyüklüğü dört katına çıktığında standard error yaklaşık yarıya iner. Bu, daha fazla veri toplamanın azalan marjinal faydasını gösterir.

## 4. Confidence interval

Bir güven aralığı, bilinmeyen parametre için bir prosedürün belirsizliğini ifade eder. Yüzde 95 güven aralığını “parametrenin bu aralıkta olma olasılığı yüzde 95” diye yorumlamak klasik frequentist çerçevede doğru değildir. Doğru yorum şudur:

> Aynı veri üretim ve örnekleme süreci çok kez tekrarlansaydı, aynı yöntemle üretilen aralıkların yaklaşık yüzde 95'i gerçek parametreyi kapsardı.

Normal yaklaşım altında mean için:

\[
\bar{x} \pm z_{1-\alpha/2} SE(\bar{x})
\]

Küçük örneklemlerde ve bilinmeyen variance durumunda t dağılımı daha uygun olabilir. Bu dersteki saf Python kodu temel normal yaklaşımı gösterir; üretim analizlerinde varsayımlar açıkça belgelenmelidir.

## 5. Bootstrap

Bootstrap, gözlenen örneklemden replacement ile tekrar örnekler çekerek bir istatistiğin sampling distribution'ını yaklaşıklar.

Temel algoritma:

1. Orijinal örneklemden aynı büyüklükte bootstrap örneği çek.
2. İlgili istatistiği hesapla.
3. İşlemi çok kez tekrarla.
4. Dağılımın standard deviation değerini bootstrap standard error olarak kullan.
5. Percentile veya başka bir yöntemle güven aralığı üret.

Bootstrap güçlüdür fakat sihirli değildir. Bağımlı gözlemler, zaman serileri, ağır selection bias ve temsil sorunu varsa basit iid bootstrap yanlış güven verebilir.

## 6. Likelihood nedir?

Probability, parametre sabitken verinin olasılığını inceler. Likelihood, gözlenen veri sabitken parametrenin hangi değerlerinin veriyi daha iyi açıkladığını karşılaştırır.

\[
L(\theta; x) = p(x \mid \theta)
\]

Likelihood bir parametre olasılık dağılımı değildir. Parametreler üzerinde normalize olmak zorunda değildir.

Bağımsız gözlemler için ortak likelihood çarpım biçimindedir:

\[
L(\theta; x_1, \ldots, x_n) = \prod_{i=1}^{n} p(x_i \mid \theta)
\]

Sayısal kararlılık için log-likelihood kullanılır:

\[
\ell(\theta) = \log L(\theta) = \sum_{i=1}^{n} \log p(x_i \mid \theta)
\]

Çarpımlar toplama dönüşür; çok küçük sayıların underflow üretme riski azalır.

## 7. Maximum likelihood estimation

MLE, gözlenen verinin likelihood değerini en büyük yapan parametreyi seçer:

\[
\hat{\theta}_{MLE} = \arg\max_{\theta} L(\theta; x)
\]

Log monoton olduğundan aynı çözüm log-likelihood ile bulunabilir:

\[
\hat{\theta}_{MLE} = \arg\max_{\theta} \ell(\theta; x)
\]

### Bernoulli örneği

Binary gözlemler için Bernoulli parametresi \(p\)'nin MLE değeri sample mean'dir:

\[
\hat{p}_{MLE} = \frac{1}{n}\sum_i x_i
\]

### Gaussian örneği

Normal dağılımda mean MLE sample mean'dir. Variance MLE ise paydaya \(n\) yazar:

\[
\hat{\sigma}^2_{MLE} = \frac{1}{n}\sum_i (x_i - \bar{x})^2
\]

Bu tahmin variance için küçük örneklemde biased olabilir. Unbiased sample variance paydaya \(n-1\) yazar; iki formülün amacı aynı değildir.

## 8. MLE ve MAP

MLE yalnızca likelihood kullanır. Maximum a posteriori estimation ise prior bilgiyi de dahil eder:

\[
\hat{\theta}_{MAP} = \arg\max_{\theta} p(\theta \mid x)
\]

Bayes kuralıyla:

\[
p(\theta \mid x) \propto p(x \mid \theta)p(\theta)
\]

Beta prior ve Bernoulli likelihood birlikte kullanıldığında posterior yine Beta dağılımıdır. Az veride prior etkisi güçlüdür; veri arttıkça likelihood genellikle baskın hale gelir.

Regularization çoğu zaman MAP perspektifiyle yorumlanabilir. Örneğin Gaussian prior, L2 regularization ile ilişkilendirilebilir.

## 9. Hipotez testi mantığı

Hipotez testi, belirli bir null hypothesis altında gözlenen veya daha uç bir sonucun ne kadar şaşırtıcı olduğunu değerlendirir.

- **Null hypothesis \(H_0\):** Genellikle fark veya etki yok varsayımı.
- **Alternative hypothesis \(H_1\):** Araştırılan fark veya etki.
- **Test statistic:** Veriyi null altında karşılaştırılabilir bir ölçeğe dönüştüren değer.
- **Significance level \(\alpha\):** Önceden belirlenen Type I error toleransı.
- **p-value:** Null doğru kabul edildiğinde gözlenen kadar veya daha uç bir test istatistiği elde etme olasılığı.

p-value, null hypothesis'in doğru olma olasılığı değildir. Etki büyüklüğünü de doğrudan ölçmez.

## 10. Tek ve çift yönlü testler

- **Two-sided test:** Her iki yöndeki farkı araştırır.
- **One-sided test:** Yalnızca önceden belirlenmiş bir yönü araştırır.

Veriye baktıktan sonra yön seçmek Type I error oranını bozar. Test yönü deney başlamadan belirlenmelidir.

## 11. Type I, Type II error ve power

- **Type I error:** Gerçekte etki yokken null'u reddetmek. False positive.
- **Type II error:** Gerçekte etki varken null'u reddedememek. False negative.
- **Power:** Gerçek bir etkiyi yakalama olasılığı; \(1-\beta\).

Power şunlardan etkilenir:

- effect size,
- sample size,
- noise/variance,
- significance level,
- test yönü,
- analiz tasarımı.

Çok büyük örneklemde küçük ve iş açısından anlamsız farklar istatistiksel olarak anlamlı olabilir. Bu nedenle p-value, güven aralığı ve effect size birlikte raporlanmalıdır.

## 12. Effect size

Effect size, farkın büyüklüğini ölçeklenmiş veya iş açısından yorumlanabilir biçimde ifade eder.

Sürekli metriklerde Cohen's d sık kullanılır:

\[
d = \frac{\bar{x}_1 - \bar{x}_2}{s_{pooled}}
\]

Dönüşüm oranlarında absolute lift, relative lift ve risk ratio raporlanabilir. Relative lift tek başına yanıltıcı olabilir; baseline mutlaka belirtilmelidir.

## 13. Permutation test

Permutation test, null altında grup etiketlerinin değiştirilebilir olduğunu varsayar.

1. Gözlenen farkı hesapla.
2. Grup etiketlerini karıştır.
3. Aynı grup büyüklükleriyle farkı yeniden hesapla.
4. Çok kez tekrarla.
5. Gözlenen kadar uç sonuçların oranını p-value olarak kullan.

Parametrik dağılım varsayımını azaltır; fakat exchangeability varsayımı hâlâ önemlidir.

## 14. Multiple testing

Aynı anda çok sayıda hipotez test edildiğinde en az bir false positive üretme olasılığı artar.

### Bonferroni

Family-wise error rate'i kontrol etmek için:

\[
\alpha_{adjusted} = \frac{\alpha}{m}
\]

Basit ve muhafazakârdır.

### Benjamini–Hochberg

False discovery rate'i kontrol eder. Çok sayıda model, özellik veya deney metriği tarandığında Bonferroni'ye göre daha güçlü olabilir.

Düzeltme yöntemi analizden önce belirlenmeli; yalnızca anlamlı görünen metrikleri raporlama alışkanlığından kaçınılmalıdır.

## 15. A/B testlerinde kritik hatalar

### Peeking

Her gün p-value kontrol edip anlamlı olduğunda testi durdurmak nominal alpha seviyesini korumaz. Sequential testing yöntemi kullanılmıyorsa örneklem büyüklüğü ve analiz zamanı önceden belirlenmelidir.

### Sample ratio mismatch

Beklenen trafik dağılımıyla gözlenen dağılım arasındaki ciddi fark; yönlendirme, logging veya eligibility hatasına işaret edebilir.

### Unit of analysis hatası

Randomization kullanıcı düzeyinde yapıldıysa bağımsız gözlem birimi de çoğu zaman kullanıcıdır. Session'ları bağımsız saymak standard error değerini yapay olarak küçültebilir.

### Novelty ve seasonality

Kısa deneyler haftanın günü, kampanya, tatil veya yeni özellik merakı etkilerini yakalayamayabilir.

### Metric hacking

Çok sayıda metric arasından yalnızca anlamlı olanı seçmek yanlış pozitif riskini büyütür. Primary metric ve guardrail metric'ler önceden tanımlanmalıdır.

### Practical significance

İstatistiksel anlamlılık ürün veya iş değerini garanti etmez. Minimum detectable effect, maliyet, risk ve operasyonel etki birlikte değerlendirilmelidir.

## 16. AI mühendisliği bağlantıları

İstatistiksel çıkarım AI sistemlerinde şu alanlarda kritiktir:

- model A/B testleri,
- offline metric farklarının belirsizliği,
- prompt veya retrieval değişikliklerinin değerlendirilmesi,
- data drift analizi,
- fairness metric karşılaştırmaları,
- calibration ve uncertainty değerlendirmesi,
- hyperparameter taramalarında multiple testing,
- benchmark sonuçlarının güven aralıkları,
- model latency ve maliyet karşılaştırmaları.

Tek bir skor yerine dağılım, uncertainty, effect size ve deney tasarımı birlikte raporlanmalıdır.

## 17. Üretim kontrol listesi

Bir çıkarım raporu en az şunları içermelidir:

1. Population ve sampling süreci.
2. Randomization ve analysis unit.
3. Primary hypothesis ve metric.
4. Sample size gerekçesi.
5. Varsayımlar ve veri kalite kontrolleri.
6. Point estimate ve confidence interval.
7. Effect size ve practical significance.
8. p-value veya Bayesian posterior özeti.
9. Multiple-testing yaklaşımı.
10. Missing data, outlier ve exclusion kuralları.
11. Reproducibility için seed, kod sürümü ve veri aralığı.
12. Sonucun sınırları ve karar önerisi.
