# scripts/utils.py
from scripts.secrets_config import *
import os
import csv
import streamlit as st
import boto3
from datetime import datetime
from io import StringIO

# AWS S3 Setup
import dotenv
dotenv.load_dotenv(override=True)

ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
CHAT_HISTORY_BUCKET = os.getenv("CHAT_HISTORY_BUCKET")
COLLECTED_DATA_BUCKET = os.getenv("COLLECTED_DATA_BUCKET")

s3 = boto3.client("s3", region_name=AWS_REGION,
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY
    )


def save_chat_history(chat_log):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    existing_files = list_chat_files()
    next_id = len(existing_files) + 1
    filename = f"chat_history_{next_id}_{timestamp}.txt"

    content = "\n## Chat Log\n"
    for entry in chat_log:
        role = entry.get("role", "unknown")
        msg = entry.get("content", "")
        time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        content += f"{role.upper()} [{time_str}]:\n{msg}\n\n"

    s3.put_object(Body=content.encode("utf-8"), Bucket=CHAT_HISTORY_BUCKET, Key=filename)
    return filename


def save_user_data_and_qna(chat_log):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    user_meta = st.session_state.get("user_metadata", {})
    existing = list_chat_files()
    next_id = len(existing)
    name_part = user_meta.get("name", "User").replace(" ", "_")
    filename = f"chat_{next_id}_{name_part}_{timestamp}.txt"

    content = "## User Metadata\n"
    for key, value in user_meta.items():
        content += f"{key.capitalize()}: {value}\n"

    content += "\n## Queries and Responses\n"
    for i in range(0, len(chat_log), 2):
        if i + 1 < len(chat_log) and chat_log[i]["role"] == "user":
            user_q = chat_log[i]["content"]
            bot_a = chat_log[i + 1]["content"] if chat_log[i + 1]["role"] == "assistant" else ""
            content += f"\nUser Query:\n{user_q}\n\nResponse:\n{bot_a}\n\n"

    s3.put_object(Body=content.encode("utf-8"), Bucket=COLLECTED_DATA_BUCKET, Key=filename)
    return filename


def append_query_to_csv(query_text):
    if len(query_text.split()) <= 3:
        return

    user_meta = st.session_state.get("user_metadata", {})
    name = user_meta.get("name", "User")
    profession = user_meta.get("profession", "")
    country = user_meta.get("country", "")
    state = user_meta.get("state", "")
    csv_key = "Survey_data.csv"

    try:
        obj = s3.get_object(Bucket=COLLECTED_DATA_BUCKET, Key=csv_key)
        csv_data = obj['Body'].read().decode('utf-8')
        buffer = StringIO(csv_data)
        reader = list(csv.reader(buffer))
    except s3.exceptions.NoSuchKey:
        reader = [["Name", "Profession", "Country", "State", "Query"]]

    reader.append([name, profession, country, state, query_text])
    out_buffer = StringIO()
    writer = csv.writer(out_buffer)
    writer.writerows(reader)

    s3.put_object(Bucket=COLLECTED_DATA_BUCKET, Key=csv_key, Body=out_buffer.getvalue().encode("utf-8"))


def list_chat_files():
    try:
        response = s3.list_objects_v2(Bucket=CHAT_HISTORY_BUCKET)
        files = [item["Key"] for item in response.get("Contents", []) if item["Key"].endswith(".txt")]
        return sorted(files, reverse=True)
    except Exception as e:
        print("Error listing files:", e)
        return []


def load_chat_file(filename):
    try:
        obj = s3.get_object(Bucket=CHAT_HISTORY_BUCKET, Key=filename)
        return obj['Body'].read().decode('utf-8')
    except Exception as e:
        print("Error loading file:", e)
        return ""
