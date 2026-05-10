import os
import shutil
import yt_dlp


def find_ffmpeg_location():
    # If ffmpeg and ffprobe are on PATH, no need to provide location
    if shutil.which("ffmpeg") and shutil.which("ffprobe"):
        return None

    # Allow user to specify FFMPEG_LOCATION or FFMPEG_HOME env var
    env_loc = os.environ.get("FFMPEG_LOCATION") or os.environ.get("FFMPEG_HOME")
    if env_loc:
        # On Windows, users often point to the bin folder; verify executables exist
        ffmpeg_exe = os.path.join(env_loc, "ffmpeg.exe") if os.name == 'nt' else os.path.join(env_loc, "ffmpeg")
        ffprobe_exe = os.path.join(env_loc, "ffprobe.exe") if os.name == 'nt' else os.path.join(env_loc, "ffprobe")
        if os.path.exists(ffmpeg_exe) and os.path.exists(ffprobe_exe):
            return env_loc

    return None


def download_audio(url, output_dir=None):
    """Download audio from a YouTube URL and return the final filepath.

    If `output_dir` is provided, files are written there.
    Returns the path to the downloaded mp3 file on success, or None on failure.
    """
    ffmpeg_location = find_ffmpeg_location()

    # Prepare output template
    outtmpl = '%(title)s.%(ext)s'
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        outtmpl = os.path.join(output_dir, outtmpl)

    ydl_opts = {
        'format': 'bestaudio/best',  # Lấy chất lượng âm thanh tốt nhất
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',   # Chuyển sang định dạng mp3
            'preferredquality': '192', # Chất lượng 192kbps
        }],
        'outtmpl': outtmpl,
        'quiet': True,
        'no_warnings': True,
    }

    if ffmpeg_location:
        ydl_opts['ffmpeg_location'] = ffmpeg_location

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            print("Đang bắt đầu tải...")
            info = ydl.extract_info(url, download=True)
            # prepare_filename gives pre-postprocessor filename; since we convert to mp3,
            # replace extension with .mp3
            prepared = ydl.prepare_filename(info)
            final_path = os.path.splitext(prepared)[0] + '.mp3'
            print("Tải thành công:", final_path)
            return final_path
        except Exception as e:
            print(f"Có lỗi xảy ra: {e}")
            err = str(e).lower()
            if 'ffmpeg' in err or 'ffprobe' in err:
                print("Không tìm thấy ffmpeg/ffprobe. Cài đặt ffmpeg và đảm bảo 'ffmpeg' và 'ffprobe' có thể chạy từ PATH, hoặc đặt biến môi trường FFMPEG_LOCATION tới thư mục chứa chúng.")
            return None


__all__ = ['find_ffmpeg_location', 'download_audio']
