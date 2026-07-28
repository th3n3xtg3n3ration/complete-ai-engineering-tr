# Teori — Python Temelleri

## Python programı nasıl çalışır?

Python kaynak kodu `.py` dosyasında tutulur. Yorumlayıcı kodu yukarıdan aşağıya çalıştırır. Bir hata oluştuğunda traceback, hata türünü ve satırını gösterir.

```python
message = "Merhaba, AI mühendisi!"
print(message)
```

## Değişkenler ve veri tipleri

Değişken, bir değere verilen isimdir. Açıklayıcı ve `snake_case` biçiminde isimler kullanılır.

```python
student_name = "Deniz"   # str
completed_lessons = 2     # int
success_rate = 0.85       # float
is_active = True          # bool
selected_model = None     # NoneType
```

## Operatörler

Aritmetik: `+`, `-`, `*`, `/`, `//`, `%`, `**`

Karşılaştırma: `==`, `!=`, `<`, `<=`, `>`, `>=`

Mantıksal: `and`, `or`, `not`

`/` ondalıklı bölme, `//` taban bölme, `%` kalan ve `**` üs işlemi yapar.

## Tip dönüşümü

`input()` her zaman metin döndürür. Sayısal işlemden önce dönüşüm gerekir.

```python
age_text = input("Yaşınız: ")
age = int(age_text)
```

Geçersiz dönüşüm `ValueError` üretir. Kullanıcı girdisi doğrulanmalıdır.

## f-string

```python
name = "Ece"
score = 91.25
print(f"{name} puanı: {score:.1f}")
```

## Fonksiyonlar

Fonksiyon tekrar kullanılabilir, küçük ve test edilebilir bir işlem birimidir.

```python
def calculate_savings(income: float, expenses: float) -> float:
    return income - expenses
```

`print` ekrana yazar; `return` değeri çağıran koda geri verir.

## Problem parçalama

Bir bütçe uygulaması şu adımlara ayrılabilir:

1. Girdileri al.
2. Girdileri doğrula.
3. Bakiyeyi hesapla.
4. Tasarruf oranını hesapla.
5. Sonucu biçimlendir.

Bu yaklaşım makine öğrenmesi ve ajan sistemlerinde de kullanılır: büyük problemi küçük, anlaşılır ve test edilebilir parçalara ayırmak.

## Hata mesajı okuma

Traceback'in en alt satırındaki hata türü ve açıklamayla başla. Sonra ilgili dosya ve satırı incele. Hata mesajını bastırmak yerine nedenini çöz.

## Test edilebilir kod

Kullanıcı girdisini hesaplama fonksiyonlarından ayırmak, fonksiyonları terminal açmadan test etmeyi sağlar.
