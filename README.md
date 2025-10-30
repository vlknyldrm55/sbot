# sbot.py – Selcuksports M3U Generator

Bu Python scripti, SelcuksportsHD yayınlarını otomatik olarak tarar ve `.m3u` formatında oynatıcıya uygun bir liste oluşturur.

## 🚀 Özellikler

- Güncel aktif domaini otomatik bulur
- Tüm Bein, Smart, Tivibu ve S Sport kanallarını listeler
- M3U dosyasını `sbot.m3u` olarak kaydeder

## ⚙️ Gereksinimler

```bash
pip install requests

🧪 Kullanım

`bash
python sbot.py
`

Çalıştırıldığında aynı dizine sbot.m3u dosyasını oluşturur.

🔁 Otomatikleştirme (Android)

1. Pydroid 3 ile sbot.py dosyasını /storage/emulated/0/Pydroid3/scripts/ klasörüne koy
2. Macrodroid ile zamanlayıcı kur:
   - Trigger: Saat (örneğin her gün 14:00)
   - Action: Shell komutu
     `bash
     python3 /storage/emulated/0/Pydroid3/scripts/sbot.py
     `

📡 Yayın Linki Paylaşımı

Oluşan sbot.m3u dosyasını GitHub’a yükleyerek şu şekilde paylaşabilirsin:

`
https://raw.githubusercontent.com/KULLANICI_ADIN/sbot/main/sbot.m3u
`

> KULLANICI_ADIN kısmını kendi GitHub kullanıcı adınla değiştir.

`

5. Sayfanın altına bir commit mesajı yaz:  
   `
   add README.md
