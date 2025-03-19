import tkinter as tk


class AboutWindow(tk.Toplevel):
    """Window for 'About Mental Health Chatbot' information
    Fönster för 'Om Mental Health Chatbot'-informationen"""

    def __init__(self, parent, user, main_root):
        super().__init__(parent)
        self.parent = parent                  # Parent window (usually root) | Föräldrafönster (vanligtvis root)
        self.user = user                      # User information if needed   | Användarinformation om det behövs
        self.main_root = main_root            # Main window to hide          | Huvudfönstret som vi vill dölja

        self.title("About Mental Health Chatbot")
        self.geometry("600x400")

        # Hide the main window if visible
        # Dölj huvudfönstret om det är synligt
        if self.main_root.winfo_exists():
            self.main_root.withdraw()

        # Center the window on the screen
        # Centrera fönstret på skärmen
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = 600
        window_height = 400
        position_x = (screen_width - window_width) // 2
        position_y = (screen_height - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

        # Information about the application
        # Information om applikationen
        about_info = """
1. Application Name: Mental Health Chatbot
2. Version:          1.0
3. Developers:       Morgan Lindbom, Yousef Martaa, Kotaiba Alabdullah, Oleh Doshchuk, Muhammad Huzaifa

4. Description:
Mental Health Chatbot is an AI-driven chat application designed to
offer support and conversation around mental health.

The application utilizes OpenAI's AI to generate empathetic and supportive
responses, while also storing users' mood history and visualizing it through graphs.
"""

        # Text widget displaying the about information
        # Text-widget som visar 'om'-informationen
        text_widget = tk.Text(self, wrap="word", font=("Arial", 12))
        text_widget.pack(expand=True, fill="both", padx=10, pady=10)
        text_widget.insert("1.0", about_info)
        text_widget.config(state="disabled")

        # Handle window closing properly
        # Hantera stängning av fönstret korrekt
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        """Restore main window when About window is closed
        Återställ huvudfönstret när 'Om'-fönstret stängs"""
        if self.main_root.winfo_exists():
            self.main_root.deiconify()    # Show the main window again | Visa huvudfönstret igen
        self.destroy()                    # Close About window         | Stäng 'Om'-fönstret
