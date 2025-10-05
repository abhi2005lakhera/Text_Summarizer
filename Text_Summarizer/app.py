# app.py
import os
import streamlit as st
from transformers import pipeline

# --- Fix: Set base directory to script's folder ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SUMMARIES_DIR = os.path.join(BASE_DIR, "summaries")

# --- Ensure summaries folder exists ---
if not os.path.exists(SUMMARIES_DIR):
    os.makedirs(SUMMARIES_DIR)

# --- Load summarization model ---
@st.cache_resource
def load_model():
    return pipeline("summarization", model="facebook/bart-large-cnn")

summarizer = load_model()

# --- Streamlit UI ---
st.set_page_config(page_title="AI Text Summarizer", page_icon="🧠", layout="centered")
st.title(" AI Text Summarizer")
st.write("Paste any article or blog post, and get a concise 3-sentence summary instantly!")

article = st.text_area("Enter your text below:", height=250, placeholder="Paste your article here...")

if st.button("Summarize"):
    if len(article.strip()) == 0:
        st.warning("Please enter some text first.")
    else:
        with st.spinner("Summarizing... Please wait ⏳"):
            summary = summarizer(article, max_length=130, min_length=30, do_sample=False)[0]['summary_text']

        st.success("Summary generated successfully!")
        st.subheader("Summary:")
        st.write(summary)

        # --- Save Summary ---
        files = os.listdir(SUMMARIES_DIR)
        file_num = len(files) + 1
        save_path = os.path.join(SUMMARIES_DIR, f"summary_{file_num}.txt")

        with open(save_path, "w", encoding="utf-8") as f:
            f.write("Original Text:\n" + article + "\n\nSummary:\n" + summary)

        st.info(f" Summary saved at: `{save_path}`")
