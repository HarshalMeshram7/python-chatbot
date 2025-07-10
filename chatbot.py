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
    user_name = None
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
        
        if "my name is" in user_input:
            user_name = user_input.split("my name is")[-1].strip()
            response = f"Nice to meet you, {user_name}!"
        elif "what is your name" in user_input:
            if user_name is not None:
                response = f"My name is Chatbot. Nice to meet you, {user_name}!"
            else:
                response = "My name is Chatbot. What's your name?"
        elif "what is my name" in user_input:
            if user_name is not None:
                response = f"Your name is {user_name}."
            else:
                response = "I don't know your name yet."
        else: 
            for key in responses:
                if key in user_input:
                    response = responses[key]
                    break
        print("Bot:", response)
        
    
if __name__ == "__main__":
    main()