import os
from supabase import create_client, Client
from dotenv import load_dotenv
from google import genai

load_dotenv()

googleClient = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))


url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)