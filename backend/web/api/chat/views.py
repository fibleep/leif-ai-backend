from fastapi import APIRouter
from fastapi.param_functions import Depends

from backend.core.assistant.llm_engine.gpt_engine import GPTEngine
from backend.db.dao.explained_image_dao import ExplainedImageDAO
from backend.web.api.chat.dtos.bot_response import BotResponse
from backend.web.api.chat.schema import Conversation

router = APIRouter()


@router.post("/")
async def chat(
    conversation: Conversation,
    organization_id: int = 1,
    explained_image_dao: ExplainedImageDAO = Depends(),
):
    """
    Chat with your location.
    """
    llm_engine = GPTEngine("gpt-3.5-turbo", explained_image_dao)
    generation = await llm_engine.generate(conversation.messages)
    results = generation[1]
    bot_response = BotResponse(
        generation[0],
        results
    )
    return bot_response
