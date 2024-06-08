from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
import time
import openai
import json
import requests

openai_api_key = "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"

model = ChatOpenAI(model="gpt-3.5-turbo", api_key=openai_api_key)
output_parser = StrOutputParser()

def invoke_single_chain(chat_history):
    user_input = input("Please enter your input: ")
    chat_history.append({"user": user_input})

    # Check if the information is important

    # POST API CALL to send the query information

    url_add = "http://localhost:8000/addToCentralizedMemory"
    payload_add = {
        "content": {
            "text": user_input
        },
        "collection": "Georgy"
    }
    headers = {
        "Content-Type": "application/json"
    }
    response_add = requests.post(url_add, json=payload_add, headers=headers)
    print("Status Code for addToCentralizedMemory:", response_add.status_code)
    print("Response for addToCentralizedMemory:", response_add.json())

    # GET API CALL to receive important information

    # URL and payload for getFromCentralizedMemory
    url_get = "http://localhost:8000/getFromCentralizedMemory"
    payload_get = {
        "query": user_input,
        "collection": "Georgy" 
    }

    # Make POST request to getFromCentralizedMemory
    response_get = requests.post(url_get, json=payload_get, headers=headers)
    print("Status Code for getFromCentralizedMemory:", response_get.status_code)
    print("Response for getFromCentralizedMemory:", response_get.json())

    content_information = ' '.join(response_get.json().values())
    print(content_information)



    try:
        request = user_input + "\n Consider this important information as context to answer the user query: \n" + content_information
        response = model.invoke(request)
        print(request)

        answer_obj = output_parser.parse(response)
        answer = str(answer_obj.content)
        print(answer)


        # POST API CALL to send the queanswer information
        url_get = "http://localhost:8000/getFromCentralizedMemory"
        payload_get = {
            "query": answer,
            "collection": "Georgy" 
        }

        # Make POST request to getFromCentralizedMemory
        response_get = requests.post(url_get, json=payload_get, headers=headers)
        print("Status Code for getFromCentralizedMemory:", response_get.status_code)
        print("Response for getFromCentralizedMemory:", response_get.json())

    except openai.RateLimitError as e:
        print(f"Rate limit exceeded. Retrying in {delay} seconds...")
        time.sleep(delay)
        raise Exception("Failed to complete request after several retries.")

    print("Bot: ", answer)
    chat_history.append({"bot": answer})

    return chat_history