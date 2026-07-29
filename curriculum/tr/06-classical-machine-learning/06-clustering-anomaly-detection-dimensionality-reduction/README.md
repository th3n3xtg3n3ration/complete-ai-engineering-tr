# Ders 6 — Clustering, Anomaly Detection ve Boyut İndirgeme

Bu ders, etiketsiz veriden yapı çıkarmayı, nadir davranışları belirlemeyi ve yüksek boyutlu veriyi daha yönetilebilir bir temsile dönüştürmeyi öğretir.

## Öğrenme hedefleri

Ders sonunda öğrenci:

- K-Means, Agglomerative Clustering ve DBSCAN algoritmalarının varsayımlarını karşılaştırabilir,
- küme sayısını silhouette, Davies–Bouldin ve iş bilgisiyle değerlendirebilir,
- Isolation Forest, Local Outlier Factor ve One-Class SVM ile anomali skoru üretebilir,
- contamination ve karar eşiğini doğrulama verisiyle seçebilir,
- PCA'nın kovaryans, özvektör ve explained variance ilişkisini açıklayabilir,
- scaling ve leakage risklerini pipeline içinde yönetebilir,
- etiketsiz problemlerde model kalitesini yalnızca tek bir metriğe indirgemeden inceleyebilir.

## Ders akışı

1. Etiketsiz öğrenme problemlerinin tanımlanması
2. K-Means ve küme geometrisi
3. Hiyerarşik kümeleme ve dendrogram
4. Yoğunluk tabanlı kümeleme: DBSCAN
5. Küme geçerlilik ölçümleri
6. Anomali tespiti ve threshold seçimi
7. PCA, SVD ve explained variance
8. Leakage-safe üretim pipeline'ları

## Dosyalar

- `theory.md`: Matematiksel ve kavramsal temel
- `lab.md`: Uçtan uca uygulama
- `exercises.md`: Özgün alıştırmalar
- `quiz.md`: Çoktan seçmeli değerlendirme
- `assignment.md`: Üretim senaryolu proje
- `interview-questions.md`: Teknik mülakat soruları
- `src/`: Tekrar kullanılabilir Python bileşenleri
- `tests/`: Davranış odaklı testler

## Ön koşullar

- NumPy ve pandas
- scikit-learn pipeline kullanımı
- temel lineer cebir
- train/validation/test ayrımı
- sınıflandırma metrikleri ve veri sızıntısı

## Temel ilke

Etiketsiz öğrenmede algoritmanın ürettiği yapı otomatik olarak iş açısından anlamlı değildir. Model çıktısı; stabilite, segment açıklanabilirliği, maliyet, veri toplama süreci ve mümkünse uzman geri bildirimiyle birlikte değerlendirilmelidir.
