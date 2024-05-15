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

groq_client  = Groq(
    api_key=API_KEY,
)

if TOKEN is None:
    raise ValueError("TOKEN environment variable is not set")

class MyClient(discord.Client):

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
            chat = ChatGroq(temperature=0.5, groq_api_key=API_KEY, model_name="llama3-70b-8192")
            human = "{text}"
            prompt = ChatPromptTemplate.from_messages([("human", human)])
            chain = prompt | chat
            
            ans = chain.invoke({"text": stripped_message})
            content = ans.content if hasattr(ans, 'content') else "Sorry, I didn't understand that."
            
            # Truncate the content if it's longer than 2000 characters
            if len(content) > 2000:
                content = content[:2000]
                
            await message.reply(content, mention_author=True)
        
client = MyClient(intents=intents)
client.run(TOKEN)
