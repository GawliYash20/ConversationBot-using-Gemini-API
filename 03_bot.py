import pyautogui
import pyperclip
import time
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables from .env file in the root directory
load_dotenv()

# Access the API_KEY variable from the .env file
API_KEY = os.getenv("API_KEY")

if API_KEY is None:
    print("API_KEY not found. Make sure it's set in the .env file.")
    exit()

print(f"API_KEY: {API_KEY}")

# Configure Generative AI Model
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Initialize chat with a detailed prompt
chat = model.start_chat(
    history=[
        {"role": "user", "parts": "Hello"},
        {
            "role": "model",
            "parts": "Hello! I am designed to respond in detailed and structured paragraphs. I will avoid using bullet points and provide answers in a more conversational, paragraph-style format.",
        },
    ]
)


def copy_text_from_coordinates():
    """Copy text from the specified WhatsApp chat coordinates."""
    # Wait a moment to allow switching to the target application
    time.sleep(7)

    # Step 2: Select text
    pyautogui.moveTo(720, 266)
    pyautogui.mouseDown()
    time.sleep(0.2)
    pyautogui.moveTo(1030, 910, duration=1)
    pyautogui.mouseUp()

    # Step 3: Copy selected text
    pyautogui.hotkey("ctrl", "c")
    time.sleep(0.6)  # Allow clipboard to update

    # Step 4: Retrieve the text from the clipboard
    chat_history = pyperclip.paste()

    return chat_history


def send_response(response_text):
    """Type and send the AI-generated response."""
    pyautogui.click(1103, 957)  # Click to focus on the input field
    time.sleep(0.5)
    pyautogui.typewrite(response_text, interval=0.05)  # Type the response
    pyautogui.press("enter")  # Send the message


if __name__ == "__main__":
    is_chat_focused = False  # Flag to track if the chat window has been selected
    while True:
        try:
            # Step 1: Check if the chat has already been focused
            if not is_chat_focused:
                pyautogui.click(1082, 1056)  # Click to focus on the chat
                time.sleep(0.5)
                is_chat_focused = True  # Set the flag to True after the first click

            # Step 2: Fetch chat history from WhatsApp
            text = copy_text_from_coordinates()
            print(f"Copied Text: {text}")

            # Step 3: Get AI response
            response = chat.send_message(text)
            print(f"AI Response: {response.text}")

            # Step 4: Send the response in WhatsApp
            send_response(response.text)

            # Wait before the next interaction
            time.sleep(5)  # Adjust as needed to avoid spamming
        except Exception as e:
            print(f"An error occurred: {e}")
            break
