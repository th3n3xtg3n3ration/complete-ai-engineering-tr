# Teori — Linear Regression, Regularization ve Regresyon Değerlendirmesi

## 1. Problem

Regresyon, sürekli bir hedefi tahmin eder. Bir gözlem için

\[
\hat{y}=w_0+w_1x_1+\dots+w_px_p
\]

şeklindeki model, özelliklerin doğrusal birleşimini kullanır. “Doğrusal” sözcüğü giriş değişkenlerinden çok parametreler açısından doğrusallığı ifade eder; polynomial feature eklenmiş bir model de parametreleri bakımından lineer olabilir.

## 2. En küçük kareler

Ordinary least squares, residual kareleri toplamını küçültür:

\[
\min_w \frac{1}{n}\|Xw-y\|_2^2
\]

Tam rank ve uygun koşullarda kapalı form çözüm:

\[
w=(X^TX)^{-1}X^Ty
\]

Pratikte açık matris tersi yerine `solve`, QR veya SVD tercih edilir. Tekillik ve kötü koşulluluk, katsayıların kararsızlaşmasına yol açabilir.

## 3. Gradient descent

MSE gradient'i:

\[
\nabla_w=\frac{2}{n}X^T(Xw-y)
\]

Öğrenme oranı çok yüksekse eğitim dağılır; çok düşükse yavaşlar. Standardization, özellik ölçeklerini yakınlaştırarak optimizasyonu kolaylaştırır.

## 4. Regresyon metrikleri

- **MAE:** Hataların mutlak büyüklüğünü hedef biriminde verir ve outlier'lara RMSE'den daha dayanıklıdır.
- **MSE:** Büyük hataları karesel cezalandırır.
- **RMSE:** MSE'nin kareköküdür ve hedef birimine döner.
- **R²:** Sabit ortalama baseline'ına göre açıklanan varyansı ölçer. Evaluation setinde negatif olabilir.
- **Adjusted R²:** Özellik sayısı arttıkça anlamsız değişkenleri cezalandırır.

Tek metrik yeterli değildir. İş maliyeti, büyük hataların önemi ve segment davranışı birlikte değerlendirilmelidir.

## 5. Ridge

Ridge, L2 cezası ekler:

\[
\min_w \mathrm{MSE}+\alpha\sum_j w_j^2
\]

Katsayıları küçültür, multicollinearity altında varyansı azaltabilir ve genellikle katsayıları tam sıfır yapmaz. Intercept çoğunlukla cezalandırılmaz.

## 6. Lasso

Lasso, L1 cezası ekler:

\[
\min_w \mathrm{MSE}+\alpha\sum_j |w_j|
\]

Bazı katsayıları tam sıfıra çekebilir. Yüksek korelasyonlu özelliklerde seçilen değişken kararsız olabilir.

## 7. Elastic Net

Elastic Net, L1 ve L2 cezalarını birleştirir. Özellikle çok sayıda ve korelasyonlu özellik olduğunda Lasso'nun sparsity davranışıyla Ridge'in kararlılığını dengeleyebilir.

## 8. Ölçekleme

Regularization doğrudan katsayı büyüklüğünü cezalandırdığı için farklı ölçeklerdeki özellikler eşit muamele görmez. StandardScaler pipeline içinde yalnızca training fold'larında fit edilmelidir. Split öncesi scaling veri sızıntısıdır.

## 9. Polynomial regression

PolynomialFeatures, etkileşim ve kuvvet terimleri üretir. Derece arttıkça model esnekleşir; ancak feature sayısı ve overfitting riski hızla büyür. Polynomial model çoğu zaman Ridge ile birlikte değerlendirilir.

## 10. Varsayımlar ve tanılama

Lineer modelin güvenilir yorumu için:

- yaklaşık doğrusal ilişki,
- bağımsız gözlemler,
- residual ortalamasının sıfıra yakın olması,
- sabit hata varyansı,
- aşırı multicollinearity bulunmaması,
- etkili gözlemlerin kontrolü

incelenir. Tahmin doğruluğu için normal residual şart değildir; fakat klasik istatistiksel çıkarım etkilenebilir.

## 11. Heteroskedasticity

Tahmin seviyesi arttıkça residual yayılımı değişiyorsa sabit varyans varsayımı bozulur. Residual ile fitted değerlerin mutlak büyüklüğü arasındaki ilişki basit bir sinyal olabilir. Log target, farklı model ailesi veya robust standart hatalar düşünülebilir.

## 12. Multicollinearity ve VIF

Bir özelliğin diğerleri tarafından güçlü biçimde açıklanması katsayı varyansını büyütür. Variance Inflation Factor:

\[
VIF_j=\frac{1}{1-R_j^2}
\]

şeklindedir. Yüksek VIF otomatik silme kararı değildir; amaç, veri üretim süreci ve model kullanımıyla birlikte yorumlanmalıdır.

## 13. Residual ve slice analizi

Global RMSE iyi görünürken belirli fiyat, bölge veya zaman dilimlerinde hata yüksek olabilir. Residual işareti sistematik underprediction/overprediction davranışını, absolute residual ise hata büyüklüğünü gösterir.

## 14. Pipeline

Üretim odaklı pipeline şu sırayı korur:

1. Train/evaluation split
2. Training üzerinde preprocessing fit
3. Aynı dönüşümle evaluation transform
4. Model fit
5. Evaluation tahmini
6. Global ve slice metrikleri
7. Artefakt ve konfigürasyon kaydı

Kategori kolonları için `OneHotEncoder(handle_unknown="ignore")`, sayısal kolonlar için imputation ve scaling sık kullanılan güvenli bir başlangıçtır.

## 15. Model seçimi

Model seçimi yalnızca en düşük validation RMSE değildir. Katsayı kararlılığı, inference gecikmesi, açıklanabilirlik, segment hataları ve veri drift hassasiyeti de kararın parçasıdır.
