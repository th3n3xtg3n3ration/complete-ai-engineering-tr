# Ders 1 — Algoritmik Düşünme, Big-O ve Temel Veri Yapıları

**Seviye:** L1 · **Tahmini süre:** 12 saat · **Durum:** Tamamlandı

## Öğrenme hedefleri

Bu dersin sonunda:

- Bir problemi girdi, çıktı, kısıt ve kenar durumlarıyla tanımlayabileceksin.
- Zaman ve alan karmaşıklığını Big-O ile analiz edebileceksin.
- `O(1)`, `O(log n)`, `O(n)`, `O(n log n)` ve `O(n²)` sınıflarını karşılaştırabileceksin.
- Python list, deque ve dictionary yapılarını doğru kullanım senaryolarıyla seçebileceksin.
- Stack, queue, hash table ve singly linked list yapılarını uygulayabileceksin.
- Amortized analysis ve time-space trade-off kavramlarını açıklayabileceksin.
- AI veri işleme akışlarında uygun veri yapısını seçebileceksin.

## Ders dosyaları

1. [Ayrıntılı teori](theory.md)
2. [Uygulama laboratuvarı](lab.md)
3. [Veri yapıları kodu](src/data_structures.py)
4. [Alıştırmalar](exercises.md)
5. [Quiz](quiz.md)
6. [Ödev ve rubrik](assignment.md)
7. [Mülakat soruları](interview-questions.md)
8. [Testler](tests/test_data_structures.py)
9. [Metadata](metadata.yml)

## Çalıştırma

```bash
python curriculum/tr/03-computer-science/01-algorithms-big-o-data-structures/src/data_structures.py
pytest curriculum/tr/03-computer-science/01-algorithms-big-o-data-structures/tests -q
```

## Mini proje

Bir model-serving kuyruğu için bounded queue, son işlemleri geri almak için stack ve kullanıcı oturumlarını saklamak için hash table tabanlı küçük bir veri yapıları paketi geliştireceksin.
