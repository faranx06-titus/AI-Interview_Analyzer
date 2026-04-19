import streamlit as st
import tempfile

from modules.transcribe import transcribe_audio
from modules.analyze import analyze_text, sentiment_timeline
from modules.metrics import compute_metrics, speaking_consistency
from modules.visualize import (
    plot_filler_words,
    plot_pauses,
    plot_wordcloud,
    plot_sentiment,
    plot_wpm_variation
)

# ================= PAGE CONFIG =================
st.set_page_config(page_title="AI Interview Analyzer", layout="wide")

# ================= ADVANCED UI CSS =================
st.markdown("""
<style>

 🌈 Animated Gradient Background */
body {
    background: linear-gradient(-45deg, #0f172a, #1e293b, #111827, #020617);
    background-size: 400% 400%;
    animation: gradient 12s ease infinite;
    color: white;
}

@keyframes gradient {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

/* ✨ Glassmorphism Cards */
.metric-box {
    padding: 20px;
    border-radius: 16px;
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    text-align: center;
    color: white;
    border: 1px solid rgba(255,255,255,0.1);
    transition: transform 0.2s ease;
}
.metric-box:hover {
    transform: scale(1.05);
}

/* 🎬 Fade Animation */
.fade-in {
    animation: fadeIn 1s ease-in;
}
@keyframes fadeIn {
    from {opacity: 0; transform: translateY(10px);}
    to {opacity: 1; transform: translateY(0);}
}

/* 🎯 Buttons Hover */
button {
    transition: all 0.3s ease !important;
}
button:hover {
    transform: scale(1.05);
    background-color: #2563eb !important;
}

</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.title("🎤 AI Interview Analyzer")
st.markdown("### 🎯 Practice. Analyze. Improve your interview performance instantly.")

# ================= SIDEBAR =================
with st.sidebar:
    st.title("⚙️ Dashboard")
    st.info("Upload audio to analyze your speaking performance")

    st.markdown("### 📌 Features")
    st.write("✔ Speech-to-Text")
    st.write("✔ Sentiment Analysis")
    st.write("✔ Voice Metrics")
    st.write("✔ Speaking Consistency")

# ================= UPLOAD =================
uploaded_file = st.file_uploader("📤 Upload Audio", type=["wav", "mp3"])

if uploaded_file is None:
    st.info("Upload an audio file to begin analysis")
    st.stop()

st.audio(uploaded_file, format="audio/wav")

# ================= SAVE TEMP =================
with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
    tmp.write(uploaded_file.read())
    file_path = tmp.name

# ================= PROCESS =================
@st.cache_data
def process_audio(file_path):
    result = transcribe_audio(file_path)
    text = result["text"]

    analysis = analyze_text(text)
    metrics = compute_metrics(result, text, file_path)

    scores, labels = sentiment_timeline(text)
    wpm_list, variation, consistency = speaking_consistency(result)

    return result, text, analysis, metrics, scores, wpm_list, consistency

with st.spinner("🔍 Analyzing your audio..."):
    result, text, analysis, metrics, scores, wpm_list, consistency = process_audio(file_path)

if not text.strip():
    st.error("❌ Transcription failed. Try clearer audio.")
    st.stop()

# ================= SCORE =================
score = int(metrics["clarity"])

if score > 75:
    color = "green"
elif score > 50:
    color = "orange"
else:
    color = "red"

st.markdown(f"## 🏆 Overall Score: <span style='color:{color}'>{score}/100</span>", unsafe_allow_html=True)

st.progress(score)

# ================= METRICS =================
st.markdown("<div class='fade-in'>", unsafe_allow_html=True)
st.subheader("📊 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.markdown(f"<div class='metric-box'>🎯<br><b>{metrics['clarity']}</b><br>Clarity</div>", unsafe_allow_html=True)
col2.markdown(f"<div class='metric-box'>⚡<br><b>{metrics['wpm']}</b><br>WPM</div>", unsafe_allow_html=True)
col3.markdown(f"<div class='metric-box'>🧭<br><b>{metrics['pace']}</b><br>Pace</div>", unsafe_allow_html=True)
col4.markdown(f"<div class='metric-box'>🎤<br><b>{metrics['monotone']}</b><br>Monotone</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# ================= VISUALS =================
st.subheader("📈 Visual Insights")

with st.expander("☁️ Word Cloud"):
    plot_wordcloud(metrics["common_words"])

with st.expander("😊 Sentiment Timeline"):
    plot_sentiment(scores)

with st.expander("🗣️ Speaking Consistency"):
    plot_wpm_variation(wpm_list)

with st.expander("🧠 Filler Words"):
    plot_filler_words(metrics["filler_freq"])

with st.expander("⏸️ Pauses"):
    plot_pauses(metrics["pauses"])

st.divider()

# ================= TRANSCRIPT =================
st.subheader("📜 Transcript")

st.markdown(f"""
<div style="background: rgba(255,255,255,0.05); padding:15px; border-radius:10px;">
{text}
</div>
""", unsafe_allow_html=True)

st.divider()

# ================= TABS =================
st.subheader("📊 Detailed Analysis")

tab1, tab2, tab3 = st.tabs(["🧠 Analysis", "🔊 Voice", "📈 Breakdown"])

with tab1:
    st.metric("Word Count", analysis["word_count"])
    st.metric("Filler Count", analysis["filler_count"])
    st.write("Sentiment:", analysis["sentiment"])

with tab2:
    st.metric("Avg Loudness", round(metrics["loudness"]["avg"], 4))
    st.metric("Max Loudness", round(metrics["loudness"]["max"], 4))
    st.metric("Loudness Score", metrics["loudness"]["score"])

    st.write("Pitch Variation:", round(metrics["pitch_variation"], 2))
    st.write("Monotone:", metrics["monotone"])

with tab3:
    st.write("Consistency:", consistency)
    st.line_chart(wpm_list)
    st.write("Common Words:", metrics["common_words"])
    st.write("Sentiment Scores:", scores)