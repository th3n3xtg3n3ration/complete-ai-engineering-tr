# Quiz — NumPy Dizileri, Vektörleştirme ve Broadcasting

Her soru için en iyi seçeneği işaretle.

1. NumPy hızının temel nedeni hangisidir?  
   A) Python sözdizimi  
   B) Homojen bellek ve düşük seviyeli optimize döngüler  
   C) Her işlemin paralel olması  
   D) Verinin otomatik sıkıştırılması

2. `(5, 4, 3)` shape'li dizinin `ndim` değeri nedir?  
   A) 3 B) 5 C) 12 D) 60

3. Basic slicing çoğunlukla ne döndürür?  
   A) View B) Deep copy C) Python listesi D) Scalar

4. `X.mean(axis=0)` iki boyutlu veride genellikle neyi hesaplar?  
   A) Her satırın ortalaması  
   B) Her sütunun ortalaması  
   C) Global minimum  
   D) Shape

5. Broadcasting boyutları hangi yönden karşılaştırır?  
   A) Soldan sağa B) Sağdan sola C) Rastgele D) Sadece ilk eksen

6. Hangi shape çifti doğrudan uyumludur?  
   A) `(32,128)` ve `(32,)`  
   B) `(32,128)` ve `(128,)`  
   C) `(32,128)` ve `(64,)`  
   D) `(32,128)` ve `(31,128)`

7. `keepdims=True` ne sağlar?  
   A) dtype'ı korur  
   B) İndirgenen ekseni uzunluğu 1 olarak korur  
   C) Copy'yi engeller  
   D) NaN'leri siler

8. `np.nanmean` ne yapar?  
   A) NaN'leri sıfır kabul eder  
   B) NaN'leri hesaba katmadan ortalama alır  
   C) NaN üretir  
   D) Yalnız integer kabul eder

9. Vektörleştirme ne anlama gelir?  
   A) Hiç döngü çalışmaz  
   B) Döngü optimize edilmiş düşük seviyeli koda taşınır  
   C) GPU zorunludur  
   D) Veri kopyalanır

10. Standardization istatistikleri nerede öğrenilmelidir?  
    A) Tüm veri  
    B) Test verisi  
    C) Yalnız eğitim verisi  
    D) Validation ve test birleşimi

11. Sabit sütunda standard deviation nedir?  
    A) 1 B) 0 C) NaN olmak zorunda D) Sonsuz

12. Cosine similarity hangi özelliğe duyarsızdır?  
    A) Vektör yönü  
    B) Pozitif skaler büyüklük  
    C) İşaret  
    D) Feature sırası

13. Pairwise distance için `A[:,None,:]-B[None,:,:]` yaklaşımının riski nedir?  
    A) Dtype kaybı  
    B) Büyük 3-D geçici dizi  
    C) Sonuç simetrik olmaz  
    D) Matris çarpımı yapılamaz

14. `argpartition` hangi durumda faydalıdır?  
    A) Tüm elemanların tam sırası gerektiğinde  
    B) Sadece top-k gerektiğinde  
    C) Dtype dönüşümünde  
    D) NaN doldurmada

15. Fit edilmemiş transformer ne yapmalıdır?  
    A) Sessizce global ortalama kullanmalı  
    B) Açık hata vermeli  
    C) Test verisinde fit olmalı  
    D) Sıfır döndürmeli

16. `np.isfinite` neyi birlikte kontrol eder?  
    A) Yalnız NaN  
    B) NaN ve ±inf dışındaki sonlu değerleri  
    C) Yalnız integer  
    D) Negatif değerleri

17. `astype(np.float32)` hangi riski taşır?  
    A) Her zaman shape değişir  
    B) Hassasiyet kaybı olabilir  
    C) NaN silinir  
    D) View zorunludur

18. Benchmark için en iyi yaklaşım hangisidir?  
    A) Tek ölçüm  
    B) Warm-up, tekrar ve medyan  
    C) Rastgele farklı input  
    D) Sonucu yalnız teoriden tahmin etmek

19. Validation verisinde yeniden `fit` etmek neye yol açar?  
    A) Regularization  
    B) Data leakage ve tutarsız dönüşüm  
    C) Daha az bellek  
    D) Dtype güvenliği

20. Pipeline state'inin değişmez olması ne sağlar?  
    A) Transform sırasında yanlışlıkla güncellenme riskini azaltır  
    B) Her zaman daha hızlıdır  
    C) NaN oluşmasını engeller  
    D) Broadcasting'i kapatır

## Cevap anahtarı

1-B, 2-A, 3-A, 4-B, 5-B, 6-B, 7-B, 8-B, 9-B, 10-C, 11-B, 12-B, 13-B, 14-B, 15-B, 16-B, 17-B, 18-B, 19-B, 20-A
