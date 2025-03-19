# Mental Health Chatbot

## Overview
The **Mental Health Chatbot** is a chatbot application designed to provide empathetic and supportive conversations to users. It leverages AI-driven text generation and integrates Firebase for authentication and chat history storage. The application is built using **Python** with a **Tkinter GUI** for user interaction.

## Features
- AI-generated responses using OpenAI GPT model
- Text-to-speech functionality
- User authentication and chat history storage via Firebase
- Mood tracking with graphical visualization
- GUI-based chatbot interaction

## File Structure
### Application Files

- `Main.py` - Entry point of the application. Initializes the chatbot GUI and AI model.
- `chatbot_gui.py` - Handles the graphical user interface (GUI) for the chatbot.
- `Ai.py` - Manages AI-generated responses and text-to-speech conversion.
- `firebase_service.py` - Manages Firebase authentication and database interactions.
- `login_window.py` - Handles user login through Firebase authentication.
- `history_window.py` - Displays mood tracking history with graphs.
- `about_window.py` - Shows application details including developers and version information.

### eBook References
The following eBooks provide guidance on Python programming, game development, and database management:

1. **Automate the Boring Stuff with Python (2nd Edition)** - Al Sweigart
2. **Essential SQLAlchemy (2nd Edition)** - Jason Myers, Rick Copeland
3. **Python, Pygame, and Raspberry Pi Game Development** - Sloan Kelly
4. **Beginning Game Development with Python and Pygame** - Will McGugan
5. **Starting Out with Python** - Tony Gaddis
6. **Python (5th Edition, Global Edition)** - Tony Gaddis

These books cover fundamental and advanced topics in Python programming, automation, SQL database handling, and game development, which may be useful for expanding and improving this chatbot project.

## Installation
### Requirements
- Python 3.x
- `openai` for AI-generated responses
- `gtts` for text-to-speech conversion
- `tkinter` for GUI interface
- `firebase-admin` for authentication and database handling
- `matplotlib` for mood tracking visualization

### Steps
1. Clone the repository.
2. Install dependencies using:
   ```sh
   pip install openai gtts firebase-admin matplotlib
   ```
3. Run the application:
   ```sh
   python Main.py
   ```

## Contributors
- Morgan Lindbom
- Yousef Martaa
- Kotaiba Alabdullah
- Oleh Doshchuk
- Muhammad Huzaifa

## License
This project is for educational purposes and is subject to OpenAI API and Firebase usage policies.

