import gradio as gr
from gradio_agentchatbot_5 import (
    AgentChatbot,
    ChatMessage,
)
from dotenv import load_dotenv
from langchain_demo import agent_executor as langchain_agent

from pathlib import Path

current_dir = Path(__file__).parent

load_dotenv()


# Import tool from Hub
async def interact_with_langchain_agent(prompt, messages):
    messages.append(ChatMessage(role="user", content=prompt))
    yield messages
    async for chunk in langchain_agent.astream({"input": prompt}):
        if "steps" in chunk:
            for step in chunk["steps"]:
                messages.append(
                    ChatMessage(
                        role="assistant",
                        content=step.action.log,
                        thought_metadata={"tool_name": step.action.tool},
                    )
                )
                yield messages
        if "output" in chunk:
            messages.append(ChatMessage(role="assistant", content=chunk["output"]))
            yield messages


with gr.Blocks() as demo:
    with gr.Tabs():
        with gr.Tab("Langchain Demo"):
            gr.Markdown("# Chat with a LangChain Agent 🦜⛓️ and see its thoughts 💭")
            chatbot_2 = AgentChatbot(
                label="Agent",
                avatar_images=[
                    None,
                    "https://em-content.zobj.net/source/twitter/141/parrot_1f99c.png",
                ],
            )
            input_2 = gr.Textbox(lines=1, label="Chat Message")
            input_2.submit(
                interact_with_langchain_agent, [input_2, chatbot_2], [chatbot_2]
            )
        with gr.Tab("Docs"):
            gr.Markdown(Path(current_dir / "docs.md").read_text())


if __name__ == "__main__":
    demo.launch()
