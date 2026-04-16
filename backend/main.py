from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from clients import supabase
from services import embeddingFunction, insertTrack, getAllTracks, throwHttpError, getMatches
from models import TrackCreate, TrackResponse


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
async def root():
    return {'status': 'Ok'}


@app.post('/track',  status_code=status.HTTP_201_CREATED)
async def addTrack(track: TrackCreate) -> TrackResponse:
    embedding = embeddingFunction(track.description, "RETRIEVAL_DOCUMENT")
    
    if embedding is None:
       throwHttpError("Something went when trying adding track")
    

    
    response = insertTrack(track, embedding)
    
    if response is None:
        throwHttpError("Something went when trying adding track")
    
    return response
        
   
@app.get('/track/query', status_code=status.HTTP_200_OK)
async def getSemanticTracks(q: str):
    print(q);
    result = embeddingFunction(q, "RETRIEVAL_QUERY")
    
    
    if result is None: 
        throwHttpError("Something went wrong")
    
    matches = getMatches(result)
    
    return matches
    

@app.get('/tracks', status_code=status.HTTP_200_OK)
async def getData() -> list[TrackResponse]:
    return getAllTracks()




