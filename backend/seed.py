from models import TrackCreate
from services import embeddingFunction, insertTrack

SEED_TRACKS = [
    TrackCreate(
        title="Midnight City",
        artist="M83",
        description="Dreamy synth-pop anthem with soaring saxophone, nostalgic and cinematic energy.",
    ),
    TrackCreate(
        title="Redbone",
        artist="Childish Gambino",
        description="Smooth funk-soul groove with falsetto vocals, warm bass, and a paranoid undertone.",
    ),
    TrackCreate(
        title="Blinding Lights",
        artist="The Weeknd",
        description="Retro 80s synthwave pop with driving beat, euphoric and heartbroken at once.",
    ),
    TrackCreate(
        title="Bohemian Rhapsody",
        artist="Queen",
        description="Operatic rock epic shifting between ballad, opera, and hard rock sections.",
    ),
    TrackCreate(
        title="Take Five",
        artist="Dave Brubeck Quartet",
        description="Cool jazz standard in 5/4 time with iconic saxophone melody and laid-back swing.",
    ),
    TrackCreate(
        title="Lose Yourself",
        artist="Eminem",
        description="Intense motivational rap with urgent piano loop and relentless lyrical delivery.",
    ),
    TrackCreate(
        title="Clair de Lune",
        artist="Claude Debussy",
        description="Gentle impressionist piano piece, moonlit and contemplative, flowing and peaceful.",
    ),
    TrackCreate(
        title="Smells Like Teen Spirit",
        artist="Nirvana",
        description="Raw grunge anthem with distorted guitar riff, angst-driven vocals, explosive chorus.",
    ),
    TrackCreate(
        title="Hotel California",
        artist="Eagles",
        description="Classic rock ballad with haunting lyrics, dual guitar solo, mysterious atmosphere.",
    ),
    TrackCreate(
        title="Rolling in the Deep",
        artist="Adele",
        description="Powerful bluesy soul-pop with stomping beat and emotionally raw vocal performance.",
    ),
    TrackCreate(
        title="Strobe",
        artist="Deadmau5",
        description="Slow-building progressive house instrumental, hypnotic and emotional, peaks gradually.",
    ),
    TrackCreate(
        title="No Surprises",
        artist="Radiohead",
        description="Melancholic alt-rock lullaby with glockenspiel, quietly devastating lyrics about apathy.",
    ),
    TrackCreate(
        title="Superstition",
        artist="Stevie Wonder",
        description="Funky clavinet-driven soul track with tight horn stabs and irresistible groove.",
    ),
    TrackCreate(
        title="Africa",
        artist="Toto",
        description="Soft rock with marimba, lush synths, and uplifting soaring chorus about longing.",
    ),
    TrackCreate(
        title="Kids",
        artist="MGMT",
        description="Anthemic indie synth-pop with bouncy hook, nostalgic and bittersweet childhood imagery.",
    ),
    TrackCreate(
        title="HUMBLE.",
        artist="Kendrick Lamar",
        description="Hard-hitting trap-influenced hip hop with minimal piano loop and aggressive delivery.",
    ),
    TrackCreate(
        title="Dreams",
        artist="Fleetwood Mac",
        description="Mellow 70s soft rock with hypnotic drums, ethereal vocals, and bittersweet reflection.",
    ),
    TrackCreate(
        title="Paranoid Android",
        artist="Radiohead",
        description="Multi-part art rock suite, shifting moods from anxious to melodic to chaotic.",
    ),
    TrackCreate(
        title="Sunflower",
        artist="Post Malone & Swae Lee",
        description="Breezy hip hop pop with warm melody, laid-back summer vibe, catchy sing-along hook.",
    ),
    TrackCreate(
        title="La Vie en Rose",
        artist="Edith Piaf",
        description="Classic French chanson, romantic and sweeping with iconic vocal and lush strings.",
    ),
]


def seed():
    for i, track in enumerate(SEED_TRACKS, 1):
        try:
            embedding = embeddingFunction(track.description, "RETRIEVAL_DOCUMENT")
            insertTrack(track, embedding)
            print(f"[{i}/{len(SEED_TRACKS)}] inserted: {track.title} - {track.artist}")
        except Exception as e:
            print(f"[{i}/{len(SEED_TRACKS)}] FAILED: {track.title} - {track.artist}: {e}")


if __name__ == "__main__":
    seed()
