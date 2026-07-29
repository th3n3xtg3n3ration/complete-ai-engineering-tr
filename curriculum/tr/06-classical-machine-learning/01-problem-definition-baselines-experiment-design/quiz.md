# Quiz — Problem Tanımı, Baseline ve Deney Tasarımı

## 1. Bir ML projesinde algoritmadan önce tanımlanması gereken temel unsur nedir?

<details><summary>Cevap</summary>

Desteklenecek karar ve tahmin problemi.

</details>

## 2. Prediction unit neyi ifade eder?

<details><summary>Cevap</summary>

Bir tahmin satırının temsil ettiği varlık veya olay grain'ini.

</details>

## 3. Temporal leakage nedir?

<details><summary>Cevap</summary>

Tahmin anından sonra oluşan bilginin özelliklerde kullanılmasıdır.

</details>

## 4. Entity split ne zaman gerekir?

<details><summary>Cevap</summary>

Aynı müşteri, hasta, cihaz veya dokümanın birden fazla satırı olduğunda.

</details>

## 5. Regression için en basit iki baseline nedir?

<details><summary>Cevap</summary>

Training mean ve training median.

</details>

## 6. Dengesiz sınıflarda accuracy neden yanıltıcıdır?

<details><summary>Cevap</summary>

Çoğunluk sınıfını tahmin eden model yüksek accuracy elde edebilir.

</details>

## 7. Balanced accuracy nasıl yorumlanır?

<details><summary>Cevap</summary>

Sınıf başına recall değerlerinin ortalamasıdır.

</details>

## 8. Precision hangi soruyu cevaplar?

<details><summary>Cevap</summary>

Pozitif tahminlerin ne kadarı doğrudur?

</details>

## 9. Recall hangi soruyu cevaplar?

<details><summary>Cevap</summary>

Gerçek pozitiflerin ne kadarı bulunmuştur?

</details>

## 10. ROC-AUC threshold bağımsız olarak neyi ölçer?

<details><summary>Cevap</summary>

Pozitif örnekleri negatiflerden üstte sıralama yeteneğini.

</details>

## 11. Log loss neyi cezalandırır?

<details><summary>Cevap</summary>

Yanlış ve aşırı güvenli olasılık tahminlerini.

</details>

## 12. R² negatif olabilir mi?

<details><summary>Cevap</summary>

Evet; referans ortalama tahmininden daha kötü performansı gösterebilir.

</details>

## 13. Primary metric neden önceden seçilmelidir?

<details><summary>Cevap</summary>

Evaluation sonucuna göre metrik seçme yanlılığını önlemek için.

</details>

## 14. Guardrail metric nedir?

<details><summary>Cevap</summary>

Birincil metriği iyileştirirken bozulmaması gereken ikincil ölçüttür.

</details>

## 15. Bootstrap ne sağlar?

<details><summary>Cevap</summary>

Metrik tahmininin örneklem belirsizliği için güven aralığı sağlar.

</details>

## 16. Paired bootstrap neden iki modeli aynı satırlarda örnekler?

<details><summary>Cevap</summary>

Metrik farkındaki ortak örneklem değişkenliğini korumak için.

</details>

## 17. Preprocessing leakage nasıl önlenir?

<details><summary>Cevap</summary>

Transformer'ları yalnızca training verisinde fit ederek.

</details>

## 18. Random seed tek başına tam tekrarlanabilirlik sağlar mı?

<details><summary>Cevap</summary>

Hayır; veri, kod, bağımlılık ve split sürümleri de kaydedilmelidir.

</details>

## 19. Baseline'ı aşmak neden tek başına yeterli değildir?

<details><summary>Cevap</summary>

İyileşme küçük, belirsiz veya operasyonel olarak değersiz olabilir.

</details>

## 20. Deney kaydında hangi bilgiler bulunmalıdır?

<details><summary>Cevap</summary>

Problem, veri/split sürümü, seed, baseline, metrikler, kod sürümü ve karar.

</details>
