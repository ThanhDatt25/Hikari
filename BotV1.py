from groq import Groq 
import os
import discord
from langchain.chains import LLMChain
from dotenv import load_dotenv
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
        activity = discord.Activity(type=discord.ActivityType.listening, name="Spotify")
        await self.change_presence(activity=activity)

    async def on_message(self, message):
        at_mention = f'<@{self.user.id}>'
        if message.author == self.user:
            return

        if message.content.startswith(at_mention):
            stripped_message = message.content[len(at_mention):].strip()
            chat_completion = groq_client.chat.completions.create(
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a friendly and helpful girl chatbot named Hikari. Your owner is Dat. You are here to assist users with their questions and engage in pleasant conversations. Always respond with a warm and approachable tone, and be sure to offer kind and considerate answers."
                    },
                    {
                        "role": "user",
                        "content" : f"{stripped_message} ### Response: "
                    }
                ],
                model="Llama3-70b-8192",
                temperature=0.5,
                stop=None,
            )
            combined_response = chat_completion.choices[0].message.content
            if len(combined_response) > 2000:
                combined_response = combined_response[:2000]
            await message.reply(combined_response, mention_author = True)
            

client = MyClient(intents=intents)
client.run(TOKEN)
