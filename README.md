# 🌾 Rice Farming Assistance Agent

This is a multi-turn conversational AI assistant that helps farmers and agricultural researchers with sustainable rice farming practices. The assistant is built using **Streamlit**, **LangChain**, **OpenAI**, and **AWS S3** for cloud-based chat history storage.

> 💬 Ask about manures, pest control, water management, or any rice farming topic — and get answers grounded in domain PDFs.

---

## 🚀 Features

- ✅ Multi-turn chat interface with context retention
- ✅ Document-grounded answers using **LangChain + FAISS**
- ✅ Embedding-based vector search across PDF knowledge
- ✅ Chat history and metadata saved to **AWS S3**
- ✅ User metadata collected via a pre-chat form
- ✅ Responsive, clean UI using Streamlit

---

## 📁 Folder Structure

```
.
├── app.py                      # Main Streamlit app
├── .env                        # (For local testing)
├── scripts/
│   ├── secrets_config.py       # Injects Streamlit secrets to os.environ
│   ├── user_form.py            # Collects user info (name, country, etc.)
│   ├── utils.py                # S3 save/load logic
│   ├── utils_local.py          # Local version of utils
│   ├── query.py                # LangChain RAG logic
│
├── pdf_data/                   # Source PDFs used for embedding
├── pdf_vectorstore/            # Persisted FAISS vector store
└── asset/
    └── Rice Farming.png        # Banner image for UI
```

## 🛠️ Tech Stack
Component	Technology
Frontend	Streamlit
Backend	Python (LangChain, OpenAI)
Vector Search	FAISS
Embeddings	OpenAI text-embedding-3-small
Storage	AWS S3 (chat history, CSV)

## 🧠 Powered By
📚 LangChain — Retrieval-Augmented Generation (RAG)

🧠 OpenAI API for embedding + language generation

🗂️ FAISS for vector similarity search

☁️ AWS S3 to persist chat logs and survey data


## 🧪 Running Locally
```
# Clone the repo
git clone https://github.com/YOUR_USERNAME/rice-farming-assistant.git
cd rice-farming-assistant

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env  # fill in the values

# Run Streamlit
streamlit run app.py
```

## 🤖 Prompted Use Cases
Sustainable rice production

Soil health and fertilizers

Crop rotation planning

Water usage optimization

Pest and disease control

## 📌 Project Purpose
This prototype is built for data collection and stress testing of our rice farming chatbot. It helps us gather:

Real user queries from farmers

Associated chat histories and metadata

Interaction patterns for analyzing performance under load

The ultimate goal is to train and fine-tune a robust domain-specific LLM tailored for rice farmers in Southeast Asia.
