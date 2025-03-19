# Main.py
import tkinter as tk  # EN: Import tkinter for GUI / SV: Importera tkinter för gränssnitt
from Ai import AI  # EN: Import AI class for chatbot responses / SV: Importera AI-klassen för chatbotens svar
from chatbot_gui import ChatbotApp  # EN: Import chatbot GUI / SV: Importera chatbot GUI

class MainApp:
    """EN: Main application class for Mental Health Chatbot.
       SV: Huvudapplikationsklass för Mental Health Chatbot."""

    def __init__(self):
        """EN: Initializes main application components.
           SV: Initierar huvudapplikationen och dess komponenter."""
        self.root = tk.Tk()  # EN: Create main Tkinter window / SV: Skapa Tkinter huvudfönster
        self.ai = AI()  # EN: Create AI instance for generating responses / SV: Skapa AI-instans för att generera svar
        self.chatbot_app = ChatbotApp(self.root, self.get_ai_response)  # EN: Initialize GUI with AI response function / SV: Initiera GUI med AI-svarsfunktion

    def get_ai_response(self, user_message):
        """EN: Get AI response for user message.
           SV: Hämta AI-svar baserat på användarens meddelande."""
        return self.ai.generate_response(user_message)

    def run(self):
        """EN: Starts the GUI application loop.
           SV: Startar GUI-applikationens huvudloop."""
        self.root.mainloop()

if __name__ == "__main__":
    app = MainApp()  # EN: Create MainApp instance / SV: Skapa instans av MainApp
    app.run()        # EN: Run the application / SV: Starta applikationen

# Installation of required packages / Installation av nödvändiga paket:
# pip install openai gtts tkinter
# pip install requests pillow
# pip install firebase-admin
# pip install matplotlib
