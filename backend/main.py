import os
from fastapi import FastAPI, HTTPException, status
from supabase import create_client, Client
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel
from uuid import UUID

load_dotenv()

googleClient = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))


url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

app = FastAPI()

class Track(BaseModel):
    id: UUID | None = None
    title: str
    artist: str
    description: str
    embedding:   list[float] | None = None

@app.get('/')
async def root():
    return {'status': 'Ok'}


@app.post('/track',  status_code=status.HTTP_201_CREATED)
async def addTrack(track: Track) -> Track:
    embedding = createTrackEmbedding(track.description)
    
    if embedding == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Something went when trying adding track")
    
    track.embedding = embedding
    
    response = insertTrack(track)
    
    if response == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Something went when trying adding track")
    
    return response
        
    
    

@app.get('/tracks')
async def getData():
    return supabase.table('tracks').select("*").execute()




def createTrackEmbedding(description: str):
    
    result = googleClient.models.embed_content(
        model="gemini-embedding-001",
        contents=description,
        # Limit the size to improve performance
        config=types.EmbedContentConfig(output_dimensionality=768)
    )
    
    return result.embeddings[0].values
    

def insertTrack(track: Track):
    response = supabase.table('tracks').insert({"title": track.title,"artist":track.artist ,"description":track.description,"embedding": track.embedding }).execute()
    return Track(**{k: v for k, v in response.data[0].items() if k != 'embedding'})

