import tkinter as tk
from tkinter import simpledialog, scrolledtext

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
    return responses["default"]

def askuser():
    user_name = simpledialog.askstring("Nickname", "What do you wish for me to call you?")
    if not user_name:
        user_name = "User"
    display_welcome_message(user_name)
    return user_name

def display_welcome_message(user_name):
    chat_window.config(state=tk.NORMAL)
    chat_window.insert(tk.END, f"Chatbot: Hello {user_name}! I'm here to listen and support you.\n\n")
    chat_window.config(state=tk.DISABLED)
    return user_name

def send_message():
    user_text = user_input.get().strip()
    if not user_text:
        return

    chat_window.config(state=tk.NORMAL)
    chat_window.insert(tk.END, f"{current_user[0]}: {user_text}\n")

    if user_text.lower() == "exit":
        chat_window.insert(tk.END, f"Chatbot: Thank you for talking with me, {current_user[0]}. Take care!\n\n")
        root.after(2000, root.quit)
        return
    elif user_text.lower() == "change":
        current_user[0] = askuser()
        return

    response = get_response(user_text)
    chat_window.insert(tk.END, f"Chatbot: {response}\n\n")
    chat_window.config(state=tk.DISABLED)
    user_input.delete(0, tk.END)

root = tk.Tk()
root.title("Mental Health Chatbot")
root.geometry("400x500")
root.configure(bg="#E8F6F3")

chat_window = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED, font=("Arial", 12), bg="white", fg="black", height=20)
chat_window.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

user_input = tk.Entry(root, font=("Arial", 14), bg="white")
user_input.pack(padx=10, pady=5, fill=tk.X)

button_frame = tk.Frame(root, bg="#E8F6F3")
button_frame.pack(pady=5)

send_button = tk.Button(button_frame, text="Send", command=send_message, font=("Arial", 12), bg="#48C9B0", fg="white")
send_button.pack(side=tk.LEFT, padx=5)

change_name_button = tk.Button(button_frame, text="Change Name", command=lambda: current_user.__setitem__(0, askuser()), font=("Arial", 12), bg="#5DADE2", fg="white")
change_name_button.pack(side=tk.LEFT, padx=5)

current_user = [askuser()]

root.mainloop()
