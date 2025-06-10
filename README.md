# 🧠 Multimodal RAG on The Batch

**Multimodal RAG on The Batch** is a fully functional Retrieval-Augmented Generation (RAG) system that integrates both text and visual content from [The Batch](https://www.deeplearning.ai/the-batch/) newsletters by DeepLearning.AI. The system allows users to ask natural language questions and receive grounded, evidence-based answers derived from article text and images.

---

## 💡 System Overview

This project implements the full RAG pipeline:
```
1. Ingestion      – Scraping and parsing The Batch HTML issues
2. Preprocessing  – Extracting text blocks, alt-texts, and downloading images
3. Embedding      – Generating vector representations via OpenAI embedding API
4. Indexing       – Building FAISS vector index from embeddings
5. Retrieval      – Performing semantic search over stored articles
6. Multimodal RAG – Sending text + base64 images + alt-texts to GPT-4o
7. UI             – Streamlit interface for interactive chat
```

---

## 🧠 Key Features

- 🔍 **Semantic Search** using OpenAI `text-embedding-3-small` and FAISS
- 🖼️ **Multimodal Inputs**: Combines text, alt-texts, and base64-encoded images
- 💬 **LLM Reasoning**: GPT-4o generates responses with citations and interpretation
- 🧾 **Citation Support**: Articles and images referenced in answers
- 🧪 **Streamlit Chat UI**: Clean and session-aware interface
- 🔁 **Embedding Caching**: Avoids recomputation
- 📦 **Modular Codebase**: Clear separation of ingestion, search, RAG, UI, etc.

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Maksn610/multimodal-rag-batch.git
cd multimodal-rag-the-batch
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

The project uses a `.env` file along with centralized logic in `config.py` to manage sensitive credentials and runtime parameters.

#### 🧾 Example `.env` Content

Create a `.env` file in the root directory with the following keys:

```
OPENAI_API_KEY=your-api-key
LLM_MODEL=gpt-4o
```

These values will be automatically loaded by both `llm_client.py` and `config.py`.

#### ⚙️ System Behavior Configuration

You can adjust system behavior directly in `config.py`, including:

- the catalog number range of newsletters to ingest (`START_ISSUE`, `END_ISSUE`)
- which embedding model to use (`EMBED_MODEL`) and the vector dimensionality (`DIM`)
- search parameters for FAISS (`TOP_K`, `SCORE_THRESHOLD`)
- paths for raw data, images, vector index, and metadata

#### 📁 Using `.env.example` (Optional)

If your project includes an `.env.example` file, you can create your actual `.env` file with:

- **On macOS/Linux**:
```bash
cp .env.example .env
```

- **On Windows (CMD)**:
```cmd
copy .env.example .env
```

- **On Windows (PowerShell)**:
```powershell
Copy-Item .env.example .env
```

### 4. Run the Full Pipeline

```bash
python app.py
```

This will:
- download and parse the latest issues of The Batch;
- extract content and images;
- generate embeddings and build the FAISS index;
- launch the Streamlit chat interface.

Or, if you’ve already ingested and indexed the data:

```bash
streamlit run src/ui/rag_ui.py
```

---

## 💬 Example Query

**User:**  
_“What are the recent advances in medical AI mentioned in The Batch?”_

**Response:**  
> In the article *“AI Boosts Cancer Detection”*, an FDA-cleared model is shown to outperform radiologists. In the accompanying image, we see a radiology scan with heatmap overlays highlighting likely tumors. The alt-text confirms that this is based on real clinical data.

---

## 🧱 Project Structure

```
.
├── app.py
├── .env
├── data/                   # Raw + parsed issues and images
├── storage/faiss/          # Vector index and metadata
└── src/
    ├── ingestion/          # Article parser (playwright-based)
    ├── embedding/          # OpenAI embedding logic
    ├── indexing/           # FAISS build/save utils
    ├── search/             # Vector search implementation
    ├── rag/                # LLM prompt + multimodal composition
    ├── ui/                 # Streamlit app
    └── utils/              # Helpers for formatting, IO, etc.
```

---

## 🔬 How Multimodal Context Works

Each GPT-4o call receives:
- the full article text
- any `alt`-descriptions of images
- the actual images (base64-encoded inline)

This context is bundled into a structured payload and passed to OpenAI’s API using the `chat.completions.create(...)` method.

---

## ✅ Evaluation Notes

- Designed to run fully locally, no LangChain used
- Fully integrates GPT-4o with image+text reasoning
- Responds with structured answers + source transparency

---

## 🧪 Testing

The project includes both unit and integration tests to validate core components.

Test files include:
- `test_builder.py` – tests embedding and indexing pipeline
- `test_embedding_client.py` – validates OpenAI embedding logic with retries
- `test_rag_engine.py` – integration test for the full multimodal RAG flow
- `test_searcher.py` – verifies semantic search results from FAISS
- `test_text_formatter.py` – ensures consistent preprocessing of article text

To run all tests:

```bash
pytest tests/
```


## 🧭 High-Level Architecture

```
User Query → Streamlit UI → Semantic Search (FAISS) 
                                ↓
        Text + Images + Alt → GPT-4o LLM → Answer
```

## 🖥️ User Interface

The interface is implemented using Streamlit and provides:
- A chat-like text input where users type questions.
- The assistant's response rendered in markdown (with bold, lists, etc).
- Inline image previews, when relevant.
- A side panel showing retrieved article metadata and scores.

## 🧠 Embedding Caching

To avoid redundant OpenAI calls, the system stores processed article IDs in `embedding_cache.jsonl`.
This allows the embedding pipeline to skip previously processed content.

## 🧩 Extending the System

To change the language model:
- Modify the `call_llm_multimodal()` method in `llm_client.py`
- Or change the `LLM_MODEL` value in `.env`

To support multiple articles per query (instead of one):
- Adjust `rag_engine.py` to pass more than one result to the LLM

To switch embedding providers (e.g., Cohere, HuggingFace):
- Replace `get_embedding()` in `embedding_client.py`

## 🎥 Demo Video

A demo walkthrough video is available to showcase:
- Launching the app
- Asking a question
- Seeing the LLM response with image references

👉 [Link to demo video](https://youtu.be/gUf4l2qFxvo)

## 📜 License

This project is licensed under the MIT License.

You are free to use, modify, and distribute this software under the conditions specified in the LICENSE file.