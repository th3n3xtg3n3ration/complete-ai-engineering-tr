# Quiz — Entropi, Cross-Entropy, KL Divergence ve Matematik Capstone

Her soru için en uygun seçeneği işaretleyin.

## Sorular

1. Bir olayın olasılığı azaldıkça surprisal nasıl değişir?
   - A) Azalır
   - B) Artar
   - C) Sabit kalır
   - D) Her zaman sıfır olur

2. Dört eşit olasılıklı sonucun entropisi bit cinsinden kaçtır?
   - A) 1
   - B) 2
   - C) 4
   - D) 8

3. Deterministik dağılımın entropisi kaçtır?
   - A) 0
   - B) 0.5
   - C) 1
   - D) Sonsuz

4. Cross-entropy için doğru eşitlik hangisidir?
   - A) `H(P,Q)=H(P)-KL(P||Q)`
   - B) `H(P,Q)=H(P)+KL(P||Q)`
   - C) `H(P,Q)=KL(Q||P)`
   - D) `H(P,Q)=H(Q)`

5. KL divergence hakkında hangisi doğrudur?
   - A) Her zaman simetriktir
   - B) Negatif olabilir
   - C) Aynı dağılımlar için sıfırdır
   - D) Üçgen eşitsizliğini her zaman sağlar

6. `P` pozitif olasılık verirken `Q` aynı olaya sıfır verirse `KL(P||Q)` ne olur?
   - A) Sıfır
   - B) Negatif
   - C) Sonsuz
   - D) Bir

7. Jensen–Shannon divergence'ın önemli özelliği hangisidir?
   - A) Simetrik olması
   - B) Her zaman negatif olması
   - C) Yalnızca binary dağılımlarda çalışması
   - D) Olasılık gerektirmemesi

8. Mutual information bağımsız değişkenlerde kaçtır?
   - A) Sıfır
   - B) Bir
   - C) Sonsuz
   - D) Tanımsız

9. Softmax'ın temel amacı nedir?
   - A) Feature standardization
   - B) Logit skorlarını olasılıklara dönüştürmek
   - C) Model boyutunu küçültmek
   - D) Etiketleri sıralamak

10. Büyük logits için kararlı softmax nasıl hesaplanır?
    - A) Tüm logitler ikiyle çarpılır
    - B) Maksimum logit çıkarılır
    - C) Minimum logit çıkarılır
    - D) Logitler yuvarlanır

11. One-hot hedefte categorical cross-entropy neye indirgenir?
    - A) Doğru sınıfın negatif log olasılığına
    - B) Tüm sınıfların ortalama logitine
    - C) Ağırlık normuna
    - D) Accuracy değerine

12. Label smoothing'in amacı hangisidir?
    - A) Sınıf sayısını azaltmak
    - B) Aşırı güveni azaltmak
    - C) Batch size'ı büyütmek
    - D) Feature sayısını artırmak

13. Focal loss hangi örneklerin etkisini azaltır?
    - A) Kolay ve doğru sınıflandırılan örneklerin
    - B) Yalnızca hatalı etiketlerin
    - C) Tüm pozitif örneklerin
    - D) Tüm negatif örneklerin

14. Perplexity hangi değerin üstelidir?
    - A) Accuracy
    - B) Ortalama negative log-likelihood
    - C) Gradient normu
    - D) Weight decay

15. Calibration neyi inceler?
    - A) Model boyutunu
    - B) Güven değerleriyle gözlenen doğruluğun uyumunu
    - C) Eğitim süresini
    - D) Feature korelasyonunu

16. Brier score hangi tür farkı kullanır?
    - A) Karesel olasılık hatası
    - B) Mutlak logit farkı
    - C) Cosine similarity
    - D) Rank farkı

17. Softmax regression'da `dL/dlogits` nedir?
    - A) `probabilities - one_hot_target`
    - B) `weights + bias`
    - C) `features - labels`
    - D) `logits / class_count`

18. L2 regularization ağırlık gradient'ine ne ekler?
    - A) Sabit bir bias
    - B) Ağırlıkla orantılı terim
    - C) Sınıf sayısı
    - D) Entropi

19. Distribution shift sırasında hangisi yararlı bir belirsizlik sinyalidir?
    - A) Predictive entropy
    - B) Yalnızca training accuracy
    - C) Dosya boyutu
    - D) Epoch numarası

20. Aynı accuracy'ye sahip iki modelin güvenilirliğini ayırmak için hangisi kullanılabilir?
    - A) ECE veya Brier score
    - B) Yalnızca sınıf sayısı
    - C) Feature count
    - D) Random seed

## Cevap anahtarı

1. B
2. B
3. A
4. B
5. C
6. C
7. A
8. A
9. B
10. B
11. A
12. B
13. A
14. B
15. B
16. A
17. A
18. B
19. A
20. A

## Başarı ölçütü

- 18–20: Konular güçlü biçimde anlaşılmıştır.
- 15–17: İyi düzey; yanlış cevaplar tekrar edilmelidir.
- 11–14: Teori ve laboratuvar yeniden çalışılmalıdır.
- 0–10: Önceki olasılık ve optimizasyon dersleriyle birlikte kapsamlı tekrar önerilir.
