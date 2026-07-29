# Teori — Ağaçlar ve Ensemble Modeller

## 1. Karar ağacı

Karar ağacı özellik uzayını eşiklerle parçalara ayırır. Her iç düğüm bir soru, her yaprak ise tahmindir. Sınıflandırmada split kalitesi çoğunlukla Gini veya entropy azalımıyla ölçülür.

Gini:

\[
G=1-\sum_k p_k^2
\]

Entropy:

\[
H=-\sum_k p_k\log_2 p_k
\]

Information gain, ebeveyn impurity ile ağırlıklı çocuk impurity farkıdır.

## 2. Aşırı uyum ve budama

Derin ağaç düşük bias fakat yüksek variance üretir. `max_depth`, `min_samples_split`, `min_samples_leaf`, `max_leaf_nodes` ve `ccp_alpha` model karmaşıklığını sınırlar. Cost-complexity pruning, hata ile ağaç büyüklüğü arasında denge kurar.

## 3. Bagging ve random forest

Bagging farklı bootstrap örneklerinde modeller eğitir ve tahminleri ortalar. Random forest ayrıca her split'te özelliklerin rastgele alt kümesini değerlendirir. Bu iki rastgelelik ağaçlar arası korelasyonu azaltır.

OOB skor, her örneği kendisini içermeyen ağaçlarla değerlendirir. Yararlı bir sinyaldir fakat bağımsız test setinin yerine geçmez.

## 4. Boosting

Boosting zayıf öğrenicileri ardışık kurar. Her yeni model mevcut ensemble'ın hatalarını azaltmaya çalışır.

- AdaBoost yanlış sınıflandırılan örneklerin ağırlığını artırır.
- Gradient Boosting loss fonksiyonunun negatif gradyanına yaklaşır.
- Histogram tabanlı boosting sürekli özellikleri bin'lere ayırarak büyük veride hız sağlar.

Boosting güçlüdür fakat learning rate, estimator sayısı, tree depth ve early stopping dikkatli seçilmelidir.

## 5. Voting ve stacking

Voting, farklı modellerin tahminlerini birleştirir. Soft voting olasılıkları ortalar. Stacking ise taban modellerin out-of-fold tahminlerini üst modele özellik olarak verir. Üst model aynı eğitim tahminleriyle eğitilirse leakage oluşur.

## 6. Feature importance

Impurity importance hızlıdır fakat yüksek kardinaliteli ve çok sayıda split seçeneği olan özellikleri kayırabilir. Permutation importance, bir özelliği karıştırınca skorun ne kadar düştüğünü ölçer. Korelasyonlu özelliklerde önem bölünebilir.

## 7. Güvenilir değerlendirme

Model karşılaştırmasında aynı split veya aynı cross-validation fold'ları kullanılmalıdır. Train–validation farkı generalization gap olarak raporlanmalıdır. Ranking metriği, probability metriği, threshold metriği ve iş maliyeti birlikte değerlendirilmelidir.
