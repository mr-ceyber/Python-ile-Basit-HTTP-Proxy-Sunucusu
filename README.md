🌐 Python ile Basit HTTP Proxy Sunucusu



📝 Proje Özeti

Bu proje, Python'ın yerleşik HTTP sunucu modülleri (http.server, socketserver) ve popüler requests kütüphanesi kullanılarak geliştirilmiş, minimal ve eğitim odaklı bir HTTP/HTTPS Vekil Sunucu (Proxy) uygulamasıdır. Amacı, istemciden gelen istekleri alıp belirli bir hedef URL'ye iletmek, yanıtı almak ve istemciye geri göndermek suretiyle temel bir proxy mekanizmasının nasıl çalıştığını göstermektir.



✨ Temel Özellikler

URL Tabanlı Yönlendirme:İstemciler, hedef URL'yi doğrudan proxy adresinin yol (path) kısmında belirtir (Örn: http://localhost:8080/https://example.com).

Çoklu Metot Desteği: GET ve POST HTTP metotlarını destekler.Başlık (Header) 

Filtreleme: Proxy sunucusu ve bağlantı katmanı için gereksiz olan başlıkları (örn: Host, Connection) otomatik olarak temizler.

Özel Loglama: Tüm gelen istekleri, hedef URL'yi ve sonuç durum kodunu (status code) kaydeden yerleşik bir loglama mekanizması içerir.

Log Görüntüleme Arayüzü: /logs adresine yapılan isteklerle toplanan loglar HTML formatında görüntülenebilir.

Hata Yönetimi: Ağ bağlantısı sorunları (502 Bad Gateway) ve iç sunucu hataları (500 Internal Error) için temel hata yakalama mekanizmasına sahiptir.



🛠️ Kurulum ve Çalıştırma

Gereksinimler

Bu projeyi çalıştırmak için yalnızca Python 3 ve requests kütüphanesine ihtiyacınız vardır.

Bash# Gerekli kütüphaneyi kurun

pip install requests



Çalıştırma

Projeyi başlatmak için terminalde aşağıdaki komutu çalıştırın:

Bash

python proxy.py

Sunucu varsayılan olarak http://localhost:8080 adresinde başlayacaktır.

🚀 Proxy başlatıldı: http://localhost:8080

Kullanım Örnekleri



Amaç

URLGET isteğihttp://localhost:8080/https://www.google.com

Logları Görüntülemehttp://localhost:8080/logs



💻 Kod Analizi: proxy.py

Projenin kalbi olan proxy.py dosyasındaki temel sınıflar ve metotlar aşağıda detaylandırılmıştır.



1. Global Değişkenler ve Yardımcı Fonksiyonlar

PORT = 8080: Proxy'nin dinleyeceği TCP portudur.

logs = []: Tüm log kayıtlarının string olarak tutulduğu global liste.

add_log(text): Log kaydını hem konsola yazdıran hem de logs listesine ekleyen fonksiyondur.



3. ProxyHandler Sınıfı

Bu sınıf, tüm HTTP isteklerini işlemek için http.server.BaseHTTPRequestHandler sınıfından türetilmiştir.



2.1. log_message(self, format, *args)Bu metot, BaseHTTPRequestHandler'ın varsayılan loglama işlevini override eder. Gelen tüm erişim loglarını formatlayarak add_log fonksiyonu aracılığıyla hem konsola hem de logs listesine kaydeder.

   

2.2. do_GET(self) ve do_POST(self)Gelen GET ve POST isteklerini işleyen ana giriş noktalarıdır.İstek yolu /logs ise, logları gösteren _serve_logs() metodu çağrılır.Diğer tüm istekler, proxy mantığının bulunduğu _handle_proxy() metoduna yönlendirilir.



2.3. _serve_logs(self)/logs adresine erişildiğinde çalışır.HTTP 200 OK yanıtı döndürür.logs listesindeki tüm kayıtları alarak, basit bir HTML <pre> etiketi içinde formatlar ve istemciye gönderir.



⚠️ Dikkat Edilmesi Gerekenler

Bu proje, bir eğitim aracı ve temel bir uygulama olarak tasarlanmıştır. Üretim ortamında kullanılması için daha fazla güvenlik, hata kontrolü, performans optimizasyonu (önbellekleme gibi) ve eşzamanlılık (threading/asyncio) yönetimi gereklidir.








































