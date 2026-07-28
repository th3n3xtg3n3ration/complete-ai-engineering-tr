# Laboratuvar — AI Görev Orkestratörü

Bu laboratuvarda küçük bir AI pipeline zamanlayıcısı geliştireceksin.

## Senaryo

Pipeline görevleri bağımlılık ilişkilerine sahiptir:

```text
load_data -> validate_data -> train_model -> evaluate_model
                       \-> build_features -/
```

Ayrıca inference talepleri öncelik puanına göre işlenmelidir.

## Görevler

1. `Graph` ile pipeline bağımlılıklarını oluştur.
2. `topological_sort()` ile geçerli çalışma sırasını üret.
3. Bilerek bir cycle ekle ve hatanın yakalandığını doğrula.
4. `PriorityQueue` ile üç inference talebi ekle.
5. Aynı önceliğe sahip taleplerin eklenme sırasını koruduğunu göster.
6. `BinarySearchTree` içine model skorlarını ekle ve inorder traversal ile sıralı sonucu üret.

## Beklenen kontroller

- DAG geçerli sırada çalıştırılmalı.
- Cycle sessizce kabul edilmemeli.
- Öncelik kuyruğu boşken `IndexError` üretmeli.
- BST duplicate değerleri ikinci kez eklememeli.

## Ek çalışma

Graph sınıfına iki düğüm arasındaki en kısa ağırlıksız yolu döndüren `shortest_path` metodu ekle ve testlerini yaz.