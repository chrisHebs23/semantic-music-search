from fastapi import FastAPI, HTTPException, status
from clients import supabase
from services import createTrackEmbedding, insertTrack
from models import TrackCreate, TrackResponse


app = FastAPI()

@app.get('/')
async def root():
    return {'status': 'Ok'}


@app.post('/track',  status_code=status.HTTP_201_CREATED)
async def addTrack(track: TrackCreate) -> TrackResponse:
    embedding = createTrackEmbedding(track.description)
    
    if embedding is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Something went when trying adding track")
    

    
    response = insertTrack(track, embedding)
    
    if response == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Something went when trying adding track")
    
    return response
        
    
    

@app.get('/tracks')
async def getData():
    return supabase.table('tracks').select("*").execute()




