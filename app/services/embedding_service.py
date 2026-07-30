import os
import voyageai
from dotenv import load_dotenv

load_dotenv()

client = voyageai.Client(
    api_key=os.getenv("VOYAGE_API_KEY")
)

MODEL = "voyage-4-lite"


def generate_embedding(text: str) -> list[float]:
    """
    Generate a single sentence embedding.
    Raises Voyage exceptions so the caller can handle them.
    """

    result = client.embed(
        texts=[text],
        model=MODEL
    )

    return result.embeddings[0]