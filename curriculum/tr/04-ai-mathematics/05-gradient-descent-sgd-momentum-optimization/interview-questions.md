# Mülakat Soruları — Optimizasyon

## Temel sorular

### 1. Gradient descent nasıl çalışır?

İyi bir cevap; loss, gradient, negatif yön ve learning rate ilişkisini güncelleme denklemiyle açıklamalıdır.

### 2. Learning rate neden kritiktir?

Çok küçük değerin yavaşlığa, çok büyük değerin salınım veya divergence'a yol açabileceğini belirt.

### 3. Batch, stochastic ve mini-batch gradient descent arasındaki fark nedir?

Gradient'in kaç örnek üzerinden hesaplandığını, varyansı, update sıklığını ve donanım verimliliğini karşılaştır.

### 4. Bir epoch ile bir optimizer step aynı şey midir?

Hayır. Bir epoch tüm veri üzerinde bir geçiştir; step sayısı batch size'a bağlıdır.

### 5. Gradient sıfırsa minimumda mıyız?

Zorunlu değildir. Maksimum, saddle point veya sayısal doygunluk da olabilir.

## Orta seviye sorular

### 6. Momentum neden işe yarar?

Geçmiş gradient yönlerini velocity state'inde biriktirerek tutarlı yönde hızlanır ve dik eksendeki salınımı azaltır.

### 7. Nesterov momentum ile klasik momentum arasındaki fark nedir?

Nesterov gradient'i momentumun götüreceği lookahead noktasında değerlendirir.

### 8. AdaGrad hangi problemlerde avantajlıdır?

Seyrek ve farklı sıklıklarda güncellenen özelliklerde koordinat bazlı learning-rate ölçeklemesi yararlı olabilir.

### 9. AdaGrad'ın temel sorunu nedir?

Kare gradient toplamı sürekli büyür; effective learning rate aşırı küçülebilir.

### 10. RMSProp bu sorunu nasıl değiştirir?

Tüm geçmişi toplamak yerine kare gradient'lerin üstel hareketli ortalamasını kullanır.

### 11. Adam hangi momentleri tahmin eder?

Gradient'in birinci momentini ve kare gradient'in ikinci ham momentini tahmin eder.

### 12. Adam'da bias correction neden gereklidir?

Moment state'leri sıfırdan başladığı için ilk tahminler sıfıra doğru yanlıdır.

### 13. Adam her zaman SGD'den iyi midir?

Hayır. Daha hızlı başlangıç sağlayabilir; ancak problem, schedule ve genelleme davranışına göre SGD veya momentum daha iyi olabilir.

### 14. Adam ve AdamW farkı nedir?

AdamW weight decay'i adaptive gradient momentlerinden ayırarak doğrudan parametre küçültmesi uygular.

### 15. Gradient clipping ne zaman kullanılır?

Exploding gradient riski olduğunda update normunu sınırlamak için kullanılır; kök nedeni tek başına çözmez.

## İleri seviye sorular

### 16. Ill-conditioned bir quadratic fonksiyonda vanilla gradient descent nasıl davranır?

Eğrilik ölçekleri farklı olduğundan dik yönde salınır, düz yönde yavaş ilerler. Uygun learning rate en büyük eğriliğe göre sınırlanır.

### 17. Hessian optimizer davranışı hakkında ne söyler?

Yerel eğrilik, condition number, saddle-point yapısı ve güvenli adım büyüklüğü hakkında bilgi verir.

### 18. Büyük batch eğitiminin optimizer dinamiklerine etkisi nedir?

Gradient varyansını azaltır, step sayısını düşürür ve learning-rate ayarını değiştirebilir. Genelleme davranışı da farklılaşabilir.

### 19. Linear scaling rule nedir?

Batch size belirli oranda büyütüldüğünde learning rate'i benzer oranda büyütme heuristiğidir; warmup ve problem doğrulaması gerektirir.

