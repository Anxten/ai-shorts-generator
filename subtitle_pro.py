import whisper
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import os
# Import konfigurasi moviepy
from moviepy.config import change_settings

# --- KONFIGURASI IMAGEMAGICK (WAJIB) ---
# Ini baris paling penting supaya error "WinError 2" hilang
change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.2-Q16\magick.exe"})

# --- KONFIGURASI PROYEK ---
INPUT_VIDEO = "hasil_stabil.mp4"   # Pastikan file ini ada di folder
OUTPUT_VIDEO = "video_final_viral.mp4"
MODEL_TYPE = "small"                  # Model AI Whisper

def split_text(text, max_chars=20):
    """
    Memotong kalimat panjang supaya muat di layar HP (Portrait)
    """
    words = text.split()
    lines = []
    current_line = []
    
    for word in words:
        if len(" ".join(current_line + [word])) <= max_chars:
            current_line.append(word)
        else:
            lines.append(" ".join(current_line))
            current_line = [word]
    lines.append(" ".join(current_line))
    return "\n".join(lines)

def process_subtitles():
    # Cek file input
    if not os.path.exists(INPUT_VIDEO):
        print(f"❌ Error: File '{INPUT_VIDEO}' tidak ditemukan!")
        print("   Pastikan Anda sudah menjalankan script camera_pintar_v3.py sebelumnya.")
        return

    print("🎧 1. Sedang mendengarkan audio (Whisper AI)...")
    print("   (Proses ini butuh waktu tergantung durasi video & kecepatan internet)")
    
    # Load model & Transkrip
    model = whisper.load_model(MODEL_TYPE)
    result = model.transcribe(INPUT_VIDEO, fp16=False)
    
    print("📝 2. Membuat subtitle overlay...")
    video = VideoFileClip(INPUT_VIDEO)
    subtitle_clips = []
    
    # Loop setiap kalimat yang didengar AI
    for segment in result['segments']:
        start_time = segment['start']
        end_time = segment['end']
        text = segment['text'].strip()
        
        # Rapikan teks
        wrapped_text = split_text(text)
        
        # --- DESAIN SUBTITLE TIKTOK ---
        txt_clip = (TextClip(wrapped_text, 
                             fontsize=50, 
                             font='Arial',       # Ganti font di sini jika mau
                             color='yellow',     # Warna teks
                             stroke_color='black', 
                             stroke_width=2,     # Ketebalan garis pinggir
                             method='caption',
                             size=(video.w * 0.9, None), 
                             align='center')
                    .set_position(('center', 0.75), relative=True) # Posisi agak bawah
                    .set_duration(end_time - start_time)
                    .set_start(start_time))
        
        subtitle_clips.append(txt_clip)

    print(f"🎬 3. Menggabungkan {len(subtitle_clips)} subtitle ke video...")
    
    # Tumpuk video asli dengan subtitle
    final_video = CompositeVideoClip([video] + subtitle_clips)
    
    print("💾 4. Sedang menyimpan video final (Rendering)...")
    # Tambahkan parameter 'ffmpeg_params' supaya Windows & HP bisa baca
    final_video.write_videofile(OUTPUT_VIDEO, 
                            codec='libx264', 
                            audio_codec='aac', 
                            ffmpeg_params=['-pix_fmt', 'yuv420p'])
    
    print(f"\n✅ SELESAI! Video siap upload: {OUTPUT_VIDEO}")

if __name__ == "__main__":
    process_subtitles()