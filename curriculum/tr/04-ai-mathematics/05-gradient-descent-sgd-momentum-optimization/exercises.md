# Alıştırmalar — Gradient Tabanlı Optimizasyon

Alıştırmaları sırasıyla çöz. Kod yazılan sorularda yalnızca sonucu değil, doğrulama stratejini de belirt.

## A. Kavramsal temel

1. Optimizasyon, model ve loss kavramlarını tek bir linear regression örneği üzerinden tanımla.
2. Gradient'in neden en hızlı artış yönünü gösterdiğini geometrik olarak açıkla.
3. Negatif gradient yönünün neden her zaman global minimuma ulaştırmadığını açıkla.
4. Learning rate çok küçük olduğunda eğitim günlüklerinde hangi belirtiler görülür?
5. Learning rate çok büyük olduğunda hangi belirtiler görülür?
6. Parametre güncellemesindeki eksi işaret kaldırılırsa ne olur?
7. Convex ve non-convex loss yüzeylerini karşılaştır.
8. Local minimum, global minimum ve saddle point kavramlarını ayır.
9. Ill-conditioned bir loss yüzeyinde gradient descent neden zikzak çizer?
10. Gradient normu sıfıra yakınken loss'un yüksek kalabileceği iki senaryo yaz.

## B. Batch stratejileri

11. Batch gradient descent'in hesaplama ve bellek maliyetlerini açıkla.
12. SGD gradient'inin neden yüksek varyanslı olduğunu açıkla.
13. Mini-batch yaklaşımının GPU kullanımına neden uygun olduğunu araştırmadan, vektörizasyon açısından açıkla.
14. Batch size iki katına çıktığında update sayısı nasıl değişir?
15. Aynı epoch sayısında batch size değiştiğinde toplam optimizer adımı neden değişir?
16. Online learning için batch size seçimini tartış.
17. Veri sıralamasını her epoch karıştırmamanın oluşturabileceği problemi örnekle.
18. Son mini-batch diğerlerinden küçük olduğunda gradient ölçeklemesini nasıl yapmalısın?

## C. Türetme ve hesaplama

19. \(f(x)=x^2\) için gradient descent'in ilk beş adımını \(x_0=4\), \(\eta=0.1\) ile elle hesapla.
20. Aynı problemi \(\eta=0.6\) ile hesapla ve davranışı yorumla.
21. \(f(x,y)=x^2+4y^2\) gradient'ini türet.
22. Önceki fonksiyonda eksenler arasındaki eğrilik farkının yolu nasıl etkilediğini açıkla.
23. Tek özellikli linear regression için MSE'nin slope gradient'ini türet.
24. Aynı model için intercept gradient'ini türet.
25. L2 regularization eklendiğinde gradient'in nasıl değiştiğini göster.
26. Global normu 50 olan bir gradient'i maksimum norm 5 olacak biçimde ölçekle.

## D. Saf Python uygulamaları

27. Tek parametreli gradient descent fonksiyonu yaz.
28. Vektör parametreleri destekleyen SGD sınıfı yaz.
29. Momentum state'inin neden optimizer içinde tutulması gerektiğini açıkla.
30. Momentum implementasyonuna shape kontrolü ekle.
31. Gradient clipping fonksiyonu yaz ve norm sınırını test et.
32. Step-decay learning-rate schedule yaz.
33. Exponential-decay schedule yaz.
34. Cosine-decay schedule yaz.
35. `NaN` gradient geldiğinde eğitimi güvenli biçimde durduran kontrol ekle.
36. Parametre update normunu hesaplayan fonksiyon yaz.

## E. Optimizer karşılaştırması

37. Vanilla SGD ve momentum'u aynı quadratic fonksiyonda karşılaştır.
38. Momentum katsayılarını `0.0`, `0.5`, `0.9`, `0.99` için tara.
39. AdaGrad effective learning rate'inin zamanla neden küçüldüğünü sayısal örnekle göster.
40. RMSProp'un AdaGrad'dan farkını state denklemleriyle açıkla.
41. Adam'ın bias correction uygulamadan ilk adımlarda nasıl yanlı davranacağını göster.
42. Adam ve AdamW arasındaki weight-decay farkını açıkla.
43. Aynı learning rate'i SGD ve Adam arasında doğrudan karşılaştırmanın neden adil olmadığını tartış.
44. Adaptive optimizer'ın seyrek gradient'lerde sağlayabileceği avantajı örnekle.
45. SGD'nin bazı problemlerde Adam'dan daha iyi genelleme gösterebilmesinin olası nedenlerini tartış.

## F. Tanılama ve üretim

46. Training loss azalırken validation loss artıyorsa teşhis ve müdahale planı yaz.
47. Loss her adımda aşağı-yukarı hareket ediyorsa üç olası neden yaz.
48. Gradient normu büyürken update normu küçük kalıyorsa optimizer açısından ne düşünülebilir?
49. Update normu büyürken gradient normu sabitse hangi state veya learning-rate problemi olabilir?
50. Early stopping için `patience` ve `minimum_delta` değerlerinin etkisini açıkla.
51. En iyi checkpoint yerine son checkpoint'i yüklemenin riskini açıkla.
52. Eğitim kesintisinden devam etmek için neden yalnızca model parametreleri yetmez?
53. Seed sabit olsa bile sonuçların farklı çıkabileceği sistem düzeyindeki iki nedeni yaz.
54. Küçük bir veri alt kümesinde overfit testinin hangi hataları yakalayabileceğini listele.
55. Bir optimizer deneyinin yeniden üretilebilir olması için kaydedilmesi gereken alanları tanımla.

## G. Meydan okuma problemleri

56. Rosenbrock fonksiyonunu saf Python ile uygula ve sayısal gradient ile optimize et.
57. Aynı fonksiyonda momentumun yolu nasıl değiştirdiğini ölç.
58. Kendi Nesterov implementasyonunu yaz ve lookahead gradient'ini doğrula.
59. Mini-batch gradient varyansını farklı batch size değerleri için ampirik olarak ölç.
60. Bir optimizer'ın convergence speed metriğini tanımla ve gerekçelendir.
61. Final loss ile wall-clock time arasında Pareto karşılaştırması tasarla.
62. Loss, gradient normu ve update normundan basit bir otomatik uyarı sistemi geliştir.
63. Learning-rate range test uygula: küçük değerden başlayıp her adım artır ve loss davranışını incele.
64. Warmup + cosine decay birleşimi uygula.
65. Saf Python optimizer state'ini JSON uyumlu biçimde kaydet ve yeniden yükle.

## Teslim standardı

Her kod alıştırmasında:

- Type hint kullan.
- Hatalı girdiler için açık exception üret.
- En az bir normal ve bir edge-case testi yaz.
- Rastgelelik varsa seed belirle.
- Sonucu loss, gradient normu veya bilinen analitik çözümle doğrula.
