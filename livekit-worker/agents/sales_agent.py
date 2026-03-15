from livekit.agents import Agent
from livekit.plugins import openai, silero, cartesia
from livekit.agents import function_tool
from utils.load_context import load_context

class SalesAgent(Agent):
    def __init__(self):
        context = load_context()

        llm = openai.LLM.with_cerebras(model="gpt-oss-120b")
        stt = cartesia.STT()
        tts = cartesia.TTS()
        vad = silero.VAD.load()

        # Put ALL context in system instructions
        instructions = f"""
        You are a sales agent communicating by voice. All text that you return
        will be spoken aloud, so don't use things like bullets, slashes, or any
        other non-pronouncable punctuation.

        You have access to the following company information:

        {context}

        CRITICAL RULES:
        - ONLY use information from the context above
        - If asked about something not in the context, say "I don't have that information"
        - DO NOT make up prices, features, or any other details
        - Quote directly from the context when possible
        - Be a sales agent but only use the provided information
        """

        super().__init__(
            instructions=instructions,
            stt=stt, llm=llm, tts=tts, vad=vad
        )

    # This tells the Agent to greet the user as soon as they join, with some context about the greeting.
    async def on_enter(self):
        print("Current Agent: 🏷️ Sales Agent 🏷️")
        self.session.generate_reply(user_input="Give a short, 1 sentence greeting. Offer to answer any questions.")

    @function_tool
    async def switch_to_tech_support(self):
        """Switch to a technical support rep"""
        from agents.technical_agent import TechnicalAgent
        await self.session.generate_reply(user_input="Confirm you are transferring to technical support")
        return TechnicalAgent()

    @function_tool
    async def switch_to_pricing(self):
        """Switch to pricing specialist"""
        from agents.pricing_agent import PricingAgent
        await self.session.generate_reply(user_input="Confirm you are transferring to a pricing specialist")
        return PricingAgent()

print("✅ Sales Agent class ready")