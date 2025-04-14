from pathlib import Path

from agentverse_ai.agent import Agent, RunResponse
from agentverse_ai.media import Image
from agentverse_ai.models.openai import OpenAIChat
from agentverse_ai.utils.audio import write_audio_to_file
from rich import print
from rich.text import Text

cwd = Path(__file__).parent.resolve()

image_agent = Agent(model=OpenAIChat(id="gpt-4o"))

image_path = Path(__file__).parent.joinpath("sample.jpg")
image_story: RunResponse = image_agent.run(
    "Write a 3 sentence fiction story about the image",
    images=[Image(filepath=image_path)],
)
formatted_text = Text.from_markup(
    f":sparkles: [bold magenta]Story:[/bold magenta] {image_story.content} :sparkles:"
)
print(formatted_text)

audio_agent = Agent(
    model=OpenAIChat(
        id="gpt-4o-audio-preview",
        modalities=["text", "audio"],
        audio={"voice": "alloy", "format": "wav"},
    ),
)

audio_story: RunResponse = audio_agent.run(
    f"Narrate the story with flair: {image_story.content}"
)
if audio_story.response_audio is not None:
    write_audio_to_file(
        audio=audio_story.response_audio.content, filename="tmp/sample_story.wav"
    )
