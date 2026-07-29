# Alıştırmalar — Vektörler, Matrisler ve Tensörler

## Temel seviye

1. Skaler, vektör, matris ve rank-3 tensöre birer AI örneği ver.
2. `(32, 128)` shape'ine sahip bir veri yapısında eksenlerin anlamını açıkla.
3. `(8, 512, 768)` tensörünün rank değerini ve toplam eleman sayısını hesapla.
4. `[2, -1, 3] + [4, 5, -2]` işlemini yap.
5. `-3 × [2, 0, -4]` işlemini yap.
6. `[1, 2, 3] · [4, 0, -1]` dot product'ını hesapla.
7. `[1, 2]` ve `[3, 4, 5]` vektörlerinin outer product matrisini yaz.
8. `[-3, 4]` vektörünün L1, L2 ve infinity normlarını hesapla.
9. `[3, 4]` vektörünü L2 normalize et.
10. Sıfır vektörünün neden normalize edilemediğini açıkla.

## Orta seviye

11. Aşağıdaki matrisin transpose'unu bul:

```text
[[1, 2, 3],
 [4, 5, 6]]
```

12. `(5, 3)` ve `(3, 7)` matrislerinin çarpım sonucunun shape'ini bul.
13. `(5, 3)` ile `(4, 2)` matrislerinin neden çarpılamadığını açıkla.
14. Bir dense katmanda input `(64, 128)`, weight `(128, 32)` ise output shape nedir?
15. `(64, 32)` çıktıya `(32,)` bias eklenmesinin broadcasting mantığını açıkla.
16. `[1, 0]` ile `[10, 0]` için cosine similarity ve Euclidean distance davranışını karşılaştır.
17. `[1, 1]` ile `[-1, -1]` vektörlerinin cosine similarity değerini hesapla.
18. Rectangular matris ile ragged nested list arasındaki farkı örnekle göster.
19. `zip(left, right)` kullanımının farklı uzunluktaki vektörlerde oluşturabileceği sessiz hatayı açıkla.
20. Floating-point sonuçları test ederken neden yaklaşık karşılaştırma kullanılmalıdır?

## Kodlama

21. `hadamard_product(left, right)` fonksiyonunu shape doğrulamasıyla geliştir.
22. `manhattan_distance(left, right)` fonksiyonunu yaz.
23. `matrix_trace(matrix)` fonksiyonunu yalnızca kare matrisler için uygula.
24. `identity_matrix(size)` fonksiyonunu yaz.
25. `batch_cosine_similarity(query, candidates)` fonksiyonunu geliştir.
26. Bir matrisin her sütununun ortalamasını döndüren `column_means` fonksiyonunu yaz.
27. Bir batch içindeki her satırı L2 normalize eden `normalize_rows` fonksiyonunu geliştir.
28. `reshape` fonksiyonu için `(2, 0, 3)` gibi sıfır boyutlu shape davranışını tanımla ve test et.
29. `tensor_shape` fonksiyonuna tuple ve list karışımını kapsayan test ekle.
30. `matrix_multiply` için identity matrix özelliğini test et.

## AI mühendisliği senaryoları

31. Bir embedding servisinde vektör boyutu 768'den 1024'e değişti. Hangi katmanlarda ve doğrulamalarda değişiklik gerekir?
32. Doküman embedding'lerinin büyüklüğü kalite sinyali taşıyorsa L2 normalizasyonunun riskini açıkla.
33. Bir image tensor `(16, 224, 224, 3)` olarak geliyor fakat model `(16, 3, 224, 224)` bekliyor. Gerekli eksen dönüşümünü açıkla.
34. Attention işleminde query `(batch, heads, query_length, depth)` ve transposed key `(batch, heads, depth, key_length)` ise score shape nedir?
35. Gradient clipping için global L2 norm kullanmanın amacını açıkla.
36. L1 regularization'ın neden bazı ağırlıkları tam sıfıra yaklaştırabildiğini sezgisel olarak anlat.
37. Cosine similarity yüksek fakat Euclidean distance da yüksek olan iki vektörün geometrisini açıkla.
38. Benzerlik aramasında top-k sıralamasının metric seçimine bağlı değişmesini nasıl test edersin?
39. Batch, sequence ve hidden eksenlerinin karıştırılması hangi tür sessiz hatalara yol açabilir?
40. Shape bilgisini type hint, runtime validation ve test seviyelerinde nasıl korursun?

## Meydan okuma

`VectorIndex` adlı küçük bir sınıf geliştir:

- Sabit embedding dimension kabul etsin.
- Doküman ID tekrarını reddetsin.
- Sıfır ve non-finite vektörleri reddetsin.
- Cosine ve Euclidean metric desteklesin.
- İsteğe bağlı L2 normalizasyonu uygulasın.
- `search(query, top_k)` ile kararlı sıralama döndürsün.
- Eşit skor durumunda document ID ile deterministik tie-break yapsın.
- En az 15 pytest testi içersin.
