## 🔍 Temel Öğrenim Noktaları 

### 1. Eğitsel Amaç ve Güvenlik ⚠️

* Bu proje, bir **eğitim aracı** olarak tasarlanmıştır. Gerçek bir **üretim ortamında (production)** veya hassas verilerin geçtiği yerlerde **kesinlikle kullanılmamalıdır.**
* Üretim seviyesinde bir proxy sunucusu için **eşzamanlılık (concurrency)**, önbellekleme (caching) ve gelişmiş güvenlik mekanizmalarına ihtiyaç vardır.

---

### 2. Vekil Sunucu (Proxy) Mantığı

* **Çift Yönlü İletişim:** Proxy, **istemci** (tarayıcınız) ile **hedef sunucu** arasındaki bir aracıdır. İstemciden isteği alır, hedefe iletir, hedeften yanıtı alır ve istemciye geri iletir.
* **Ayrı Bağlantılar:** İstemci, proxy sunucusu ile ayrı bir bağlantı kurar. Proxy sunucusu ise hedefe ayrı bir bağlantı kurar. **İki bağlantı birbirinden bağımsızdır.**

---

### 3. Koddaki Kritik Noktalar

#### A. Başlık (Header) Filtreleme
* En kritik adım, **`HEADERS_TO_FILTER`** listesidir. Proxy işlemi sırasında **`Host`**, **`Connection`**, **`Transfer-Encoding`** gibi başlıkların temizlenmesi veya güncellenmesi gerekir.
* Bu başlıklar, istemci ile proxy arasındaki bağlantıya özeldir ve hedefe olduğu gibi gönderilirse **ağ hatalarına** veya **yanlış yönlendirmelere** neden olur.

#### B. URL Yönlendirme
* Bu projedeki basit proxy'de, hedef URL'yi istemcinin isteğinin **yol (path)** kısmında belirtmesi (`http://localhost:8080/https://google.com`) eğitici bir yaklaşımdır.
* Geleneksel proxy'lerde ise istemci, doğrudan hedef URL'yi gönderir ve proxy sunucusu bir konfigürasyon dosyasına ihtiyaç duymaz.

#### C. Hata Yönetimi
* **502 Bad Gateway:** Proxy'nin hedef sunucuya **bağlanamadığı** (ağ hatası) durumlarda döndürdüğü en yaygın koddur.
* **500 Internal Error:** Proxy sunucusunun **kendi kodunda** bir mantık hatasıyla karşılaştığı durumlarda döndürdüğü genel hatadır.


























