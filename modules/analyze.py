from transformers import pipeline
import streamlit as st
import re


# ✅ Cache model (important for Streamlit)
@st.cache_resource
def load_sentiment_model():
    return pipeline("sentiment-analysis")


sentiment_model = load_sentiment_model()


# ✅ Safe text chunking (prevents tensor errors)
def chunk_text(text, max_words=120):
    words = text.split()
    for i in range(0, len(words), max_words):
        yield " ".join(words[i:i + max_words])


def analyze_text(text):
    if not text.strip():
        return {
            "sentiment": {"label": "NEUTRAL", "score": 0},
            "filler_count": 0,
            "word_count": 0
        }

    # 🔹 Split into safe chunks
    chunks = list(chunk_text(text))

    sentiments = []
    for chunk in chunks:
        result = sentiment_model(chunk, truncation=True, max_length=512)[0]
        score = result["score"]

        if result["label"] == "NEGATIVE":
            score = -score

        sentiments.append(score)

    # 🔹 Average sentiment
    avg_score = sum(sentiments) / len(sentiments)

    sentiment = {
        "label": "POSITIVE" if avg_score > 0 else "NEGATIVE",
        "score": abs(avg_score)
    }

    # 🔹 Better filler detection (word boundaries)
    filler_words = ["um", "uh", "like", "actually", "basically"]
    filler_count = sum(
        len(re.findall(rf"\b{word}\b", text.lower()))
        for word in filler_words
    )

    # 🔹 Word count
    word_count = len(text.split())

    return {
        "sentiment": sentiment,
        "filler_count": filler_count,
        "word_count": word_count
    }


def sentiment_timeline(text):
    # 🔹 Better sentence split
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]

    scores = []
    labels = []

    for sentence in sentences:
        result = sentiment_model(
            sentence,
            truncation=True,
            max_length=512
        )[0]

        score = result["score"]

        if result["label"] == "NEGATIVE":
            score = -score

        scores.append(score)
        labels.append(result["label"])

    return scores, labels