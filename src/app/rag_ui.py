import streamlit as st
from src.rag.rag_engine import answer_query_multimodal
from src.rag.llm_client import last_payload  # Assuming this is available for debug if needed

st.set_page_config(page_title="The Batch Insight Navigator", layout="centered", page_icon="🗞️")
st.title("🗞️ The Batch Insight Navigator")

if "messages" not in st.session_state:
    st.session_state.messages = []
col1, col2, col3 = st.columns([1, 6, 1])

with col2:
    if prompt := st.chat_input("Ask a question about The Batch articles..."):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.spinner("Searching and generating answer..."):
            try:
                result = answer_query_multimodal(prompt)
                if result and "answer" in result:
                    response_content = result["answer"]
                else:
                    response_content = "Sorry, I could not find an answer to your query in The Batch articles."
            except Exception as e:
                response_content = f"An error occurred while processing your request: {e}"
            finally:
                st.session_state.messages.append({"role": "assistant", "content": response_content})

chat_history_container = st.container()
for message in st.session_state.messages:
    with chat_history_container.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant" and "result" in message:
            result = message["result"]
            with chat_history_container.expander("Details and Sources"):
                if result and "articles" in result:
                    st.markdown("**Found articles:**")
                    for i, art in enumerate(result["articles"]):
                        score = art.get("score", "?")
                        st.markdown(f"{i + 1}. **{art.get('title', 'N/A')}** — Score: {score:.4f}")
                        for path in art.get("local_image_paths", []):
                            st.markdown(f"📷 `{path}`")
                else:
                    st.info("No additional sources found.")

                if last_payload:
                    st.markdown("**GPT-4o Request Details (Technical Info):**")
                    for chunk in last_payload:
                        if chunk["type"] == "text":
                            st.code(f"Text: {chunk['text'][:200]}..." if len(
                                chunk['text']) > 200 else f"Text: {chunk['text']}", language="text")
                        elif chunk["type"] == "image_url":
                            st.code(f"Image (URL): {chunk['image_url']['url'][:50]}...", language="text")

st.markdown("---")
st.info("""
    💡 **The Batch Insight Navigator**: Explore "The Batch" articles with AI.
    Using **Multimodal RAG**, it processes text and images for comprehensive answers.
    Ask anything related to the content and get insights from relevant sources.
""")
