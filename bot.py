from groq import Groq
import os
import discord
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import asyncio

load_dotenv()

TOKEN = os.getenv("TOKEN")
API_KEY = os.getenv("GROQ_API_KEY")

intents = discord.Intents.default()
intents.message_content = True

if TOKEN is None:
    raise ValueError("TOKEN environment variable is not set")

class MyClient(discord.Client):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_conversations = {}

    async def on_ready(self):
        print('Logged on as', self.user)
        activity = discord.Activity(type=discord.ActivityType.listening, name="Hikari~~")
        await self.change_presence(activity=activity)

    async def on_message(self, message):
        at_mention = f'<@{self.user.id}>'
        if message.author == self.user:
            return

        if message.content.startswith(at_mention):
            stripped_message = message.content[len(at_mention):].strip()

            user_id = message.author.id
            if user_id not in self.user_conversations:
                self.user_conversations[user_id] = []

            # Append the user's message to the conversation history
            self.user_conversations[user_id].append(f"Human: {stripped_message}")

            # Construct the conversation history prompt
            conversation_history = "\n".join(self.user_conversations[user_id])
            prompt_text = f"{conversation_history}\nAssistant:"
            system = "You are a friendly and cute girl chatbot named Hikari. Your owner is Dat. You love to chat with people like a close friend. Use a warm, approachable, and adorable tone in your responses. Always be kind, considerate, and engaging in your conversations. Remember to keep the chat fun and light-hearted!"
            chat = ChatGroq(temperature=0.5, groq_api_key=API_KEY, model_name="llama3-70b-8192")
            prompt = ChatPromptTemplate.from_messages([("system", system), ("human", prompt_text)])
            chain = prompt | chat

            try:
                ans = chain.invoke({"text": stripped_message})
                content = ans.content if hasattr(ans, 'content') else "Sorry, I didn't understand that."
            except Exception as e:
                content = f"An error occurred: {e}"

            # Save the assistant's response in the conversation history
            self.user_conversations[user_id].append(f"Assistant: {content}")

            # Truncate the content if it's longer than 2000 characters
            if len(content) > 2000:
                content = content[:2000]

            await message.reply(content, mention_author=True)

client = MyClient(intents=intents)
client.run(TOKEN)
