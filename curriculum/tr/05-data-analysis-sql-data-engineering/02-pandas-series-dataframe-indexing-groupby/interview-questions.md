# Mülakat Soruları — pandas Series, DataFrame, İndeksleme ve GroupBy

## Temel sorular

1. pandas Series ile NumPy array arasındaki temel farklar nelerdir?
2. Index alignment nasıl çalışır ve hangi hatalara yol açabilir?
3. `loc` ve `iloc` arasındaki farkı örnekle açıkla.
4. `at` ve `iat` ne zaman tercih edilir?
5. pandas nullable dtype'ları neden vardır?
6. `object`, `string` ve `category` dtype'larını karşılaştır.
7. `NaN`, `None`, `pd.NA` ve `NaT` arasındaki farklar nelerdir?
8. Chained assignment nedir ve neden risklidir?
9. View ve copy davranışı neden önemlidir?
10. Bir DataFrame'in gerçek bellek kullanımını nasıl ölçersin?

## GroupBy soruları

11. Split–apply–combine modelini açıkla.
12. `agg`, `transform`, `filter` ve `apply` farkları nelerdir?
13. Grup ortalamasından satır bazında sapma nasıl hesaplanır?
14. Eksik grup anahtarlarını nasıl korursun?
15. `observed=True` kategorik gruplamada neyi değiştirir?
16. MultiIndex çıktısını düz şemaya nasıl dönüştürürsün?
17. Her gruptaki en yüksek üç satırı deterministik biçimde nasıl seçersin?
18. `groupby().apply()` neden performans sorunu yaratabilir?

## Birleştirme soruları

19. `merge`, `join` ve `concat` arasındaki farkları açıkla.
20. `one_to_one`, `one_to_many`, `many_to_one` ve `many_to_many` ne anlama gelir?
21. Merge sonrası satır sayısının beklenmedik biçimde artmasının olası nedeni nedir?
22. `validate` parametresi hangi veri kalitesi problemini yakalar?
23. `left join` sonucunda sağ taraftan eşleşmeyen kayıtları nasıl tespit edersin?
24. Aynı isimli anahtar kolonları farklı adlara sahipse nasıl merge yaparsın?
25. Aylık dosyaları concat ederken hangi şema kontrollerini uygularsın?

## Veri kalitesi ve pipeline soruları

26. Duplicate kayıt çözümleme politikası nasıl tasarlanmalıdır?
27. Hatalı tarihleri sessizce `NaT` yapmak neden risklidir?
28. Median imputation neden yalnızca eğitim verisinde fit edilmelidir?
29. Testte yeni bir kategori geldiğinde ne yaparsın?
30. Deterministik one-hot encoding nasıl sağlanır?
31. Bir pandas fonksiyonunun girdiyi değiştirmediğini nasıl test edersin?
32. Şema doğrulamasında hangi kontroller bulunmalıdır?
33. İşlemi olmayan müşterileri müşteri raporunda nasıl korursun?
34. Veri sızıntısına yol açabilecek beş pandas işlemi say.
35. Tarih-saat verisini neden UTC olarak saklamayı tercih edersin?

## Performans ve tasarım soruları

36. `iterrows()` neden çoğu zaman önerilmez?
37. `itertuples()` hangi durumda kabul edilebilir?
38. `apply(axis=1)` yerine hangi yaklaşımları denersin?
39. Düşük kardinaliteli string kolonu optimize etmek için ne yaparsın?
40. Büyük CSV okurken bellek kullanımını nasıl azaltırsın?
41. `usecols`, `dtype` ve `chunksize` parametreleri ne sağlar?
42. Gereksiz kopyaları azaltırken yan etkileri nasıl kontrol edersin?
43. Notebook kodunu üretim paketine dönüştürürken hangi katmanları ayırırsın?
44. pandas pipeline'ında idempotency ne demektir?
45. Çıktı satır sırasının deterministik olması neden önemlidir?

## Senaryo soruları

46. Bir merge işlemi satır sayısını 10 kat artırdı. Nasıl teşhis edersin?
47. Eğitimde olmayan şehirler production verisinde görünmeye başladı. Pipeline'ı nasıl tasarlarsın?
48. Aynı işlem kimliği farklı zaman ve fiyatlarla iki kez geliyor. Hangi iş kurallarını sorarsın?
49. Grup toplamları beklenenden düşük. Eksik grup anahtarlarıyla ilişkili olabilecek hatayı açıkla.
50. Model doğrulama skoru notebook'ta yüksek, production'da düşük. pandas preprocessing kaynaklı leakage olasılığını nasıl araştırırsın?
51. Bir kolon `object` görünüyor ancak sayısal değerler içeriyor. Güvenli dönüşüm yaklaşımın nedir?
52. Müşteri boyut tablosunda duplicate anahtar var. Sessizce ilk kaydı tutmak yerine ne yaparsın?
53. Tarih kolonunda farklı timezone'lar bulunuyor. Normalizasyon stratejin nedir?
54. DataFrame belleği beklenenden çok yüksek. Hangi kolonları ve metrikleri incelersin?
55. Pipeline sonucu her çalıştırmada farklı satır sırası üretiyor. Olası nedenleri ve çözümü açıkla.