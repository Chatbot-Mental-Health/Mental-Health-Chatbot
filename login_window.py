import tkinter as tk
from tkinter import messagebox
from firebase_service import FirebaseService


class LoginWindow:
    """Handles the login window for Mental Health Chatbot.
    Hanterar inloggningsfönstret för Mental Health Chatbot."""

    def __init__(self, root, on_login_success, main_window):
        """Initializes the login window.
        Initierar inloggningsfönstret."""
        self.root = root
        self.on_login_success = on_login_success
        self.main_window = main_window  # EN: Reference to main window / SV: Referens till huvudfönstret
        self.firebase = FirebaseService()  # EN: Initialize Firebase service / SV: Initiera Firebase-tjänst

        self.root.title("Log in")
        self.root.geometry("300x250")
        self.root.resizable(False, False)

        self.center_window()  # EN: Center window on screen / SV: Centrera fönstret på skärmen
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)  # EN: Handle window close event / SV: Hantera stängning av fönster

        self.create_widgets()  # EN: Create GUI elements / SV: Skapa GUI-komponenter

    def center_window(self):
        """Centers the login window on the screen.
        Centrerar inloggningsfönstret på skärmen."""
        self.root.update_idletasks()
        width, height = 300, 250
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def create_widgets(self):
        """Creates and arranges all GUI elements in the window.
        Skapar och placerar alla GUI-komponenter i fönstret."""
        self.frame = tk.Frame(self.root, padx=10, pady=10)
        self.frame.pack(expand=True, fill="both")

        # Title / Titel
        self.title_label = tk.Label(self.frame, text="Log in", font=("Arial", 14, "bold"))
        self.title_label.pack(pady=(0, 10))

        # Email field / E-postfält
        self.email_label = tk.Label(self.frame, text="Email:", font=("Arial", 10))
        self.email_label.pack(anchor="w")
        self.email_entry = tk.Entry(self.frame, font=("Arial", 12), width=25)
        self.email_entry.pack(pady=2)
        self.email_entry.insert(0, "mogge@kalle.com")

        # Password field / Lösenordsfält
        self.password_label = tk.Label(self.frame, text="Password:", font=("Arial", 10))
        self.password_label.pack(anchor="w")
        self.password_entry = tk.Entry(self.frame, font=("Arial", 12), width=25, show="*")
        self.password_entry.pack(pady=2)
        self.password_entry.insert(0, "123456")

        # Button frame / Knappsektion
        self.button_frame = tk.Frame(self.frame)
        self.button_frame.pack(pady=10)

        # Cancel button / Avbryt-knapp
        self.cancel_button = tk.Button(
            self.button_frame, text="Cancel", font=("Arial", 10), width=10, command=self.on_close
        )
        self.cancel_button.pack(side="left", padx=5)

        # Login button / Inloggningsknapp
        self.login_button = tk.Button(
            self.button_frame, text="Log in", font=("Arial", 10), width=10, command=self.on_login
        )
        self.login_button.pack(side="left", padx=5)

    def on_login(self):
        """Handles login and validates user credentials.
        Hanterar inloggning och validerar användaruppgifter."""
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        if not email or not password:
            messagebox.showwarning("Error", "Both email and password must be filled in.")
            return

        response = self.firebase.authenticate_user(email, password)

        if response["success"]:
            self.root.destroy()  # EN: Close login window / SV: Stäng inloggningsfönstret
            self.main_window.deiconify()  # EN: Show main window / SV: Visa huvudfönstret
            self.on_login_success(email)
        else:
            self.handle_failed_login(email, password)

    def handle_failed_login(self, email, password):
        """Handles failed login attempts and offers account creation.
        Hanterar misslyckad inloggning och erbjuder kontoskapande."""
        create_account = messagebox.askyesno(
            "Account not found", "No user found. Would you like to create an account?"
        )

        if create_account:
            register_response = self.firebase.register_user(email, password)
            if register_response["success"]:
                messagebox.showinfo("Success", "Account created! Please log in with your credentials.")
            else:
                messagebox.showerror("Error", "Unable to create account. Please try again.")
        else:
            messagebox.showinfo("Info", "Please try again or use a different email.")

    def on_close(self):
        """Closes the login window and restores the chatbot GUI.
        Stänger inloggningsfönstret och återställer chatbotens GUI."""
        self.root.destroy()
        self.main_window.deiconify()  # EN: Restore main chatbot window / SV: Återställ huvudfönstret
