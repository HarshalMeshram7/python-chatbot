
def bot_response(user_input):
    if not user_input:
        return "Please provide some input." 
    elif user_input == "hello" or user_input == "hi":
        return "Hello! How can I assist you today?"
    elif user_input == "help":
        return "How can I help you? You can ask me anything."
    elif user_input == "what is your name?":
        return "I am a chatbot created to assist you."
    elif user_input == "how are you?":
        return "I'm just a program, but thanks for asking! How can I help you?"
    elif user_input == "thank you":
        return "You're welcome! If you have any more questions, feel free to ask."
    else:
        return "I'm not sure how to respond to that. Can you please rephrase or ask something else?"
    
def main():
    print("Welcome to the chatbot! Type 'exit', 'quit', 'stop', or 'bye' to end the conversation.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "stop", "bye"]:
            print("Bot: Goodbye!")
            break
        response = bot_response(user_input)
        print("Bot:", response)
        
    
if __name__ == "__main__":
    main()