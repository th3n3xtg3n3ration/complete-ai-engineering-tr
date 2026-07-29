# Alıştırmalar — SVM, Margin, Kernel ve Ölçekleme

Alıştırmalar kolaydan zora ilerler. Her çözümde varsayımlarını, kullandığın metriği ve veri sızıntısını nasıl önlediğini açıkla.

## A. Geometri ve margin

1. İki boyutlu, doğrusal ayrılabilir sekiz nokta oluştur ve sınıfları ayıran üç farklı doğru çiz. Hangi doğrunun margin'i en büyük, hesapla.
2. `w=[3,4]` olan canonical bir hiper-düzlemin toplam margin genişliğini hesapla.
3. Bir örnek için functional margin ile geometric margin arasındaki farkı sayısal örnekle göster.
4. `y_i(w^T x_i+b)=1` koşulunu sağlayan üç noktanın neden support vector adayı olduğunu açıkla.
5. Aynı karar sınırını temsil eden `(w,b)` ve `(2w,2b)` çiftlerinin functional margin'lerini karşılaştır.
6. Hard-margin SVM'in tek bir yanlış etiketli örnek nedeniyle neden çözümsüz kalabileceğini çizimle göster.
7. Margin içinde fakat doğru sınıflandırılmış bir örnek üret; slack değerini hesapla.
8. Yanlış sınıflandırılmış bir örnek için slack değerinin neden 1'den büyük olduğunu göster.
9. İki farklı `w` vektörü için `0.5 * ||w||²` regularization terimini hesapla ve geniş margin ile ilişkilendir.
10. Canonical hiper-düzlem varsayımı olmadan `2/||w||` formülünün neden doğrudan kullanılamayacağını açıkla.

## B. Hinge loss ve optimizasyon

11. Hinge loss'u yalnızca NumPy kullanarak sıfırdan uygula.
12. `y=[1,-1,1]`, skorlar `[1.4,-0.2,-2.0]` için örnek bazlı ve ortalama hinge loss hesapla.
13. Hinge loss ile logistic loss'u aynı karar skorları üzerinde karşılaştır.
14. `C=0.1`, `1` ve `100` için primal objective değerlerini aynı `w` ve skorlarla hesapla.
15. Hinge loss'un türevlenemediği noktayı belirle ve subgradient yaklaşımını açıkla.
16. Lagrangian'a ait primal değişkenleri, dual değişkenleri ve kısıtları tablo halinde yaz.
17. KKT complementary slackness koşulunu support vector davranışıyla ilişkilendir.
18. `alpha_i=0`, `0<alpha_i<C` ve `alpha_i=C` durumlarını geometrik olarak yorumla.
19. Küçük bir veri seti için Gram matrix oluştur ve simetrik olduğunu doğrula.
20. Bir Gram matrix'in özdeğerlerini hesaplayarak positive semidefinite olup olmadığını kontrol et.

## C. Kernel fonksiyonları

21. Linear kernel'i NumPy ile uygula ve matris çarpımıyla doğrula.
22. Degree 2 polynomial kernel için açık feature mapping'i iki özellikli veri üzerinde türet.
23. Polynomial kernel'da `coef0=0` ve `coef0=1` sonuçlarını karşılaştır.
24. RBF kernel'i sıfırdan uygula ve `K(x,x)=1` özelliğini test et.
25. `gamma=0.01`, `0.1`, `1` ve `10` için aynı iki noktanın RBF benzerliğini hesapla.
26. RBF Gram matrix'in sayısal yuvarlama toleransı içinde PSD olduğunu test et.
27. Sigmoid kernel'in her parametre seçimi için geçerli kernel olmayabileceğini araştır ve kısa not yaz.
28. Kendi custom kernel fonksiyonunu `SVC(kernel=callable)` ile kullan.
29. Precomputed kernel ile eğitim ve tahmin için gerekli train/test matris boyutlarını göster.
30. Linear kernel ile `SVC(kernel="linear")` karar skorlarını doğrudan lineer modele karşılaştır.

