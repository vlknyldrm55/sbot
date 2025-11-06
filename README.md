# sbot.py – DeaTHLesS M3U Generator

Bu Python scripti, aşağıdaki 3 kaynaktan yayınları otomatik olarak tarar ve `.m3u` formatında bir liste oluşturur:

- ✅ SelcuksportsHD
- ✅ BirazcıkSpor
- ✅ BilyonerSport

Oluşturulan liste `sbot.m3u` dosyasına kaydedilir. Script mobil ve PC ortamlarında çalışacak şekilde optimize edilmiştir.

## Dosyalar

- `sbot.py` → Ana bot scripti (3 kaynaklı)
- `sbot.m3u` → Oluşturulan yayın listesi
- `upload.py` → M3U dosyasını sunucuya veya cihaza aktarmak için yardımcı script

## Özellikler

- Otomatik domain bulma ve stream link çıkarma
- Mobil uyumlu dosya kaydetme
- HTML arayüz desteği (isteğe bağlı)
- Otomatik zamanlama (Tasker, Termux, Windows Scheduler ile uyumlu)

## Kullanım

```bash
python sbot.py
