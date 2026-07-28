# Ders 2 — Arama, Sıralama ve Recursion

**Seviye:** L1 · **Tahmini süre:** 12 saat · **Durum:** Tamamlandı

## Öğrenme hedefleri

Bu dersin sonunda:

- Linear search ve binary search algoritmalarını uygulayabileceksin.
- Binary search için sıralı veri ön koşulunu açıklayabileceksin.
- Bubble, selection ve insertion sort algoritmalarını karşılaştırabileceksin.
- Merge sort ve quick sort algoritmalarını divide-and-conquer yaklaşımıyla uygulayabileceksin.
- Recursion için base case ve recursive case tasarlayabileceksin.
- Zaman ve alan karmaşıklığını analiz edebileceksin.
- Python'da algoritma benchmark'ı hazırlayabileceksin.
- AI veri işleme senaryolarında uygun arama ve sıralama yaklaşımını seçebileceksin.

## Ders dosyaları

1. [Ayrıntılı teori](theory.md)
2. [Uygulama laboratuvarı](lab.md)
3. [Algoritma implementasyonları](src/algorithms.py)
4. [Benchmark aracı](src/benchmark.py)
5. [Alıştırmalar](exercises.md)
6. [Quiz](quiz.md)
7. [Ödev ve rubrik](assignment.md)
8. [Mülakat soruları](interview-questions.md)
9. [Testler](tests/test_algorithms.py)
10. [Metadata](metadata.yml)

## Çalıştırma

```bash
python curriculum/tr/03-computer-science/02-search-sort-recursion/src/benchmark.py
pytest curriculum/tr/03-computer-science/02-search-sort-recursion/tests -q
```

## Mini proje

Farklı büyüklükteki yapay zekâ veri kümelerinde linear search, binary search, insertion sort, merge sort ve quick sort algoritmalarını karşılaştıran tekrarlanabilir bir benchmark paketi geliştireceksin.
