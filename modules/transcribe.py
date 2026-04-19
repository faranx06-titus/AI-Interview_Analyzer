import whisper
import torch


# ✅ Load model only once (Streamlit safe)
def load_model():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    return whisper.load_model("base", device=device)


model = load_model()


def transcribe_audio(file_path):
    try:
        result = model.transcribe(
            file_path,
            fp16=torch.cuda.is_available(),  # faster on GPU
            verbose=False
        )

        # ensure required keys exist
        return {
            "text": result.get("text", ""),
            "segments": result.get("segments", [])
        }

    except Exception as e:
        print("Transcription Error:", e)

        # return safe fallback
        return {
            "text": "",
            "segments": []
        }