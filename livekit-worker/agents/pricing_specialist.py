from livekit.agents import Agent
from livekit.plugins import openai, silero, cartesia
from livekit.agents import function_tool
from utils.load_context import load_context

class PricingAgent(Agent):
    """Pricing specialist for budget and cost discussions"""

    def __init__(self):
        context = load_context()

        llm = openai.LLM.with_cerebras(model="gpt-oss-120b")
        stt = cartesia.STT()
        tts = cartesia.TTS(voice="4df027cb-2920-4a1f-8c34-f21529d5c3fe")
        vad = silero.VAD.load()

        instructions = f"""
        You are a pricing specialist communicating by voice. All text that you return
        will be spoken aloud, so don't use things like bullets, slashes, or any
        other non-pronouncable punctuation.

        You specialize in pricing, budgets, discounts, and financial aspects.
        Help customers find the best value for their needs.

        You have access to the following company information:

        {SALES_CONTEXT}

        CRITICAL RULES:
        - ONLY use pricing information from the context above
        - Focus on value proposition and ROI
        - Help customers understand pricing tiers and options
        - DO NOT make up prices or discounts

        You can transfer to other specialists:
        - Use switch_to_sales() to return to general sales
        - Use switch_to_technical() for technical questions
        """

        super().__init__(
            instructions=instructions,
            stt=stt, llm=llm, tts=tts, vad=vad
        )

    async def on_enter(self):
        """Called when entering this agent"""
        print("Current Agent: 💰 Pricing Agent 💰")
        await self.session.say("Hello, I'm the pricing specialist. I can help you understand our pricing options and find the best value for your needs.")

    @function_tool
    async def switch_to_sales(self):
        """Switch back to sales representative"""
        await self.session.generate_reply(user_input="Confirm you are transferring to the sales team")
        from agents.sales_agent import SalesAgent
        return SalesAgent()

    @function_tool
    async def switch_to_technical(self):
        """Switch to technical specialist"""
        await self.session.generate_reply(user_input="Confirm you are transferring to technical support")
        from agents.technical_agent import TechnicalAgent
        return TechnicalAgent()

print("✅ Simple Pricing Agent ready")
