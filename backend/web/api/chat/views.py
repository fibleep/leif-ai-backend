from fastapi import APIRouter
from fastapi.param_functions import Depends

from backend.core.assistant.llm_engine.gpt_engine import GPTEngine
from backend.db.dao.explained_image_dao import ExplainedImageDAO
from backend.web.api.chat.schema import Conversation

router = APIRouter()


@router.post("/")
async def chat(
    conversation: Conversation,
    explained_image_dao: ExplainedImageDAO = Depends(),
):
    """
    Chat with your location.
    """
    llm_engine = GPTEngine("gpt-4", explained_image_dao)
    generation = await llm_engine.generate(conversation.messages)
    
    return generation
