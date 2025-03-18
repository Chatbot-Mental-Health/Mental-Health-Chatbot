# about_window.py

import tkinter as tk


class AboutWindow(tk.Toplevel):
    """Fönster för 'Om Mental Health Chatbot'-informationen"""

    def __init__(self, parent, user, main_root):
        super().__init__(parent)
        self.parent = parent  # Föräldrafönstret (brukar vara root)
        self.user = user      # Användarinfo om det behövs
        self.main_root = main_root  # Huvudfönstret som vi vill dölja

        self.title("Om Mental Health Chatbot")
        self.geometry("600x400")

        # Dölj huvudfönstret om det är synligt
        if self.main_root.winfo_exists():
            self.main_root.withdraw()

        # Centrera fönstret
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = 600
        window_height = 400
        position_x = (screen_width - window_width) // 2
        position_y = (screen_height - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

        about_info = """
1. Programnamn: Mental Health Chatbot
2. Version:     1.0
3. Utvecklare: Morgan Lindbom, Yousef Martaa, Kotaiba Alabdullah, Oleh Doshchuk

4. Beskrivning:
Mental Health Chatbot är en AI-driven chattapplikation designad för att
erbjuda stöd och samtal kring mental hälsa.

Programmet använder OpenAI:s AI för att generera empatiska och stödjande
svar, samtidigt som användarnas humörhistorik lagras och visualiseras i grafer.
"""

        text_widget = tk.Text(self, wrap="word", font=("Arial", 12))
        text_widget.pack(expand=True, fill="both", padx=10, pady=10)
        text_widget.insert("1.0", about_info)
        text_widget.config(state="disabled")

        # Hantera fönsterstängning korrekt
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        """Återställ huvudfönstret när 'Om'-fönstret stängs"""
        if self.main_root.winfo_exists():
            self.main_root.deiconify()  # Visa huvudfönstret igen
        self.destroy()  # Stäng 'Om'-fönstret
