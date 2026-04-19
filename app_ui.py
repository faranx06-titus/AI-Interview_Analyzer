'''import streamlit as st
import tempfile
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Custom modules
from modules.transcribe import transcribe_audio
from modules.analyze import analyze_text, sentiment_timeline
from modules.metrics import compute_metrics, speaking_consistency, pause_timeline

# Page config
st.set_page_config(page_title="AI Interview Analyzer", layout="wide")

st.title("🎤 AI Interview Analyzer")

# File upload
uploaded_file = st.file_uploader("Upload Audio", type=["wav", "mp3"])

if uploaded_file is None:
    st.warning("Please upload an audio file")
    st.stop()

# Save uploaded file
with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
    tmp.write(uploaded_file.read())
    file_path = tmp.name

# Transcription
result = transcribe_audio(file_path)
text = result["text"]

# Analysis
analysis = analyze_text(text)
metrics = compute_metrics(result, text, file_path)

scores, _ = sentiment_timeline(text)
wpm_list, variation, consistency = speaking_consistency(result)

# FIXED: extract timestamps properly
timestamps = [(seg["start"], seg["end"]) for seg in result["segments"]]
positions, pauses = pause_timeline(text, timestamps)

# ================= UI =================

col1, col2, col3 = st.columns(3)

col1.metric("Clarity", metrics["clarity"])
col2.metric("WPM", metrics["wpm"])
col3.metric("Pace", metrics["pace"])

# Sentiment Timeline
fig, ax = plt.subplots()
ax.plot(scores, marker='o')
ax.axhline(0, linestyle='--')
ax.set_title("Sentiment Timeline")
st.pyplot(fig)

# Pause Timeline
fig2, ax2 = plt.subplots()
ax2.bar(positions, pauses)
ax2.set_title("Pause Timeline")
st.pyplot(fig2)

# Speaking Consistency
fig3, ax3 = plt.subplots()
ax3.plot(wpm_list, marker='o')
ax3.set_title("Speaking Consistency")
st.pyplot(fig3)

# Wordcloud
wc = WordCloud(width=800, height=400).generate_from_frequencies(
    dict(metrics["common_words"])
)
st.image(wc.to_array())

# Transcript
st.subheader("Transcript")
st.write(text)




---------------------------------------------------------------------------


from modules.transcribe import transcribe_audio
from modules.analyze import analyze_text
from modules.metrics import compute_metrics
from modules.visualize import plot_filler_words, plot_pauses
from modules.visualize import plot_wordcloud
from modules.analyze import sentiment_timeline
from modules.visualize import plot_sentiment
from modules.metrics import speaking_consistency
from modules.visualize import plot_wpm_variation


file_path = "sample_audio/harvard.wav"

result = transcribe_audio(file_path)
text = result["text"]

analysis = analyze_text(text)
metrics = compute_metrics(result, text,file_path)

plot_wordcloud(metrics["common_words"])

scores, labels = sentiment_timeline(text)

wpm_list, variation, consistency = speaking_consistency(result)

plot_wpm_variation(wpm_list)


plot_sentiment(scores)

print("\n--- TRANSCRIPT ---\n", text)
print("\n--- ANALYSIS ---\n", analysis)
print("\n--- METRICS ---\n", metrics)
print("\n--- LOUDNESS ---\n", metrics["loudness"])
print("\n--- MOST REPEATED WORDS ---\n", metrics["common_words"])
print("\n--- SENTIMENT TIMELINE ---")
print(scores)
print("\n--- MONOTONE ---")
print("Monotone:", metrics["monotone"])
print("Pitch Variation:", metrics["pitch_variation"])

print("\n--- SPEAKING CONSISTENCY ---")
print("WPM per segment:", wpm_list)
print("Variation:", variation)
print("Consistency:", consistency)



plot_filler_words(metrics["filler_freq"])
plot_pauses(metrics["pauses"])'''