# Laboratuvar — pandas ile Güvenilir Tablo Analitiği

## Amaç

Bu laboratuvarda işlem ve müşteri tablolarını kullanarak veri kalitesi kontrollü, sızıntısız ve test edilebilir bir pandas pipeline'ı geliştireceksin.

## Ön koşullar

```bash
python -m pip install pandas pytest
```

## Veri senaryosu

İki tablo kullanacağız:

- `transactions`: işlem kimliği, müşteri kimliği, zaman damgası, adet ve birim fiyat
- `customers`: müşteri kimliği, şehir, segment ve yaş

Ham veride duplicate işlem, eksik yaş, bilinmeyen şehir ve metin biçiminde tarih alanları bulunacaktır.

## 1. DataFrame oluşturma ve profil çıkarma

```python
import pandas as pd

from src.pandas_foundations import profile_frame

transactions = pd.DataFrame(
    {
        "transaction_id": [1, 2, 2, 3],
        "customer_id": [10, 10, 10, 20],
        "timestamp": [
            "2026-01-01T10:00:00Z",
            "2026-01-02T11:00:00Z",
            "2026-01-02T11:05:00Z",
            "2026-01-03T09:00:00Z",
        ],
        "quantity": [1, 2, 3, 1],
        "unit_price": [10.0, 5.0, 5.0, 7.5],
    }
)

print(profile_frame(transactions))
```

Kontrol et:

- Satır ve kolon sayısı
- Duplicate satır sayısı
- Eksik hücre sayısı
- Bellek kullanımı

## 2. Kolon isimlerini standardize etme

```python
from src.pandas_foundations import normalize_frame_columns

raw = pd.DataFrame({"Customer ID": [1], "Order-Value": [20.0]})
clean = normalize_frame_columns(raw)
print(clean.columns.tolist())
```

Normalizasyon sonrası iki kolon aynı isme dönüşüyorsa fonksiyon hata vermelidir.

## 3. Güvenli satır seçimi

```python
from src.pandas_foundations import filter_rows

selected = filter_rows(
    transactions,
    equals={"customer_id": 10},
    minimums={"quantity": 2},
)
```

Aşağıdakileri doğrula:

- Girdi DataFrame değişmedi.
- Çıktı bağımsız bir kopyadır.
- Mask index'i kaynak tabloyla uyumludur.

## 4. İşlem hazırlama

```python
from src.customer_analytics import prepare_transactions

prepared = prepare_transactions(transactions)
print(prepared)
```

Bu adım:

1. Gerekli kolonları doğrular.
2. `transaction_id` duplicate kayıtlarında son kaydı tutar.
3. Tarihi UTC datetime'a dönüştürür.
4. `quantity * unit_price` ile `revenue` üretir.
5. Negatif değerleri reddeder.
6. Çıktıyı zaman damgasına göre deterministik sıralar.

## 5. GroupBy metrikleri

```python
from src.customer_analytics import customer_metrics

metrics = customer_metrics(prepared)
print(metrics)
```

Her müşteri için:

- Benzersiz sipariş sayısı
- Toplam gelir
- Ortalama sipariş değeri
- İlk işlem zamanı
- Son işlem zamanı

hesaplanır.

Ayrıca `transform` ile müşteri toplamındaki işlem payını üret:

```python
prepared["customer_total"] = prepared.groupby("customer_id")["revenue"].transform("sum")
prepared["revenue_share"] = prepared["revenue"] / prepared["customer_total"]
```

Her müşterinin `revenue_share` toplamının yaklaşık 1 olduğunu doğrula.

## 6. Kardinalitesi doğrulanmış merge

```python
from src.customer_analytics import build_customer_report

customers = pd.DataFrame(
    {
        "customer_id": [10, 20, 30],
        "city": ["Ankara", "İzmir", "Bursa"],
        "segment": ["A", "B", "C"],
        "age": [30, None, 45],
    }
)

report = build_customer_report(transactions, customers)
print(report)
```

`validate="one_to_one"` müşteri boyut tablosundaki duplicate anahtarları yakalar. Müşteri 30'un işlemi olmadığı için gelir metrikleri sıfır olmalıdır.

## 7. Eğitim ve test ayrımı

```python
from src.dataframe_pipeline import TabularPreprocessor

train = customers.iloc[:2].copy()
test = pd.DataFrame(
    {
        "customer_id": [40],
        "city": ["Eskişehir"],
        "segment": ["D"],
        "age": [None],
    }
)

preprocessor = TabularPreprocessor(
    numeric_columns=("age",),
    categorical_columns=("city", "segment"),
)
preprocessor.fit(train)

train_transformed = preprocessor.transform(train)
test_transformed = preprocessor.transform(test)
```

Beklenen davranış:

- Eksik yaş yalnızca eğitim median'ı ile doldurulur.
- Testteki yeni şehir ve segment `__unknown__` olur.
- Test verisi kategori sözlüğünü değiştirmez.

## 8. One-hot encoding

```python
from src.dataframe_pipeline import one_hot_encode

encoded = one_hot_encode(
    test_transformed,
    columns=["city", "segment"],
)
print(encoded)
```

Kolon sırasının kategori sözlüğü nedeniyle deterministik olduğunu doğrula.

## 9. Top-N analizi

```python
from src.pandas_foundations import top_n_per_group

top_orders = top_n_per_group(
    prepared,
    group_column="customer_id",
    value_column="revenue",
    n=2,
)
```

Eşit değerlerde stable sıralamanın kaynak sırasını koruduğunu incele.

## 10. Testleri çalıştırma

```bash
pytest curriculum/tr/05-data-analysis-sql-data-engineering/02-pandas-series-dataframe-indexing-groupby/tests -q
```

## Laboratuvar teslimi

Teslim paketi şu çıktıları içermelidir:

- Çalışan pipeline kodu
- Test sonucu
- Ham ve hazırlanmış veri kalite profili
- Merge kardinalitesi açıklaması
- Fit/transform veri sızıntısı analizi
- En az üç GroupBy metriği
- Bellek tüketimi ve dtype iyileştirme notları
- Beş maddelik hata analizi