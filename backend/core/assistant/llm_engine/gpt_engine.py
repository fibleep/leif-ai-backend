import os

from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings

from .llm_engine import LLMEngine

load_dotenv()


class GPTEngine(LLMEngine):
    def __init__(self, model_name):
        self.model_name = model_name
        api_key = os.environ["BACKEND_OPENAI_API_KEY"]
        self.llm = ChatOpenAI(api_key=api_key, temperature=0.7, model="gpt-4")
        self.embeddings_engine = OpenAIEmbeddings(openai_api_key=api_key)

    def generate(self, prompt, history=None):
        pass

    def create_embeddings(self, text):
        return self.embeddings_engine.embed_query(text)
