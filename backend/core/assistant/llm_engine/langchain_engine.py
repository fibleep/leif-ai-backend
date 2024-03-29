import asyncio
import logging
import os
from typing import AsyncIterable

from math import asin, cos, sin, sqrt

from dotenv import load_dotenv
from langchain.chains import create_extraction_chain_pydantic
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import create_extraction_chain
from langchain_core.tools import tool
from sqlalchemy import UUID
from langchain.chat_models import ChatOpenAI
from backend.models.context_decision_format import ContextDecisionFormat
from backend.models.explained_image import ExplainedImage
from backend.models.image_decision import ImageDecision
from backend.models.location import Location
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.agents import AgentType, Tool, initialize_agent
from langchain.llms import OpenAI
from langchain.retrievers.document_compressors import CohereRerank
from .llm_engine import LLMEngine
from langchain.callbacks import AsyncIteratorCallbackHandler
import cohere
import re

load_dotenv()


class LangchainEngine(LLMEngine):
    def __init__(self, model_name, explained_image_dao=None):
        self.model_name = model_name
        api_key = os.environ["BACKEND_OPENAI_API_KEY"]
        self.llm = ChatOpenAI(api_key=api_key, temperature=0.4, model=model_name)
        self.streaming_llm = ChatOpenAI(api_key=api_key, temperature=0.4,
                                        model=model_name, streaming=True)
        self.embeddings_engine = OpenAIEmbeddings(openai_api_key=api_key)
        self.system_prompt_with_context = """
You are Echo, you are an expert at navigating through different places. You will be
given a context of a place and you will have to describe it to the user. Talk in a
friendly,
encouraging tone. If you don't understand the user, ask them to repeat themselves.
Only talk about the distance. Explain in a short and concise manner.
Always mention how far away it is from the user, give a visual explanation of what it looks like.

If the answer is not about a place, ask the user to repeat themselves, do it in a
friendly, encouraging tone.


Examples:
User: Where is the nearest McDonalds?
Echo: The nearest McDonalds is 100 meters away from you, it is a red building with a yellow M on it.

User: What is the weather like?
Echo: I'm sorry, I don't understand what you're saying, can you repeat yourself?

Tips:
- Mention keypoints from the description, the user will be able to recognize the place
- Be friendly and encouraging
- You will be rewarded if you are able to answer the user's question

FOLLOW THE FORMAT THAT IS GIVEN TO YOU, OTHERWISE THE SYSTEM WILL NOT WORK
"""
        self.system_prompt_without_context = """
You are Echo, you are an expert at navigating through different places. You will talk with the user and help them out.
If you see this, that means that the system didn't find any locations for the
user. Tell the user that you couldn't find anything and let them know that this was
outside your scope.
"""
        self.explained_image_dao = explained_image_dao
        self.co = cohere.Client(os.environ["BACKEND_COHERE_API_KEY"])

    async def generate(self, messages, echo_id: UUID = None):

        current_message = messages[-1]

        # Do we need to include the context?

        parsed_context, chosen_context = await self._get_parsed_context(
            current_message,
            echo_id)

        prompt = f"""
This is the location recommended by the system:
Some tips:
- Title is most likely the most important field
- Additional comment is the description of the place, use this to guide the user

CONTEXT:
====================
{parsed_context[0]}
====================
USER QUERY TO ANSWER:
{current_message.content}
"""
        try:
            to_evaluate = (f"""USER QUERY: {current_message.content}
CONTEXT:
{chosen_context[0][0].title}
{chosen_context[0][0].additional_comment}""")
            included_context = self._decide_include_context(to_evaluate)
        except Exception as e:
            logging.error(e)
            print(e)
            included_context = False
        print(included_context)
        prompt = prompt if included_context else f"USER QUERY: {current_message.content}"

        parsed_messages = [
            HumanMessage(content=message.content)
            if message.role == "user"
            else AIMessage(content=message.content)
            for message in messages[:-1]
        ]

        parsed_messages.append(HumanMessage(content=prompt))
        chosen_prompt = self.system_prompt_with_context if included_context else self.system_prompt_without_context
        parsed_messages.insert(0, SystemMessage(content=chosen_prompt))
        # Truncate the messages
        if len(parsed_messages) > 5:
            parsed_messages = parsed_messages[-5:]
        return parsed_messages, chosen_context if included_context else []

    async def generate_stream(self, messages) -> AsyncIterable[str]:
        """
        Generate a stream of messages
        """
        async for message in self.streaming_llm.astream(messages):
            yield str(message.content)

    def _decide_include_context(self, to_evaluate):
        schema = {
            "properties": {
                "context_is_useful": {
                    "type": "boolean",
                }
            }
        }
        extraction_chain = create_extraction_chain(
            schema=schema,
            llm=self.llm
        )
        decision_message = (f"""
        # CONTEXT #
        You are going to make a decision about whether or not to include the context
        about the location.

        # OBJECTIVE #
        Guide the user to their destination or answer their question. Be as accurate as possible.
        If the context doesn't match the user query, don't include it. - return False

        # STYLE #
        Follow the format that is given to you, otherwise the system will not work.

        # RESPONSE #
        Return True if the returned context matches the user query or if its useful,
        otherwise return False. REMEMBER! This will have huge impact on the user experience.

        # EXAMPLE #
        USER QUERY: Where is the nearest McDonalds?
        CONTEXT:"talks about McDonalds"
        RESPONSE: True

        # QUERY + RETRIEVED CONTEXT TO EVALUATE #
        {to_evaluate}
        """)
        included_context = extraction_chain.run(decision_message)[0]
        return included_context['context_is_useful']


    def haversine_distance(self, lat1, lon1, lat2, lon2):
        """
        Calculate the great circle distance between two points
        on the earth (specified in decimal degrees)
        """
        # convert decimal degrees to radians
        lat1, lon1, lat2, lon2 = map(
            lambda x: float(x) * 3.141592 / 180.0, [lat1, lon1, lat2, lon2]
        )

        # haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = pow(sin(dlat / 2), 2) + cos(lat1) * cos(lat2) * pow(sin(dlon / 2), 2)
        c = 2 * asin(sqrt(a))
        r = 6371

        return c * r

    def create_embeddings(self, text):
        return self.embeddings_engine.embed_query(text)

    async def _get_parsed_context(self, current_message,
                                  echo_id:
                                  UUID =
                                  None):
        """
        Get the parsed context, rerank and get the most relevant context
        :param current_message: current message
        :param combined_user_messages: all messages of users, joined
        :param echo_id: echo id
        :return: parsed_context and chosen_context
        """
        results = await self.get_most_relevant_context(current_message.content, echo_id)
        results_and_distances = []
        for result in results:
            results_and_distances.append(
                (result, self.calculate_distance(current_message, result) * 1000)
            )

        # Find the most relevant context
        chosen_context = await self._find_relevant_context(
            combined_user_messages=current_message.content,
            possible_locations=results_and_distances,
        )

        # Parse the context
        parsed_context = []
        if type(chosen_context) == tuple:
            chosen_context = [chosen_context]
        for idx, context_item in enumerate(chosen_context):
            parsed_context.append(
                f"""
        INDEX: {idx}
        TITLE:
        {context_item[0].title}
        DISTANCE:
        {context_item[1]} meters away from User
        DESCRIPTION (TO BE USED AS A GUIDE):
        {context_item[0].additional_comment}
        ====================
        """
            )
        return parsed_context, chosen_context

    async def _find_relevant_context(self, combined_user_messages,
                                     possible_locations, threshold_difference=0.2):
        """
        Based on the user query and location, choose which of the retrieved contexts
        are the most relevant
        :param combined_user_messages: The combined user messages
        :param possible_locations: The possible locations (distance, result)
        :param threshold_difference: The threshold difference between the first and
        second
        """

        # If there is only one possible location, return it
        if len(possible_locations) == 1:
            return possible_locations[0]

        # If there are multiple locations, rank them
        parsed_documents = [
            f"""
            INDEX[{idx}]
            {context[1]} away from User
            Title (MOST IMPORTANT FIELD): {context[0].title}
            Additional comment: {context[0].additional_comment}"""
            for idx, context in enumerate(possible_locations)]
        parsed_query = (f"These are the last three messages from the user, rerank my "
                        f"documents to find the most relevant one, the latest message has the most weight: "
                        f": {combined_user_messages}")
        results = self.co.rerank(query=parsed_query,
                                 documents=parsed_documents, top_n=2,
                                 model="rerank-multilingual-v2.0"
                                 )
        pattern = r"INDEX\[(\d+)\]"
        sorted_results = [re.findall(pattern, str(result))[0] for result in
                          results.results]
        sorted_locations = [possible_locations[int(idx)] for idx in sorted_results]
        return sorted_locations

    async def get_most_relevant_context(self, text: str, echo_id: UUID = None):
        """
        Get the most relevant context for a given set of text
        """
        from backend.web.api.chat.dtos.explained_image_dto import ExplainedImageDTO

        vectorized_message = self.create_embeddings(text)

        results = await self.explained_image_dao.similarity_search(
            vectorized_message, echo_id=echo_id)
        results = [
            ExplainedImageDTO(
                id=result.id,
                image=result.image,
                title=result.title,
                date=result.date,
                latitude=result.latitude,
                longitude=result.longitude,
                altitude=result.altitude,
                location=result.location,
                direction=result.direction,
                additional_comment=result.additional_comment,
            )
            for result in results
        ]
        return results

    def calculate_distance(self, current_message, result):
        distance = self.haversine_distance(
            current_message.geolocation.coordinates.lat,
            current_message.geolocation.coordinates.lng,
            result.latitude,
            result.longitude,
        )
        return distance

    def get_all_images(self):
        return self.explained_image_dao.get_all_explained_images()
