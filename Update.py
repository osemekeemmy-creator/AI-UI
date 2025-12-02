version: '3.8'
services:
  qdrant:
    image: qdrant/qdrant:latest
    ports:
      - "6333:6333"
    volumes:
      - qdrant_data:/qdrant/storage

  jamb-ai:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - qdrant
    environment:
      - API_KEY=your-secret-key-here

volumes:
  qdrant_data:
