import ChatTTS
import torch
import torchaudio
import numpy as np

chat = ChatTTS.Chat()
chat.load(compile=False)

#choose one for them
for i in range(5):
    spk = chat.sample_random_speaker()
    wavs = chat.infer(
        ["你好，我是测试语音"],
        params_infer_code=ChatTTS.Chat.InferCodeParams(spk_emb=spk),
    )
    wav_tensor = torch.from_numpy(wavs[0]).unsqueeze(0)
    torchaudio.save(f"speaker_{i}.wav", wav_tensor, 24000)
    print(f"✅ Saved speaker_{i}.wav")
    torch.save(spk, f"speaker_{i}.pt")

