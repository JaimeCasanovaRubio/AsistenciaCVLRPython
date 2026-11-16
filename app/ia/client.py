
from app.core.config import settings
from google import genai


client = genai.Client(api_key=settings.GOOGLE_GENAI_API_KEY)

async def get_genai_client() -> genai.Client:
    """
    Generador de cliente para Google GenAI.
    """
    return genai.Client(api_key=settings.GOOGLE_GENAI_API_KEY)

async def get_embedded_text(text: str) -> list[float]:
    """
    Obtiene el embedding de un texto usando Google GenAI.
    """
    response = await client.embeddings.create(
        model = "gemini-embedding-2",
        input = text
    )
    return response.data[0].embedding