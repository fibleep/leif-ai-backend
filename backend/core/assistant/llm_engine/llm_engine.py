from abc import ABC, abstractmethod


class LLMEngine(ABC):
    """
    Create embeddings and generate text using a LLM
    """

    @abstractmethod
    def generate(self, prompt, rag_results):
        pass

    @abstractmethod
    def create_embeddings(self, text):
        pass
