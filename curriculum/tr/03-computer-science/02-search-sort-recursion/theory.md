# Teori — Arama, Sıralama ve Recursion

## 1. Arama problemi

Arama algoritmaları, bir koleksiyon içinde hedef değerin konumunu bulur.

### Linear search

Linear search elemanları soldan sağa inceler.

- En iyi durum: `O(1)`
- Ortalama durum: `O(n)`
- En kötü durum: `O(n)`
- Ek alan: `O(1)`

Verinin sıralı olmasını gerektirmez.

### Binary search

Binary search, sıralı bir dizinin arama aralığını her adımda ikiye böler.

- En iyi durum: `O(1)`
- Ortalama ve en kötü durum: `O(log n)`
- İteratif ek alan: `O(1)`

Binary search yalnızca karşılaştırılabilir ve sıralı veri üzerinde doğrudan uygulanabilir.

## 2. Basit sıralama algoritmaları

### Bubble sort

Komşu elemanları karşılaştırır ve yanlış sıradaysa yer değiştirir. Eğitim açısından yararlıdır fakat büyük veri için verimsizdir.

- Ortalama ve en kötü durum: `O(n²)`
- Ek alan: `O(1)`
- Stable: Evet

### Selection sort

Her turda kalan bölümün minimum elemanını seçer.

- Tüm durumlarda: `O(n²)`
- Ek alan: `O(1)`
- Stable: Varsayılan uygulamada hayır

### Insertion sort

Elemanları büyüyen sıralı bir ön bölüme yerleştirir. Küçük veya neredeyse sıralı veri üzerinde etkilidir.

- En iyi durum: `O(n)`
- Ortalama ve en kötü durum: `O(n²)`
- Ek alan: `O(1)`
- Stable: Evet

## 3. Divide and conquer

Divide-and-conquer yaklaşımı problemi daha küçük alt problemlere ayırır, alt problemleri çözer ve sonuçları birleştirir.

### Merge sort

Diziyi ikiye böler, parçaları recursive olarak sıralar ve sıralı parçaları birleştirir.

- Tüm durumlarda: `O(n log n)`
- Ek alan: `O(n)`
- Stable: Evet

### Quick sort

Bir pivot seçer; küçükleri pivotun soluna, büyükleri sağına ayırır.

- Ortalama durum: `O(n log n)`
- En kötü durum: `O(n²)`
- Ek alan: Uygulamaya bağlıdır
- Stable: Genellikle hayır

Pivot seçimi performans açısından önemlidir.

## 4. Recursion

Recursive bir fonksiyon iki temel parçaya sahiptir:

1. **Base case:** Çağrı zincirini durdurur.
2. **Recursive case:** Problemi daha küçük bir örneğe indirger.

Base case eksikse sonsuz recursion oluşur ve Python `RecursionError` üretir.

Recursive çözümler bazı problemleri doğal biçimde ifade eder; ancak her çağrı call stack üzerinde alan kullanır. Bu nedenle iterative çözüm bazen daha güvenlidir.

## 5. Recurrence sezgisi

Merge sort için çalışma süresi yaklaşık şöyle ifade edilir:

```text
T(n) = 2T(n / 2) + O(n)
```

İki alt problem vardır ve birleştirme aşaması lineer zaman alır. Sonuç `O(n log n)` olur.

Binary search için:

```text
T(n) = T(n / 2) + O(1)
```

Sonuç `O(log n)` olur.

## 6. Benchmark tasarımı

Sağlıklı bir benchmark:

- Aynı girdileri algoritmalar arasında paylaşır.
- Birden fazla tekrar yapar.
- Veri üretim maliyetini ölçümden ayırır.
- Sonuçların doğru olduğunu da kontrol eder.
- Küçük ve büyük veri boyutlarını ayrı değerlendirir.

Tek ölçüm üzerinden kesin sonuç çıkarmak güvenilir değildir.

## 7. AI mühendisliği bağlantısı

Arama ve sıralama algoritmaları AI sistemlerinde şu alanlarda görülür:

- Benzerlik sonuçlarını skora göre sıralama
- Top-k aday seçimi
- Veri seti indeksleme
- Batch önceliklendirme
- Log ve deney kayıtlarında arama
- Ön işleme adımlarında sıralı birleştirme

Üretim kodunda çoğunlukla Python'ın yerleşik `sorted`, `list.sort` ve `bisect` gibi optimize edilmiş araçları tercih edilir. Sıfırdan implementasyon ise algoritmik düşünme ve karmaşıklık analizi kazandırır.
