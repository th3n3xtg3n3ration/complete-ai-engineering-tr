# Quiz — Gradient Descent ve Optimizasyon

Her soru tek doğru cevaba sahiptir.

## Sorular

### 1
Gradient descent hangi yönde hareket eder?

A. Gradient yönünde  
B. Negatif gradient yönünde  
C. Rastgele bir yönde  
D. Hessian'ın en büyük özvektörü yönünde

### 2
Learning rate çok büyük olduğunda en olası sonuç hangisidir?

A. Eğitim mutlaka daha hızlı yakınsar.  
B. Parametreler sabit kalır.  
C. Loss salınabilir veya büyüyebilir.  
D. Gradient otomatik olarak küçülür.

### 3
Batch gradient descent bir güncelleme için ne kullanır?

A. Tek örnek  
B. Rastgele iki örnek  
C. Tüm eğitim verisi  
D. Yalnızca validation verisi

### 4
SGD'nin batch gradient descent'e göre tipik özelliği hangisidir?

A. Daha düşük gradient varyansı  
B. Daha gürültülü güncellemeler  
C. Her adımda tüm veri kullanımı  
D. Optimizer state gerektirmemesi

### 5
Mini-batch kullanımının temel pratik avantajı hangisidir?

A. Gradient'i her zaman tam yapar.  
B. Loss'u convex hale getirir.  
C. Vektörizasyon ile sık güncellemeyi dengeler.  
D. Learning rate ihtiyacını ortadan kaldırır.

### 6
Momentum hangi bilgiyi biriktirir?

A. Geçmiş loss değerlerinin toplamını  
B. Geçmiş gradient yönlerini bir hız state'inde  
C. Validation örneklerini  
D. Hessian matrisini

### 7
Momentum özellikle hangi durumda faydalı olabilir?

A. Dar ve uzun vadilerdeki salınımlarda  
B. Loss fonksiyonu sabitken  
C. Gradient hiç hesaplanamıyorken  
D. Veri seti boşken

### 8
Nesterov momentumun ayırt edici fikri nedir?

A. Gradient'i geçmiş parametrelerde hesaplamak  
B. Gradient'i lookahead noktasında hesaplamak  
C. Learning rate'i sıfırlamak  
D. İkinci türevi doğrudan ters çevirmek

### 9
AdaGrad'ın önemli bir zayıflığı hangisidir?

A. Hiç state tutmaması  
B. Effective learning rate'in zamanla aşırı küçülebilmesi  
C. Seyrek gradient'lerde çalışmaması  
D. Gradient işaretini değiştirmesi

### 10
RMSProp, AdaGrad'ın hangi sorununu azaltır?

A. Gradient hesaplanamaması  
B. Kare gradient toplamının sınırsız büyümesi  
C. Batch oluşturulamaması  
D. Parametre sayısının artması

### 11
Adam hangi iki temel fikri birleştirir?

A. Momentum ve ikinci moment ölçeklemesi  
B. Dropout ve batch normalization  
C. PCA ve SVD  
D. Early stopping ve data augmentation

### 12
Adam'da bias correction neden kullanılır?

A. İlk moment tahminleri sıfır başlangıcına yanlı olduğu için  
B. Gradient'in işaretini düzeltmek için  
C. Batch size'ı büyütmek için  
D. Loss'u normalize etmek için

### 13
Gradient clipping'in amacı nedir?

A. Küçük gradient'leri büyütmek  
B. Gradient normunu sınırlandırmak  
C. Parametre sayısını azaltmak  
D. Validation loss'u training loss'a eşitlemek

### 14
Global norm clipping uygulandığında ne korunur?

A. Gradient vektörünün yönü yaklaşık olarak korunur.  
B. Her bileşen aynı değere dönüşür.  
C. Learning rate sıfır olur.  
D. Parametre normu sabitlenir.

### 15
Training loss düşerken validation loss yükseliyorsa en olası durum hangisidir?

