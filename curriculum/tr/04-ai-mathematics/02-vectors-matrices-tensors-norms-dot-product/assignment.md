# Ödev — Saf Python Embedding Arama Motoru

## Senaryo

Bir doküman platformu, küçük veri kümelerinde dış bağımlılık kullanmadan çalışan ve matematiksel davranışı kolayca denetlenebilen bir embedding arama prototipi istiyor. Görevin; shape doğrulaması, farklı metrikler, normalizasyon ve deterministik sıralama içeren bir arama motoru geliştirmektir.

## Zorunlu teslim yapısı

```text
submission/
├── README.md
├── src/
│   ├── vector_index.py
│   └── run_demo.py
├── tests/
│   └── test_vector_index.py
├── data/
│   └── embeddings.csv
└── report.md
```

## Fonksiyonel gereksinimler

### 1. Veri modeli

Her kayıt şu alanları içermelidir:

- `document_id`: benzersiz string
- `title`: boş olmayan string
- `vector`: sabit boyutlu finite sayı dizisi
- `metadata`: isteğe bağlı string-string sözlüğü

### 2. `VectorIndex`

Sınıf aşağıdaki sözleşmeyi desteklemelidir:

```python
index = VectorIndex(dimension=4, metric="cosine", normalize_vectors=True)
index.add(document_id="doc-1", title="Example", vector=[0.1, 0.2, 0.3, 0.4])
results = index.search([0.1, 0.2, 0.3, 0.4], top_k=5)
```

Zorunlu davranışlar:

- `dimension` pozitif integer olmalı.
- Metric `cosine` veya `euclidean` olmalı.
- Duplicate document ID reddedilmeli.
- Yanlış dimension reddedilmeli.
- `NaN`, infinity ve boolean değerler reddedilmeli.
- Cosine metric için sıfır vektörü reddedilmeli.
- `top_k` pozitif olmalı.
- Sonuçlar en iyiden en kötüye sıralanmalı.
- Eşit skorda document ID ile deterministik tie-break uygulanmalı.
- Arama sonucu rank, score, document ID ve title içermeli.

### 3. Kalıcılık

Aşağıdaki seçeneklerden birini uygula:

- CSV kaydetme/yükleme
- JSON Lines kaydetme/yükleme

Yükleme sırasında aynı validasyonlar tekrar uygulanmalıdır.

### 4. Deneyler

Aynı veri kümesinde dört konfigürasyonu karşılaştır:

1. Cosine, normalizasyon kapalı
2. Cosine, normalizasyon açık
3. Euclidean, normalizasyon kapalı
4. Euclidean, normalizasyon açık

En az:

- 50 doküman
- 8 boyutlu vektör
- 5 farklı sorgu
- Her sorgu için top-5 sonuç

kullan.

## Test gereksinimleri

En az 20 pytest testi yaz. Şunları mutlaka kapsa:

- Başarılı kayıt ekleme
- Duplicate ID
- Yanlış dimension
- Empty title
- Non-finite değer
- Boolean değer
- Sıfır vektörü
- Geçersiz metric
- Geçersiz `top_k`
- Cosine sıralama yönü
- Euclidean sıralama yönü
- Deterministik tie-break
- Normalizasyon sonrası birim norm
- Kaydetme/yükleme round-trip
- Bozuk kalıcılık dosyası
- Empty index araması
- Query dimension hatası
- Aynı query ile tekrarlanabilir sonuç
- `top_k` doküman sayısından büyükken davranış
- Metadata korunumu

## Teknik rapor

`report.md` en az 800 kelime olmalı ve şu soruları yanıtlamalıdır:

1. Dot product ile cosine similarity arasındaki ilişki nedir?
2. Normalizasyon sıralamayı hangi koşullarda değiştirir?
3. Cosine ve Euclidean sonuçları hangi sorgularda ayrıştı?
4. Vektör büyüklüğü veri için anlam taşıyor mu?
5. Shape validasyonunu hangi katmanda yaptın ve neden?
6. Saf Python yaklaşımının performans sınırları nelerdir?
7. Sistemi NumPy, FAISS veya bir vector database'e taşırken API sözleşmesini nasıl korursun?

## Kalite gereksinimleri

- Python 3.11+
- Type hints
- Docstring
- Küçük ve tek sorumluluklu fonksiyonlar
- Açıklayıcı exception mesajları
- Global mutable state kullanılmaması
- Deterministik test verileri
- Testlerde yaklaşık floating-point karşılaştırması
- README içinde çalıştırma komutları

## Rubrik — 100 puan

| Alan | Puan |
|---|---:|
| Matematiksel doğruluk | 20 |
| Shape ve veri validasyonu | 15 |
| Cosine/Euclidean sıralama | 15 |
| Normalizasyon tasarımı | 10 |
| Kalıcılık ve hata yönetimi | 10 |
| Test kapsamı | 15 |
| Kod kalitesi ve API tasarımı | 10 |
| Teknik rapor | 5 |

## Başarı ölçütü

- **90–100:** Üretim kalitesine yakın, güvenilir ve iyi belgelenmiş
- **75–89:** Temel gereksinimler doğru, küçük tasarım eksikleri var
- **60–74:** Çalışıyor ancak validasyon veya test kapsamı yetersiz
- **0–59:** Matematiksel veya işlevsel temel gereksinimler eksik

## Bonus

Her biri en fazla 5 puan:

- Batch query desteği
- Manhattan distance metriği
- Vektör silme ve güncelleme
- Basit recall@k değerlendirmesi
- Benchmark ve `cProfile` raporu

Toplam puan bonuslarla 110'u geçebilir; resmi başarı notu 100 üzerinden değerlendirilir.
