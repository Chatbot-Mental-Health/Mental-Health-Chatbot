# firebase_service.py

import firebase_admin
from firebase_admin import credentials, auth, firestore
import logging
import datetime
import os
from Dir import dir
from tkinter import messagebox


class FirebaseService:
    """Handles Firebase Authentication and Firestore database operations"""

    def __init__(self):
        # Initialize Firebase if it hasn't been initialized yet
        if firebase_admin._DEFAULT_APP_NAME not in firebase_admin._apps:
            cred_path = os.path.join(dir.BASE_DIR, dir.FIREBASE_CODE)
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)

        self.db = firestore.client()
        logging.basicConfig(level=logging.INFO)

    def authenticate_user(self, email, password, status_label=None, auth_button=None):
        try:
            user = auth.get_user_by_email(email)
            logging.info(f"User found: {user.email}, UID: {user.uid}")

            if status_label:
                status_label.config(text="Inloggning lyckades", fg="green")
            if auth_button:
                auth_button.config(text="Logga ut")

            return {"success": True, "message": "User found", "uid": user.uid}

        except auth.UserNotFoundError:
            logging.warning(f"User {email} not found in Firebase Authentication.")
            return {"success": False, "message": "Användaren hittades inte"}

        except Exception as e:
            logging.error(f"Authentication error: {e}")
            return {"success": False, "message": "Serverfel"}

    def register_user(self, email, password):
        try:
            user = auth.create_user(email=email, password=password)
            logging.info(f"User created in Firebase Authentication: {user.uid}")
            doc_id = email.replace("@", "_at_").replace(".", "_dot_")
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            today = datetime.datetime.now().strftime("%Y-%m-%d")

            # Create user document in Firestore with today as an empty list
            user_doc_ref = self.db.collection("Users").document(doc_id)
            user_doc_ref.set({
                "account_info": {
                    "email": email,
                    "password": password,
                    "uid": user.uid,
                    "created_at": timestamp
                },
                "chat_history": {today: []}  # Initialize today as a list
            }, merge=True)

            logging.info(f"Firestore document created for {email}")
            return {"success": True, "message": "User registered", "uid": user.uid}

        except Exception as e:
            logging.error(f"User registration error: {e}")
            return {"success": False, "message": "Kunde inte registrera användare"}

    def save_mood(self, email, mood):
        """Saves user's mood rating before first chat, ensuring no duplicate entries for the same day."""
        try:
            doc_id = email.replace("@", "_at_").replace(".", "_dot_")
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            today = datetime.datetime.now().strftime("%Y-%m-%d")

            user_doc_ref = self.db.collection("Users").document(doc_id)
            user_doc = user_doc_ref.get()

            # Fetch existing user data or initialize a new structure
            user_data = user_doc.to_dict() or {}
            mood_history = user_data.get("moodhistory", [])

            # Check if today's mood already exists
            for mood_entry in mood_history:
                if mood_entry["date"] == today:
                    logging.info(f"✅ Mood for {email} on {today} already exists. Skipping new entry.")
                    return {"success": False, "message": "Mood already recorded for today"}

            # Append new mood entry
            mood_entry = {
                "date": today,
                "timestamp": timestamp,
                "mood": mood
            }
            mood_history.append(mood_entry)

            # Update Firestore
            user_doc_ref.set({"moodhistory": mood_history}, merge=True)

            logging.info(f"✅ Mood {mood} saved for {email} at {timestamp}")
            return {"success": True, "message": "Mood saved"}

        except Exception as e:
            logging.error(f"Error saving mood: {e}")
            return {"success": False, "message": "Failed to save mood"}

    def save_chat_history(self, email, user_message, ai_response):
        """Saves chat history for a user."""
        try:
            doc_id = email.replace("@", "_at_").replace(".", "_dot_")
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            today = datetime.datetime.now().strftime("%Y-%m-%d")

            user_doc_ref = self.db.collection("Users").document(doc_id)
            user_doc = user_doc_ref.get()

            # Retrieve existing data or create an empty dictionary
            user_data = user_doc.to_dict() or {}
            chat_history = user_data.get("chat_history", {})

            # Ensure today's chat history exists as a list
            if today not in chat_history or not isinstance(chat_history[today], list):
                chat_history[today] = []

            # Append new message to chat history
            chat_entry = {
                "timestamp": timestamp,
                "user": user_message,
                "ai": ai_response
            }
            chat_history[today].append(chat_entry)

            # Update Firestore
            user_doc_ref.set({"chat_history": chat_history}, merge=True)

            logging.info(f"✅ Chat log saved for {email} under {today}")
            return {"success": True, "message": "Chat history saved"}

        except Exception as e:
            logging.error(f"Error saving chat history: {e}")
            return {"success": False, "message": "Failed to save chat history"}

    def get_user_mood(self, email, date):
        """Fetches the user's mood rating for a given date."""
        try:
            doc_id = email.replace("@", "_at_").replace(".", "_dot_")
            user_doc = self.db.collection("Users").document(doc_id).get()

            if not user_doc.exists:
                return None

            user_data = user_doc.to_dict() or {}
            mood_history = user_data.get("moodhistory", [])

            # Check if today's mood exists
            for mood_entry in mood_history:
                if mood_entry["date"] == date:
                    return mood_entry["mood"]  # ✅ Return mood if found

            return None  # ❌ No mood found for today
        except Exception as e:
            logging.error(f"Error fetching mood rating: {e}")
            return None

    def check_user_exists(self, email):
        try:
            auth.get_user_by_email(email)
            return True
        except auth.UserNotFoundError:
            return False
        except Exception as e:
            logging.error(f"Error checking user existence: {e}")
            return False

    def get_user_messages_by_date(self, email, date):
        try:
            doc_id = email.replace("@", "_at_").replace(".", "_dot_")
            user_doc = self.db.collection("Users").document(doc_id).get()

            if user_doc.exists:
                chat_history = user_doc.to_dict().get("chat_history", {})
                return chat_history.get(date, [])
            return []
        except Exception as e:
            logging.error(f"Error retrieving messages: {e}")
            return []

    def show_user_messages(self, email, date):
        """Displays user messages from a specific date."""
        messages = self.get_user_messages_by_date(email, date)
        if messages:
            messagebox.showinfo("User Messages", "\n".join(str(m) for m in messages))
        else:
            messagebox.showinfo("User Messages", "No messages found.")

    def logout_user(self, status_label, auth_button):
        """Handles user logout."""
        status_label.config(text="Du har loggat ut", fg="red")
        auth_button.config(text="Logga in")
        logging.info("User logged out successfully.")
        return {"success": True, "message": "User logged out"}

    def get_mood_history(self, email):
        """Retrieves the user's mood history from Firestore."""
        try:
            doc_id = email.replace("@", "_at_").replace(".", "_dot_")
            user_doc = self.db.collection("Users").document(doc_id).get()

            if not user_doc.exists:
                return []

            user_data = user_doc.to_dict() or {}
            mood_history = user_data.get("moodhistory", [])

            # Sort moods by date (oldest to newest)
            mood_history = sorted(mood_history, key=lambda x: x["date"])

            return mood_history  # Return full mood history as a list

        except Exception as e:
            logging.error(f"Error retrieving mood history: {e}")
            return []
