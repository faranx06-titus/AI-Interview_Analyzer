import whisper
import torch

model = None

def load_model():
    global model
    if model is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model = whisper.load_model("base", device=device)
    return model


def transcribe_audio(file_path):
    model = load_model()

    try:
        result = model.transcribe(
            file_path,
            fp16=torch.cuda.is_available(),
            verbose=False
        )

        return {
            "text": result.get("text", ""),
            "segments": result.get("segments", [])
        }

    except Exception as e:
        print("Transcription Error:", e)
        return {"text": "", "segments": []}