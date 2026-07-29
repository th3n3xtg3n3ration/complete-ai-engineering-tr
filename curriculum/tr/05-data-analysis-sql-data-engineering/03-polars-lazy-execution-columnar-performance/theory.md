# Teori — Polars, Lazy Execution ve Kolon Tabanlı Performans

## 1. Polars neden farklıdır?

Polars, analitik tablo işlemleri için tasarlanmış kolon tabanlı bir sorgu motorudur. Python API'si olsa da kritik yürütme katmanı Rust ile geliştirilmiştir. Veri işlemleri güçlü bir expression API üzerinden tanımlanır; motor bu ifadeleri paralel, vektörleştirilmiş ve mümkün olduğunda optimize edilmiş biçimde çalıştırır.

Satır odaklı düşüncede bir kaydı alır, alanlarını işler ve sonraki kayda geçersin. Kolon odaklı analitikte ise aynı tipteki değerler bitişik tutulur. Bu düzen aggregation, filtreleme, encoding ve sayısal dönüşümlerde CPU cache kullanımını ve SIMD fırsatlarını iyileştirebilir.

Kolon tabanlı olmak her iş yükünde otomatik olarak daha hızlı olmak anlamına gelmez. Küçük veri, yüksek Python entegrasyonu gerektiren özel nesneler veya tek satırlık operasyonel güncellemeler farklı araçlara daha uygun olabilir. Mühendislik kararı benchmark ve sistem sınırlarıyla verilmelidir.

## 2. DataFrame ve LazyFrame

### Eager DataFrame

Eager modelde her çağrı hemen yürütülür:

```python
result = (
    frame.filter(pl.col("status") == "paid")
    .with_columns((pl.col("quantity") * pl.col("unit_price")).alias("revenue"))
    .group_by("customer_id")
    .agg(pl.col("revenue").sum())
)
```

Bu model etkileşimli analiz ve küçük veri için anlaşılırdır. Ancak her ara adım ayrı ayrı materialize olabilir ve motor tüm işlem zincirini baştan optimize edemez.

### LazyFrame

Lazy modelde çağrılar bir sorgu planı oluşturur; veri `collect`, `sink_*` veya benzeri terminal işlem gelene kadar materialize edilmez:

```python
query = (
    pl.scan_parquet("orders.parquet")
    .filter(pl.col("status") == "paid")
    .with_columns((pl.col("quantity") * pl.col("unit_price")).alias("revenue"))
    .group_by("customer_id")
    .agg(pl.col("revenue").sum())
)
result = query.collect()
```

Motor tüm grafiği gördüğü için filtreleri kaynağa yaklaştırabilir, kullanılmayan kolonları okumayabilir ve ortak alt ifadeleri azaltabilir.

## 3. Expression API

Polars'ta `pl.col`, `pl.lit`, `when/then/otherwise` ve namespace metodları birer ifade üretir. İfadeler satır satır Python fonksiyonu değildir; motorun optimize edebildiği deklaratif hesaplama düğümleridir.

```python
clean = frame.with_columns(
    pl.col("email").str.strip_chars().str.to_lowercase(),
    pl.col("amount").cast(pl.Float64, strict=False),
    pl.when(pl.col("amount") >= 1_000)
    .then(pl.lit("high"))
    .otherwise(pl.lit("standard"))
    .alias("value_band"),
)
```

Native expression varken `map_elements` veya Python lambda kullanmak genellikle kaçınılması gereken bir yoldur. Python UDF motorun tip bilgisi, paralellik ve query optimization avantajlarını kısıtlayabilir.

## 4. Kolon seçimi ve projection pushdown

Bir veri kaynağında yüzlerce kolon bulunabilir; fakat sorgu yalnızca beş kolona ihtiyaç duyabilir. Lazy motor gerekli kolonları bilir ve desteklenen kaynağa yalnızca bu kolonları okutabilir. Buna projection pushdown denir.

```python
query = (
    pl.scan_parquet("events.parquet")
    .select("user_id", "event_at", "event_type", "amount")
)
```

Erken `select`, hem niyeti görünür kılar hem de bellek ve I/O maliyetini azaltabilir. `select(pl.all())` gibi gereksiz geniş seçimler bu avantajı zayıflatır.

