import os
from fastapi import FastAPI
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()


url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)


app = FastAPI()

@app.get('/')
async def root():
    return {'status': 'Ok'}



@app.get('/data')
async def getData():
    return supabase.table('tracks').select("*").execute()