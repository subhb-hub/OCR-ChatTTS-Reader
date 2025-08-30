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
if you want to fix a speaker, you can:
```bash
python Test_ChatTTS.py
```
over and over again to get your favorite speaker and then load it by change this in main.py:

```python
# --- 初始化 ChatTTS ---
device = "mps" if torch.mps.is_available() else "cpu"
device = "cuda" if torch.cuda.is_available() else device
print(f"Using device : {device}")
chat = ChatTTS.Chat()
chat.load(compile=False)  
rand_spk = chat.sample_random_speaker()
# if you prefer specific speaker
# rand_spk = torch.load("speaker_1.pt")
```

to this:

```python
# --- 初始化 ChatTTS ---
device = "mps" if torch.mps.is_available() else "cpu"
device = "cuda" if torch.cuda.is_available() else device
print(f"Using device : {device}")
chat = ChatTTS.Chat()
chat.load(compile=False)  
rand_spk = chat.sample_random_speaker()
# if you prefer specific speaker
rand_spk = torch.load("speaker_1.pt")
```



## Main Thanks

- **PyQt6** – [PyQt6](https://www.riverbankcomputing.com/software/pyqt/)
- **pytesseract** – [pytesseract](https://github.com/madmaze/pytesseract)
- **Pillow (PIL)** – [Pillow](https://python-pillow.org/)
- **mss** – [mss](https://github.com/BoboTiG/python-mss)
- **ChatTTS** – [ChatTTS](https://github.com/2noise/ChatTTS)
- **torch / torchaudio** – [PyTorch](https://pytorch.org/)
- **playsound** – [playsound](https://github.com/TaylorSMarks/playsound)
