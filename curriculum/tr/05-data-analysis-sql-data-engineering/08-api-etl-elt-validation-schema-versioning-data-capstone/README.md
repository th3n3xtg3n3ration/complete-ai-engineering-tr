# Ders 8 — API, ETL/ELT, Veri Doğrulama, Şema, Versiyonlama ve Veri Capstone

**Seviye:** L2 · **Tahmini süre:** 24 saat · **Durum:** Tamamlandı

## Öğrenme hedefleri

Bu dersin sonunda:

- REST API kaynaklarında pagination, timeout, retry, exponential backoff ve rate-limit davranışını güvenilir biçimde uygulayabileceksin.
- Ham veriyi değiştirilemez ve checksum ile doğrulanabilir bronze snapshot'ları olarak saklayabileceksin.
- ETL ile ELT yaklaşımlarını veri hacmi, yönetişim ve hedef sistem bağlamında karşılaştırabileceksin.
- Alan tipi, zorunluluk, null, aralık, enum, pattern ve primary-key kuralları içeren sürümlü veri sözleşmeleri geliştirebileceksin.
- Geçersiz kayıtları pipeline'ı durdurmadan quarantine katmanına taşıyıp ayrıntılı hata nedenleri üretebileceksin.
- Idempotent upsert, güncelleme zamanı, foreign-key kontrolü ve incremental load ilkelerini uygulayabileceksin.
- Bronze, silver ve gold katmanları arasında açık lineage kurabileceksin.
- Dataset version, contract fingerprint, input checksum ve pipeline version ile tekrarlanabilir veri ürünleri yayımlayabileceksin.
- Manifest dosyalarıyla artefakt yolu, satır sayısı, checksum ve bağımlılık bilgisini izleyebileceksin.
- API'den analitik özellik tablosuna uzanan, test edilen uçtan uca bir veri pipeline'ı geliştirebileceksin.

## Ders dosyaları

1. [Ayrıntılı teori](theory.md)
2. [Uygulama laboratuvarı](lab.md)
3. [API extraction ve raw snapshot araçları](src/api_client.py)
4. [Sürümlü veri sözleşmeleri](src/data_contracts.py)
5. [Uçtan uca ETL/ELT capstone pipeline'ı](src/data_pipeline.py)
6. [Alıştırmalar](exercises.md)
7. [Quiz](quiz.md)
8. [Ödev ve rubrik](assignment.md)
9. [Mülakat soruları](interview-questions.md)
10. [Testler](tests/test_data_capstone.py)
11. [Metadata](metadata.yml)

## Çalıştırma

```bash
python curriculum/tr/05-data-analysis-sql-data-engineering/08-api-etl-elt-validation-schema-versioning-data-capstone/src/api_client.py
python curriculum/tr/05-data-analysis-sql-data-engineering/08-api-etl-elt-validation-schema-versioning-data-capstone/src/data_pipeline.py
pytest curriculum/tr/05-data-analysis-sql-data-engineering/08-api-etl-elt-validation-schema-versioning-data-capstone/tests -q
```

Dersin çekirdek pipeline'ı Python standart kütüphanesi ve SQLite ile çalışır. Testler dış ağa bağlanmaz; HTTP transport bağımlılığı sahte yanıtlarla enjekte edilir.

## Modül capstone

Müşteri ve sipariş API'lerinden veri alan üretim odaklı bir veri ürünü geliştireceksin. Sistem cursor pagination, transient hata retry'ı ve rate-limit bekleme davranışını uygulayacak; ham yanıtları content-addressed bronze snapshot'ları olarak saklayacak; sürümlü veri sözleşmeleriyle kayıtları doğrulayıp hatalı veriyi quarantine tablosuna taşıyacak; geçerli kayıtları SQLite warehouse'a idempotent upsert ile yükleyecek; SQL ile müşteri özellikleri üretecek ve silver/gold artefaktlarını yayımlayacak. Her çalıştırma input checksum, contract fingerprint, pipeline version, lineage, satır sayıları ve artefakt checksum'larını içeren bir manifest ile izlenecek.
