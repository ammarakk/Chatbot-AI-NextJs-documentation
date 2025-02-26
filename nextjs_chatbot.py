import streamlit as st
import pandas as pd

# Load Next.js documentation dataset with content
try:
    df = pd.read_csv("nextjs_docs.csv")
except FileNotFoundError:
    st.error("❌ Error: `nextjs_docs.csv` not found. Please run `scrape_nextjs_docs.py` first.")
    st.stop()

# Function to get relevant answers
def get_answer(query):
    query = query.lower()
    
    # Check if required columns exist
    if "keyword" not in df.columns or "description" not in df.columns or "content" not in df.columns:
        return "❌ Error: Missing required columns in CSV. Please re-run the scraper."

    # Search for matching topics
    results = df[df["keyword"].str.contains(query, na=False, case=False)]
    
    if results.empty:
        return "❌ No matching documentation found. Try using different keywords."
    
    response = "### 🔎 Answer Found:\n\n"
    
    for _, row in results.iterrows():
        response += f"🔹 **{row['description']}**\n\n{row['content'][:500]}...\n\n"  # Show first 500 characters
    
    return response

# Streamlit UI
st.set_page_config(page_title="Next.js AI Chatbot", page_icon="⚡", layout="wide")

st.title("🤖 Next.js Documentation AI Chatbot")
st.write("Ask any question about Next.js, and get answers instantly!")

# User input
query = st.text_input("🔎 Type your Next.js-related question:")

if query:
    answer = get_answer(query)
    st.markdown(answer)
