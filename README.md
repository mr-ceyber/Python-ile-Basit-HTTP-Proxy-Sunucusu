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





 # proxy.py
import http.server
import socketserver
import requests
from urllib.parse import urlparse, unquote
PORT = 8080  # Proxy'nin çalışacağı por
logs = []
def add_log(text):
    print(text)
    logs.append(text)
class ProxyHandler(http.server.BaseHTTPRequestHandler):
    # Basit log formatı
    def log_message(self, format, *args):
        msg = f"{self.client_address[0]} - {self.log_date_time_string()} - {format % args}"
        add_log(msg)   # ← log kaydediliyor
    def do_GET(self):
        if self.path == "/logs":      # önce logs kontrolü
            return self._serve_logs()
        self._handle_proxy("GET")
    def do_POST(self):
        self._handle_proxy("POST")
    def _serve_logs(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        html = "<html><body><h2>Proxy Logları</h2><pre>"
        html += "\n".join(logs)
        html += "</pre></body></html>"
        self.wfile.write(html.encode("utf-8"))
    def _handle_proxy(self, method):
        # Tarayıcı favicon isteğini sessizce karşıla
        if self.path == "/favicon.ico":
            self.send_response(204)  # No Content
            self.end_headers()
            return
        raw = self.path[1:]
        raw = unquote(raw)
        parsed = urlparse(raw)
        if parsed.scheme not in ("http", "https") or not parsed.netloc:
            self.send_error(400, "Geçersiz URL. Format: /http://example.com veya /https://example.com")
            return
        body = None
        if method == "POST":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length) if length > 0 else None
        forward_headers = {}
        for k, v in self.headers.items():
            lk = k.lower()
            if lk in ("host", "connection", "proxy-connection", "upgrade",
                      "keep-alive", "transfer-encoding"):
                continue
            forward_headers[k] = v
        forward_headers.setdefault("User-Agent", "MiniProxy/1.1")
        try:
            resp = requests.request(
                method=method,
                url=raw,
                headers=forward_headers,
                data=body,
                allow_redirects=False,
                timeout=15
            )
            self.send_response(resp.status_code)

            for k, v in resp.headers.items():
                lk = k.lower()
                if lk in ("content-encoding", "transfer-encoding", "connection"):
                    continue
                self.send_header(k, v)
            self.end_headers()
            self.wfile.write(resp.content)
            self.log_message("[%s] %s -> %s", method, raw, resp.status_code)
        except requests.exceptions.RequestException as e:
            self.send_error(502, f"Hedefe ulaşılamadı: {e}")
            self.log_message("[ERR] %s", str(e))
        except Exception as e:
            self.send_error(500, f"Proxy Hatası: {e}")
            self.log_message("[ERR] %s", str(e))
def run():
    with socketserver.TCPServer(("", PORT), ProxyHandler) as httpd:
        print(f"🚀 Proxy başlatıldı: http://localhost:{PORT}")
        httpd.serve_forever()
if __name__ == "__main__":
    run()              














































