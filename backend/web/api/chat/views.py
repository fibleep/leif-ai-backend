from uuid import UUID

from fastapi import APIRouter
from fastapi.param_functions import Depends

from backend.core.assistant.llm_engine.gpt_engine import GPTEngine
from backend.core.assistant.llm_engine.langchain_engine import LangchainEngine
from backend.db.dao.explained_image_dao import ExplainedImageDAO
from backend.web.api.chat.dtos.bot_response import BotResponse
from backend.web.api.chat.schema import Conversation

router = APIRouter()


@router.post("/{echo_id}", tags=["bot"])
async def chat(
    conversation: Conversation,
    echo_id: UUID,
    explained_image_dao: ExplainedImageDAO = Depends(),
):
    """
    Chat with your location.
    """
    llm_engine = LangchainEngine("gpt-3.5-turbo", explained_image_dao)
    generation = await llm_engine.generate(conversation.messages, echo_id)
    results = generation[1] if len(generation) > 1 else []
    bot_response = BotResponse(
        generation[0],
        results
    )
    return bot_response
