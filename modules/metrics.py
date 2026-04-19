from collections import Counter
import librosa
import numpy as np
import re


def compute_metrics(result, text, file_path):

    segments = result.get("segments", [])

    # ⏱ Duration (safe)
    if segments:
        duration = segments[-1]["end"]
    else:
        duration = 1  # avoid division errors

    # 🧮 Word count
    words = text.split()
    word_count = len(words)

    # ⚡ WPM (safe)
    wpm = word_count / (duration / 60) if duration > 0 else 0

    # 🧭 Pace classification
    if wpm < 100:
        pace = "Too Slow"
    elif wpm > 160:
        pace = "Too Fast"
    else:
        pace = "Optimal"

    # ⏸ Pause detection
    pauses = []
    for i in range(1, len(segments)):
        gap = segments[i]["start"] - segments[i - 1]["end"]
        pauses.append(max(0, gap))

    short = sum(1 for p in pauses if p < 1)
    medium = sum(1 for p in pauses if 1 <= p <= 3)
    long = sum(1 for p in pauses if p > 3)

    # 🧠 Better filler detection
    filler_words = ["um", "uh", "like", "actually", "basically"]
    filler_freq = Counter(w.lower() for w in words if w.lower() in filler_words)
    filler_count = sum(filler_freq.values())

    # 🧠 Clarity score (bounded 0–100)
    clarity = 100 - (filler_count * 2 + long * 5 + abs(wpm - 130))
    clarity = max(0, min(100, clarity))

    # 🔊 Loudness (safe load)
    try:
        y, sr = librosa.load(file_path, sr=None)
        rms = librosa.feature.rms(y=y)[0]

        avg_loudness = float(np.mean(rms))
        max_loudness = float(np.max(rms))

        loudness_score = min(100, avg_loudness * 1000)
    except:
        avg_loudness, max_loudness, loudness_score = 0, 0, 0

    # 🎤 Pitch analysis (safe)
    try:
        f0 = librosa.yin(y, fmin=50, fmax=300)
        f0 = f0[~np.isnan(f0)]

        if len(f0) > 0:
            pitch_variation = float(np.std(f0))
        else:
            pitch_variation = 0
    except:
        pitch_variation = 0

    monotone = "Yes" if pitch_variation < 5 else "No"

    # 📊 Common words
    clean_words = re.findall(r'\b\w+\b', text.lower())

    stopwords = {
        "the", "is", "and", "a", "to", "of", "in", "it",
        "that", "this", "on", "for", "with", "as", "was"
    }

    filtered_words = [w for w in clean_words if w not in stopwords]
    common_words = Counter(filtered_words).most_common(10)

    return {
        "duration": round(duration, 2),
        "wpm": round(wpm, 2),
        "pace": pace,
        "pauses": {
            "short": short,
            "medium": medium,
            "long": long
        },
        "filler_freq": dict(filler_freq),
        "clarity": round(clarity, 2),

        "loudness": {
            "avg": avg_loudness,
            "max": max_loudness,
            "score": round(loudness_score, 2)
        },

        "common_words": common_words,

        "monotone": monotone,
        "pitch_variation": pitch_variation
    }


def speaking_consistency(result):
    segments = result.get("segments", [])

    wpm_list = []

    for seg in segments:
        duration = seg["end"] - seg["start"]
        words = seg["text"].split()
        word_count = len(words)

        if duration > 0:
            wpm = word_count / (duration / 60)
            wpm_list.append(wpm)

    if len(wpm_list) > 1:
        variation = float(np.std(wpm_list))
    else:
        variation = 0

    if variation < 20:
        consistency = "Stable"
    elif variation < 40:
        consistency = "Moderate"
    else:
        consistency = "Unstable"

    return wpm_list, variation, consistency