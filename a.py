from dotenv import load_dotenv
import os

load_dotenv()
print("✅ Active Key:", os.getenv("AWS_ACCESS_KEY_ID"))
