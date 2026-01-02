import cv2
from moviepy.editor import VideoFileClip
import os

# --- KONFIGURASI ---
INPUT_VIDEO = "test_video.mp4"       # Pastikan nama file ini sesuai video baru Anda
OUTPUT_VIDEO = "hasil_stabil_v3.mp4"

# Load detektor wajah
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# --- LOGIKA STABILIZER ---
# Kita butuh variabel global untuk menyimpan posisi terakhir
last_center_x = None

def get_face_center_smooth(frame):
    global last_center_x
    
    # 1. Deteksi Wajah
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    
    current_center = None
    frame_h, frame_w, _ = frame.shape
    default_center = frame_w // 2

    # 2. Jika Wajah Ketemu
    if len(faces) > 0:
        # Ambil wajah terbesar
        (x, y, w, h) = sorted(faces, key=lambda f: f[2]*f[3], reverse=True)[0]
        current_center = x + (w // 2)
    
    # 3. Logika "Ingatan" (Stabilizer)
    if last_center_x is None:
        # Ini frame pertama
        if current_center is not None:
            last_center_x = current_center
        else:
            last_center_x = default_center
        return last_center_x
    
    if current_center is not None:
        # --- TEKNIK SMOOTHING (Exponential Moving Average) ---
        # Rumus: Posisi Baru = (10% Posisi Baru) + (90% Posisi Lama)
        # Ini membuat kamera bergerak pelan (gliding), tidak loncat kaget.
        alpha = 0.4 
        smooth_x = int((alpha * current_center) + ((1 - alpha) * last_center_x))
        last_center_x = smooth_x
    else:
        # Jika wajah HILANG, jangan panik!
        # Tetap pakai posisi terakhir (Jangan reset ke tengah)
        pass 
        
    return last_center_x

def process_video_frames(get_frame, t):
    frame = get_frame(t)
    frame_h, frame_w, _ = frame.shape

    # Target 9:16
    # Trik matematika: Bagi 2 lalu kali 2 untuk memastikan angka selalu genap
    target_width = int(frame_h * 9 / 16) // 2 * 2
    
    # Ambil posisi tengah yang sudah distabilkan
    center_x = get_face_center_smooth(frame)

    # Hitung crop
    x1 = center_x - (target_width // 2)
    
    # Batas aman kiri/kanan
    if x1 < 0: x1 = 0
    if x1 + target_width > frame_w: x1 = frame_w - target_width

    return frame[:, x1:x1+target_width]

# --- EKSEKUSI ---
if not os.path.exists(INPUT_VIDEO):
    print(f"❌ Error: File '{INPUT_VIDEO}' tidak ada. Download video dulu!")
else:
    print("🎥 Sedang memproses dengan STABILIZER MODE...")
    print("   (Gerakan kamera akan lebih halus & tidak ngeblink saat wajah hilang)")

    try:
        clip = VideoFileClip(INPUT_VIDEO)
        # Trik: Kita harus pakai loop manual sedikit agar variabel global bekerja per frame
        # Tapi cara paling aman di MoviePy adalah membiarkannya berjalan seadanya
        cropped_clip = clip.fl(process_video_frames)
        
        cropped_clip.write_videofile(OUTPUT_VIDEO, codec='libx264', audio_codec='aac')
        print(f"\n✅ SUKSES! Cek file: {OUTPUT_VIDEO}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")