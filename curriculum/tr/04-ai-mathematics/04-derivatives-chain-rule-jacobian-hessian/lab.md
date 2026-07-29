# Laboratuvar — Gradient, Jacobian, Hessian ve Autodiff

## Amaç

Bu laboratuvarda analitik türev, finite difference ve reverse-mode autodiff sonuçlarını karşılaştıracaksın.

## Bölüm 1 — Skaler türev

1. `f(x)=x^3-2x+1` için analitik türevi çıkar.
2. `central_difference` ile `x=-2,-1,0,1,2` noktalarını ölç.
3. `step` değerini `1e-1` ile `1e-10` arasında değiştir ve hatayı incele.

## Bölüm 2 — Gradient

`f(x,y)=(x-3)^2+2(y+1)^2` fonksiyonunun gradient'ını `[0,0]`, `[3,-1]` ve `[10,5]` noktalarında hesapla. Gradient yönünün minimumla ilişkisini yorumla.

## Bölüm 3 — Directional derivative

Aynı noktada `[1,0]`, `[0,1]` ve `[1,1]` yönlerini karşılaştır. Yön vektörünün normalize edilmesinin neden gerekli olduğunu açıkla.

## Bölüm 4 — Jacobian

`F(x,y)=[x*y, x^2+y, sin(x)]` fonksiyonunun Jacobian'ını sayısal olarak hesapla ve analitik sonuçla karşılaştır.

## Bölüm 5 — Hessian

İki değişkenli quadratic fonksiyon için Hessian hesapla. Simetriyi, diagonal/off-diagonal terimleri ve eğriliği yorumla.

## Bölüm 6 — Autodiff

`Value` sınıfıyla `L=(wx+b-y)^2` grafiğini kur. `x`, `w` ve `b` gradient'larını elle çıkardığın sonuçlarla karşılaştır.

## Bölüm 7 — Gradient checking

`gradient_check.py` aracını çalıştır. Bir backward kuralını bilinçli olarak bozup relative error'ın nasıl değiştiğini gözlemle; ardından düzelt.

## Teslim

- Çalışan kod ve testler
- En az üç deney tablosu
- Step-size seçimi, gradient birikimi ve Hessian yorumu hakkında kısa teknik rapor
