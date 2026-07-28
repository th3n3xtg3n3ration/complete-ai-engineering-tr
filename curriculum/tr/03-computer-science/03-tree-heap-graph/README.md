# Ders 3 — Tree, Heap ve Graph

**Seviye:** L2 · **Tahmini süre:** 14 saat · **Durum:** Tamamlandı

## Öğrenme hedefleri

Bu dersin sonunda:

- Binary tree ve binary search tree yapılarını açıklayabileceksin.
- Preorder, inorder, postorder ve level-order traversal uygulayabileceksin.
- Min-heap ile öncelik kuyruğu geliştirebileceksin.
- Graph yapılarını adjacency list ile modelleyebileceksin.
- BFS ve DFS algoritmalarını karşılaştırabileceksin.
- Cycle detection ve topological ordering mantığını açıklayabileceksin.
- AI iş akışlarında tree, heap ve graph kullanım alanlarını seçebileceksin.

## Ders dosyaları

1. [Ayrıntılı teori](theory.md)
2. [Uygulama laboratuvarı](lab.md)
3. [Veri yapıları ve algoritmalar](src/structures.py)
4. [Alıştırmalar](exercises.md)
5. [Quiz](quiz.md)
6. [Ödev ve rubrik](assignment.md)
7. [Mülakat soruları](interview-questions.md)
8. [Testler](tests/test_structures.py)
9. [Metadata](metadata.yml)

## Çalıştırma

```bash
python curriculum/tr/03-computer-science/03-tree-heap-graph/src/structures.py
pytest curriculum/tr/03-computer-science/03-tree-heap-graph/tests -q
```

## Mini proje

Bir AI görev orkestratörü için bağımlılık graph'ı, öncelik heap'i ve karar tree'si içeren küçük bir zamanlayıcı geliştireceksin.