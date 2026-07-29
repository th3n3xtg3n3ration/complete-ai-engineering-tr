# Teori — pandas Series, DataFrame, İndeksleme ve GroupBy

## 1. pandas neden gereklidir?

NumPy homojen ve çok boyutlu sayısal diziler için güçlüdür. Gerçek veri ürünleri ise çoğu zaman farklı tiplerde kolonlar, isimlendirilmiş satırlar, eksik değerler, tarih-saat alanları ve ilişkisel tablolar içerir. pandas bu ihtiyaçları `Series`, `DataFrame` ve `Index` soyutlamalarıyla karşılar.

Bir `DataFrame` yalnızca iki boyutlu bir tablo değildir. Kolonların kendi veri tipleri vardır, satırlar bir index ile adreslenir ve birçok işlem index etiketlerine göre hizalanır. Bu hizalama davranışı hem güçlü hem de hata üretmeye açıktır.

## 2. Series, DataFrame ve Index

`Series`, değer dizisi ile index etiketlerinin birleşimidir. `DataFrame`, aynı satır index'ini paylaşan kolonlardan oluşur.

```python
import pandas as pd

prices = pd.Series([10.0, 20.0], index=["p1", "p2"], name="price")
frame = pd.DataFrame({"price": prices, "stock": [4, 7]})
```

pandas işlemleri çoğu zaman konuma göre değil etikete göre hizalar:

```python
left = pd.Series([1, 2], index=["a", "b"])
right = pd.Series([10, 20], index=["b", "c"])
result = left + right
```

Sonuçta ortak olmayan etiketler `NaN` üretir. Bu davranış rastgele değildir; pandas veri kimliğini korumaya çalışır. Beklenmeyen `NaN` görüldüğünde ilk kontrol index hizalaması olmalıdır.

## 3. Veri tipleri ve nullable dtype'lar

Klasik NumPy tamsayı tipi eksik değer taşıyamaz. pandas, `Int64`, `Float64`, `boolean` ve `string` gibi nullable dtype'lar sunar.

```python
frame = pd.DataFrame(
    {
        "customer_id": pd.Series([1, None, 3], dtype="Int64"),
        "active": pd.Series([True, None, False], dtype="boolean"),
        "city": pd.Series(["Ankara", None, "İzmir"], dtype="string"),
    }
)
```

`object` tipi çok esnektir fakat bellek ve doğrulama açısından zayıftır. Üretim pipeline'larında mümkün olduğunca açık dtype seçilmelidir.

## 4. Kolon ve satır seçimi

### 4.1 Etiket tabanlı seçim: `loc`

```python
subset = frame.loc[frame["revenue"] >= 100, ["customer_id", "revenue"]]
```

`loc` satır ve kolon etiketleriyle çalışır. Dilimlerin son sınırı dahildir.

### 4.2 Konum tabanlı seçim: `iloc`

```python
first_rows = frame.iloc[:5, :3]
```

`iloc` Python dilimleme kurallarına göre konum kullanır ve son sınırı dahil etmez.

### 4.3 Boolean mask

Mask index'i ile DataFrame index'i uyumlu olmalıdır. Farklı index taşıyan maskeler yanlış hizalama veya hata üretebilir.

```python
mask = frame["status"].eq("active") & frame["score"].ge(0.8)
selected = frame.loc[mask].copy()
```

`copy()` kullanımı, alt kümenin bağımsız bir çalışma nesnesi olduğunu açık hale getirir.

## 5. Chained assignment ve mutasyon riski

Aşağıdaki desen güvenilir değildir:

```python
frame[frame["score"] < 0]["score"] = 0
```

İlk seçim view veya copy döndürebilir. Bu nedenle atama tek bir `loc` ifadesiyle yapılmalıdır:

```python
frame.loc[frame["score"] < 0, "score"] = 0
```

Daha güvenli bir üretim yaklaşımı, fonksiyonların girdiyi değiştirmemesi ve yeni bir DataFrame döndürmesidir.

## 6. Eksik değer semantiği

`NaN`, `None` ve `pd.NA` aynı değildir ancak çoğu pandas fonksiyonu bunları eksik değer olarak ele alabilir.

Temel işlemler:

- `isna()` ve `notna()`
- `fillna()`
- `dropna()`
- `interpolate()`

İmputation istatistikleri tüm veri üzerinde hesaplanmamalıdır. Median, ortalama veya kategori sözlüğü yalnızca eğitim verisinde öğrenilmeli; doğrulama ve test verisine değiştirilmeden uygulanmalıdır.

## 7. Duplicate kayıtlar

`duplicated()` tam satır veya anahtar bazında duplicate tespiti yapar.

```python
mask = frame.duplicated(subset="transaction_id", keep=False)
```

Duplicate çözümleme bir iş kuralıdır. “İlkini tut” veya “sonuncuyu tut” kararı zaman damgası, kaynak önceliği ya da sürüm alanıyla desteklenmelidir. Sessiz `drop_duplicates()` veri kaybı yaratabilir.

