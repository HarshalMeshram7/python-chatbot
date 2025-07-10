import json

file_path = 'responses.json'

def load_json(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
        return None
    except json.JSONDecodeError:
        print(f"Error: The file {file_path} is not a valid JSON file.")
        return None
    return data

def main():
    print("Welcome to the chatbot! Type 'exit', 'quit', 'stop', or 'bye' to end the conversation.")
    while True:
        user_input = input("You: ").lower()
        if user_input.lower() in ["exit", "quit", "stop", "bye"]:
            print("Bot: Goodbye!")
            break
        responses = load_json(file_path)
        if responses is None:
            print("Bot: Sorry, I cannot respond at the moment.")
            continue
        response = "I'm not sure how to respond to that."
        for key in responses:
            if key in user_input:
                response = responses[key]
                break
        print("Bot:", response)
        
    
if __name__ == "__main__":
    main()