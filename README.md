# scuba-cat
İki el algılandığında özel GIF pencerelerini tetikler.
## 📂 Kurulum ve Çalıştırma
1. Bu depoyu klonlayın veya dosyaları indirin.
2. Kod içerisindeki `GIF_PATH_1` ve `GIF_PATH_2` değişkenlerini kendi GIF dosyalarınızın yoluyla güncelleyin:
   ```python
   GIF_PATH_1 = "dosya_yolu/gif_adi.gif"
Uygulamayı çalıştırın:

Bash
python main.py
Şöyle tek parça, kopyalayıp direkt `README.md` olarak kaydedebileceğin profesyonel bir taslak hazırladım:
Markdown
# Interactive Screen Overlay - Hand Gesture GIF Control 👐✨

Bu proje, **MediaPipe** ve **OpenCV** kullanarak gerçek zamanlı el tespiti yapan ve el sayısına göre dinamik pencereler tetikleyen interaktif bir Python uygulamasıdır.

## 🚀 Proje Mantığı
Uygulama, bilgisayar kamerasından gelen görüntüyü anlık olarak işler:
- **Tek El Algılandığında:** Sadece kamera penceresi görünür ve el takibi yapılır.
- **İki El Algılandığında:** Önceden belirlenen konumlarda iki farklı GIF penceresi açılır ve animasyon başlar.
- **Eller Çekildiğinde:** GIF pencereleri otomatik olarak kapanır, kaynak tüketimi minimize edilir.

## 🛠️ Gereksinimler
Projenin çalışması için bilgisayarınızda Python yüklü olmalı ve aşağıdaki kütüphaneleri kurmalısınız:

```bash
pip install opencv-python mediapipe Pillow numpy
📂 Kurulum ve Çalıştırma
Bu depoyu klonlayın veya dosyaları indirin.

Kod içerisindeki GIF_PATH_1 ve GIF_PATH_2 değişkenlerini kendi GIF dosyalarınızın yoluyla güncelleyin:

Python
GIF_PATH_1 = "dosya_yolu/gif_adi.gif"
Uygulamayı çalıştırın:

Bash
python main.py
🎮 Kontroller
İki El Göster: GIF pencerelerini açar.

Elleri Çek: GIF pencerelerini kapatır.

'q' Tuşu: Uygulamadan güvenli bir şekilde çıkış yapar.

🧠 Kullanılan Teknolojiler
OpenCV: Görüntü yakalama ve pencere yönetimi.

MediaPipe: Yüksek doğruluklu el ayası ve parmak takibi.

Pillow (PIL): GIF karelerinin parçalanması ve boyutlandırılması.

NumPy: Matris tabanlı görüntü işleme.

Geliştirici: Elif Çalışkaner
