# Laboratuvar — Arama, Sıralama ve Recursion

## Amaç

Arama ve sıralama algoritmalarını çalıştırmak, doğruluklarını kontrol etmek ve farklı veri boyutlarında performanslarını karşılaştırmak.

## Adımlar

1. `src/algorithms.py` içindeki implementasyonları incele.
2. Linear search ve binary search sonuçlarını aynı sıralı veri üzerinde karşılaştır.
3. Binary search'ü sıralanmamış veri üzerinde çalıştırıp neden güvenilir olmadığını açıkla.
4. Bubble, selection ve insertion sort algoritmalarını küçük veri üzerinde çalıştır.
5. Merge sort ve quick sort için recursive çağrı ağacını çiz.
6. Benchmark aracını çalıştır:

```bash
python curriculum/tr/03-computer-science/02-search-sort-recursion/src/benchmark.py
```

7. Veri boyutlarını değiştir ve ölçümleri kaydet.
8. Testleri çalıştır:

```bash
pytest curriculum/tr/03-computer-science/02-search-sort-recursion/tests -q
```

## İnceleme soruları

- Insertion sort hangi veri dağılımında daha iyi sonuç verir?
- Merge sort neden ek bellek kullanır?
- Quick sort'un en kötü durumu nasıl oluşur?
- Benchmark sonucunu yalnızca tek çalıştırmayla değerlendirmek neden yanıltıcıdır?
