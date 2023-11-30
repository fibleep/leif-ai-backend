from backend.core.image_parser.image_engine import ImageEngine
from backend.core.assistant.llm_engine.llm_engine import LLMEngine
from backend.db.dao.explained_image_dao import ExplainedImageDAO

class IndexEngine:
    """
    Handles saving images to the database
    """
    def __init__(self):
        pass

    async def index(self, explained_image):
        """
        Save image to the database
        """
        explained_image_dao = ExplainedImageDAO()
        await explained_image_dao.create_explained_image(explained_image)


