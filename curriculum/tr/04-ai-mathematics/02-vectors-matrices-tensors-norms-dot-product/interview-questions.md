# Mülakat Soruları — Vektörler, Matrisler ve Tensörler

## Temel kavramlar

1. Skaler, vektör, matris ve tensör arasındaki fark nedir?
2. Shape, rank ve axis kavramlarını bir NLP tensörü üzerinden açıklar mısın?
3. Dot product geometrik olarak ne ifade eder?
4. Outer product hangi shape'i üretir ve nerelerde kullanılabilir?
5. Matrix multiplication için boyut uyumluluğu kuralı nedir?
6. Transpose işlemi shape'i nasıl değiştirir?
7. L1, L2 ve infinity normları arasındaki fark nedir?
8. Normalizasyon ile standardizasyon aynı şey midir?
9. Cosine similarity hangi aralıkta değer alır?
10. Sıfır vektörü için cosine similarity neden hesaplanamaz?

## Uygulama ve mühendislik

11. Farklı uzunluktaki vektörleri `zip` ile çarpmak neden risklidir?
12. Ragged nested list neden geçerli bir dense tensor değildir?
13. Floating-point lineer cebir sonuçlarını nasıl test edersin?
14. Bir matrix multiplication API'sinde hangi validasyonları yaparsın?
15. Bir embedding dimension değişikliği üretim sistemini nasıl etkiler?
16. Cosine similarity ile Euclidean distance arasında nasıl seçim yaparsın?
17. L2 normalize edilmiş vektörlerde dot product neden cosine similarity'ye eşittir?
18. Normalizasyon hangi durumda anlamlı bilgiyi yok edebilir?
19. Batch matris işlemleri neden tek tek örnek işlemekten daha verimlidir?
20. Broadcasting sessiz bir mantık hatasına nasıl dönüşebilir?

## AI bağlantıları

21. Dense layer işlemini shape'lerle açıkla.
22. Attention mekanizmasında query-key dot product neden kullanılır?
23. Scaled dot-product attention neden ölçekleme uygular?
24. Embedding retrieval sisteminde top-k arama nasıl çalışır?
25. Gradient clipping ile norm kavramı arasındaki ilişki nedir?
26. L1 regularization ile sparsity arasındaki ilişki nedir?
27. L2 regularization ağırlıkları nasıl etkiler?
28. Bir görüntü tensöründe channels-first ve channels-last farkı nedir?
29. Transformer hidden state tensörünün eksenleri neyi temsil eder?
30. Vector database'e yazılan embedding'lerde dimension sözleşmesini nasıl korursun?

## Tasarım soruları

31. Saf Python ile güvenli bir `matrix_multiply` fonksiyonu tasarla.
32. Sabit dimension kullanan bir `VectorIndex` API'si tasarla.
33. Cosine ve Euclidean metric destekleyen arama sonuçlarını nasıl tek bir arayüzde modelliyorsun?
34. Eşit skorlu sonuçlarda deterministik sıralamayı nasıl sağlarsın?
35. Embedding servisinde non-finite değerleri hangi sınırda reddedersin?
36. Normalizasyonu kayıt sırasında mı sorgu sırasında mı yaparsın? Trade-off'ları açıkla.
37. Büyük veri kümesinde saf Python aramasından approximate nearest neighbor sistemine geçiş planını anlat.
38. Bir modelin beklediği `(batch, sequence, hidden)` yerine `(sequence, batch, hidden)` geldiğinde hatayı nasıl teşhis edersin?
39. Shape sözleşmesini type hints, schema validation, runtime assertion ve tests ile nasıl güçlendirirsin?
40. Bir embedding model güncellemesinden sonra eski ve yeni vektörlerin aynı index'te karışmasını nasıl önlersin?

## Kısa problem çözme

41. `[1, 2, 3] · [4, 5, 6]` sonucunu hesapla.
42. `(12, 64) @ (64, 256)` sonucunun shape'i nedir?
43. `[3, 4]` vektörünün normalize edilmiş halini bul.
44. `[1, 0]` ile `[0, 1]` cosine similarity değeri nedir?
45. `(8, 12, 16)` tensörünün toplam eleman sayısı nedir?
46. `[[1, 2], [3]]` yapısının shape'i neden güvenilir biçimde tanımlanamaz?
47. İki vektör aynı yönde fakat çok farklı büyüklükteyse cosine ve Euclidean sonuçları nasıl davranır?
48. Identity matrix ile çarpımın sonucu neden girdiye eşittir?
49. Orthogonal iki vektörün dot product sonucu nedir?
50. Bir rank-4 image tensor için olası iki axis düzeni yaz.

## Güçlü cevapta beklenenler

- Formülün yanında geometrik sezgi
- Shape dönüşümünün açık yazılması
- Edge case ve failure mode'ların belirtilmesi
- Metric seçiminin veri semantiğine bağlanması
- Normalizasyonun koşulsuz iyi kabul edilmemesi
- Üretim sistemlerinde validation, versioning ve test yaklaşımı
