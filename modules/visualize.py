import matplotlib.pyplot as plt
from wordcloud import WordCloud
import streamlit as st


def plot_filler_words(filler_freq):
    words = list(filler_freq.keys())
    counts = list(filler_freq.values())

    fig, ax = plt.subplots()
    ax.bar(words, counts)
    ax.set_title("Filler Words Frequency")
    ax.set_xlabel("Words")
    ax.set_ylabel("Count")

    st.pyplot(fig)


def plot_pauses(pauses):
    labels = ["Short", "Medium", "Long"]
    values = [pauses["short"], pauses["medium"], pauses["long"]]

    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct='%1.1f%%')
    ax.set_title("Pause Distribution")

    st.pyplot(fig)


def plot_wordcloud(common_words):
    word_dict = dict(common_words)

    wc = WordCloud(width=800, height=400, background_color="white")
    wc.generate_from_frequencies(word_dict)

    fig, ax = plt.subplots()
    ax.imshow(wc)
    ax.axis("off")
    ax.set_title("Most Used Words")

    st.pyplot(fig)


def plot_sentiment(scores):
    fig, ax = plt.subplots()
    ax.plot(scores, marker='o')
    ax.axhline(0, linestyle='--')
    ax.set_title("Sentiment Timeline")
    ax.set_xlabel("Sentence Index")
    ax.set_ylabel("Sentiment Score")

    st.pyplot(fig)


def plot_wpm_variation(wpm_list):
    fig, ax = plt.subplots()
    ax.plot(wpm_list, marker='o')
    ax.set_title("Speaking Pace Variation")
    ax.set_xlabel("Segment Index")
    ax.set_ylabel("WPM")

    st.pyplot(fig)