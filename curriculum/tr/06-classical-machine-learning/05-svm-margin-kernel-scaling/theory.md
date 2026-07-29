# Teori — SVM, Margin, Kernel ve Ölçekleme

İkili sınıflandırmada karar fonksiyonu \(f(x)=w^Tx+b\) biçimindedir. SVM, sınıfları ayıran hiper-düzlemler arasında geometrik margin'i en büyük yapan çözümü arar. Canonical ölçeklemede toplam margin genişliği \(2/\|w\|\) değerindedir.

Hard margin tüm örnekler için \(y_i(w^Tx_i+b)\ge1\) ister. Soft margin ise slack değişkenleri ve `C` ile ihlalleri kabul eder. Büyük `C` daha zayıf regularization ve daha dar margin, küçük `C` daha güçlü regularization ve daha geniş margin eğilimi yaratır.

Hinge loss:

\[
L_i=\max(0,1-y_if(x_i))
\]

Kernel trick, açık feature mapping üretmeden \(K(x,z)=\phi(x)^T\phi(z)\) iç çarpımını hesaplar.

- Linear: `x.T @ z`
- Polynomial: `(gamma * x.T @ z + coef0) ** degree`
- RBF: `exp(-gamma * ||x-z||²)`

RBF kernel'da büyük `gamma` daha lokal ve karmaşık, küçük `gamma` daha yumuşak karar sınırı oluşturur. SVM mesafe ve iç çarpıma dayalı olduğu için scaling pipeline içinde uygulanmalıdır.

`class_weight` eğitim hedefini, threshold tuning karar politikasını değiştirir. SVM karar skorları olasılık değildir; sigmoid veya isotonic calibration uygulanabilir. Hiperparametreler training verisi içinde cross-validation ile seçilmeli, test kümesi yalnızca son değerlendirmede kullanılmalıdır.
