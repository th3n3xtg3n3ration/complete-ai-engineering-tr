# Quiz — pandas Series, DataFrame, İndeksleme ve GroupBy

Her soru için en doğru seçeneği işaretle.

## Sorular

1. pandas Series işlemlerinde değerler varsayılan olarak neye göre hizalanır?
   - A) Bellek adresine
   - B) Index etiketine
   - C) Veri tipine
   - D) Kolon sırasına

2. `loc` ile `iloc` arasındaki temel fark nedir?
   - A) `loc` yalnızca kolon seçer
   - B) `iloc` yalnızca boolean mask kabul eder
   - C) `loc` etiket, `iloc` konum kullanır
   - D) Aralarında fark yoktur

3. Güvenli koşullu atama için hangi desen tercih edilir?
   - A) `df[df.x < 0]["x"] = 0`
   - B) `df.loc[df.x < 0, "x"] = 0`
   - C) `df.iloc[df.x < 0] = 0`
   - D) `df.query("x < 0")["x"] = 0`

4. Eksik değer taşıyan tamsayı kolonunda uygun pandas dtype hangisidir?
   - A) `int64`
   - B) `Int64`
   - C) `object64`
   - D) `number`

5. `groupby(...).agg(...)` tipik olarak ne üretir?
   - A) Girdiyle aynı satır sayısını zorunlu olarak korur
   - B) Grup başına özet sonuç üretir
   - C) Yalnızca metin kolonlarında çalışır
   - D) Index'i siler

6. `groupby(...).transform(...)` için hangisi doğrudur?
   - A) Sonuç girdiyle hizalanabilir
   - B) Yalnızca tek satır üretir
   - C) Merge ile aynıdır
   - D) Grupları siler

7. Eksik grup anahtarlarını GroupBy çıktısında korumak için ne kullanılır?
   - A) `dropna=True`
   - B) `dropna=False`
   - C) `ignore_na=True`
   - D) `keep_null=True`

8. Kategorik kolonlarda yalnızca gözlenen grupları üretmek için hangi seçenek kullanılır?
   - A) `observed=True`
   - B) `visible=True`
   - C) `compact=True`
   - D) `dense=False`

9. Bir müşteri tablosunda `customer_id` tekil, işlem tablosunda çokluysa beklenen merge kardinalitesi nedir?
   - A) `one_to_one`
   - B) `one_to_many`
   - C) `many_to_many`
   - D) `cross`

10. `merge(validate=...)` neden önemlidir?
    - A) Kolonları otomatik küçültür
    - B) Beklenmeyen satır çoğalmasını yakalar
    - C) Tüm eksik değerleri doldurur
    - D) Tarihleri UTC yapar

11. `concat` hangi senaryoda en doğal seçimdir?
    - A) Ortak anahtarla müşteri ve işlem tablosunu birleştirme
    - B) Aynı şemalı aylık dosyaları alt alta ekleme
    - C) Grup ortalaması hesaplama
    - D) Kategori kodlama

12. `category` dtype'ın temel avantajlarından biri nedir?
    - A) Her string'i benzersiz hale getirir
    - B) Tekrarlanan düşük kardinaliteli metinlerde bellek azaltabilir
    - C) Eksik değerleri yasaklar
    - D) Merge'i engeller

13. Veri sızıntısını önlemek için median hangi veri üzerinde öğrenilmelidir?
    - A) Eğitim, doğrulama ve test birleşiminde
    - B) Yalnızca test verisinde
    - C) Yalnızca eğitim verisinde
    - D) Her satır için ayrı

14. Yeni kategoriler için güvenli transform davranışı hangisidir?
    - A) Kategori sözlüğünü test verisiyle genişletmek
    - B) Satırı silmek
    - C) Açık bir bilinmeyen kategoriye yönlendirmek
    - D) Rastgele mevcut kategori atamak

15. `pd.to_datetime(..., errors="coerce")` geçersiz değerlerde ne üretir?
    - A) Sıfır
    - B) Boş string
    - C) `NaT`
    - D) `False`

16. Duplicate işlem kaydında hangi kaydın tutulacağı neye dayanmalıdır?
    - A) Rastgele seçime
    - B) Açık iş kuralına ve sıralama alanına
    - C) DataFrame'in bellek adresine
    - D) Kolon sayısına

17. `memory_usage(deep=True)` neden kullanılır?
    - A) Yalnızca index'i silmek için
    - B) Nesne/string içeriğini de hesaba katan bellek tahmini için
    - C) CPU süresini ölçmek için
    - D) Merge planı oluşturmak için

18. `apply(axis=1)` için en doğru ifade hangisidir?
    - A) Her zaman vektörleştirmeden hızlıdır
    - B) Satır bazlı Python çağrıları nedeniyle pahalı olabilir
    - C) Sadece GroupBy sonrasında çalışır
    - D) DataFrame'i otomatik test eder

19. Bir fonksiyonun girdi DataFrame'i değiştirmemesi neden yararlıdır?
    - A) Yan etkileri azaltır ve test edilebilirliği artırır
    - B) Her zaman daha az bellek kullanır
    - C) Index ihtiyacını kaldırır
    - D) Eksik veriyi otomatik düzeltir

20. Üretim pandas pipeline'ında en güçlü güvenlik kombinasyonu hangisidir?
    - A) Sessiz type conversion ve `many_to_many` merge
    - B) Şema doğrulama, kardinalite kontrolü, fit/transform ayrımı ve testler
    - C) Tüm kolonları `object` yapmak
    - D) Her adımda `apply(axis=1)` kullanmak

## Cevap anahtarı

1. B
2. C
3. B
4. B
5. B
6. A
7. B
8. A
9. B
10. B
11. B
12. B
13. C
14. C
15. C
16. B
17. B
18. B
19. A
20. B

## Değerlendirme

- 18–20: Konuya hâkimsin.
- 15–17: İyi düzey; merge kardinalitesi ve leakage bölümlerini tekrar et.
- 11–14: Laboratuvarı yeniden uygula.
- 0–10: Series, index alignment, seçim ve GroupBy temellerinden tekrar başla.