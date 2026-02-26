from dotenv import load_dotenv
from langchain_openrouter import ChatOpenRouter
load_dotenv()


model = ChatOpenRouter(
    model="arcee-ai/trinity-large-preview:free"
)

response = model.invoke("What is the capital of India?")
# print(response)
print(response.content)