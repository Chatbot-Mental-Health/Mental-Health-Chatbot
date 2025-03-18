# login_window.py

import tkinter as tk
from tkinter import messagebox
from firebase_service import FirebaseService


class LoginWindow:
    """Hantera inloggningsfönstret för Mental Health Chatbot."""

    def __init__(self, root, on_login_success, main_window):
        """
        Initierar inloggningsfönstret.

        :param root: Tkinter Toplevel-fönster (login-fönstret)
        :param on_login_success: Callback-funktion som körs vid lyckad inloggning
        :param main_window: Huvudfönstret (Chatbot GUI) som ska döljas/visas
        """
        self.root = root
        self.on_login_success = on_login_success
        self.main_window = main_window  # Referens till huvudfönstret
        self.firebase = FirebaseService()

        self.root.title("Logga in")
        self.root.geometry("300x250")
        self.root.resizable(False, False)

        # Centrera fönstret på skärmen
        self.center_window()

        # Hantera fönsterstängning via X-knappen
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Skapa GUI-element
        self.create_widgets()

    def center_window(self):
        """Centrerar login-fönstret på skärmen."""
        self.root.update_idletasks()
        width, height = 300, 250
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def create_widgets(self):
        """Skapar och placerar alla GUI-komponenter i fönstret."""
        self.frame = tk.Frame(self.root, padx=10, pady=10)
        self.frame.pack(expand=True, fill="both")

        # Titel
        self.title_label = tk.Label(self.frame, text="Logga in", font=("Arial", 14, "bold"))
        self.title_label.pack(pady=(0, 10))

        # Email-fält
        self.email_label = tk.Label(self.frame, text="Email:", font=("Arial", 10))
        self.email_label.pack(anchor="w")
        self.email_entry = tk.Entry(self.frame, font=("Arial", 12), width=25)
        self.email_entry.pack(pady=2)
        self.email_entry.insert(0, "mogge@kalle.com")

        # Lösenord-fält
        self.password_label = tk.Label(self.frame, text="Lösenord:", font=("Arial", 10))
        self.password_label.pack(anchor="w")
        self.password_entry = tk.Entry(self.frame, font=("Arial", 12), width=25, show="*")
        self.password_entry.pack(pady=2)
        self.password_entry.insert(0, "123456")  # Sätt lösenordet
        # Knapp-rad
        self.button_frame = tk.Frame(self.frame)
        self.button_frame.pack(pady=10)

        # Avbryt-knapp
        self.cancel_button = tk.Button(
            self.button_frame, text="Avbryt", font=("Arial", 10), width=10, command=self.on_close
        )
        self.cancel_button.pack(side="left", padx=5)

        # Login-knapp
        self.login_button = tk.Button(
            self.button_frame, text="Logga in", font=("Arial", 10), width=10, command=self.on_login
        )
        self.login_button.pack(side="left", padx=5)

    def on_login(self):
        """Hanterar inloggningen och validerar användarinformation."""
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        if not email or not password:
            messagebox.showwarning("Fel", "Både email och lösenord måste fyllas i.")
            return

        response = self.firebase.authenticate_user(email, password)

        if response["success"]:
            self.root.destroy()  # Stäng login-fönstret
            self.main_window.deiconify()  # Visa huvudfönstret (chatbot)
            self.on_login_success(email)
        else:
            self.handle_failed_login(email, password)

    def handle_failed_login(self, email, password):
        """Hanterar misslyckad inloggning och erbjuder att skapa konto."""
        create_account = messagebox.askyesno(
            "Konto saknas", "Ingen användare hittades. Vill du skapa ett konto?"
        )

        if create_account:
            register_response = self.firebase.register_user(email, password)
            if register_response["success"]:
                messagebox.showinfo("Lyckat", "Konto skapat! Logga in med dina uppgifter.")
            else:
                messagebox.showerror("Fel", "Kunde inte skapa konto. Försök igen.")
        else:
            messagebox.showinfo("Info", "Försök igen eller använd en annan e-postadress.")

    def on_close(self):
        """Stänger login-fönstret och visar chatbot-GUI igen när användaren trycker på X."""
        self.root.destroy()
        self.main_window.deiconify()  # Visa huvudfönstret (chatbot)
