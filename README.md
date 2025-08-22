# RAG-Based YouTube Video Chatbot

A Retrieval-Augmented Generation (RAG) chatbot that allows users to interact with YouTube videos by posting a video link and asking questions. The system retrieves transcript content via embeddings, and—optionally—leverages external knowledge to answer questions beyond the transcript context.

---

##  Features

- **YouTube Transcript Retrieval**  
  Automatically fetches video captions (English/Hindi) using `YouTubeTranscriptApi`.

- **Vector-Based Retrieval (FAISS)**  
  Splits transcript into chunks, generates embeddings with Google Generative AI Embeddings, and indexes them in FAISS for semantic search.

- **Conversational LLM Integration**  
  Chat with the video using an LLM (Gemini via `ChatGoogleGenerativeAI`) with multi-turn memory (`ConversationBufferMemory`).

- **Retrieval-Augmented Generation (RAG)**  
  Incorporates both transcript context and optional external sources for answering user queries.

- **Extensible with External Knowledge APIs**  
  Ideal for plugging in external APIs like Wikipedia, Wikidata, or custom KB for unanswered questions.

---

##  How It Works (Workflow)

1. **Indexing Phase**  
   - Extracts the video ID from the YouTube URL.  
   - Retrieves and preprocesses transcript text.  
   - Splits into chunks and indexes them using FAISS.

2. **Retrieval & Response Phase**  
   - For each user query:
     - Retrieves relevant chunks from FAISS.  
     - Optional: Fetch external knowledge when transcript lacks sufficient info.  
   - Generates response via LLM using provided context.

---

##  Quick Start

```bash
git clone https://github.com/Om-711/RAG-Based-YouTube-Video-Chatbot.git
cd RAG-Based-YouTube-Video-Chatbot
pip install -r requirements.txt
