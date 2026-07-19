from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from src.config import settings

class LLMClient:
    """Client for interacting with the Language Model."""
    def __init__(self, model_name: str = "gpt-4-turbo-preview"):
        # If open_ai_api_key is empty, rely on the environment variable explicitly or mock
        # Langchain ChatOpenAI will auto-use os.environ["OPENAI_API_KEY"] if it's set.
        self.llm = ChatOpenAI(
            model=model_name,
            api_key=settings.openai_api_key or None,
            temperature=0.0
        )

    async def generate_response(self, system_prompt: str, user_prompt: str) -> str:
        """Generate a response using the LLM."""
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]

        response = await self.llm.ainvoke(messages)
        return response.content
