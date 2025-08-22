# RAG-Based YouTube Video Chatbot

A Retrieval-Augmented Generation (RAG) chatbot that allows users to interact with YouTube videos by posting a video link and asking questions. The system retrieves transcript content via embeddings, and optionally leverages external knowledge to answer questions beyond the transcript context.

---

## ✨ Features  
- 📺 **YouTube Transcript Retrieval** – fetches captions in English/Hindi using `YouTubeTranscriptApi`.  
- 🔍 **Vector Search with FAISS** – chunks transcript, generates embeddings with Google Generative AI, and retrieves relevant segments.  
- 🤖 **Conversational LLM (Gemini)** – answers questions using transcript context and remembers chat history.  
- 🔄 **Retrieval-Augmented Generation (RAG)** – ensures answers are grounded in real transcript data.  
- 🌐 **Streamlit Interface** – easy-to-use UI to paste video links and chat live with the video.  

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
