import tkinter as tk
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from firebase_service import FirebaseService

class HistoryWindow:
    def __init__(self, root, user_email, main_window):
        """Initializes the mood history window and hides the main window.
        Initierar fönstret för humörhistorik och gömmer huvudfönstret."""
        self.root = root
        self.user_email = user_email
        self.main_window = main_window  # EN: Reference to main window / SV: Referens till huvudfönstret
        self.root.title("Mood History")
        self.root.geometry("1000x500")

        self.firebase = FirebaseService()  # EN: Initializes Firebase service / SV: Initierar Firebase-tjänsten

        self.center_window()  # EN: Centers the window on the screen / SV: Centrerar fönstret på skärmen
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)  # EN: Handles window closing event / SV: Hanterar fönsterstängning

        # EN: Frame for mood chart / SV: Ram för humörgrafen
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.show_mood_chart()  # EN: Display mood chart / SV: Visar humörgrafen

    def center_window(self):
        """Centers the history window on the screen.
        Centrerar historikfönstret på skärmen."""
        self.root.update_idletasks()
        width = 1000
        height = 500
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def show_mood_chart(self):
        """Retrieves mood history from Firebase and displays it as a chart.
        Hämtar humörhistorik från Firebase och visar den som en graf."""
        mood_history = self.firebase.get_mood_history(self.user_email)

        if not mood_history:
            tk.Label(self.frame, text="No mood data available.", font=("Arial", 12)).pack(pady=20)
            return

        # EN: Extract dates and mood values / SV: Extrahera datum och humörvärden
        dates = [entry["date"] for entry in mood_history]
        moods = [entry["mood"] for entry in mood_history]

        # EN: Create and configure the plot / SV: Skapa och konfigurera grafen
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(dates, moods, marker="o", linestyle="-", color="b", label="Mood Over Time")

        ax.set_title("Mood History")
        ax.set_xlabel("Date")
        ax.set_ylabel("Mood (0-10)")
        ax.set_ylim(0, 10)
        ax.grid(True)
        ax.legend()

        # EN: Embed the matplotlib plot in the Tkinter window / SV: Bädda in Matplotlib-grafen i Tkinter-fönstret
        canvas = FigureCanvasTkAgg(fig, master=self.frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def on_close(self):
        """Restores the main window when the history window is closed.
        Återställer huvudfönstret när historikfönstret stängs."""
        self.main_window.deiconify()
        self.root.destroy()
