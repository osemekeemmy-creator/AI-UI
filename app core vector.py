from qdrant_client import QdrantClient, models
from sentence_transformers import SentenceTransformer
from config import settings
from app.utils.dedup import is_duplicate
import uuid

client = QdrantClient(host=settings.QDRANT_HOST, port=settings.QDRANT_PORT)
embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)

def init_qdrant():
    if not client.collection_exists(settings.COLLECTION_NAME):
        client.create_collection(
            collection_name=settings.COLLECTION_NAME,
            vectors_config=models.VectorParams(
                size=settings.EMBEDDING_DIM,
                distance=models.Distance.COSINE
            )
        )

async def upsert_questions(questions: list[str], subject: str, year: int, source: str):
    vectors = embedding_model.encode(questions).tolist()
    points = []

    for q, vec in zip(questions, vectors):
        if await is_duplicate(vec):
            continue
        points.append(models.PointStruct(
            id=str(uuid.uuid4()),
            vector=vec,
            payload={
                "question": q[:3000],
                "subject": subject.upper(),
                "year": year,
                "source": source
            }
        ))

    if points:
        client.upsert(collection_name=settings.COLLECTION_NAME, points=points)

async def search(query: str, top_k: int = 6):
    vector = embedding_model.encode(query).tolist()
    results = client.search(
        collection_name=settings.COLLECTION_NAME,
        query_vector=vector,
        limit=top_k,
        with_payload=True
    )
    return results
