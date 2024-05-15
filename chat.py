from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")

chat = ChatGroq(temperature=0, groq_api_key=API_KEY, model_name="llama3-8b-8192")

system = "You are a helpful assistant."
human = "{text}"
prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])

chain = prompt | chat
ans = chain.invoke({"text": "Count from 1 to 10"})
print(ans)