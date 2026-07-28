# Quiz

## Sorular

1. Git branch teknik olarak nedir?
2. Rebase bir commit dizisine ne yapar?
3. Interactive rebase içindeki `squash` ile `fixup` farkı nedir?
4. Cherry-pick neden aynı commit SHA'sını korumaz?
5. Reflog hangi tür kayıplarda yardımcı olur?
6. `git bisect` hangi arama yaklaşımını kullanır?
7. `git bisect run` ne sağlar?
8. `--force-with-lease`, `--force` seçeneğine göre neden daha güvenlidir?
9. Paylaşılan bir branch'teki hatalı commit için neden çoğunlukla `revert` tercih edilir?
10. `git reset --hard` hangi üç alanı etkiler?

## Cevap anahtarı

1. Belirli bir commit'i gösteren hareketli referanstır.
2. Commit'leri yeni bir taban üzerinde yeniden üretir ve geçmişi yeniden yazar.
3. İkisi de önceki commit ile birleştirir; `squash` mesaj düzenletir, `fixup` ikincil mesajı atar.
4. Değişiklikleri mevcut branch üzerinde yeni bir commit olarak uygular.
5. Yerel referans hareketleri hâlâ reflog'da duruyorsa reset, rebase veya branch silme sonrası commit kurtarmada.
6. İkili arama.
7. Her aday commit'te otomatik test çalıştırarak iyi/kötü sınıflandırmasını otomatikleştirir.
8. Uzak referans beklenmedik şekilde değişmişse push'u reddeder.
9. Geçmişi yeniden yazmadan ters değişiklik içeren yeni ve izlenebilir bir commit oluşturur.
10. Commit referansını, staging area'yı ve working tree'yi.
