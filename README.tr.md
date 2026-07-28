# Açık Yapay Zekâ Mühendisliği Akademisi

## Vizyon

Bu projenin amacı, yapay zekâyı yalnızca hazır API çağrıları düzeyinde öğreten bir kaynak oluşturmak değildir. Hedefimiz; hiç programlama bilmeyen bir öğrenciyi Python, matematik ve bilgisayar bilimi temellerinden başlayarak makine öğrenmesi, derin öğrenme, Transformer, büyük dil modelleri, RAG, model uyarlama, Agentic AI, MLOps/LLMOps, değerlendirme ve güvenlik alanlarında üretim seviyesine taşıyan yaşayan bir açık kaynak akademi kurmaktır.

## Projenin farkı

- Ana anlatım dili Türkçedir.
- Kod, dosya ve API isimleri uluslararası uygulamaya uygun şekilde İngilizcedir.
- Teknik terimler Türkçe karşılıklarıyla birlikte öğretilir.
- Her kavram önce sezgisel, ardından matematiksel ve uygulamalı olarak ele alınır.
- Kritik algoritmalar kütüphanesiz veya düşük seviyeli araçlarla sıfırdan yazılır.
- Sonraki aşamada modern framework ve üretim araçları kullanılır.
- Notebook'ların yanında test edilebilir Python paketleri ve gerçek uygulamalar bulunur.
- RAG, ajan ve LLM sistemleri ölçüm, güvenlik, maliyet ve yetki sınırlarıyla birlikte öğretilir.

## Kimler için?

- Yapay zekâya sıfırdan başlamak isteyenler
- Yazılımcılıktan AI mühendisliğine geçmek isteyenler
- Veri bilimi ve makine öğrenmesini sistematik öğrenmek isteyenler
- LLM, RAG veya Agentic AI uygulamaları geliştirenler
- Teknik eğitim veren öğretmen ve mentorlar
- Araştırma ve yüksek lisans için temel oluşturmak isteyenler

## Eğitim yaklaşımı

Her ders aşağıdaki öğretim döngüsünü izler:

```text
Ön koşullar
→ Öğrenme hedefleri
→ Ön değerlendirme
→ Sezgisel açıklama
→ Teknik teori
→ Matematik
→ Sıfırdan uygulama
→ Framework uygulaması
→ Laboratuvar
→ Hata ayıklama
→ Alıştırma
→ Ödev ve rubrik
→ Son değerlendirme
→ Ek kaynaklar
```

## Ana öğrenme yolu

```text
Oryantasyon
→ Python
→ Bilgisayar Bilimi ve Yazılım Mühendisliği
→ Matematik
→ Veri Analizi, SQL ve Veri Mühendisliği
→ Makine Öğrenmesi
→ Derin Öğrenme ve PyTorch
→ Uygulamalı AI
→ Attention ve Transformer
→ LLM Mühendisliği
→ RAG
→ Fine-tuning ve Alignment
→ Agentic AI
→ MLOps ve LLMOps
→ Evaluation, Güvenlik ve Responsible AI
→ Bitirme Projesi
```

Ayrıntılı plan için [`CURRICULUM.md`](CURRICULUM.md) dosyasına bakın.

## Seviye sistemi

| Seviye | Tanım |
|---|---|
| L0 | Daha önce teknik deneyimi olmayan öğrenci |
| L1 | Başlangıç düzeyinde kavramları tanıyan öğrenci |
| L2 | Rehberle uygulama geliştirebilen öğrenci |
| L3 | Bağımsız proje geliştirebilen orta seviye öğrenci |
| L4 | İleri modelleri ve mimarileri uygulayabilen öğrenci |
| L5 | Üretim ortamı sorumluluğu alabilen mühendis |
| L6 | Makale okuyup yöntem yeniden üretebilen araştırma seviyesi |

## Depo yapısı

```text
complete-ai-engineering-tr/
├── curriculum/       # Ana Türkçe müfredat
├── specializations/  # İleri uzmanlık yolları
├── docs/             # Kurulum, sözlük ve rehberler
├── templates/        # Ders ve proje şablonları
├── tools/            # Müfredat doğrulama ve otomasyon araçları
├── tests/            # Kod ve depo yapısı testleri
└── .github/          # CI ve katkı şablonları
```

## İlk sürümde hazır olanlar

- Proje vizyonu ve 84 haftalık müfredat
- Genişletilebilir klasör mimarisi
- Makine tarafından okunabilir ders metadata standardı
- Yeni ders oluşturma aracı
- Metadata ve depo yapısı doğrulama araçları
- GitHub Actions kalite iş akışı
- Katkı, güvenlik ve davranış kuralları
- Modül 0, Ders 1: AI ekosisteminin kavram haritası
- Ön test, son test, ödev, rubrik ve kod örneği

## Yerel geliştirme

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
ruff check .
pytest
python tools/curriculum-validator/validate_metadata.py
```

## Yeni ders oluşturma

```bash
python tools/create_lesson.py \
  --module curriculum/tr/01-python \
  --lesson 01-variables-and-data-types \
  --title "Değişkenler ve Veri Tipleri" \
  --level L0
```

## Katkı

Küçük yazım düzeltmelerinden yeni uzmanlık yollarına kadar katkılar değerlidir. Katkı yapmadan önce [`CONTRIBUTING.md`](CONTRIBUTING.md) dosyasını okuyun.

## İçerik ilkesi

Bu proje “çok başlık, az içerik” deposu olmayacaktır. Bir ders **Stable** olarak işaretlenmeden önce:

- Hedefleri tanımlanmalı,
- Kodları çalışmalı,
- Testleri geçmeli,
- En az bir alıştırma içermeli,
- Çözüm veya rubrik sunmalı,
- Kaynakları belirtilmeli,
- Teknik ve pedagojik incelemeden geçmelidir.

## Proje durumu

Şu anda **Foundation / v0.1.0** aşamasındayız. Bir sonraki hedef Python modülünün ilk sekiz dersini, iki mini projeyi ve statik eğitim sitesinin ilk sürümünü tamamlamaktır.
