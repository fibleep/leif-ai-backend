import json
from uuid import UUID

from fastapi import APIRouter
from fastapi.param_functions import Depends
from starlette.responses import StreamingResponse

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
    model = "gpt-4-1106-preview"
    llm_engine = LangchainEngine(model, explained_image_dao)
    generation = await llm_engine.generate(conversation.messages, echo_id)
    results = generation[1] if len(generation) > 1 else []
    results = [(results[0].json(), results[1]) for results in results]
    async def combined_stream():
        async for part in llm_engine.generate_stream(generation[0]):
            yield part
        # Encode and yield the additional data
        yield "\n --- END --- \n"
        yield json.dumps({"results": results}).encode()


    return StreamingResponse(combined_stream(), media_type="text/event-stream")
