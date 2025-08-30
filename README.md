# OCR-ChatTTS-Reader

A desktop application based on Python that can select a screen area, perform real-time OCR text recognition, and read aloud with ChatTTS. It supports both Chinese and English recognition and is compatible with GPU acceleration (MPS) on macOS M series chips. 
---

## Features and Functions 
- Real-time OCR for selected screen areas
- Text recognition for both Chinese and English (`chi_sim+eng`)
- ChatTTS text-to-speech synthesis, with the option to fix a preferred speaker
- Monitor text changes and automatically read new content
- Supports macOS M1/M2/M3/M4 GPU (MPS) acceleration 
---

## Installation Method 
```bash
git clone https://github.com/yourname/OCR-ChatTTS-Reader.git
cd OCR-ChatTTS-Reader
conda create -n ocr python=3.10 conda activate ocr
pip install -r requirements.txt
```

## Run
```bash
python main.py
```
