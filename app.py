import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_classic.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_classic.chains import ConversationalRetrievalChain
from langchain_classic.memory import ConversationBufferMemory
import tempfile
import os
from dotenv import load_dotenv

#  Load API key 
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

#  Page config
st.set_page_config(page_title="DocMind – Chat with your PDF", page_icon="📄", layout="wide")

#  Custom CSS 
st.markdown("""
<style>
    .stApp { background-color: #0f1117; }
    h1 { color: #ffffff; font-size: 2.2rem !important; }
    h3 { color: #a0aec0; }
    .upload-box {
        border: 2px dashed #4a5568; border-radius: 12px; padding: 2rem;
        text-align: center; color: #718096; background: #1a202c; margin-bottom: 1rem;
    }
    .chat-user {
        background: #2d3748; border-radius: 12px 12px 2px 12px;
        padding: 0.8rem 1.1rem; margin: 0.4rem 0; color: #e2e8f0; text-align: right;
    }
    .chat-ai {
        background: #1a3a2a; border-radius: 12px 12px 12px 2px;
        padding: 0.8rem 1.1rem; margin: 0.4rem 0; color: #e2e8f0;
        border-left: 3px solid #38a169;
    }
    .status-box {
        background: #1a202c; border-radius: 8px; padding: 0.6rem 1rem;
        font-size: 0.85rem; color: #68d391; border: 1px solid #276749; margin-bottom: 1rem;
    }
    div[data-testid="stSidebar"] { background-color: #1a202c; }
</style>
""", unsafe_allow_html=True)

#  Session state 
for key, val in [("chat_history", []), ("chain", None), ("doc_name", None)]:
    if key not in st.session_state:
        st.session_state[key] = val

#  Sidebar 
with st.sidebar:
    st.markdown("## 📄 DocMind")
    st.markdown("### 📚 How it works")
    st.markdown("""
1. **Upload** a PDF document
2. App **indexes** it with Gemini ⚡
3. **Ask anything** — instant answers
4. Full **conversation memory** included
    """)
    st.divider()
    st.markdown("`LangChain` · `Gemini` · `FAISS` · `Streamlit`")
    if st.session_state.doc_name:
        st.divider()
        st.markdown(f"📄 **Loaded:** `{st.session_state.doc_name}`")
        if st.button("🗑️ Clear & Reset", use_container_width=True):
            st.session_state.chat_history = []
            st.session_state.chain = None
            st.session_state.doc_name = None
            st.rerun()

#  Main UI 
st.markdown("# 📄 DocMind")
st.markdown("### Chat with your PDF using LangChain + Gemini ⚡")
st.divider()

if not GOOGLE_API_KEY:
    st.error("⚠️ API key not found! Create a `.env` file with `GOOGLE_API_KEY=AIza...`")
    st.stop()

#  PDF Upload 
if not st.session_state.chain:
    uploaded_file = st.file_uploader("Upload a PDF to get started", type=["pdf"])

    if uploaded_file:
        progress = st.progress(0, text="📖 Reading PDF...")
        try:
            # Step 1: Save temp file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_file.read())
                tmp_path = tmp.name

            progress.progress(25, text="✂️ Splitting into chunks...")
            loader = PyPDFLoader(tmp_path)
            docs = loader.load()
            splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=100)
            chunks = splitter.split_documents(docs)

            progress.progress(55, text="⚡ Embedding with Gemini (fast!)...")
            # Gemini embeddings — fast, no local model download!
            embeddings = GoogleGenerativeAIEmbeddings(
                model="gemini-embedding-2-preview",
                google_api_key=GOOGLE_API_KEY
            )
            vectorstore = FAISS.from_documents(chunks, embeddings)

            progress.progress(80, text="🧠 Building Q&A chain...")
            memory = ConversationBufferMemory(
                memory_key="chat_history", return_messages=True, output_key="answer"
            )
            llm = ChatGoogleGenerativeAI(
                model="gemini-2.5-flash",
                google_api_key=GOOGLE_API_KEY,
                temperature=0.3,
                convert_system_message_to_human=True
            )
            st.session_state.chain = ConversationalRetrievalChain.from_llm(
                llm=llm,
                retriever=vectorstore.as_retriever(search_kwargs={"k": 4}),
                memory=memory,
                return_source_documents=True,
            )
            st.session_state.doc_name = uploaded_file.name
            os.unlink(tmp_path)

            progress.progress(100, text="✅ Done!")
            st.success(f"✅ **{uploaded_file.name}** ready! Start asking questions.")
            st.rerun()

        except Exception as e:
            progress.empty()
            st.error(f"❌ Error: {str(e)}")
    else:
        st.markdown("""
        <div class="upload-box">
            ⬆️ Drop your PDF above to begin<br>
            <small>Supports research papers, books, reports, contracts — any PDF</small>
        </div>
        """, unsafe_allow_html=True)

#  Chat 
if st.session_state.chain:
    st.markdown(f"""
    <div class="status-box">
        ✅ <strong>{st.session_state.doc_name}</strong> loaded — Ask me anything!
    </div>
    """, unsafe_allow_html=True)

    for msg in st.session_state.chat_history:
        css_class = "chat-user" if msg["role"] == "user" else "chat-ai"
        icon = "🧑" if msg["role"] == "user" else "🤖"
        st.markdown(f'<div class="{css_class}">{icon} {msg["content"]}</div>', unsafe_allow_html=True)

    if not st.session_state.chat_history:
        st.markdown("**💡 Try asking:**")
        col1, col2, col3 = st.columns(3)
        for col, suggestion in zip([col1, col2, col3],
            ["Summarize this document", "What are the key findings?", "What is the main topic?"]):
            with col:
                if st.button(f"💬 {suggestion}", use_container_width=True):
                    st.session_state._quick_q = suggestion
                    st.rerun()

    quick_q = st.session_state.pop("_quick_q", None)
    question = quick_q or st.chat_input("Ask a question about your document...")

    if question:
        st.session_state.chat_history.append({"role": "user", "content": question})
        with st.spinner("🤔 Thinking..."):
            try:
                result = st.session_state.chain({"question": question})
                answer = result["answer"]
                sources = result.get("source_documents", [])
                if sources:
                    pages = sorted(set(
                        doc.metadata.get("page", "?") + 1
                        for doc in sources if isinstance(doc.metadata.get("page"), int)
                    ))
                    answer += f"\n\n*📎 Sources: Page(s) {', '.join(str(p) for p in pages)}*"
                st.session_state.chat_history.append({"role": "ai", "content": answer})
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