A. Underflow  
B. Overfitting  
C. Gradient checking başarısı  
D. Convexity garantisi

### 16
Early stopping'deki `patience` neyi ifade eder?

A. Toplam batch sayısını  
B. İyileşme olmadan beklenen değerlendirme sayısını  
C. Başlangıç learning rate'ini  
D. Parametre sayısını

### 17
Ill-conditioned loss yüzeyi ne anlama gelir?

A. Tüm yönlerde aynı eğrilik vardır.  
B. Bazı yönlerin eğriliği diğerlerinden çok farklıdır.  
C. Loss her yerde sıfırdır.  
D. Gradient yalnızca pozitif değer alır.

### 18
Saddle point için doğru ifade hangisidir?

A. Her yönde minimumdur.  
B. Her yönde maksimumdur.  
C. Bazı yönlerde minimum, bazı yönlerde maksimum davranışı gösterir.  
D. Gradient her zaman büyüktür.

### 19
Optimizer state kaydedilmeden eğitim devam ettirilirse ne olabilir?

A. Momentum ve moment tahminleri kaybolur.  
B. Model parametreleri otomatik iyileşir.  
C. Veri seti küçülür.  
D. Loss fonksiyonu değişir.

### 20
Bir optimizasyon koşusunu değerlendirmek için en iyi yaklaşım hangisidir?

A. Yalnızca son training loss'a bakmak  
B. Yalnızca epoch sayısını karşılaştırmak  
C. Loss, validation metriği, gradient normu ve update normunu birlikte izlemek  
D. En büyük learning rate'i seçmek

## Cevap anahtarı

| Soru | Cevap | Kısa gerekçe |
|---:|:---:|---|
| 1 | B | Loss'u azaltmak için negatif gradient yönünde ilerlenir. |
| 2 | C | Büyük adımlar minimumu aşarak salınım veya divergence oluşturabilir. |
| 3 | C | Batch yöntemi tüm eğitim örneklerini kullanır. |
| 4 | B | Tek veya az örnek kullanımı gradient varyansını artırır. |
| 5 | C | Mini-batch, vektörizasyon ve güncelleme sıklığı arasında denge kurar. |
| 6 | B | Momentum geçmiş gradient yönlerini velocity state'inde biriktirir. |
| 7 | A | Momentum tutarlı yönde hızlanır, dik yöndeki salınımı azaltır. |
| 8 | B | Nesterov gradient'i tahmini gelecekteki noktada değerlendirir. |
| 9 | B | Birikimli kare gradient effective learning rate'i sürekli küçültebilir. |
| 10 | B | Üstel hareketli ortalama sınırsız birikimi önler. |
| 11 | A | Adam birinci ve ikinci moment tahminlerini birleştirir. |
| 12 | A | Sıfır başlangıcı ilk moment tahminlerini düşük yanlı yapar. |
| 13 | B | Clipping aşırı büyük gradient güncellemelerini sınırlar. |
| 14 | A | Vektör tek bir ölçek katsayısıyla küçültülür. |
| 15 | B | Model training verisine uyum sağlarken genelleme kötüleşmektedir. |
| 16 | B | Belirli sayıda başarısız değerlendirme sonrasında eğitim durur. |
| 17 | B | Hessian yönleri arasında büyük ölçek farkı vardır. |
| 18 | C | Saddle point'in eğriliği yönlere göre işaret değiştirir. |
| 19 | A | Momentum, RMSProp ve Adam state'leri yeniden sıfırdan başlar. |
| 20 | C | Tek metrik optimizer sağlığını açıklamak için yeterli değildir. |

## Puanlama

- 18–20: Konuya güçlü hâkimiyet
- 15–17: İyi seviye, birkaç noktayı tekrar et
- 11–14: Teori ve kod denklemlerini yeniden çalış
- 0–10: Ders teorisi ve laboratuvarı baştan uygula
