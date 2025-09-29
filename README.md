# 📂 Fat Files Compressor

Fat Files Compressor is a Python-based command-line tool for compressing various file types, including videos, audio, images, and PDFs. It uses popular tools like `ffmpeg`, `pngquant`, and `ghostscript` to reduce file sizes while maintaining configurable quality levels. Ideal for users who need to save disk space or optimize files for sharing.

![](https://github.com/fast-archer/Fat-Files-Compressor/blob/main/Screenshot%20From%202025-09-29%2007-28-52%20(Edit).png)

## 🚀 Features
- **Supported Formats**:
  - **Videos**: `.mp4`, `.mkv`, `.avi`, `.mov`
  - **Audio**: `.mp3`, `.aac`, `.wav`, `.flac`
  - **Images**: `.jpg`, `.jpeg`, `.png`, `.webp`, `.gif`
  - **Documents**: `.pdf`
- **Quality Presets**:
  - Fast and strong compression (lowest quality)
  - Balanced (recommended)
  - High quality (less compression)
- Automatic dependency checking with an option to install missing tools.
- Progress bar for batch compression using `tqdm`.
- Detailed output showing original size, compressed size, savings, and processing time.
- Logs errors to `compression.log` for debugging.

## 📦 Installation

### Prerequisites
- Python 3.6 or higher
- Linux environment (Arch Linux recommended, but works on other distributions)

### Dependencies
The script requires the following tools:
- `ffmpeg`: For video, audio, JPEG, WebP, and GIF compression.
- `pngquant`: For PNG compression.
- `ghostscript`: For PDF compression.

Install them on Arch Linux:
```bash
sudo pacman -S ffmpeg pngquant ghostscript
```

### 📥 Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/fast-archer/fat-files-compressor.git
   cd fat-files-compressor
   ```
2. Ensure the script is executable:
   ```bash
   chmod +x fatfiles.py
   ```

## 👨🏻‍💻 Usage
Run the script from the command line:
```bash
./fatfiles.py
```

1. **Enter the folder path** containing files to compress.
2. Choose to compress **all files** (`a`) or a specific file by **number** (`n`).
3. Select a quality preset (1–3):
   - `1`: Fast and strong compression (lowest quality)
   - `2`: Balanced (recommended)
   - `3`: High quality (less compression)
4. Compressed files are saved in a `compressed` subfolder.

### 💡 Example
```bash
$ ./fatfiles.py
Fat Files Compressor v1.0
Enter folder path: /home/user/Pictures/sw

Folder contents:
1. example.mp4
2. image.png
3. document.pdf

Compress (a) all files or (n) file number? a

Choose quality level:
1. Fast and strong compression (lowest quality)
2. Balanced (recommended)
3. High quality (less compression)
Your choice (1-3): 2

Compressing files: 100%|██████████████████████████| 3/3 [00:15<00:00,  5.00s/it]
Done! All compressed files are in the 'compressed' folder.
```

## 📝 Notes
- Large files (>100 MB) trigger a confirmation prompt to avoid long processing times.
- If a dependency is missing, the script prompts to install it via `pacman`.
- WebP compression uses `ffmpeg` with `libwebp` support. Ensure your `ffmpeg` is compiled with WebP support (`ffmpeg -h encoder=libwebp`).
- GIF compression may be slow for large files due to palette optimization.

## 🗣️ Contributing
Contributions are welcome! Feel free to open issues or submit pull requests for new features, bug fixes, or additional format support.

## 🌐 Contact

For discussions or suggestions, reach out:
- **Email**: epidermis_essential@proton.me
- **Inktree**: [here](https://linktr.ee/fastarcher)

## 📜 License

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)

## 🤝 Acknowledgments
- Built with `ffmpeg`, `pngquant`, and `ghostscript`.
- Inspired by the need to efficiently compress media and documents.
