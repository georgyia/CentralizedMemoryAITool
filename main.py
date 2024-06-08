import json
from convChain import invoke_single_chain

def main():
    user_input = ''
    try:
        while user_input.lower() != 'exit':
            user_input = input("Please enter your input: ")
            chatID = 123
            output = invoke_single_chain(user_input, chatID)
    except KeyboardInterrupt:
        print("\nInterrupted by user. Exiting...")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()