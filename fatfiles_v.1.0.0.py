#!/usr/bin/env python3
import os
import subprocess
import shutil
from tqdm import tqdm
import logging
import time

# Настройка логирования
logging.basicConfig(filename='compression.log', level=logging.ERROR, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Пресеты качества
QUALITY_PRESETS = {
    "1": {"desc": "Fast and strong compression (lowest quality)", "video": ["-crf", "32"], "audio": ["-b:a", "96k"], "image": 40, "webp": 50, "gif": 64},
    "2": {"desc": "Balanced (recommended)", "video": ["-crf", "28"], "audio": ["-b:a", "128k"], "image": 30, "webp": 75, "gif": 128},
    "3": {"desc": "High quality (less compression)", "video": ["-crf", "23"], "audio": ["-b:a", "192k"], "image": 15, "webp": 90, "gif": 256},
}

def check_and_install_dependencies():
    dependencies = [
        ("ffmpeg", "ffmpeg", "Error: ffmpeg is not installed! Required for video, audio, JPEG, WebP, and GIF compression."),
        ("pngquant", "pngquant", "Error: pngquant is not installed! Required for PNG compression."),
        ("gs", "ghostscript", "Warning: Ghostscript (gs) is not installed! PDF compression will be skipped.")
    ]
    
    for cmd, pkg, msg in dependencies:
        if not shutil.which(cmd):
            print(msg)
            if input("Attempt to install {}? (y/n): ".format(pkg)).strip().lower() == 'y':
                try:
                    subprocess.run(["sudo", "pacman", "-S", pkg], check=True)
                    print(f"{pkg} installed successfully.")
                except subprocess.CalledProcessError:
                    print(f"Failed to install {pkg}. Please install it manually.")
                    if cmd == "ffmpeg" or cmd == "pngquant":
                        exit(1)
    
    # Проверка поддержки WebP в ffmpeg
    try:
        result = subprocess.run(["ffmpeg", "-h", "encoder=libwebp"], capture_output=True, text=True)
        if "libwebp" not in result.stdout:
            print("Warning: ffmpeg does not support libwebp! WebP compression will be skipped.")
    except subprocess.CalledProcessError:
        print("Error: ffmpeg check failed! WebP compression will be skipped.")

def get_file_size(file_path):
    return os.path.getsize(file_path) / (1024 * 1024)  # Размер в МБ

def compress_file(input_file, output_file, quality):
    ext = os.path.splitext(input_file)[1].lower()
    input_size = get_file_size(input_file)
    start_time = time.time()

    # Предупреждение для больших файлов
    if input_size > 100:
        print(f"Warning: {input_file} is {input_size:.2f} MB. Compression may take time.")
        if input("Continue? (y/n): ").strip().lower() != 'y':
            print(f"Skipping {input_file}")
            return False

    if ext in [".mp4", ".mkv", ".avi", ".mov"]:
        cmd = ["ffmpeg", "-i", input_file, "-vcodec", "libx264", *quality["video"], "-preset", "fast", output_file]
    elif ext in [".mp3", ".aac", ".wav", ".flac"]:
        cmd = ["ffmpeg", "-i", input_file, *quality["audio"], output_file]
    elif ext == ".png":
        cmd = ["pngquant", "--quality", f"{quality['image']}-80", "--output", output_file, "--force", input_file]
    elif ext in [".jpg", ".jpeg"]:
        cmd = ["ffmpeg", "-i", input_file, "-q:v", str(quality["image"]), "-update", "1", output_file]
    elif ext == ".pdf":
        if not shutil.which("gs"):
            print(f"Skipping {input_file}: Ghostscript not installed for PDF compression")
            return False
        pdf_preset = {1: "ebook", 2: "printer", 3: "screen"}.get(int(quality["preset_id"]), "ebook")
        cmd = ["gs", "-sDEVICE=pdfwrite", f"-dPDFSETTINGS=/{pdf_preset}", "-dNOPAUSE", "-dQUIET", "-dBATCH", "-sOutputFile=" + output_file, input_file]
    elif ext == ".webp":
        try:
            subprocess.run(["ffmpeg", "-h", "encoder=libwebp"], check=True, capture_output=True, text=True)
            cmd = ["ffmpeg", "-i", input_file, "-c:v", "libwebp", "-quality", str(quality["webp"]), "-y", output_file]
        except subprocess.CalledProcessError:
            print(f"Skipping {input_file}: ffmpeg does not support libwebp")
            return False
    elif ext == ".gif":
        cmd = ["ffmpeg", "-i", input_file, "-vf", f"palettegen=max_colors={quality['gif']}:stats_mode=full", "palette.png", "-y"]
        subprocess.run(cmd, check=True, stderr=subprocess.PIPE, text=True)
        cmd = ["ffmpeg", "-i", input_file, "-i", "palette.png", "-lavfi", f"paletteuse=dither=bayer:bayer_scale=3", "-y", output_file]
    else:
        print(f"Skipping {input_file}, unsupported file type")
        return False

    print(f"Compressing: {input_file} → {output_file}")
    try:
        result = subprocess.run(cmd, check=True, timeout=120, stderr=subprocess.PIPE, text=True)
        output_size = get_file_size(output_file) if os.path.exists(output_file) else 0
        elapsed_time = time.time() - start_time
        print(f"Size: {input_size:.2f} MB → {output_size:.2f} MB (Saved: {input_size - output_size:.2f} MB, Time: {elapsed_time:.2f}s)")
        if ext == ".gif" and os.path.exists("palette.png"):
            os.remove("palette.png")  # Удаляем временную палитру
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error compressing {input_file}: {e.stderr}")
        logging.error(f"Failed to compress {input_file}: {e.stderr}")
        return False
    except subprocess.TimeoutExpired:
        print(f"Timeout while compressing {input_file}")
        logging.error(f"Timeout while compressing {input_file}")
        return False

def main():
    print("Fat Files Compressor v1.0")
    check_and_install_dependencies()

    folder = input("Enter folder path: ").strip()
    if not os.path.isdir(folder):
        print("That folder doesn't exist!")
        return

    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    if not files:
        print("The folder is empty!")
        return

    print("\nFolder contents:")
    for i, f in enumerate(files, 1):
        print(f"{i}. {f}")

    choice = input("\nCompress (a) all files or (n) file number? ").strip()

    print("\nChoose quality level:")
    for k, v in QUALITY_PRESETS.items():
        print(f"{k}. {v['desc']}")
    q_choice = input("Your choice (1-3): ").strip()
    selected_quality = QUALITY_PRESETS.get(q_choice, QUALITY_PRESETS["2"])
    selected_quality["preset_id"] = q_choice

    compressed_folder = os.path.join(folder, "compressed")
    os.makedirs(compressed_folder, exist_ok=True)

    if choice.lower() == "a":
        for f in tqdm(files, desc="Compressing files"):
            input_path = os.path.join(folder, f)
            output_path = os.path.join(compressed_folder, f)
            compress_file(input_path, output_path, selected_quality)
    elif choice.isdigit():
        idx = int(choice) - 1
        if idx < 0 or idx >= len(files):
            print("Invalid file number.")
            return
        input_path = os.path.join(folder, files[idx])
        output_path = os.path.join(compressed_folder, files[idx])
        compress_file(input_path, output_path, selected_quality)

    print("\nDone! All compressed files are in the 'compressed' folder.")

if __name__ == "__main__":
    main()
