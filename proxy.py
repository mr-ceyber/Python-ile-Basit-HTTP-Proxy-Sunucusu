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