# sql_agent_tool/llm/gemini.py
import google.generativeai as genai
from .base import LLMInterface, LLMResponse

class GeminiLLM(LLMInterface):
    def __init__(self, api_key: str, model: str = "models/gemini-1.5-flash"):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model)

    def generate_sql(self, prompt: str) -> LLMResponse:
        response = self.model.generate_content(prompt)
        return LLMResponse(content = response.text.strip())