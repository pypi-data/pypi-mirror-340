from pydantic import Field
from gradio.data_classes import GradioModel, FileData, GradioRootModel
from typing import Literal, List, Generator, Optional, Union


class ThoughtMetadata(GradioModel):
    tool_name: Optional[str] = None
    error: bool = False


class Message(GradioModel):
    role: Literal["user", "assistant"]
    thought_metadata: ThoughtMetadata = Field(default_factory=ThoughtMetadata)


class ChatMessage(Message):
    content: str


class ChatFileMessage(Message):
    file: FileData
    alt_text: Optional[str] = None


class ChatbotData(GradioRootModel):
    root: List[Union[ChatMessage, ChatFileMessage]]


def pull_message(step_log: dict):
    if step_log.get("rationale"):
        yield ChatMessage(
            role="assistant", content=step_log["rationale"], thought=True
        )
    if step_log.get("tool_call"):
        used_code = step_log["tool_call"]["tool_name"] == "code interpreter"
        content = step_log["tool_call"]["tool_arguments"]
        if used_code:
            content = f"```py\n{content}\n```"
        yield ChatMessage(
            role="assistant",
            thought_metadata=ThoughtMetadata(
                tool_name=step_log["tool_call"]["tool_name"]
            ),
            content=content,
            thought=True,
        )
    if step_log.get("observation"):
        yield ChatMessage(
            role="assistant", content=f"```\n{step_log['observation']}\n```", thought=True
        )
    if step_log.get("error"):
        yield ChatMessage(
            role="assistant",
            content=str(step_log["error"]),
            thought=True,
            thought_metadata=ThoughtMetadata(error=True),
        )
