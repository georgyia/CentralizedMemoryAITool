from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
import openai
import json

# Setup for OpenAI and models
openai_api_key = "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"

model = ChatOpenAI(model="gpt-4", api_key=openai_api_key)
output_parser = StrOutputParser()

def analysis_agent_bot(input_str, output_str):
    # Pass the chat history to the model and ask it to find important information about the user
    response = model.invoke(f"""
You are an intelligent analysis agent. Your task is to analyze the answer , and extract any important information about the user. The information should be as precise and concise as possible.

Here is the query from the user:

{input_str}

Here is the answer from the bot:

{output_str}

***Important Instruction***

If there is no information about the user in the conversation, then just write - "No information"

******

You should look for information such as the user's name, age, hobbies, city of residence, interests, job, and any other relevant details.

For example, if the conversation history is:

"user": "hello, I am George, I study at MIT" "bot": "Hello George! How can I assist you today?" "user": "I need some assistance in AI for my startup" "bot": "Sure. What is your question?" "user": "Thank you so much, I am happy that you can help" "bot": "Sure."

You should extract the following information:

- Name: George
- Education: Studying at MIT
- Interests: Wants to found a startup in the field of AI

Now, please analyze the given conversation history and extract any important information about the user if there are some.
""")
    important_info = output_parser.parse(response)
    # Save the important information to a file
    return important_info.content

def analysis_agent_user(input_str):
    # Pass the chat history to the model and ask it to find important information about the user
    response = model.invoke(f"""
You are an intelligent analysis agent. Your task is to analyze the text about from the user, and extract any important information about the user. The information should be as precise and concise as possible.

Here is the conversation history:

{input_str}

***Important Instruction***

If there is no information about the user in the conversation, then just write - "No information"

******

You should look for information such as the user's name, age, hobbies, city of residence, interests, job, and any other relevant details.

For example, if the conversation history is:

"user": "hello, I am George, I study at MIT" "bot": "Hello George! How can I assist you today?" "user": "I need some assistance in AI for my startup" "bot": "Sure. What is your question?" "user": "Thank you so much, I am happy that you can help" "bot": "Sure."

You should extract the following information:

- Name: George
- Education: Studying at MIT
- Interests: Wants to found a startup in the field of AI

Now, please analyze the given conversation history and extract any important information about the user if there are some.
""")
    important_info = output_parser.parse(response)
    # Save the important information to a file
    return important_info.content

if __name__ == "__main__":
    analysis_agent()