## 8. GroupBy: split–apply–combine

`groupby` üç aşamalı bir modeldir:

1. Veriyi anahtarlara göre böl.
2. Her gruba fonksiyon uygula.
3. Sonuçları birleştir.

```python
summary = (
    frame.groupby("segment", dropna=False, observed=True)
    .agg(
        customer_count=("customer_id", "nunique"),
        total_revenue=("revenue", "sum"),
        average_revenue=("revenue", "mean"),
    )
    .reset_index()
)
```

`dropna=False`, eksik grup anahtarlarını raporda korur. `observed=True`, kategorik kolonlarda gözlenmeyen kategori kombinasyonlarını üretmez.

## 9. `agg`, `transform`, `filter` ve `apply`

### `agg`

Her grup için daha küçük bir özet üretir.

### `transform`

Girdi ile aynı satır sayısını korur. Grup ortalamasından sapma veya grup içi oran için uygundur.

```python
frame["segment_mean"] = frame.groupby("segment")["revenue"].transform("mean")
frame["relative_revenue"] = frame["revenue"] / frame["segment_mean"]
```

### `filter`

Grup düzeyindeki koşula göre tam grupları tutar veya eler.

### `apply`

Esnektir ancak çoğu durumda daha yavaş ve daha az tahmin edilebilirdir. Önce `agg`, `transform` veya vektörleştirilmiş yöntem aranmalıdır.

## 10. Çok seviyeli index

Birden fazla grup kolonu kullanıldığında MultiIndex oluşabilir. Üretim çıktılarında `reset_index()` ile düz kolon yapısına dönmek genellikle veri paylaşımını ve SQL aktarımını kolaylaştırır.

## 11. Merge, join ve concat

### `merge`

İlişkisel JOIN karşılığıdır.

```python
result = orders.merge(
    customers,
    on="customer_id",
    how="left",
    validate="many_to_one",
)
```

`validate` kritik bir güvenlik katmanıdır:

- `one_to_one`
- `one_to_many`
- `many_to_one`
- `many_to_many`

Beklenen kardinalite bozulduğunda pipeline sessiz satır çoğaltmak yerine hata vermelidir.

### `concat`

Aynı şemaya sahip parçaları satır veya kolon ekseninde birleştirir. `ignore_index=True` yeni sıralı index üretir. Kolon şemaları farklıysa eksik alanlar oluşabilir; bu nedenle concat öncesi şema doğrulanmalıdır.

## 12. Tarih-saat verisi

Tarih alanları string bırakılmamalıdır.

```python
frame["timestamp"] = pd.to_datetime(frame["timestamp"], errors="raise", utc=True)
```

UTC kullanımı sistemler arası veri taşımada daha güvenlidir. Yerel saat yalnızca sunum katmanında uygulanmalıdır. Geçersiz tarihleri sessizce `NaT` yapmak yerine saymak ve raporlamak gerekir.

## 13. Kategorik veri

Tekrarlanan metin kolonları `category` dtype ile daha az bellek kullanabilir. Ancak kategori sözlüğü eğitim verisinde sabitlenmeli ve yeni kategoriler açık bir `__unknown__` seviyesine yönlendirilmelidir.

## 14. Bellek ve performans

`memory_usage(deep=True)` gerçekçi bellek tahmini verir. Performans için:

- Python satır döngülerinden kaçın.
- `iterrows()` yerine vektörleştirme veya uygun GroupBy kullan.
- Gereksiz `copy()` zincirlerinden kaçın; fakat mutasyon sınırlarını açık tut.
- String kolonlarda uygun olduğunda `string` veya `category` kullan.
- Büyük dosyalarda `usecols`, `dtype` ve parça okuma seçeneklerini değerlendir.

## 15. Veri sızıntısı

Aşağıdaki işlemler tüm veri üzerinde yapılırsa leakage oluşturabilir:

- Median ve ortalama hesaplama
- Kategori frekansı
- Outlier sınırı
- Target encoding
- Feature selection

Doğru tasarım:

1. Eğitim verisinde `fit`.
2. Öğrenilen istatistikleri sakla.
3. Eğitim, doğrulama ve test verisine aynı `transform` uygula.
4. Şema ve bilinmeyen kategori davranışını test et.

## 16. Üretim kontrol listesi

Bir pandas pipeline'ı şu sorulara yanıt vermelidir:

- Gerekli kolonlar var mı?
- Kolon tipleri beklenen biçimde mi?
- Anahtarlar benzersiz mi?
- Merge kardinalitesi doğrulandı mı?
- Eksik ve duplicate kayıt politikası açık mı?
- Tarihler UTC ve geçerli mi?
- Fit/transform ayrımı korunuyor mu?
- Girdi mutasyona uğruyor mu?
- Çıktı sırası deterministik mi?
- Kalite metrikleri ve testler mevcut mu?

Bu ilkeler pandas kodunu yalnızca çalışan bir notebook hücresi olmaktan çıkarıp güvenilir bir veri ürünü bileşenine dönüştürür.