# Mülakat Soruları — SVM, Margin, Kernel ve Ölçekleme

Sorular; temel kavram, matematik, uygulama, hata ayıklama ve üretim tasarımını birlikte ölçer. Her cevapta varsayım, trade-off ve mümkünse sayısal örnek beklenir.

## Temel ve geometri

1. Maximum-margin sınıflandırıcı neyi optimize eder? Geometrik sezgiyle açıkla.
2. Functional margin ile geometric margin arasındaki fark nedir?
3. `w` ve `b` aynı pozitif katsayıyla çarpıldığında karar sınırı değişmezken functional margin neden değişir?
4. Canonical hyperplane ölçeklemesi nedir ve `2/||w||` formülü nasıl elde edilir?
5. Support vector nedir? Karar sınırının yalnızca bu örneklere bağlı olması ne anlama gelir?
6. Hard-margin SVM hangi varsayımları gerektirir ve gerçek veride neden kırılgandır?
7. Soft margin'de slack variable değerlerini `0`, `(0,1]` ve `>1` aralıklarında yorumla.
8. Büyük `C` ve küçük `C` için bias–variance davranışını karşılaştır.
9. Hinge loss'un logistic loss'a göre farkları nelerdir?
10. Hinge loss'un sıfır olduğu örnekler gradient'e neden katkı vermez?

## Optimizasyon ve dual form

11. Primal soft-margin SVM objective ve kısıtlarını yaz.
12. SVM dual problemine neden ihtiyaç duyulur?
13. Lagrange multiplier'ların SVM'deki rolü nedir?
14. KKT koşullarını support vector davranışıyla ilişkilendir.
15. `alpha_i=0`, `0<alpha_i<C` ve `alpha_i=C` durumları ne anlatır?
16. Dual formda karar fonksiyonunun yalnızca iç çarpımlara bağlı olması kernel trick'i nasıl mümkün kılar?
17. SVM optimizasyon probleminin convex olması neden önemlidir?
18. SMO algoritmasının temel fikri nedir?

## Kernel ve feature uzayı

19. Kernel trick'i açık feature mapping ile karşılaştırarak açıkla.
20. Gram matrix nedir ve neden simetrik olmalıdır?
21. Positive semidefinite kernel ne demektir?
22. Mercer koşullarının pratik kernel tasarımı açısından anlamı nedir?
23. Linear kernel ne zaman RBF kernel'dan daha iyi bir başlangıçtır?
24. Polynomial kernel'da degree, gamma ve coef0 nasıl etkileşir?
25. RBF kernel'da gamma parametresini örneklerin etki yarıçapı üzerinden yorumla.
26. Büyük `C` ve büyük `gamma` birlikte kullanıldığında ne tür bir hata profili beklersin?
27. Küçük `C` ve küçük `gamma` birlikte kullanıldığında ne tür bir hata profili beklersin?
28. Sigmoid kernel neden her parametre kombinasyonunda geçerli bir kernel olmayabilir?
29. Custom kernel yazarken hangi matematiksel ve yazılımsal kontrolleri yaparsın?
30. Precomputed kernel kullanırken train ve test kernel matrix boyutları nasıl olmalıdır?

## Scaling, sparse veri ve model seçimi

31. SVM neden feature scaling'e duyarlıdır?
32. StandardScaler, MinMaxScaler ve RobustScaler arasında nasıl seçim yaparsın?
33. Sparse text verisinde centering neden sorun yaratır?
34. `LinearSVC`, `SVC(kernel="linear")` ve `SGDClassifier(loss="hinge")` seçeneklerini ölçeklenebilirlik açısından karşılaştır.
35. RBF SVC neden yüz binlerce örnekte problemli olabilir?
36. `gamma="scale"` ve `gamma="auto"` arasındaki fark nedir?
37. Grid search'ü pipeline dışında yapmak nasıl leakage oluşturabilir?
38. `C` ve `gamma` için logaritmik aralıklar neden tercih edilir?
39. Validation curve ile learning curve farklı hangi soruları cevaplar?
40. Nested cross-validation ne zaman gereklidir?

## Dengesizlik, calibration ve threshold

41. `class_weight="balanced"` nasıl hesaplanır ve loss'u nasıl etkiler?
42. Class weighting ile oversampling arasındaki farklar nelerdir?
43. Class weighting ile threshold tuning neden aynı işlem değildir?
44. SVM `decision_function` çıktısı neden doğrudan olasılık değildir?
45. Platt scaling nasıl çalışır?
46. Isotonic calibration hangi durumda sigmoid calibration'dan daha iyi olabilir?
47. Isotonic calibration az veride neden overfit olabilir?
48. Calibration kalitesini hangi metrik ve grafiklerle değerlendirirsin?
49. ROC-AUC iyi olduğu hâlde Brier score neden kötü olabilir?
50. False negative maliyeti false positive maliyetinden çok yüksekse threshold'u nasıl seçersin?

## Çok sınıf, yorumlama ve üretim

51. One-vs-one ve one-vs-rest stratejilerinin model sayısı ve prediction cost farkı nedir?
52. `SVC` ve `LinearSVC` çok sınıflı problemi nasıl ele alır?
53. Çok sınıflı decision score'ların yorumlanmasında hangi sorunlar ortaya çıkar?
54. Support vector oranının çok yüksek olması neye işaret edebilir?
55. Bir SVM modelini debug ederken ilk kontrol edeceğin beş şey nedir?
56. Eğitim skoru yüksek, validation skoru düşük bir RBF SVM'i nasıl düzeltirsin?
57. Eğitim ve validation skorları birlikte düşükse hangi hiperparametre ve feature kontrollerini yaparsın?
58. Segment bazlı recall farkları üretimde nasıl risk oluşturur?
59. Bir SVM pipeline'ını serialize ederken model dışında hangi artefaktları saklarsın?
60. Üretimde hangi drift, latency, calibration ve maliyet metriklerini izlersin?

## Sistem tasarımı senaryoları

61. Bir milyon sparse doküman ve yüz bin feature içeren spam sistemi için SVM tasarımını anlat.
62. On bin örnekli, doğrusal olmayan sensör verisi için model ve kernel seçimini savun.
63. Pozitif oranı %0,5 olan fraud probleminde split, metric, class weight, calibration ve threshold sürecini tasarla.
64. Aynı entity'nin farklı satırlarda bulunduğu bir veri setinde leakage-safe cross-validation nasıl kurulur?
65. Modelin probability calibration'ı zaman içinde bozulursa yeniden eğitim yapmadan hangi ara çözümler uygulanabilir?
66. Kernel SVC latency hedefini karşılamıyorsa hangi alternatifleri değerlendirirsin?
67. Yeni bir kategori production'da ilk kez görülürse pipeline nasıl davranmalıdır?
68. Bir aday model daha yüksek ROC-AUC, diğeri daha düşük toplam iş maliyeti üretiyor. Hangisini seçersin ve neden?
69. Hyperparameter search sonrası raporlanan skorun iyimser olduğunu nasıl tespit edersin?
70. SVM'in modern gradient boosting veya neural network yerine tercih edilmesini haklı çıkaran bir kullanım senaryosu ver.
