# 📄 DocMind — Chat with Your PDF (FREE)

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-FF4B4B?logo=streamlit)
![LangChain](https://img.shields.io/badge/LangChain-0.2%2B-green)
![Gemini](https://img.shields.io/badge/Google-Gemini%201.5%20Flash-4285F4?logo=google)
![Free](https://img.shields.io/badge/API-100%25%20Free-brightgreen)
![License](https://img.shields.io/badge/License-MIT-yellow)

> Upload any PDF and have a full conversation with it — powered by LangChain, **Google Gemini 1.5 Flash (FREE)**, and FAISS vector search with local HuggingFace embeddings.

---

## ✨ Features

- 📤 **Upload any PDF** — research papers, books, contracts, reports
- 🧠 **Local Embeddings** — HuggingFace `all-MiniLM-L6-v2` runs on your machine (free, no API)
- 💬 **Conversation Memory** — ask follow-up questions naturally
- 📎 **Source Citations** — answers include the page numbers used
- 🔒 **API Key Safe** — entered in UI at runtime, never stored or committed
- 💸 **100% Free** — Gemini 1.5 Flash free tier: 1500 requests/day

---

## 🚀 Quick Start

### 1. Get your FREE Gemini API Key
- Go to 👉 **https://aistudio.google.com**
- Sign in with Google → Click **"Get API Key"**
- No credit card required!

### 2. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/langchain-doc-qa.git
cd langchain-doc-qa
```

### 3. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Run the app
```bash
streamlit run app.py
```

### 6. Open browser at `http://localhost:8501`
Enter your **Gemini API key** in the sidebar, upload a PDF, and start chatting!

---

## 🔑 API Key — Safe Handling

> ⚠️ **Never hardcode your API key in the code.**

The key is entered at runtime in the sidebar. To use environment variables locally:

```bash
# .env file (already in .gitignore — safe!)
GOOGLE_API_KEY=AIza...
```

---

## 🧱 Tech Stack

| Tool | Role | Cost |
|------|------|------|
| **Streamlit** | Frontend UI | Free |
| **LangChain** | RAG pipeline | Free |
| **Gemini 1.5 Flash** | LLM (chat + answers) | **Free** (1500 req/day) |
| **HuggingFace Embeddings** | Text embeddings | **Free** (runs locally) |
| **FAISS** | Vector similarity search | Free |
| **PyPDF** | PDF parsing | Free |

---

## 📁 Project Structure

```
langchain-doc-qa/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── .gitignore          # Keeps secrets & cache out of Git
└── README.md           # This file
```

---

## ☁️ Deploy to Streamlit Cloud (Free)

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo → select `app.py`
4. Add your key under **Settings → Secrets**:
   ```toml
   GOOGLE_API_KEY = "AIza..."
   ```
5. Deploy! 🎉

---

## 📜 License

MIT — free to use, modify, and share.
