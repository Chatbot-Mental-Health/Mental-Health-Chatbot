# chatbot_gui.py

import tkinter as tk
from tkinter import scrolledtext, messagebox
from datetime import datetime
from firebase_service import FirebaseService
from login_window import LoginWindow
from history_window import HistoryWindow
from about_window import AboutWindow


class ChatbotApp:
    def __init__(self, root, ai_response_function):
        """
        Initializes the chatbot application.
        Initierar chatbot-applikationen.
        """
        self.root = root
        self.ai_response_function = ai_response_function
        self.root.title("Mental Health Chatbot")

        self.root.geometry("400x400")  # Sets window size / Ställer in fönsterstorlek
        self.root.minsize(300, 300)  # Sets minimum size / Ställer in minsta storlek

        self.root.configure(bg="#E8F6F3")  # Sets background color / Ställer in bakgrundsfärg

        self.firebase = FirebaseService()  # Initializes Firebase service / Initierar Firebase-tjänst
        self.is_logged_in = False  # Tracks login status / Spårar inloggningsstatus
        self.current_user = None  # Stores current user / Lagrar aktuell användare
        self.asked_mood = False  # Tracks if mood has been asked / Spårar om humör har frågats

        self.create_widgets()  # Calls function to create UI elements / Anropar funktion för att skapa UI-element
        self.center_window()  # Centers the window on screen / Centrerar fönstret på skärmen
        self.root.bind("<Configure>", self.on_resize)  # Binds resize event / Binder omstorlekshändelse

    def create_widgets(self):
        """
        Creates and configures all UI components.
        Skapar och konfigurerar alla UI-komponenter.
        """
        # Konfigurera root-layout för att stödja dynamisk storlek
        self.root.grid_rowconfigure(1, weight=1)  # Chat window should expand
        self.root.grid_rowconfigure(2, weight=0)  # Bottom frame should stay fixed
        self.root.grid_columnconfigure(0, weight=1)  # Full width

        # 🟢 Top Frame (for buttons & status)
        self.top_frame = tk.Frame(self.root, bg="#E8F6F3")
        self.top_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=5)

        # 🟢 Make buttons expand dynamically
        self.top_frame.grid_columnconfigure(0, weight=1)
        self.top_frame.grid_columnconfigure(1, weight=1)
        self.top_frame.grid_columnconfigure(2, weight=1)

        # 🔵 About button
        self.about_button = tk.Button(
            self.top_frame, text="About", command=self.show_about,
            font=("Arial", 12), bg="#5DADE2", fg="white"
        )
        self.about_button.grid(row=0, column=0, sticky="ew", padx=5)

        # 🔵 History button
        self.history_button = tk.Button(
            self.top_frame, text="Visa Historik", command=self.open_history_window,
            font=("Arial", 12), bg="#5DADE2", fg="white"
        )
        self.history_button.grid(row=0, column=1, sticky="ew", padx=5)

        # 🔵 Login/Logout button
        self.auth_button = tk.Button(
            self.top_frame, text="Logga in", command=self.open_login_window,
            font=("Arial", 12), bg="#5DADE2", fg="white"
        )
        self.auth_button.grid(row=0, column=2, sticky="ew", padx=5)

        # 🟢 Status Label (below buttons)
        self.status_label = tk.Label(
            self.top_frame, text="Inte inloggad", font=("Arial", 12), bg="#E8F6F3", fg="red"
        )
        self.status_label.grid(row=1, column=0, columnspan=3, sticky="ew", pady=5)

        # 🟠 Chat Window (Scrollable)
        self.chat_window = scrolledtext.ScrolledText(
            self.root, wrap=tk.WORD, state=tk.DISABLED,
            font=("Arial", 12), bg="white", fg="black"
        )
        self.chat_window.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)

        # 🟣 Bottom Frame (for input & send button)
        self.bottom_frame = tk.Frame(self.root)
        self.bottom_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=5)

        # Make input field and send button stretch
        self.bottom_frame.grid_columnconfigure(0, weight=4)  # Input field gets more space
        self.bottom_frame.grid_columnconfigure(1, weight=1)  # Send button

        # 🟡 User Input Field
        self.user_input = tk.Entry(self.bottom_frame, font=("Arial", 14), bg="white")
        self.user_input.grid(row=0, column=0, sticky="ew", padx=(0, 5))

        # 🟡 Send Button
        self.send_button = tk.Button(
            self.bottom_frame, text="Skicka", command=self.send_message,
            font=("Arial", 12), bg="#5DADE2", fg="white"
        )
        self.send_button.grid(row=0, column=1, sticky="ew")

        # Bind Enter key to send_message
        self.user_input.bind("<Return>", self.send_message)

        # Set focus on user input field
        self.user_input.focus()

    def center_window(self):
        """Centers the application window on the screen."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def show_about(self):
        """Öppnar 'Om'-fönstret"""
        AboutWindow(self.root, "current_user", self.root)  # Se till att du skickar rätt argument

    def on_resize(self, event):
        """Hanterar storleksändringar och anpassar gränssnittets element."""
        self.chat_window.config(width=event.width, height=event.height - 150)

    def open_login_window(self):
        """Öppnar inloggningsfönstret och gömmer huvudfönstret."""
        self.root.withdraw()
        login_root = tk.Toplevel(self.root)
        LoginWindow(login_root, self.on_login_success, self.root)

    def on_login_success(self, email, *args):
        """Uppdaterar UI och lagrar användarens e-post vid lyckad inloggning."""
        self.current_user = email
        self.is_logged_in = True
        self.status_label.config(text=f"Inloggad som {email}", fg="green")
        self.auth_button.config(text="Logga ut", command=self.logout)
        self.ask_for_mood()

    def ask_for_mood(self):
        """Ber användaren om sin sinnesstämning (0-10)."""
        today = datetime.now().strftime("%Y-%m-%d")
        existing_mood = self.firebase.get_user_mood(self.current_user, today)

        if existing_mood is not None:
            self.update_chat_window("How can I help you today?\n")
            return

        self.update_chat_window("How are you feeling today? (Enter a number between 0 and 10)\n")
        self.awaiting_mood_input = True

    def send_message(self, event=None):
        """Hanterar användarinmatning och AI-svar."""

        # Kontrollera om användaren är inloggad
        if not self.is_logged_in:
            messagebox.showwarning("Ej inloggad", "Logga in först för att använda chatten.")
            return

        # Hämta och rensa användarens meddelande
        user_message = self.user_input.get().strip()
        self.user_input.delete(0, tk.END)  # Rensar inmatningsfältet direkt

        # Om meddelandet är tomt, gör inget
        if not user_message:
            return

        # Lägg till meddelandet i chatten
        self.update_chat_window(f"You: {user_message}")

        # Hantera mood-input (om det väntas en siffra mellan 0 och 10)
        if getattr(self, 'awaiting_mood_input', False):
            try:
                mood = int(user_message)
                if 0 <= mood <= 10:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self.firebase.save_mood(self.current_user, mood)
                    self.update_chat_window(f"Mood registered as {mood} at {timestamp}.")
                    self.update_chat_window("How can I help you today?.")
                    self.awaiting_mood_input = False  # Avsluta mood-input-läge
                else:
                    self.update_chat_window("\nPlease enter a valid number between 0 and 10.\n")
                return  # Avsluta här, så vi inte skickar detta till AI:n
            except ValueError:
                self.update_chat_window("\nInvalid input. Please enter a number between 0 and 10.\n")
                return  # Avsluta här

        # *** Anropa AI för svar ***
        try:
            ai_response = self.ai_response_function(user_message)  # Hämta AI-svar
            self.update_chat_window(f"Bot: {ai_response}\n")
        except Exception as e:
            self.update_chat_window("Bot: Tyvärr, jag kan inte svara just nu.")
            print(f"Fel vid AI-anrop: {e}")  # Skriver ut felet i terminalen för debugging

    def update_chat_window(self, message):
        """Uppdaterar chattfönstret med ett nytt meddelande."""
        self.chat_window.config(state=tk.NORMAL)
        self.chat_window.insert(tk.END, message + "\n")
        self.chat_window.config(state=tk.DISABLED)
        self.chat_window.yview(tk.END)

    def logout(self):
        """Hanterar utloggning och rensar chattfönstret."""
        self.current_user = None
        self.is_logged_in = False
        self.status_label.config(text="Inte inloggad", fg="red")
        self.auth_button.config(text="Logga in", command=self.open_login_window)
        self.chat_window.config(state=tk.NORMAL)
        self.chat_window.delete("1.0", tk.END)
        self.chat_window.config(state=tk.DISABLED)

    def focus_user_input(self, event=None):
        self.user_input.focus_set()
        self.user_input.update_idletasks()

    def open_history_window(self):
        """Öppnar fönstret för att visa chattens historik och gömmer huvudfönstret."""
        if not self.is_logged_in:
            messagebox.showwarning("Ej inloggad", "Logga in först för att visa historik.")
            return

        self.root.withdraw()  # Dölj huvudfönstret

        history_root = tk.Toplevel(self.root)
        HistoryWindow(history_root, self.current_user, self.root)

    def scroll_chat_to_bottom(self):
        """Scrollar chattfönstret till botten så att senaste meddelandet syns."""
        self.chat_window.yview_moveto(1.0)
