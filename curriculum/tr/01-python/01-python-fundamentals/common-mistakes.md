# Yaygın Hatalar

## `=` ile `==` karıştırmak

`=` atama, `==` karşılaştırmadır.

## `input()` sonucunu sayı sanmak

`input()` metin döndürür. `int()` veya `float()` ile dönüştür.

## Değişkeni tanımlamadan kullanmak

Bir isim kullanılmadan önce değer atanmalıdır.

## Ondalık ayırıcı sorunu

Türkiye'de kullanıcı `12,5` yazabilir; `float()` virgüllü metni doğrudan kabul etmez. Girdiyi doğrula.

## `print` sonucunu kullanmaya çalışmak

`print()` ekrana yazar ve `None` döndürür. Hesap sonucunu başka yerde kullanacaksan `return` et.

## Yerleşik isimleri ezmek

`list`, `str`, `sum` ve `input` gibi isimleri değişken adı olarak kullanma.

## Her şeyi tek fonksiyona yazmak

Girdi alma, hesaplama ve çıktı biçimlendirmeyi ayır; böylece kod test edilebilir olur.
