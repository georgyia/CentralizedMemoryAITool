from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
import time
import openai

# Setup for OpenAI and models
openai_api_key = "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"

model = ChatOpenAI(model="gpt-3.5-turbo", api_key=openai_api_key)
output_parser = StrOutputParser()

def invoke_single_chain(chat_history):
    # Get user input
    user_input = input("Please enter your input: ")
    chat_history.append({"user": user_input})

    # Generate an answer using the model
    try:
        response = model.invoke(user_input)  # Pass string directly
        answer = output_parser.parse(response)
    except openai.RateLimitError as e:
        print(f"Rate limit exceeded. Retrying in {delay} seconds...")
        time.sleep(delay)
        raise Exception("Failed to complete request after several retries.")

    # Print the answer and save it in the chat history
    print("Bot: ", answer.content)  # Assuming AIMessage has a content attribute
    chat_history.append({"bot": answer.content})  # Save only the content of the answer

    return chat_history