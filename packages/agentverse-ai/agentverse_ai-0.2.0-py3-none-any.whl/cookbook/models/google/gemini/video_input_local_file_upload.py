from pathlib import Path

from agentverse_ai.agent import Agent
from agentverse_ai.media import Video
from agentverse_ai.models.google import Gemini

agent = Agent(
    model=Gemini(id="gemini-2.0-flash-exp"),
    markdown=True,
)

# Get sample videos from https://www.pexels.com/search/videos/sample/
video_path = Path(__file__).parent.joinpath("sample_video.mp4")

agent.print_response("Tell me about this video?", videos=[Video(filepath=video_path)])
