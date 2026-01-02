# 🎥 AI Shorts Generator

Alat otomatis berbasis Python untuk mengubah video YouTube (Landscape) menjadi video pendek vertikal (Shorts/TikTok/Reels) lengkap dengan **Face Tracking** dan **Subtitle Otomatis**.

## 🔥 Fitur Utama

1.  **Smart Face Tracking**: Menggunakan OpenCV untuk mendeteksi wajah dan menjaga kamera tetap fokus ke pembicara, mengubah rasio 16:9 menjadi 9:16 secara halus (stabilizer).
2.  **Auto Subtitles**: Menggunakan OpenAI Whisper untuk transkrip audio ke teks dengan akurasi tinggi.
3.  **Viral Style Caption**: Auto-generate subtitle warna kuning dengan outline hitam (gaya video viral) menggunakan ImageMagick.
4.  **Optimized for Performance**: Mendukung penggunaan model Whisper `small` untuk akurasi lebih baik.

## 🛠️ Cara Install

1.  **Clone repository ini**
    git clone https://github.com/username-anda/ai-shorts-generator.git
    cd ai-shorts-generator

2.  **Buat Virtual Environment**
    python -m venv venv
    .\venv\Scripts\activate

3.  **Install Dependencies**
    pip install -r requirements.txt

4.  **Install Aplikasi Tambahan (Wajib)**
    * **ImageMagick**: Download dan install. Pastikan centang opsi "Install legacy utilities (e.g. convert)".
    * **FFmpeg**: Pastikan terinstall di sistem.

## 🚀 Cara Penggunaan

### Langkah 1: Siapkan Video
Simpan video input (misal `test_video.mp4`) di folder root project.

### Langkah 2: Jalankan Kamera Pintar (Tracking & Crop)
Edit `camera_pintar.py`, pastikan nama file input sesuai. Lalu jalankan:
python camera_pintar.py
*Output: `hasil_stabil.mp4`*

### Langkah 3: Generate Subtitle
Edit `subtitle_pro.py`, pastikan `INPUT_VIDEO` mengarah ke file hasil langkah 2 (`hasil_stabil.mp4`). Lalu jalankan:
python subtitle_pro.py
*Output Akhir: `video_final_viral.mp4`*

## ⚙️ Konfigurasi Penting
Jika script Subtitle error (ImageMagick tidak ditemukan), edit path di `subtitle_pro.py`:

change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.2-Q16\magick.exe"})

---
Dibuat dengan ❤️ menggunakan Python, OpenCV, & MoviePy.