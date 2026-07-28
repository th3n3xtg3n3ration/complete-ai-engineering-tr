# Quiz

## Sorular

1. Working tree ile staging area arasındaki fark nedir?
2. `git add` komutu ne yapar?
3. İyi bir commit hangi özelliğe sahip olmalıdır?
4. `git fetch` ile `git pull` arasındaki fark nedir?
5. Merge conflict neden oluşur?
6. Paylaşılmış bir commit'i güvenli biçimde geri almak için hangi komut tercih edilir?
7. `git restore --staged file.py` ne yapar?
8. `.gitignore` geçmişte commit edilmiş bir dosyayı otomatik olarak geçmişten kaldırır mı?
9. API anahtarı commit edildiğinde neden yalnızca dosyayı silmek yeterli değildir?
10. Büyük model ağırlıkları neden normal Git repository'sinde tutulmamalıdır?

## Cevap anahtarı

1. Working tree güncel dosyaları, staging area ise sonraki commit için seçilmiş değişiklikleri içerir.
2. Değişiklikleri staging area'ya ekler.
3. Tek bir mantıksal ve anlaşılır değişikliği temsil etmelidir.
4. `fetch` uzak veriyi indirir; `pull` indirme sonrası mevcut branch ile bütünleştirir.
5. Git aynı bölümdeki farklı değişiklikler arasında otomatik seçim yapamadığında oluşur.
6. `git revert <sha>`.
7. Dosyayı stage alanından çıkarır, çalışma alanındaki değişikliği korur.
8. Hayır. Yalnızca gelecekte izlenmesini engeller; önce index'ten çıkarılması gerekir.
9. Secret Git geçmişinde ve kopyalarda kalabilir; iptal edilip yenilenmelidir.
10. Repository boyutunu ve klonlama maliyetini büyütür; artifact storage veya uygun büyük dosya çözümü kullanılmalıdır.
