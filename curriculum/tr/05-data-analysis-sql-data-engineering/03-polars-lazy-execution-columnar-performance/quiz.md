# Quiz

Her soru için en doğru seçeneği işaretle.

1. LazyFrame ne zaman materialize edilir?  
   A) `scan_csv` çağrısında · B) Her expression'da · C) `collect` veya sink çağrısında · D) Import sırasında

2. Projection pushdown'ın temel amacı nedir?  
   A) Daha çok satır okumak · B) Yalnız gereken kolonları kaynaktan okumak · C) Sıralama yapmak · D) Null doldurmak

3. Predicate pushdown nedir?  
   A) Filtreyi kaynağa yaklaştırmak · B) Join'i kaldırmak · C) Dtype değiştirmek · D) Index üretmek

4. Native expression yerine Python UDF kullanmanın olası sonucu nedir?  
   A) Her zaman daha hızlıdır · B) Optimizasyon ve paralellik fırsatlarını azaltabilir · C) Şemayı zorunlu kılar · D) Veriyi otomatik sıkıştırır

5. `scan_parquet` hangi tür nesne üretir?  
   A) Series · B) DataFrame · C) LazyFrame · D) Python list

6. `validate="m:1"` neyi güvence altına alır?  
   A) Sol anahtar tekildir · B) Sağ anahtar tekildir · C) İki taraf çokludur · D) Null yoktur

7. `maintain_order=True` için doğru ifade hangisidir?  
   A) Daima ücretsizdir · B) Sıra garantisi verir fakat maliyet ve streaming kısıtı oluşturabilir · C) Dtype değiştirir · D) Join'i hızlandırır

8. Streaming engine'in ana faydası nedir?  
   A) Her sorguyu GPU'da çalıştırır · B) Veriyi batch'lerle işleyerek bellek baskısını azaltabilir · C) SQL üretir · D) Duplicate siler

9. Query planı hangi metotla incelenir?  
   A) `describe` · B) `show` · C) `explain` · D) `inspect_schema`

10. Polars'ta anlamlı satır index'i için doğru ifade hangisidir?  
    A) pandas gibi her zaman zorunludur · B) Temel veri modelinin merkezinde değildir · C) Yalnız string olabilir · D) Her join sonrası oluşur

11. Aşağıdakilerden hangisi eager okuma yapar?  
    A) `scan_csv` · B) `scan_parquet` · C) `read_csv` · D) `LazyFrame`

12. Büyük tabloda join öncesi en iyi iyileştirmelerden biri hangisidir?  
    A) Gereksiz kolon ve satırları azaltmak · B) Her şeyi string yapmak · C) Python loop eklemek · D) Global sort yapmak

13. `strict=False` cast başarısız değerlerde genellikle ne üretir?  
    A) Null · B) Sıfır · C) Sonsuz · D) Duplicate

14. Deterministik top-N için ne gerekir?  
    A) Yalnız değer kolonuna sort · B) Eşitlik durumunda açık tie-breaker · C) Random seed gereksizdir · D) `collect` kaldırılmalıdır

15. Benchmark'ta sonuç eşitliği neden doğrulanır?  
    A) Hızlı ama farklı iş mantığını karşılaştırmayı önlemek için · B) Dosyayı küçültmek için · C) Dtype'ı kaldırmak için · D) GPU seçmek için

16. Parquet'in CSV'ye göre lazy analizde olası avantajı nedir?  
    A) Şema ve kolon/row-group bilgisiyle daha seçici okuma · B) Metin olması · C) Index zorunluluğu · D) Python nesnesi saklaması

17. `sink_parquet` ne sağlar?  
    A) Query sonucunu doğrudan dosyaya yazma · B) DataFrame'i listeye dönüştürme · C) Join cardinality · D) UDF hızlandırma

18. Aşağıdakilerden hangisi veri kalitesi kontrolüdür?  
    A) Join anahtarı tekilliğini doğrulamak · B) Her kolon için global sort · C) Her adımda collect · D) Tüm dtype'ları Object yapmak

19. Lazy pipeline'da `collect` nerede bulunmalıdır?  
    A) Her satırda · B) Mümkün olduğunca terminal aşamada · C) Import sırasında · D) Her `with_columns` sonrasında

20. Polars performans kararı nasıl verilmelidir?  
    A) Yalnız pazarlama iddiasıyla · B) Temsili veri ve doğrulanmış benchmark ile · C) Yalnız satır sayısıyla · D) Her zaman lazy seçerek

## Cevap anahtarı

1-C, 2-B, 3-A, 4-B, 5-C, 6-B, 7-B, 8-B, 9-C, 10-B, 11-C, 12-A, 13-A, 14-B, 15-A, 16-A, 17-A, 18-A, 19-B, 20-B