## 5. Filtre ve predicate pushdown

Filtre mümkün olduğunca veri kaynağına yakın çalıştırılırsa gereksiz satırlar sonraki düğümlere taşınmaz:

```python
query = (
    pl.scan_parquet("orders.parquet")
    .filter(
        (pl.col("order_at") >= pl.date(2026, 1, 1))
        & (pl.col("status") == "paid")
    )
)
```

Parquet gibi istatistik ve row-group bilgisi taşıyan formatlarda bazı veri blokları hiç okunmadan atlanabilir. CSV'de de filtre aşağı itilebilir; ancak metin dosyasının ayrıştırma özellikleri farklı olduğundan kazanç aynı seviyede olmayabilir.

## 6. `scan_*` ve `read_*` farkı

- `read_csv` ve `read_parquet` eager `DataFrame` üretir.
- `scan_csv` ve `scan_parquet` lazy `LazyFrame` üretir.

Büyük veya çok adımlı pipeline'larda önce `scan_*`, sonra expression zinciri, en sonunda `collect` veya `sink_*` tercih edilir. `scan_csv` çağrısı tek başına dosyayı tam olarak materialize etmez; sorgunun yürütülmesi terminal operasyonda başlar.

## 7. Query plan okuma

`LazyFrame.explain(optimized=True)` optimize edilmiş planı gösterir. Plan incelenirken şu sorular sorulur:

1. Filtre kaynağa yakın mı?
2. Yalnızca gereken kolonlar mı taranıyor?
3. Join öncesinde veri küçültülebiliyor mu?
4. Aynı dönüşüm birden fazla kez mi hesaplanıyor?
5. Global sort gerçekten gerekli mi?
6. Python UDF planı opak hâle getiriyor mu?

Plan metni sürümler arasında değişebilir; otomatik testlerde belirli satır biçimine bağımlı kalmak yerine planın üretilebildiğini ve davranışın doğru olduğunu test etmek daha güvenlidir.

## 8. GroupBy ve aggregation

Polars'ta aggregation expression tabanlıdır:

```python
summary = (
    orders.group_by("customer_id")
    .agg(
        pl.len().alias("row_count"),
        pl.col("order_id").n_unique().alias("order_count"),
        pl.col("revenue").sum().alias("total_revenue"),
        pl.col("revenue").mean().alias("average_order_value"),
    )
)
```

`maintain_order=True` grup sırasını korur; fakat ek maliyet oluşturabilir ve bazı streaming fırsatlarını engelleyebilir. Sıra yalnızca iş gereksinimiyse korunmalıdır. Rapor deterministik olacaksa sonucu açıkça `sort` etmek çoğu zaman daha anlaşılırdır.

## 9. Join ve kardinalite

Join sonucu yalnızca anahtar eşleşmesine değil, anahtarların tekillik yapısına bağlıdır:

- `1:1`: iki tarafta da anahtar tekil.
- `1:m`: sol tekil, sağ çoklu.
- `m:1`: sol çoklu, sağ tekil.
- `m:m`: iki taraf da çoklu.

Beklenen kardinalite doğrulanmazsa satır patlaması oluşabilir. Örneğin 1.000 sipariş, duplicate müşteri boyut tablosuyla join edildiğinde gelir yanlışlıkla iki veya üç kez sayılabilir. `validate="m:1"` gibi kontroller veri sözleşmesinin çalıştırılabilir parçasıdır.

## 10. Streaming engine

Streaming engine sorguyu daha küçük batch'ler hâlinde işleyerek bellek baskısını azaltabilir:

```python
result = query.collect(engine="streaming")
```

Her operatör aynı düzeyde streaming uyumlu değildir. Global sıralama, bazı join türleri veya tüm veriyi aynı anda gerektiren algoritmalar sınır oluşturabilir. `explain` ve ölçüm sonuçları birlikte değerlendirilmelidir.

Streaming yalnızca hız tekniği değildir; çoğu zaman temel amaç peak memory kullanımını kontrol etmektir. Daha düşük bellek, biraz daha uzun çalışma süresi karşılığında üretim sistemini kararlı hâle getirebilir.

## 11. Eager ve lazy karşılaştırması

Karşılaştırma adil olmalıdır:

