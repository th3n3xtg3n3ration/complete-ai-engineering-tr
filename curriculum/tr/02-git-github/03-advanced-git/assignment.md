# Ödev — Git Geçmişi Kurtarma ve Regresyon Analizi

## Senaryo

Bir AI servis repository'sinde aşağıdaki sorunlar oluşmuştur:

- Feature branch'te dağınık ve anlamsız commit'ler vardır.
- Kritik bir düzeltme yanlış branch'e commit edilmiştir.
- Bir deney commit'i yanlışlıkla `reset --hard` ile kaybolmuştur.
- Model değerlendirme skorunu düşüren commit bilinmemektedir.

## Görevler

1. En az altı commit içeren örnek geçmiş oluştur.
2. Interactive rebase ile geçmişi en fazla üç anlamlı commit'e indir.
3. Yanlış branch'teki düzeltmeyi cherry-pick ile doğru branch'e taşı.
4. Reflog kullanarak kayıp commit'i bul ve recovery branch'inde koru.
5. En az sekiz aday commit arasındaki regresyonu `git bisect run` ile tespit et.
6. Kullanılan komutları ve riskleri `REPORT.md` içinde açıkla.
7. Paylaşılan branch için uygun geri alma stratejisini gerekçelendir.

## Teslimler

- Git repository
- `REPORT.md`
- Otomatik bisect test betiği
- `git log --graph --oneline --all` çıktısı

## Rubrik — 100 puan

- Commit geçmişi ve interactive rebase: 20
- Cherry-pick uygulaması: 15
- Reflog ile güvenli kurtarma: 20
- Otomatik bisect ve doğru regresyon tespiti: 25
- Risk analizi ve rapor kalitesi: 15
- Repository hijyeni: 5

## Güvenlik kuralı

Ödev sırasında gerçek üretim repository'sinde force push yapılmamalıdır. Tüm deneyler geçici veya yerel bir repository üzerinde yürütülmelidir.
