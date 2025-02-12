                                            #MENTAL HEALTH CHATBOT
def get_response(user_input):
    
    responses = {
        "anxious": "I’m really sorry you’re feeling this way. Take a deep breath, and let’s take things one step at a time.",
        "lonely": "I’m here for you. You’re not alone, and it’s okay to feel this way sometimes.",
        "stressed": "That sounds tough. Have you tried taking small breaks during the day? It can help relieve some stress.",
        "sleeping": "Sleep can be difficult when your mind is racing. Have you tried calming techniques like deep breathing before bed?",
        "mental health": "It's great that you're acknowledging it. If you're feeling this way for a long time, it might help to talk to a professional for support.",
        "default": "I'm here to listen. Can you tell me more about how you're feeling?"
    }

    
    user_input = user_input.lower()

   
    for keyword, response in responses.items():
        if keyword in user_input:
            return response
    
    # If no keyword matches, return the default response
    return responses["default"]


def askuser():
    """
    Function to ask the user for their nickname and display a personalized message.
    """
    user_name = input("What do you wish for me to call you as?\n")
    display_welcome_message(user_name)
    return user_name


def display_welcome_message(user_name):
    """
    Function to display a welcome message using the user's nickname.
    Args:
        user_name (str): The user's nickname.
    """
    print(f"Hello {user_name}! I'm here to listen and support you. Feel free to share how you're feeling, and let's talk.")


def main():
    print("Welcome to the Mental Health Chatbot!")
    print("Type 'exit' to end the conversation.")
    print("Type 'change' to change your name as used by the chatbot.")

    # Ask the user for their nickname
    user_name = askuser()

    while True:
        user_input = input(f"{user_name}: ")

# Exit condition
        if user_input.lower() == "exit":
            print(f"Chatbot: Thank you for talking with me, {user_name}. Take care!")
            break

 # Change name condition
        elif user_input.lower() == "change":
            user_name = askuser()

        
        else:
            response = get_response(user_input)
            print(f"Chatbot: {response}")

if __name__ == "__main__":
    main()
