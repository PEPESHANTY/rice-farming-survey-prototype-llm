import streamlit as st
from PIL import Image
from scripts.secrets_config import *   # Ensures environment is configured
from scripts.user_form import collect_user_info

# for cloud deployed version
from scripts.utils import save_chat_history, list_chat_files, load_chat_file, save_user_data_and_qna, append_query_to_csv

# this is for local running
# from scripts.utils_local import save_chat_history, list_chat_files, load_chat_file, save_user_data_and_qna, append_query_to_csv
from scripts.query import get_response_from_chain

# === Page Config ===
st.set_page_config(page_title="🌾Rice Farming Agent", layout="wide")

# === Session State Initialization ===
if "chat_log" not in st.session_state:
    st.session_state.chat_log = []

if "view_mode" not in st.session_state:
    st.session_state.view_mode = "main"

if "selected_chat" not in st.session_state:
    st.session_state.selected_chat = None

if "chat_saved" not in st.session_state:
    st.session_state.chat_saved = False

if "reset_selector" not in st.session_state:
    st.session_state.reset_selector = False

if "show_chat" not in st.session_state:
    st.session_state.show_chat = False

if st.session_state.reset_selector:
    st.session_state.chat_selector = "📌 Current Chat"
    st.session_state.reset_selector = False

# === Collect User Info First ===
if not st.session_state.show_chat:
    collect_user_info()
    st.stop()

# === Sidebar: Chat History Selector ===
with st.sidebar:
    st.markdown("### 📂 Previous Chats")
    history_files = sorted(list_chat_files(), reverse=True)
    dropdown_options = ["📌 Current Chat"] + history_files
    if "chat_selector" not in st.session_state:
        st.session_state.chat_selector = "📌 Current Chat"
    selected_label = st.selectbox("Select a past chat", dropdown_options, key="chat_selector")

    if selected_label != "📌 Current Chat":
        if not st.session_state.chat_saved:
            st.warning("⚠️ Unsaved chat will be discarded.")
        st.session_state.chat_log = []
        st.session_state.chat_saved = False
        st.session_state.view_mode = "history"
        st.session_state.selected_chat = selected_label
    else:
        st.session_state.view_mode = "main"

# === Top Banner and Title ===
img = Image.open("asset/Rice Farming.png")
resized_img = img.resize((700, 400))
st.image(resized_img)
st.markdown("## 🌾 Rice Farming Assistance Agent")
st.divider()

if not st.session_state.chat_log:
    st.info("💡 Click the sidebar (top-left) to access previous chats!", icon="🧾")

# === Chat Log Display ===
if st.session_state.view_mode == "main":
    with st.container():
        for entry in st.session_state.chat_log:
            role = entry["role"]
            avatar = "🧑‍🌾" if role == "user" else "🤖🚜"
            st.markdown(f"**{avatar} {role.capitalize()}:**\n\n{entry['content']}")

    # === Chat Input and Response ===
    user_input = st.chat_input("Ask about rice farming...")

    if user_input:
        st.chat_message("user").markdown(user_input)
        st.session_state.chat_log.append({"role": "user", "content": user_input})

        append_query_to_csv(user_input)

        history_so_far = [f"{m['role'].capitalize()}: {m['content']}" for m in st.session_state.chat_log]
        response_text, sources = get_response_from_chain(user_input, history_so_far)

        # Extract & format sources
        unique_sources = sorted(set(doc.metadata.get("source", "Unknown") for doc in sources))
        sources_text = f"\n\nSources: {', '.join(unique_sources)}" if unique_sources else ""

        # Show only response in UI
        st.chat_message("assistant").markdown(response_text)

        # Save response + sources to chat history (so they'll go into the .txt file)
        st.session_state.chat_log.append({
            "role": "assistant",
            "content": f"{response_text}{sources_text}"
        })

        # st.chat_message("assistant").markdown(response_text)
        # st.session_state.chat_log.append({"role": "assistant", "content": response_text})

        unique_sources = set(doc.metadata.get("source", "Unknown") for doc in sources)
        with st.expander("📚 Sources used"):
            for src in sorted(unique_sources):
                st.markdown(f"- `{src}`")

# === History View Mode ===
elif st.session_state.view_mode == "history":
    st.markdown(f"### 🧾 Viewing: `{st.session_state.selected_chat}`")
    file_content = load_chat_file(st.session_state.selected_chat)
    st.code(file_content, language="text")

    if st.button("⬅️ Back to main chat"):
        st.session_state.view_mode = "main"
        st.session_state.selected_chat = None
        st.session_state.reset_selector = True
        st.rerun()

# === Save Chat Option ===
if st.session_state.view_mode == "main" and len(st.session_state.chat_log) > 0:
    if st.button("💾 Save This Chat"):
        save_chat_history(st.session_state.chat_log)
        save_user_data_and_qna(st.session_state.chat_log)
        st.success("✅ Chat saved successfully.")
        st.rerun()