### 20. Gradient noise faydalı olabilir mi?

Mini-batch gürültüsü dar minimumlardan veya düz bölgelerden çıkmaya yardım edebilir ve implicit regularization etkisi oluşturabilir.

### 21. Training loss sabitken gradient normu büyükse ne düşünürsün?

Learning rate küçük olabilir, gradient'ler birbirini iptal ediyor olabilir, clipping aşırı agresif olabilir veya optimizer state update'i bastırıyor olabilir.

### 22. Loss azalırken update normu büyüyorsa bu sağlıklı mıdır?

Kısa süreli olabilir; fakat parametre ve gradient normlarıyla birlikte izlenmelidir. Yaklaşan instability veya schedule değişimi söz konusu olabilir.

### 23. Bir optimizer implementasyonunu nasıl doğrularsın?

Bilinen tek adımlı örnekler, finite-difference gradient checking, quadratic yakınsama testi, state doğrulaması ve referans kütüphane karşılaştırması kullanılır.

### 24. Optimizer state neden checkpoint'e dahil edilmelidir?

Momentum ve moment tahminleri eğitim geçmişini taşır. State kaybolursa devam eden eğitim farklı dinamiklerle yeniden başlar.

### 25. Reproducibility için seed yeterli midir?

Hayır. Veri sırası, kütüphane sürümleri, donanım kernel'leri, paralellik ve nondeterministic işlemler de kontrol edilmelidir.

## Sistem tasarımı soruları

### 26. Üretim kalitesinde bir training loop nasıl tasarlanır?

Beklenen başlıklar:

- Yapılandırma doğrulaması
- Veri karıştırma ve batching
- Forward, loss, backward ve step ayrımı
- Finite değer kontrolleri
- Gradient clipping
- Metrik ve log kaydı
- Validation
- Early stopping
- Checkpoint ve resume
- Test ve seed yönetimi

### 27. Otomatik optimizer tanılama sistemi nasıl kurarsın?

Loss, gradient normu, update normu, parameter normu, learning rate ve validation gap sinyallerini zaman pencereleriyle analiz eden açıklanabilir kurallar tasarlanabilir.

### 28. Learning-rate tuning'i nasıl yaparsın?

Logaritmik arama, learning-rate range test, kısa kontrollü koşular, schedule seçimi ve tekrarlı seed deneyleriyle yapılır.

### 29. Optimizer benchmark'ında adil karşılaştırma nasıl sağlanır?

Aynı veri bölünmesi, seed, initialization, update bütçesi, evaluation sıklığı ve hesaplama bütçesi kullanılır; optimizer'a özgü learning rate ayrı ayarlanır.

### 30. Eğitim aniden NaN olduğunda hangi sırayla araştırırsın?

1. Loss girdileri ve log/division işlemleri
2. Gradient normları
3. Learning rate ve schedule
4. Mixed precision ölçekleme
5. Gradient clipping
6. Veri outlier'ları
7. Optimizer state
8. Son sağlıklı checkpoint ile karşılaştırma

## Kodlama soruları

### 31. Saf Python ile global norm clipping yaz.

Adayın norm hesaplaması, sıfır norm, finite kontrolü ve tek ölçek katsayısı kullanımı değerlendirilir.

### 32. Momentum optimizer sınıfı yaz.

State initialization, shape kontrolü ve update denklemi beklenir.

### 33. Adam'ın tek adımını uygula.

Birinci/ikinci moment, timestep, bias correction ve epsilon kullanımı beklenir.

### 34. Early stopping sınıfı yaz.

Best value, minimum delta, patience, best epoch ve restore edilecek best state tasarımı değerlendirilir.

### 35. Loss geçmişinden oscillation tespit eden heuristik yaz.

Adayın zaman penceresi, ölçek bağımsızlığı, false-positive riski ve açıklanabilir çıktı üretmesi beklenir.
