# Laboratuvar — Müşteri Segmentasyonu ve İşlem Anomalileri

Bu laboratuvarda aynı sentetik veri üzerinde clustering, anomali tespiti ve PCA uygulanır. Amaç yalnızca model kurmak değil, leakage-safe ve yorumlanabilir bir deney tasarlamaktır.

## 1. Kurulum

```python
import numpy as np
import pandas as pd

from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.compose import ColumnTransformer
from sklearn.decomposition import PCA
from sklearn.ensemble import IsolationForest
from sklearn.metrics import silhouette_score, davies_bouldin_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
```

## 2. Veri üretimi

```python
rng = np.random.default_rng(42)
n = 1200

segment = rng.choice([0, 1, 2], size=n, p=[0.45, 0.35, 0.20])
centers = np.array([
    [1500, 3, 0.08],
    [5000, 8, 0.22],
    [12000, 16, 0.41],
])
noise = rng.normal(0, [450, 1.2, 0.04], size=(n, 3))
X = centers[segment] + noise

frame = pd.DataFrame(X, columns=["monthly_spend", "visits", "digital_ratio"])
frame["region"] = rng.choice(["north", "south", "west"], size=n)
frame["customer_id"] = np.arange(n)

# Nadir ve yüksek harcamalı işlemler
anomaly_idx = rng.choice(n, size=25, replace=False)
frame.loc[anomaly_idx, "monthly_spend"] *= 4
frame.loc[anomaly_idx, "visits"] += 20
frame["known_anomaly"] = 0
frame.loc[anomaly_idx, "known_anomaly"] = 1
```

`customer_id` kimlik bilgisidir; uzaklık hesabına sokulmaz. `known_anomaly` yalnızca değerlendirme için tutulur.

## 3. Train ve test ayrımı

```python
train, test = train_test_split(frame, test_size=0.25, random_state=42)
features = ["monthly_spend", "visits", "digital_ratio", "region"]
numeric = ["monthly_spend", "visits", "digital_ratio"]
categorical = ["region"]

preprocessor = ColumnTransformer([
    ("num", StandardScaler(), numeric),
    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical),
])
```

Unsupervised problemde split gereksiz değildir. Dönüşümlerin ve merkezlerin yeni veriye genellenip genellenmediğini görmek için holdout veri kullanılır.

## 4. K-Means karşılaştırması

```python
X_train = preprocessor.fit_transform(train[features])
X_test = preprocessor.transform(test[features])

rows = []
for k in range(2, 9):
    model = KMeans(n_clusters=k, n_init=20, random_state=42)
    labels = model.fit_predict(X_train)
    rows.append({
        "k": k,
        "inertia": model.inertia_,
        "silhouette": silhouette_score(X_train, labels),
        "davies_bouldin": davies_bouldin_score(X_train, labels),
    })

results = pd.DataFrame(rows)
print(results.sort_values("silhouette", ascending=False))
```

Seçimi yalnızca en yüksek silhouette değerine göre yapma. Küme büyüklüklerini ve profil farklarını incele.

```python
best = KMeans(n_clusters=3, n_init=20, random_state=42)
train_labels = best.fit_predict(X_train)
train_profile = train.assign(cluster=train_labels).groupby("cluster")[numeric].agg(["mean", "median", "count"])
print(train_profile)
```

## 5. DBSCAN

```python
for eps in [0.4, 0.6, 0.8, 1.0]:
    labels = DBSCAN(eps=eps, min_samples=10).fit_predict(X_train)
    clusters = len(set(labels)) - (1 if -1 in labels else 0)
    noise_ratio = np.mean(labels == -1)
    print(eps, clusters, round(noise_ratio, 3))
```

Silhouette yalnızca en az iki gerçek küme varsa ve tüm örnekler gürültü değilse hesaplanmalıdır.

## 6. Hiyerarşik kümeleme

```python
sample = X_train[:400]
for linkage in ["ward", "complete", "average"]:
    labels = AgglomerativeClustering(n_clusters=3, linkage=linkage).fit_predict(sample)
    print(linkage, silhouette_score(sample, labels))
```

## 7. PCA

```python
pca = PCA(n_components=0.95, svd_solver="full")
Z_train = pca.fit_transform(X_train)
Z_test = pca.transform(X_test)

print("Bileşen sayısı:", pca.n_components_)
print("Kümülatif varyans:", pca.explained_variance_ratio_.sum())
```

PCA sonrası K-Means kurup sonuçları orijinal feature space üzerindeki modelle karşılaştır.

## 8. Isolation Forest

```python
iso = IsolationForest(
    n_estimators=300,
    contamination="auto",
    random_state=42,
)
iso.fit(X_train)

# Düşük score daha anormaldir.
validation_scores = iso.score_samples(X_test)
threshold = np.quantile(validation_scores, 0.03)
predicted_anomaly = (validation_scores <= threshold).astype(int)
```

Etiketli kontrol örnekleri bulunduğu için precision ve recall hesaplanabilir. Üretimde eşik, manuel inceleme kapasitesi ve hata maliyetiyle seçilmelidir.

## 9. Pipeline

```python
pipeline = Pipeline([
    ("preprocess", preprocessor),
    ("pca", PCA(n_components=0.95, svd_solver="full")),
    ("cluster", KMeans(n_clusters=3, n_init=20, random_state=42)),
])

pipeline.fit(train[features])
test_clusters = pipeline.predict(test[features])
```

## 10. Beklenen rapor

Raporunda şunları göster:

- feature seçimi ve dışlanan alanlar,
- scaling'in sonuçlara etkisi,
- farklı `k`, linkage ve DBSCAN parametrelerinin karşılaştırması,
- kümelerin profil tabloları,
- PCA bileşen sayısı ve explained variance,
- anomali threshold gerekçesi,
- modelin zaman içinde nasıl izleneceği.