## D. Ölçekleme ve veri hazırlama

31. Bir özelliği metre, diğerini milimetre ölçeğinde olan veri üret; scaling öncesi ve sonrası karar sınırını karşılaştır.
32. `StandardScaler`, `MinMaxScaler` ve `RobustScaler` ile RBF SVM sonuçlarını karşılaştır.
33. Scaling'i split öncesinde uygulayarak kasıtlı leakage oluştur ve doğru pipeline sonucu ile farkı ölç.
34. Sayısal ve kategorik sütunlar için `ColumnTransformer` tabanlı SVM pipeline kur.
35. Eksik sayısal değerleri median, kategorik değerleri most-frequent stratejisiyle doldur.
36. Eğitimde görülmeyen kategorinin `OneHotEncoder(handle_unknown="ignore")` ile işlendiğini test et.
37. Sparse text verisinde neden `StandardScaler(with_mean=False)` gerektiğini açıkla.
38. TF-IDF + LinearSVC kullanarak küçük bir metin sınıflandırma deneyi yap.
39. Yüksek boyutlu seyrek veride LinearSVC ile RBF SVC eğitim süresini karşılaştır.
40. Pipeline'ın yalnızca train fold üzerinde fit edildiğini doğrulayan bir otomatik test yaz.

## E. Model seçimi ve değerlendirme

41. Linear SVM için `C` validation curve üret ve underfitting/overfitting bölgelerini yorumla.
42. RBF SVM için `C` ve `gamma` değerlerinden oluşan heatmap üret.
43. `gamma="scale"` ile `gamma="auto"` sonuçlarını aynı veri üzerinde karşılaştır.
44. Stratified 5-fold CV ile ROC-AUC, average precision ve balanced accuracy raporla.
45. Dengesiz veri üzerinde accuracy'nin neden yanıltıcı olduğunu göster.
46. `class_weight=None` ile `class_weight="balanced"` sonuçlarını minority recall açısından karşılaştır.
47. Validation kümesinde F1'i maksimize eden karar threshold'unu seç.
48. False negative maliyeti ₺400, false positive maliyeti ₺25 iken toplam maliyeti minimize eden threshold'u bul.
49. Seçilen threshold'u test kümesine yalnızca bir kez uygula ve sonucu raporla.
50. GridSearchCV ile seçilen parametrelerin nested CV tahminine göre neden iyimser olabileceğini göster.

## F. Calibration, çok sınıf ve üretim

51. LinearSVC karar skorlarını sigmoid calibration ile olasılığa dönüştür.
52. Sigmoid ve isotonic calibration'ı Brier score ve log loss ile karşılaştır.
53. En az 10 bin örnek olmadan isotonic calibration kullanmanın riskini tartış.
54. Reliability diagram üret ve aşırı güvenli tahmin bölgelerini belirle.
55. Üç sınıflı veri üzerinde SVC'nin one-vs-one davranışını incele.
56. Aynı veri üzerinde OneVsRestClassifier + LinearSVC kur ve eğitim sürelerini karşılaştır.
57. Support vector sayısını sınıf bazında raporla; yüksek oranın olası nedenlerini yorumla.
58. Veri büyüklüğünü kademeli artırarak kernel SVC eğitim süresi eğrisi üret.
59. Model artefaktıyla birlikte scaler, feature sırası, sınıf etiketleri ve dependency sürümlerini kaydet.
60. Veri drift'i, latency, calibration drift ve segment performansı için üretim izleme planı hazırla.

## Teslim standardı

Her alıştırma çözümü mümkün olduğunda şu bileşenleri içermelidir:

- yeniden üretilebilir kod ve sabit `random_state`,
- train/validation/test ayrımı,
- uygun metrik ve kısa yorum,
- en az bir otomatik doğrulama,
- leakage ve üretim riski değerlendirmesi.
