# Ders 3 — İleri Git: Rebase, Cherry-pick, Reflog ve Bisect

**Seviye:** L2 · **Tahmini süre:** 10 saat · **Durum:** Tamamlandı

## Öğrenme hedefleri

Bu dersin sonunda:

- Commit graph yapısını okuyabileceksin.
- Interactive rebase ile commit geçmişini düzenleyebileceksin.
- Cherry-pick ile seçili commit'leri güvenli biçimde taşıyabileceksin.
- Reflog ile kaybolmuş commit'leri kurtarabileceksin.
- Bisect ile hatalı commit'i sistematik olarak bulabileceksin.
- Force push risklerini ve `--force-with-lease` kullanımını açıklayabileceksin.
- AI projelerinde deney kodu, veri ve model değişikliklerini temiz bir geçmişle yönetebileceksin.

## Ders dosyaları

1. [Ayrıntılı teori](theory.md)
2. [Uygulama laboratuvarı](lab.md)
3. [Alıştırmalar](exercises.md)
4. [Quiz](quiz.md)
5. [Ödev ve rubrik](assignment.md)
6. [Mülakat soruları](interview-questions.md)
7. [Bisect demo betiği](scripts/bisect_demo.py)
8. [Metadata](metadata.yml)

## Mini proje

Bir makine öğrenmesi deney repository'sinde dağınık commit geçmişini düzenleyecek, yanlış branch'e atılan commit'i cherry-pick ile taşıyacak, silinmiş bir commit'i reflog ile kurtaracak ve performans regresyonunu `git bisect` ile bulacaksın.
