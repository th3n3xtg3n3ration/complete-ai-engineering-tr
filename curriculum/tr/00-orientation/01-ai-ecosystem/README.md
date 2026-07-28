# Ders 1 — AI Ekosistemi ve Temel Kavramlar

**Seviye:** L0 · **Tahmini süre:** 4 saat · **Durum:** Draft

## Bu derste ne öğreneceğiz?

Bu dersin sonunda:

- Yapay zekâ, makine öğrenmesi ve derin öğrenme kavramlarını ayırabileceksin.
- Transformer'ın bir model ailesi değil, farklı modellerin üzerine kurulduğu bir mimari olduğunu anlayacaksın.
- LLM, üretken yapay zekâ, RAG ve Agentic AI ilişkisini açıklayabileceksin.
- Bir problem için klasik yazılım, makine öğrenmesi, LLM, RAG veya ajan yaklaşımından hangisinin daha uygun olduğunu tartışabileceksin.

## Ders dosyaları

1. [Kavram haritası](concept-map.md)
2. [Ayrıntılı teori](theory.md)
3. [Kod örneği](src/concept_demo.py)
4. [Başlangıç alıştırmaları](exercises/beginner.md)
5. [Yaygın hatalar](common-mistakes.md)
6. [Ödev](assignment/assignment.md)
7. [Değerlendirme rubriği](assignment/rubric.md)
8. [Mülakat soruları](interview-questions.md)

## Öğrenme sırası

```text
Kural tabanlı yazılım
        ↓
Yapay zekâ
        ↓
Makine öğrenmesi
        ↓
Derin öğrenme
        ↓
Attention ve Transformer
        ↓
Büyük dil modelleri
        ↓
RAG + araç kullanımı + durum yönetimi
        ↓
Agentic AI sistemleri
```

Bu şema bir “her yeni kavram eskisini tamamen değiştirir” sıralaması değildir. Örneğin bir ajan, LLM ile birlikte klasik yazılım kuralları, veritabanı, arama sistemi ve güvenlik politikaları da kullanabilir.

## Hızlı karşılaştırma

| Kavram | Temel soru | Örnek |
|---|---|---|
| Klasik yazılım | Kuralları açıkça yazabilir miyiz? | Vergi hesaplama |
| AI | Makinenin algı, karar veya üretim yapmasını istiyor muyuz? | Görüntü tanıma |
| ML | Sistem örüntüyü veriden mi öğrenmeli? | Müşteri kaybı tahmini |
| DL | Büyük ve karmaşık örüntüler için sinir ağı mı gerekli? | Konuşma tanıma |
| Transformer | Dizilerde ilişkileri attention ile mi modelleyeceğiz? | Metin üretimi |
| LLM | Doğal dille anlama/üretim mi istiyoruz? | Sohbet asistanı |
| RAG | Model güncel veya özel belgelere dayanmalı mı? | Şirket belgeleriyle soru-cevap |
| Agentic AI | Sistem hedef için araç kullanıp çok adımlı hareket etmeli mi? | Araştırma ve raporlama ajanı |

## Uygulama

```bash
python curriculum/tr/00-orientation/01-ai-ecosystem/src/concept_demo.py
```

Kod, verilen problem özelliklerine göre öğretici bir yaklaşım önerisi üretir. Gerçek dünyada karar çok daha ayrıntılı analiz gerektirir; örnek yalnızca kavramları somutlaştırmak içindir.

## Tamamlama ölçütü

- Son quizde en az %70
- Alıştırmaların tamamlanması
- Ödevde en az 14/20 puan
- Beş farklı probleme uygun yaklaşım seçimini gerekçelendirebilme

## Sonraki ders

Geliştirme ortamı: Python, VS Code, Jupyter, sanal ortam ve terminal.
