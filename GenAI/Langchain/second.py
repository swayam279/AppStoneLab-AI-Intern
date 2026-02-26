from dotenv import load_dotenv

load_dotenv()
from langchain_openrouter import ChatOpenRouter

model = ChatOpenRouter(
    model="liquid/lfm-2.5-1.2b-thinking:free"
)

response = model.invoke("Write a long poem about the sky.")
# print(response)
print(response.content)