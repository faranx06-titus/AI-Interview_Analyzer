from transformers import pipeline
import streamlit as st


@st.cache_resource
def load_generator():
    return pipeline("text2text-generation", model="google/flan-t5-base")


generator = load_generator()


def generate_feedback(text, analysis):

    if not text.strip():
        return "No answer detected."

    prompt = f"""
You are an AI interview evaluator.

Analyze this response:
{text}

Metrics:
- Sentiment: {analysis['sentiment']['label']}
- Filler words: {analysis['filler_count']}
- Word count: {analysis['word_count']}

Give output in this format:

Score: (0-100)

Strengths:
- ...

Weaknesses:
- ...

Suggestions:
- ...
"""

    result = generator(
        prompt,
        max_length=300,
        do_sample=False
    )

    return result[0]["generated_text"]