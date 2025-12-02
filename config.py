from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_KEY: str = "jamb-pro-secret-2025-change-me"
    QDRANT_HOST: str = "qdrant"
    QDRANT_PORT: int = 6333
    COLLECTION_NAME: str = "jamb_questions_v4"
    EMBEDDING_MODEL: str = "BAAI/bge-small-en-v1.5"
    EMBEDDING_DIM: int = 384

    class Config:
        env_file = ".env"

settings = Settings()
