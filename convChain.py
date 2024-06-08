from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
import time
import openai

openai_api_key = "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"

model = ChatOpenAI(model="gpt-3.5-turbo", api_key=openai_api_key)
output_parser = StrOutputParser()

def invoke_single_chain(chat_history):
    user_input = input("Please enter your input: ")
    chat_history.append({"user": user_input})

    # POST API CALL to send the query information
    # GET API CALL to receive important information

    try:
        response = model.invoke(user_input) # add important information
        print(user_input)
        answer = output_parser.parse(response)
        # POST API CALL to send the queanswer information

    except openai.RateLimitError as e:
        print(f"Rate limit exceeded. Retrying in {delay} seconds...")
        time.sleep(delay)
        raise Exception("Failed to complete request after several retries.")

    print("Bot: ", answer.content)
    chat_history.append({"bot": answer.content})

    return chat_history