# Quiz

1. Binary search hangi ön koşulu gerektirir?
2. Linear search'ün en kötü durum zaman karmaşıklığı nedir?
3. Neredeyse sıralı küçük bir veri kümesi için hangi basit sıralama algoritması uygundur?
4. Merge sort'un zaman karmaşıklığı nedir?
5. Merge sort neden `O(n)` ek alan kullanabilir?
6. Quick sort hangi durumda `O(n²)` çalışabilir?
7. Recursive fonksiyondaki base case ne işe yarar?
8. `T(n) = T(n/2) + O(1)` hangi büyüme sınıfına karşılık gelir?
9. Stable sorting ne demektir?
10. Tek benchmark çalıştırması neden yeterli değildir?

## Cevap anahtarı

1. Verinin sıralı ve karşılaştırılabilir olması.
2. `O(n)`.
3. Insertion sort.
4. `O(n log n)`.
5. Birleştirme sırasında geçici koleksiyon tuttuğu için.
6. Pivotlar sürekli dengesiz bölmeler oluşturduğunda.
7. Recursive çağrı zincirini durdurur.
8. `O(log n)`.
9. Eşit anahtarlı elemanların göreli sırasının korunmasıdır.
10. Sistem yükü ve ölçüm gürültüsü sonucu etkileyebilir; tekrar gerekir.
