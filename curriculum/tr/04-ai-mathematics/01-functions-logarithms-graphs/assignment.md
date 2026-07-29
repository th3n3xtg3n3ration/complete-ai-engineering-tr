# Ödev — Aktivasyon ve Loss Fonksiyonu Laboratuvarı

## Senaryo

Bir AI ekibi, yeni başlayan mühendislerin aktivasyon ve loss fonksiyonlarını hazır framework çağrılarının arkasına saklanmadan öğrenmesini istiyor. Görevin; fonksiyonları saf Python ile uygulayan, sayısal kararlılığı test eden, deney verisi üreten ve sonuçları teknik olarak yorumlayan küçük bir matematik paketi geliştirmektir.

## Zorunlu çıktı yapısı

```text
activation-loss-lab/
├── README.md
├── pyproject.toml
├── src/
│   └── activation_lab/
│       ├── __init__.py
│       ├── activations.py
│       ├── losses.py
│       ├── calculus.py
│       ├── sampling.py
│       └── cli.py
├── tests/
│   ├── test_activations.py
│   ├── test_losses.py
│   ├── test_calculus.py
│   └── test_cli.py
├── reports/
│   └── findings.md
└── generated/
    └── .gitkeep
```

## Fonksiyonel gereksinimler

### 1. Aktivasyonlar

Aşağıdaki fonksiyonları uygula:

- `sigmoid(x)`
- `tanh(x)`
- `relu(x)`
- `leaky_relu(x, negative_slope=0.01)`
- `softplus(x)`
- `softmax(logits)`
- `temperature_softmax(logits, temperature=1.0)`

Gereksinimler:

- Büyük pozitif ve negatif girdiler overflow üretmemeli.
- Boş softmax vektörü reddedilmeli.
- `NaN` ve sonsuz girdiler açık hata üretmeli.
- Softmax çıktılarının toplamı floating-point toleransı içinde 1 olmalı.
- `temperature <= 0` reddedilmeli.

### 2. Loss fonksiyonları

Aşağıdaki fonksiyonları uygula:

- `mean_squared_error(targets, predictions)`
- `binary_cross_entropy(targets, probabilities, epsilon=1e-12)`
- `categorical_cross_entropy(target_distribution, probabilities, epsilon=1e-12)`
- `binary_cross_entropy_with_logits(targets, logits)`

Gereksinimler:

- Boş koleksiyonlar reddedilmeli.
- Uzunluk uyuşmazlığı açık hata üretmeli.
- Olasılıklar `[0, 1]` aralığında doğrulanmalı.
- Hedef dağılımların toplamı kontrol edilmeli.
- `log(0)` ve `exp(1000)` gibi riskler kararlı formüllerle yönetilmeli.

### 3. Sayısal kalkülüs

Aşağıdaki araçları geliştir:

- `forward_difference(function, x, step=...)`
- `central_difference(function, x, step=...)`
- `gradient_check(function, analytical_derivative, points, tolerance=...)`

`gradient_check`, her nokta için analitik ve sayısal eğimi karşılaştırmalı ve yapılandırılmış sonuç döndürmelidir.

### 4. Örnekleme ve deney

Bir fonksiyonu seçilen aralıkta örnekleyen ortak veri katmanı geliştir. En az şu alanları üret:

```text
x,function_name,value,numerical_slope
```

Desteklenen çıktı formatları:

- CSV
- JSON Lines

### 5. CLI

Örnek kullanım:

```bash
python -m activation_lab.cli sample \
  --functions sigmoid,tanh,relu,softplus \
  --start -8 \
  --stop 8 \
  --step 0.25 \
  --format csv \
  --output generated/curves.csv
```

CLI aşağıdaki durumlarda başarısız exit code üretmeli:

- bilinmeyen fonksiyon,
- geçersiz aralık,
- sıfır veya negatif step,
- desteklenmeyen format,
- mevcut dosyayı `--overwrite` olmadan ezme girişimi.

### 6. Teknik rapor

`reports/findings.md` şu bölümleri içermeli:

1. Fonksiyon ailelerinin kısa özeti
2. Sigmoid ve tanh doygunluğu
3. ReLU ile softplus karşılaştırması
4. Softmax shift invariance
5. Temperature etkisi
6. BCE ve MSE davranış farkı
7. Sayısal kararlılık kararları
8. Gradient check sonuçları
9. Limitasyonlar ve sonraki geliştirmeler

Rapor, yalnızca teori tekrarı olmamalı; üretilen deney verilerinden sayısal örnekler içermelidir.

## Test gereksinimleri

En az 25 test yaz.

Zorunlu test sınıfları:

- bilinen değer testleri,
- extreme value testleri,
- domain validation testleri,
- parametrized invalid-input testleri,
- softmax normalization ve shift-invariance testleri,
- loss ordering testleri,
- gradient approximation testleri,
- geçici dizin kullanan CLI/output testleri.

Test komutu:

```bash
pytest -q
```

## Kalite gereksinimleri

- İngilizce değişken, fonksiyon ve sınıf adları
- Type hint
- Public fonksiyonlarda docstring
- Küçük ve tek sorumluluklu modüller
- Açıklayıcı exception mesajları
- Standart kütüphaneyle çalışan ana implementasyon
- Global mutable state kullanmama
- Deterministic çıktı
- Kullanıcı girdisini `eval` veya shell interpolation ile çalıştırmama

## Bonus görevler

Her biri en fazla 3 bonus puan:

1. Harici plotting paketi olmadan SVG çizgi grafiği üretme
2. NumPy mevcutsa vektörleştirilmiş opsiyonel backend
3. Log-sum-exp ve multiclass cross-entropy-with-logits implementasyonu
4. Property-based testler
5. Benchmark komutu ve naive/kararlı implementasyon karşılaştırması

Toplam not bonuslarla birlikte 100'ü aşamaz.

## Rubrik

| Alan | Puan |
|---|---:|
| Aktivasyonların doğruluğu ve kararlılığı | 18 |
| Loss fonksiyonlarının doğruluğu ve doğrulama kuralları | 18 |
| Sayısal türev ve gradient check | 12 |
| Örnekleme, CSV/JSONL ve CLI | 14 |
| Test kapsamı ve edge case kalitesi | 16 |
| Teknik rapor ve matematiksel yorum | 12 |
| Kod kalitesi, tipler ve dokümantasyon | 10 |
| **Toplam** | **100** |

## Geçme kriteri

- En az 70 puan
- Tüm zorunlu fonksiyonların mevcut olması
- Testlerin geçmesi
- Extreme value senaryolarında overflow kaynaklı çökme olmaması
- Teknik raporun bulunması

## Teslim kontrol listesi

- [ ] Paket temiz ortamda kuruluyor.
- [ ] `pytest -q` başarılı.
- [ ] CLI örnek komutu çalışıyor.
- [ ] CSV ve JSONL çıktıları üretiliyor.
- [ ] Extreme value testleri mevcut.
- [ ] Matematiksel formüller kaynak veya açıklamayla belgelenmiş.
- [ ] Rapor deney verilerine dayanıyor.
- [ ] Repository'de üretilmiş büyük veya gereksiz dosyalar bulunmuyor.
