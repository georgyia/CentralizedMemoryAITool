import json
from convChain import invoke_single_chain
from info_analyser import analysis_agent

def main():
    chat_history = []
    user_input = ''
    try:
        while user_input.lower() != 'exit':
            chat_history = invoke_single_chain(chat_history)
            with open('history.json', 'w') as f:
                json.dump(chat_history, f)
            user_input = chat_history[-1]['user'] if 'user' in chat_history[-1] else ''
    except KeyboardInterrupt:
        print("\nInterrupted by user. Exiting...")
    except Exception as e:
        print(f"An error occurred: {e}")

    # analysis_agent()

if __name__ == "__main__":
    main()