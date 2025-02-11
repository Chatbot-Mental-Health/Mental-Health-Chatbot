# Mental Health Chatbot

def get_response(user_input):
    # Dictionary of possible responses based on keywords
    responses = {
        "anxious": "I’m really sorry you’re feeling this way. Take a deep breath, and let’s take things one step at a time.",
        "lonely": "I’m here for you. You’re not alone, and it’s okay to feel this way sometimes.",
        "stressed": "That sounds tough. Have you tried taking small breaks during the day? It can help relieve some stress.",
        "sleeping": "Sleep can be difficult when your mind is racing. Have you tried calming techniques like deep breathing before bed?",
        "mental health": "It's great that you're acknowledging it. If you're feeling this way for a long time, it might help to talk to a professional for support.",
        "default": "I'm here to listen. Can you tell me more about how you're feeling?"
    }

    # Convert user input to lowercase for easier matching
    user_input = user_input.lower()

    # Check for keywords in the user input and return the corresponding response
    for keyword, response in responses.items():
        if keyword in user_input:
            return response
    
    # If no keyword matches, return the default response
    return responses["default"]

def main():
    print("Welcome to the Mental Health Chatbot!")
    print("Type 'exit' to end the conversation.")
    
    while True:
        user_input = input("User: ")
        
        # Exit condition
        if user_input.lower() == "exit":
            print("Chatbot: Thank you for talking with me. Take care!")
            break
        
        # Get the chatbot's response
        response = get_response(user_input)
        print(f"Chatbot: {response}")

if __name__ == "__main__":
    main()
