from clients import supabase, googleClient
from models import TrackCreate, TrackResponse
from google.genai import types
from fastapi import HTTPException, status

def embeddingFunction(description: str, task_type: str) -> list[float]:
    
    result = googleClient.models.embed_content(
        model="gemini-embedding-001",
        contents=description,

        config=types.EmbedContentConfig(output_dimensionality=768, task_type=task_type)
    )
    
    return result.embeddings[0].values
    

def insertTrack(track: TrackCreate, embedding):
    response = supabase.table('tracks').insert({"title": track.title,"artist":track.artist ,"description":track.description,"embedding": embedding }).execute()
    return TrackResponse(**response.data[0])

def getAllTracks():
    return supabase.table('tracks').select("*").execute().data

def getMatches(embedding):
    return supabase.rpc("match_tracks", {
        "query_embedding": embedding,
        "match_threshold": 0.55,
        "match_count": 5
    }).execute().data


def throwHttpError(msg: str): 
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)
