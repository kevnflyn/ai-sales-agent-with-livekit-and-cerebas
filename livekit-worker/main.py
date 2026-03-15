import os
from dotenv import load_dotenv
from livekit import agents
from livekit.agents import Agent, AgentSession, JobContext, WorkerOptions, cli
from livekit.plugins import openai, silero, cartesia
from pathlib import Path

from agents.sales_agent import SalesAgent

load_dotenv()

# Set the API key in environment variables (required for the services to work)
os.environ["CARTESIA_API_KEY"] = os.getenv("CARTESIA_API_KEY")
os.environ["CEREBRAS_API_KEY"] = os.getenv("CEREBRAS_API_KEY")

async def entrypoint(ctx: JobContext):
    await ctx.connect()
    agent = SalesAgent()
    session = AgentSession()
    await session.start(room=ctx.room, agent=agent)

if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            # plus your LiveKit host/key/secret via env or options
            ws_url=os.getenv("LIVEKIT_URL"),
            api_key=os.getenv("LIVEKIT_API_KEY"),
            port=os.getenv("LIVEKIT_PORT")
        )
    )
