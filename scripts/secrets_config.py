import os
import streamlit as st

# Inject secrets for boto3 and OpenAI
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
os.environ["AWS_ACCESS_KEY_ID"] = st.secrets["AWS_ACCESS_KEY_ID"]
os.environ["AWS_SECRET_ACCESS_KEY"] = st.secrets["AWS_SECRET_ACCESS_KEY"]
os.environ["AWS_REGION"] = st.secrets["AWS_REGION"]
os.environ["CHAT_HISTORY_BUCKET"] = st.secrets["CHAT_HISTORY_BUCKET"]
os.environ["COLLECTED_DATA_BUCKET"] = st.secrets["COLLECTED_DATA_BUCKET"]