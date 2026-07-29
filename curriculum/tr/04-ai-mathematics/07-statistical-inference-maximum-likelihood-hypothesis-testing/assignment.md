# Ödev — Üretim Kalitesinde A/B Test Analiz Paketi

## Amaç

Saf Python kullanarak sürekli ve binary metrikleri analiz eden, belirsizlik ve deney tasarımı risklerini görünür kılan yeniden kullanılabilir bir A/B test paketi geliştir.

## Senaryo

Bir AI ürününde yeni retrieval pipeline'ı test ediliyor. Control ve treatment grupları için şu metrikler var:

- task completion rate,
- kullanıcı başına latency,
- kullanıcı başına token tüketimi,
- safety violation oranı,
- kullanıcı memnuniyet skoru.

Primary metric task completion rate'tir. Latency ve safety violation guardrail metric olarak izlenir. Analiz bir kullanıcıyı bağımsız gözlem birimi kabul etmelidir.

## Zorunlu teslimler

### 1. Paket yapısı

```text
ab_inference/
├── __init__.py
├── validation.py
├── estimation.py
├── tests.py
├── multiple_testing.py
├── reporting.py
└── cli.py
```

### 2. Veri doğrulama

Aşağıdaki kontroller zorunludur:

- empty input,
- NaN ve infinity,
- binary metric için 0/1 dışı değer,
- duplicate user identifier,
- group overlap,
- beklenmeyen sample ratio,
- minimum sample size,
- analiz tarih aralığı,
- randomization unit ile analysis unit uyumu.

### 3. Sürekli metrik analizi

Fonksiyon en az şunları üretmelidir:

- control ve treatment sample size,
- mean ve sample variance,
- treatment-minus-control estimate,
- unequal-variance standard error,
- yüzde 95 confidence interval,
- approximate two-sided p-value,
- Cohen's d,
- seed kontrollü permutation p-value,
- minimum practical effect kararı.

### 4. Binary metrik analizi

Fonksiyon en az şunları üretmelidir:

- control ve treatment conversion rate,
- absolute lift,
- relative lift,
- pooled z statistic,
- two-sided p-value,
- difference confidence interval,
- risk ratio,
- minimum practical effect kararı.

### 5. Bootstrap

En az bir metrik için:

- bootstrap standard error,
- percentile confidence interval,
- bootstrap distribution özeti

üret.

`resamples` ve `seed` dışarıdan verilebilir olmalıdır.

### 6. Multiple testing

Guardrail metric'ler dahil aynı deneyde birden fazla test yürütüldüğü için:

- Bonferroni adjusted p-value,
- Benjamini–Hochberg adjusted p-value,
- raw ve adjusted kararlar

raporlanmalıdır.

### 7. Deney kalite uyarıları

Rapor şu durumlarda uyarı üretmelidir:

- sample ratio mismatch,
- düşük sample size,
- confidence interval'ın minimum practical effect sınırını kapsaması,
- statistical significance olup practical significance olmaması,
- primary metric iyileşirken guardrail metric bozulması,
- çok sayıda metric üzerinde düzeltmesiz test,
- sonuçlara tekrar tekrar bakıldığına dair analiz metadata'sı.

### 8. CLI

Örnek kullanım:

```bash
python -m ab_inference.cli \
  --input experiment.csv \
  --group-column variant \
  --unit-column user_id \
  --primary-metric completed \
  --continuous-metric latency_ms \
  --guardrail-metric safety_violation \
  --alpha 0.05 \
  --minimum-effect 0.01 \
  --permutations 10000 \
  --seed 42 \
  --output report.json
```

CLI non-zero exit code ile invalid input bildirmelidir.

### 9. Rapor formatı

JSON rapor en az şu üst seviye alanları içermelidir:

```json
{
  "experiment": {},
  "data_quality": {},
  "primary_metric": {},
  "guardrail_metrics": [],
  "multiple_testing": {},
  "decision": {},
  "warnings": [],
  "reproducibility": {}
}
```

### 10. Testler

En az 25 otomatik test yaz:

- happy path,
- invalid input,
- zero variance,
- zero control conversion,
- deterministic bootstrap,
- deterministic permutation,
- known MLE values,
- known p-value ordering,
- multiple-testing edge cases,
- practical-significance decision,
- sample-ratio warning,
- JSON serialization.

## Teknik rapor

`REPORT.md` dosyasında aşağıdakileri açıkla:

1. Population ve sampling süreci.
2. Randomization unit ve analysis unit.
3. Primary ve guardrail metric seçimleri.
4. Null ve alternative hypotheses.
5. Minimum practical effect gerekçesi.
6. Confidence interval ve effect size yorumu.
7. Parametrik test ile permutation test farkı.
8. Multiple-testing düzeltmesinin karara etkisi.
9. Peeking riskinin nasıl yönetileceği.
10. Son karar ve sınırlamalar.

## Kısıtlar

- İstatistik hesaplarında NumPy, SciPy, pandas veya statsmodels kullanma.
- Standart kütüphane kullanılabilir.
- Kod İngilizce; açıklamalar ve rapor Türkçe olmalıdır.
- Random işlemler seed kontrollü olmalıdır.
- p-value tek başına karar mekanizması olarak kullanılmamalıdır.
- Hatalar sessizce yutulmamalıdır.

## Rubrik — 100 puan

| Alan | Puan |
|---|---:|
| Veri doğrulama ve deney bütünlüğü | 15 |
| Point estimation ve confidence interval | 15 |
| Binary ve continuous test implementasyonları | 20 |
| Bootstrap ve permutation test | 15 |
| Multiple-testing düzeltmeleri | 10 |
| Effect size ve practical significance | 10 |
| Test kapsamı ve tekrarlanabilirlik | 10 |
| Teknik rapor ve kullanım deneyimi | 5 |

## Başarı ölçütü

- **90–100:** Üretim kalitesine yakın; varsayımlar ve riskler açık.
- **75–89:** Doğru ana akış; bazı edge-case veya raporlama eksikleri var.
- **60–74:** Temel hesaplar çalışıyor fakat deney tasarımı ve test kapsamı zayıf.
- **0–59:** Kritik istatistiksel veya yazılım hataları bulunuyor.

## Bonus

En fazla 10 bonus puan:

- paired test desteği,
- sequential testing için alpha-spending simülasyonu,
- power ve sample-size tahmini,
- BCa bootstrap araştırma notu,
- Markdown rapor çıktısı,
- A/A test sağlık kontrolü.
