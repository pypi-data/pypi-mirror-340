from typing import Optional

import structlog
from jinja2 import Template

from rasa.core.tracker_store import DialogueStateTracker
from rasa.shared.constants import (
    LANGFUSE_CUSTOM_METADATA_DICT,
    LANGFUSE_METADATA_SESSION_ID,
    LANGFUSE_METADATA_USER_ID,
    LANGFUSE_TAGS,
)
from rasa.shared.providers.llm.llm_client import LLMClient
from rasa.shared.utils.llm import (
    tracker_as_readable_transcript,
)

structlogger = structlog.get_logger()

_DEFAULT_SUMMARIZER_TEMPLATE = """Summarize the provided conversation between
a user and a conversational AI. The summary should be a short text that
captures the main points of the conversation.

Conversation:
{{conversation}}

Summary:"""
SUMMARY_PROMPT_TEMPLATE = Template(_DEFAULT_SUMMARIZER_TEMPLATE)
MAX_TURNS_DEFAULT = 20


def _create_summarization_prompt(
    tracker: DialogueStateTracker, max_turns: Optional[int]
) -> str:
    """Creates an LLM prompt to summarize the conversation in the tracker.

    Args:
        tracker: tracker of the conversation to be summarized
        max_turns: maximum number of turns to summarize


    Returns:
        The prompt to summarize the conversation.
    """
    transcript = tracker_as_readable_transcript(tracker, max_turns=max_turns)
    return SUMMARY_PROMPT_TEMPLATE.render(
        conversation=transcript,
    )


async def summarize_conversation(
    tracker: DialogueStateTracker,
    llm: LLMClient,
    max_turns: Optional[int] = MAX_TURNS_DEFAULT,
    user_id: Optional[str] = None,
    sender_id: Optional[str] = None,
) -> str:
    """Summarizes the dialogue using the LLM.

    Args:
        tracker: the tracker to summarize
        llm: the LLM to use for summarization
        max_turns: maximum number of turns to summarize

    Returns:
        The summary of the dialogue.
    """
    prompt = _create_summarization_prompt(tracker, max_turns)
    metadata = {
        LANGFUSE_METADATA_USER_ID: user_id or "unknown",
        LANGFUSE_METADATA_SESSION_ID: sender_id or "",
        LANGFUSE_CUSTOM_METADATA_DICT: {"component": "summarize_conversation"},
        LANGFUSE_TAGS: ["summarize_conversation"],
    }
    try:
        llm_response = await llm.acompletion(prompt, metadata)
        summarization = llm_response.choices[0].strip()
        structlogger.debug(
            "summarization.success", summarization=summarization, prompt=prompt
        )
        return summarization
    except Exception as e:
        transcript = tracker_as_readable_transcript(tracker, max_turns=max_turns)
        structlogger.error("summarization.error", error=e)
        return transcript
