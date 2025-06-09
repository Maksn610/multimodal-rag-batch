import json
import streamlit as st
from src.rag.rag_engine import answer_query_multimodal
from src.rag.llm_client import last_payload

st.set_page_config(page_title="Multimodal RAG Search", layout="wide")
st.title("🔍 Multimodal RAG Search")

query = st.text_input("Enter your query:", "")
debug = st.checkbox("Show debug info", value=True)

if st.button("Submit") and query:
    result = answer_query_multimodal(query)

    st.markdown("### 💬 Answer")
    st.write(result["answer"])

    if debug:
        st.markdown("### 🐞 Debug Info")

        st.markdown("**User Query:**")
        st.code(query)

        st.markdown("**Retrieved Articles:**")
        for i, art in enumerate(result["articles"]):
            score = art.get("score", "?")
            st.markdown(f"{i+1}. {art['title']} — Score: {score}")
            for path in art.get("local_image_paths", []):
                st.markdown(f"📷 images/{path}")

        if last_payload:
            st.markdown("### 📦 Raw Multimodal Payload to GPT-4o")
            for chunk in last_payload:
                if chunk["type"] == "text":
                    st.markdown("**Text:**")
                    st.code(chunk["text"][:3000])
                elif chunk["type"] == "image_url":
                    st.markdown("**Image (base64 truncated):**")
                    st.code(chunk["image_url"]["url"][:200] + "...", language="text")
