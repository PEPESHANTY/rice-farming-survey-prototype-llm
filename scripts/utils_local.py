# scripts/utils_local.py

import os
from datetime import datetime
import streamlit as st
import csv

def save_chat_history(chat_log):
    os.makedirs("chat_history", exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    existing = os.listdir("chat_history")
    next_id = len(existing) + 1
    filename = f"chat_history_{next_id}_{timestamp}.txt"
    filepath = os.path.join("chat_history", filename)

    with open(filepath, "w", encoding="utf-8") as f:
        # # --- User Info ---
        # metadata = st.session_state.get("user_metadata", {})
        # f.write("## User Info\n")
        # for key, value in metadata.items():
        #     f.write(f"{key.capitalize()}: {value}\n")

        f.write("\n## Chat Log\n")
        # --- Chat Entries ---
        for entry in chat_log:
            role = entry.get("role", "unknown")
            msg = entry.get("content", "")
            time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"{role.upper()} [{time_str}]:\n{msg}\n\n")

    return filename

def save_user_data_and_qna(chat_log):
    os.makedirs("chat_data_collected", exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    user_meta = st.session_state.get("user_metadata", {})
    existing = os.listdir("chat_data_collected")
    next_id = len(existing) + 1
    name_part = user_meta.get("name", "User").replace(" ", "_")
    filename = f"chat_{next_id}_{name_part}_{timestamp}.txt"
    filepath = os.path.join("chat_data_collected", filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("## User Metadata\n")
        for key, value in user_meta.items():
            f.write(f"{key.capitalize()}: {value}\n")

        f.write("\n## Queries and Responses\n")
        for i in range(0, len(chat_log), 2):
            if i + 1 < len(chat_log) and chat_log[i]["role"] == "user":
                user_q = chat_log[i]["content"]
                bot_a = chat_log[i + 1]["content"] if chat_log[i + 1]["role"] == "assistant" else ""
                f.write(f"\nUser Query:\n{user_q}\n\nResponse:\n{bot_a}\n\n")

    return filename



def append_query_to_csv(query_text):
    if len(query_text.split()) <= 3:
        return  # Ignore short queries

    user_meta = st.session_state.get("user_metadata", {})
    name = user_meta.get("name", "User")
    profession = user_meta.get("profession", "")
    country = user_meta.get("country", "")
    state = user_meta.get("state", "")

    os.makedirs("chat_data_collected", exist_ok=True)
    csv_file = os.path.join("chat_data_collected", "Survey_data.csv")

    file_exists = os.path.isfile(csv_file)
    with open(csv_file, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists or os.stat(csv_file).st_size == 0:
            writer.writerow(["Name", "Profession", "Country", "State", "Query"])  # header
        writer.writerow([name, profession, country, state, query_text])


def list_chat_files():
    folder = "chat_history"
    if not os.path.exists(folder):
        return []
    return sorted([f for f in os.listdir(folder) if f.endswith(".txt")], reverse=True)

def load_chat_file(filename):
    filepath = os.path.join("chat_history", filename)
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"❌ Error loading file {filename}:", e)
        return ""