- Aynı veri ve aynı iş mantığı kullanılmalı.
- İlk çalıştırmanın cache ve initialization etkisi ayrı değerlendirilmelidir.
- Birden fazla tekrar ve medyan süre raporlanmalıdır.
- Sonuç tablolarının eşitliği doğrulanmalıdır.
- Yalnızca süre değil, peak memory ve okunan veri miktarı da ölçülmelidir.
- Küçük sentetik benchmark sonucu büyük üretim verisine doğrudan genellenmemelidir.

100.000 satırda eager daha hızlı çıkabilir; 100 milyon satırda lazy ve streaming yaklaşımı belirgin biçimde daha sürdürülebilir olabilir.

## 12. Polars ve pandas zihinsel model farkları

Polars'a geçerken yalnızca sözdizimini çevirmek yeterli değildir:

- Polars'ta anlamlı bir satır index'i varsayılan veri modeli değildir.
- Expression API, satır bazlı `apply` yerine temel çalışma modelidir.
- Lazy execution birinci sınıf özelliktir.
- Dtype ve şema daha merkezi bir tasarım unsurudur.
- API çoğunlukla immutable dönüşüm zincirlerini teşvik eder.
- Sıra korunması gerektiğinde açıkça belirtilmelidir.

pandas bilgisi değerlidir; fakat Polars kodunu pandas kalıplarını birebir taklit ederek yazmak performans ve okunabilirlik avantajlarını azaltabilir.

## 13. Veri kalitesi ve şema

Hızlı çalışan yanlış bir pipeline üretim için başarısızdır. Her kaynakta en az şu kontroller bulunmalıdır:

- Zorunlu kolonlar mevcut mu?
- Kolon adları normalize edildiğinde çakışma oluşuyor mu?
- Kimlik kolonları null mı?
- Sayısal cast başarısızlıkları null üretiyor mu?
- Tarih ayrıştırma hataları var mı?
- Negatif miktar veya fiyat gibi iş kuralı ihlalleri bulunuyor mu?
- Join anahtarları beklenen kardinaliteye sahip mi?
- Deduplication kuralı deterministik mi?

## 14. Örnek üretim pipeline'ı

Bir e-ticaret pipeline'ı aşağıdaki katmanlara ayrılabilir:

1. **Scan:** Ham CSV/Parquet dosyalarını lazy tara.
2. **Contract:** Kolon ve dtype gereksinimlerini doğrula.
3. **Clean:** Tarih, sayısal alan, kategori ve kimlikleri normalize et.
4. **Filter:** Geçersiz kayıtları karantina veya hata tablosuna ayır.
5. **Enrich:** `quantity × unit_price` ile gelir üret.
6. **Join:** Müşteri boyut tablosunu `m:1` doğrulamasıyla ekle.
7. **Aggregate:** Müşteri bazlı sipariş, gelir ve güncellik özellikleri üret.
8. **Sink:** Sonucu Parquet olarak yayımla.
9. **Observe:** Satır sayıları, null oranları, plan ve süre metriklerini kaydet.

Örneğin bir müşterinin toplam alışverişi `12.500 ₺` ise bu rakamın duplicate join nedeniyle iki katına çıkmadığı veri sözleşmesi ve testlerle güvence altına alınmalıdır.

## 15. Sık yapılan hatalar

- Büyük CSV'yi `read_csv` ile tamamen okuyup sonra filtrelemek.
- Her dönüşümde `collect` çağırmak.
- Native expression yerine Python lambda kullanmak.
- Global sıralamayı gereksiz yere erken yapmak.
- Join kardinalitesini doğrulamamak.
- Sıra garantisini varsaymak.
- Çok geniş tabloyu gereksiz kolonlarla taşımak.
- Benchmark'ta sonuç eşitliğini kontrol etmemek.
- Lazy planı görmeden yalnızca API zincirine bakmak.

## 16. Resmî kaynaklar

- Polars Python API: https://docs.pola.rs/api/python/stable/reference/
- Lazy API ve yürütme: https://docs.pola.rs/user-guide/lazy/
- CSV okuma ve scanning: https://docs.pola.rs/user-guide/io/csv/
- pandas'tan Polars'a geçiş: https://docs.pola.rs/user-guide/migration/pandas/
