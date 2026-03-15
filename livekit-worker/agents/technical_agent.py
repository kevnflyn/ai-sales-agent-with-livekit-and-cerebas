from livekit.agents import Agent
from livekit.plugins import openai, silero, cartesia
from livekit.agents import function_tool
from utils.load_context import load_context

class TechnicalAgent(Agent):
    """Technical specialist for detailed product specifications"""

    def __init__(self):
        context = load_context()

        llm = openai.LLM.with_cerebras(model="llama3.1-8b") # gpt-oss-120b or llama3.1-8b
        stt = cartesia.STT()
        tts = cartesia.TTS(voice="bf0a246a-8642-498a-9950-80c35e9276b5")
        vad = silero.VAD.load()

        instructions = f"""
        You are a technical specialist communicating by voice. All text that you return
        will be spoken aloud, so don't use things like bullets, slashes, or any
        other non-pronouncable punctuation.

        You specialize in technical details, specifications, and implementation questions.
        Focus on technical accuracy and depth.

        You have access to the following company information:

        {context}

        CRITICAL RULES:
        - ONLY use information from the context above
        - Focus on technical specifications and features
        - Explain technical concepts clearly for non-technical users
        - DO NOT make up technical details

        You can transfer to other specialists:
        - Use switch_to_sales() to return to general sales
        - Use switch_to_pricing() for pricing questions
        """

        super().__init__(
            instructions=instructions,
            stt=stt, llm=llm, tts=tts, vad=vad
        )

    async def on_enter(self):
        """Called when entering this agent"""
        print("Current Agent: 💻 Technical Specialist 💻")
        await self.session.say("Hi, I'm the technical specialist. I can help you with detailed technical questions about our products.")

    @function_tool
    async def switch_to_sales(self):
        """Switch to a sales representative"""
        from agents.sales_agent import SalesAgent
        await self.session.generate_reply(user_input="Confirm you are transferring to the sales team")
        return SalesAgent()

    @function_tool
    async def switch_to_pricing(self):
        """Switch to pricing specialist"""
        from agents.pricing_agent import PricingAgent
        await self.session.generate_reply(user_input="Confirm you are transferring to a pricing specialist")
        return PricingAgent()

print("✅ Technical Agent ready")

