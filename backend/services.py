from clients import supabase, googleClient
from models import TrackCreate, TrackResponse
from google.genai import types

def createTrackEmbedding(description: str):
    
    result = googleClient.models.embed_content(
        model="gemini-embedding-001",
        contents=description,
        # Limit the size to improve performance
        config=types.EmbedContentConfig(output_dimensionality=768)
    )
    
    return result.embeddings[0].values
    

def insertTrack(track: TrackCreate, embedding):
    response = supabase.table('tracks').insert({"title": track.title,"artist":track.artist ,"description":track.description,"embedding": embedding }).execute()
    return TrackResponse(**response.data[0])