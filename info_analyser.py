from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
import openai
import json

# Setup for OpenAI and models
openai_api_key = "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"

model = ChatOpenAI(model="gpt-3.5-turbo", api_key=openai_api_key)
output_parser = StrOutputParser()

def analysis_agent():
    with open('history.json', 'r') as f:
        chat_history = json.load(f)
    # Convert the chat history into a string
    chat_history_str = '\n'.join([f"{item['user'] if 'user' in item else 'Bot'}: {item['user'] if 'user' in item else item['bot']}" for item in chat_history])
    # Pass the chat history to the model and ask it to find important information about the user
    response = model.invoke(f"""
You are an intelligent analysis agent. Your task is to analyze the conversation history between a user and a bot, and extract any important information about the user. The information should be as precise and concise as possible.

Here is the conversation history:

{chat_history_str}

If there is no information about the user in the conversation, you don't need to provide any output.

You should look for information such as the user's name, age, hobbies, city of residence, interests, job, and any other relevant details.

For example, if the conversation history is:

"user": "hello, I am Georgy, I study at TUM" "bot": "Hello Georgy! How can I assist you today?" "user": "I need some assistance in AI for my startup" "bot": "Sure. What is your question?" "user": "Thank you so much, I am happy that you can help" "bot": "Sure."

You should extract the following information:

- Name: Georgy
- Education: Studying at TUM
- Interests: Wants to found a startup in the field of AI

Now, please analyze the given conversation history and extract any important information about the user.
""")
    important_info = output_parser.parse(response)
    # Api call centralised memory
    # Save the important information to a file
    with open('./infos/important_information.json', 'w') as f:
        json.dump({"important_info": important_info.content}, f)

if __name__ == "__main__":
    analysis_agent()