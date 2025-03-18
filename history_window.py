# history_window.py

import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from firebase_service import FirebaseService


class HistoryWindow:
    def __init__(self, root, user_email, main_window):
        """Initialiserar history-fönstret, centrerar det och döljer huvudfönstret."""
        self.root = root
        self.user_email = user_email
        self.main_window = main_window  # Referens till huvudfönstret
        self.root.title("Mood History")
        self.root.geometry("1000x500")

        # Centrera fönstret
        self.center_window()

        self.firebase = FirebaseService()

        # Gör så att huvudfönstret syns igen när detta fönster stängs
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Skapa en ram för grafen
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Visa grafen
        self.show_mood_chart()

    def center_window(self):
        """Centrerar history-fönstret på skärmen."""
        self.root.update_idletasks()
        width = 1000
        height = 500
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def show_mood_chart(self):
        """Hämtar humörhistorik och plottar den i en graf."""
        # Hämta humörhistorik från Firebase
        mood_history = self.firebase.get_mood_history(self.user_email)

        if not mood_history:
            tk.Label(self.frame, text="No mood data available.", font=("Arial", 12)).pack()
            return

        # Extrahera datum och humörvärden
        dates = [entry["date"] for entry in mood_history]
        moods = [entry["mood"] for entry in mood_history]

        # Skapa Matplotlib-figuren
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.plot(dates, moods, marker="o", linestyle="-", color="b", label="Mood Over Time")

        # Formatera grafen
        ax.set_title("Mood History")
        ax.set_xlabel("Date")
        ax.set_ylabel("Mood (0-10)")
        ax.set_ylim(0, 10)  # Y-axeln mellan 0 och 10
        ax.legend()
        ax.grid(True)

        # Visa grafen i Tkinter-fönstret
        canvas = FigureCanvasTkAgg(fig, master=self.frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def on_close(self):
        """Visar huvudfönstret igen när history-fönstret stängs."""
        self.main_window.deiconify()
        self.root.destroy()
