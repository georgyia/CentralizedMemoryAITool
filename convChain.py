from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
import time
import openai
import json
import requests
from info_analyser import analysis_agent_user, analysis_agent_bot

openai_api_key = "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"

model = ChatOpenAI(model="gpt-3.5-turbo", api_key=openai_api_key)
output_parser = StrOutputParser()

def invoke_single_chain(user_input, chatID):
    collection = "Georgy1"
    headers = {
        "Content-Type": "application/json"
    }
    print("\nUser input: " + user_input)

    # Check if the information is important
    important_info_input = analysis_agent_user(user_input)
    print("Important information retrieved: " + important_info_input + "\n")

    # POST API CALL to send the query information
    if important_info_input != "No information":
        url_add = "http://localhost:8000/addToCentralizedMemory"
        payload_add = {
            "content": {
                "text": important_info_input
            },
            "collection": collection
        }
        response_add = requests.post(url_add, json=payload_add, headers=headers)
        print("Status Code for addToCentralizedMemory:", response_add.status_code)

    # GET API CALL to receive important information

    # URL and payload for getFromCentralizedMemory
    url_get = "http://localhost:8000/getFromCentralizedMemory"
    payload_get = {
        "query": user_input,
        "collection": collection
    }

    # Make POST request to getFromCentralizedMemory
    response_get = requests.post(url_get, json=payload_get, headers=headers)
    print("Status Code for getFromCentralizedMemory:", response_get.status_code)

    content_information = ' '.join(response_get.json().values())
    print("\nImportant information retrieved: " + content_information)

    try:
        request = user_input + "\n Consider this important information as context to answer the user query: \n" + content_information
        response = model.invoke(request)
        print("\nRequest: " + request)

        answer_obj = output_parser.parse(response)
        answer = str(answer_obj.content)
        print(answer)

        important_info_bot = analysis_agent_bot(user_input,answer)

        # POST API CALL to send the queanswer information
        url_get = "http://localhost:8000/getFromCentralizedMemory"
        payload_get = {
            "query": important_info_bot,
            "collection": collection
        }

        # Make POST request to getFromCentralizedMemory
        response_get = requests.post(url_get, json=payload_get, headers=headers)
        print("Status Code for getFromCentralizedMemory:", response_get.status_code)

    except openai.RateLimitError as e:
        print(f"Rate limit exceeded. Retrying in {delay} seconds...")
        time.sleep(delay)
        raise Exception("Failed to complete request after several retries.")

    print("\nBot: ", answer)

    return answer