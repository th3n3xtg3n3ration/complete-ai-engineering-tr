# Teori — Keşifsel Veri Analizi ve Görselleştirme

## 1. EDA'nın amacı

Keşifsel veri analizi yalnızca grafik üretmek değildir. Amaç; veri toplama sürecini, kalite sorunlarını, değişken dağılımlarını, segment farklarını ve modelleme risklerini sistematik biçimde ortaya çıkarmaktır.

İyi bir EDA şu sorulara yanıt verir:

- Her satır ve kolon neyi temsil ediyor?
- Gözlem birimi nedir?
- Hangi değerler eksik, geçersiz veya tekrar ediyor?
- Dağılımlar ve segment farkları nasıl?
- Hedef değişken dengeli mi?
- Zaman, grup veya veri kaynağı kaynaklı sapmalar var mı?
- Görülen ilişki gerçek bir mekanizmayı mı, veri üretim hatasını mı gösteriyor?

## 2. Önce veri sözleşmesi

Grafik çizmeden önce kolon anlamı, dtype, ölçü birimi, izin verilen aralık, missing anlamı, benzersizlik kuralı, zaman dilimi ve gözlem birimi netleştirilmelidir. EDA veri sözleşmesinin yerine geçmez; sözleşmenin veride karşılanıp karşılanmadığını kontrol eder.

## 3. Yapısal profil

Temel profil en az satır/kolon sayısı, dtype dağılımı, eksik hücre sayısı, duplicate satır sayısı, bellek tüketimi ve kolon rollerini içermelidir. Örneklem kullanılıyorsa seçim yöntemi raporda açıklanmalıdır.

## 4. Sayısal değişkenler

Tek başına ortalama yeterli değildir. Count, missing count, mean, median, standard deviation, minimum, maximum, Q1, Q3, IQR ve skewness birlikte değerlendirilmelidir. Mean–median farkı çarpıklığa işaret edebilir; ancak gelir ve işlem tutarı gibi değişkenlerde çarpıklık doğal olabilir.

## 5. Kategorik değişkenler

Kategorik kolonlarda benzersiz değer sayısı, sınıf count/rate değerleri, missing sınıf, rare category ve yazım normalizasyonu incelenir. Yüksek kardinalite kimlik alanına, serbest metne veya standardizasyon sorununa işaret edebilir.

## 6. Dağılım grafikleri

Histogram dağılım şeklini gösterir. Bin sayısı çok düşükse yapı gizlenir, çok yüksekse gürültü büyür. Grafik yorumlanırken örneklem büyüklüğü ve sessizce düşürülen missing değerler belirtilmelidir.

## 7. Kategorik grafikler

Bar chart count veya rate karşılaştırması için uygundur. Çok fazla kategori varsa top-N ve açık bir `other` kuralı uygulanabilir. Eksen sıfırdan başlamadığında küçük farklar abartılabilir.

## 8. İlişki analizi

Scatter plot iki sayısal değişken arasındaki kümeleri, aykırı gözlemleri ve doğrusal olmayan yapıları gösterir. Pearson doğrusal ilişkiyi, Spearman sıralama temelli monoton ilişkiyi ölçer.

Korelasyon:

- nedensellik kanıtlamaz,
- aykırı değerlere duyarlı olabilir,
- doğrusal olmayan ilişkileri kaçırabilir,
- üçüncü bir değişken nedeniyle yüksek görünebilir.

## 9. Segment analizi

Global ortalama davranış farklarını gizleyebilir. Segment analizi müşteri tipi, bölge, ürün, cihaz, kanal, dönem veya hedef sınıf üzerinden yapılabilir. Her segmentte `count` mutlaka raporlanmalıdır; küçük segment oranları oynaktır.

## 10. Zaman analizi

Veri hacmi, toplam/ortalama metrik, missing oranı, kategori dağılımı ve hedef oranı zaman içinde izlenmelidir. Ani kırılmalar gerçek iş değişikliği, ölçüm sistemi değişikliği veya pipeline hatası olabilir.

## 11. Missingness

Kolon bazlı missing rate başlangıçtır. Daha derin analizde eksikliklerin birlikte oluşumu, segment ve zamanla ilişkisi incelenir. Missingness rastgele değilse imputation yanlı sonuç üretebilir.

## 12. Korelasyon heatmap'i

Heatmap çok sayıda sayısal değişkeni özetler; fakat kolon sayısı arttıkça okunabilirlik düşer, türetilmiş feature'lar tekrar eden ilişkiler yaratır ve target proxy alanları gizlenebilir. Heatmap keşif aracıdır, karar mekanizması değildir.

## 13. Hedef değişken

Supervised learning öncesinde hedefin missing count'u, sınıf dağılımı, pozitif oranı, zaman içindeki değişimi, segmentlere göre dağılımı ve üretim zamanı incelenmelidir. Hedef sonrasında oluşan feature'lar leakage yaratabilir.

## 14. Görselleştirme etiği

Yanıltıcı grafikler çoğunlukla ekseni kesmek, log scale'i belirtmemek, seçilmiş zaman aralığı kullanmak, küçük örneklemi gizlemek, paydayı açıklamamak veya missing gözlemleri sessizce düşürmekten doğar.

## 15. Tekrarlanabilir EDA

Üretim kalitesinde EDA:

- açık bir config kullanır,
- kolon rollerini görünür tutar,
- hesaplamaları fonksiyonlara ayırır,
- notebook dışından çalışır,
- CSV/JSON gibi makinece okunabilir tablolar üretir,
- grafikleri deterministik adlarla kaydeder,
- testlerle doğrulanır,
- veri ve kod sürümünü kaydeder.

## 16. Ders mimarisi

`eda_foundations.py` istatistiksel tabloları, `visualization.py` Matplotlib figürlerini, `eda_report.py` ise Markdown, CSV, JSON ve PNG artefaktlarının orkestrasyonunu yönetir. Böylece hesaplama, sunum ve raporlama sorumlulukları ayrılır.
