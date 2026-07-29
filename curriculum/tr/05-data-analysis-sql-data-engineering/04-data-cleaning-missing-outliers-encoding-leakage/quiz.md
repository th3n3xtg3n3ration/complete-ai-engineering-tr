# Quiz

1. MCAR neyi ifade eder?
2. Median hangi dağılımlarda mean'e göre daha dayanıklıdır?
3. IQR nasıl hesaplanır?
4. Her aykırı değer neden silinmemelidir?
5. One-hot encoding hangi kategori türü için uygundur?
6. Ordinal encoding hangi koşulda anlamlıdır?
7. Bilinmeyen kategori neden ayrı yönetilmelidir?
8. Rare-category eşiği neden yalnızca train verisinde öğrenilmelidir?
9. `fit` ile `transform` arasındaki temel fark nedir?
10. Preprocessing leakage nasıl oluşur?
11. Target leakage örneği ver.
12. Temporal leakage örneği ver.
13. Entity leakage nedir?
14. Aynı row ID'nin iki split'te bulunması ne anlama gelir?
15. Time-based split hangi problemlerde gereklidir?
16. Aggregation leakage nasıl oluşur?
17. Missing indicator ne zaman yararlı olabilir?
18. Clipping ile satır silme arasındaki fark nedir?
19. Pipeline neden girdiyi yerinde değiştirmemelidir?
20. Olağandışı yüksek validation skoru neden leakage sinyali olabilir?

## Cevap anahtarı

1. Eksikliğin gözlenen ve gözlenmeyen değişkenlerden bağımsız olmasını.
2. Çarpık ve uç değer içeren dağılımlarda.
3. `Q3 - Q1`.
4. Nadir fakat geçerli ve iş açısından önemli sinyal olabilir.
5. Nominal kategoriler için.
6. Gerçek ve anlamlı bir sıralama varsa.
7. Üretimde kolon kayması ve sessiz hata oluşmaması için.
8. Evaluation dağılımı preprocessing kararına sızmamalıdır.
9. Fit istatistik öğrenir; transform öğrenilen durumu uygular.
10. Tüm veri üzerinde imputation, scaling veya encoding fit edilirse.
11. Hedefin doğrudan kopyasının feature olması.
12. Tahmin anından sonraki bilginin feature olması.
13. Aynı varlığın benzer kayıtlarının split'lere dağılması.
14. Doğrudan satır sızıntısı.
15. Forecasting, churn, fraud ve zamanla değişen süreçlerde.
16. Özet pencere geleceği veya hedef satırı içerirse.
17. Eksikliğin kendisi bilgi taşıyorsa.
18. Clipping satırı korur, silme gözlemi kaldırır.
19. Tekrarlanabilirlik ve yan etki kontrolü için.
20. Model gerçek dışı bilgi kullanıyor olabilir.
