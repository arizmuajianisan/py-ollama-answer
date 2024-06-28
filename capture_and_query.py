import cv2
import numpy as np
from PIL import ImageGrab, Image
import pygetwindow as gw
from pynput import keyboard
import requests
import base64
from text_extractor_easyocr import OCRProcessor
import easyocr

def capture_chrome_window():
    chrome_windows = [window for window in gw.getAllTitles() if "Chrome" in window]
    print(chrome_windows)
    if chrome_windows:
        chrome_window_title = chrome_windows[
            0
        ]  # Assuming the first window found is the correct one
        chrome_window = gw.getWindowsWithTitle(chrome_window_title)[0]
        if chrome_window.isMinimized or not chrome_window.isActive:
            chrome_window.restore()  # Restore window if minimized
            chrome_window.activate()
        bbox = (
            chrome_window.left,
            chrome_window.top,
            chrome_window.right,
            chrome_window.bottom,
        )
        screen = ImageGrab.grab(bbox)
        screen_np = np.array(screen)
        return cv2.cvtColor(screen_np, cv2.COLOR_RGB2BGR)
    else:
        raise Exception("Chrome window not found")


def query_llama3(image):
    print("Start OCR processor...")
    ocr_processor = OCRProcessor(languages=["en", "id"])

    # Process the image to text using OCR
    ocr_result = ocr_processor.process_image_from_pil(Image.fromarray(image))

    # If OCR failed, return a placeholder message
    if not ocr_result:
        return "OCR failed to extract text from the image."

    # Prepare the prompt for the LLM
    # The prompt includes the OCR result, and the user's question about the extracted text.
    url = "http://localhost:11434/api/generate"
    data = {
        "model": "llama3",
        "prompt": f"""I have some multiple choise type of question below:
        {ocr_result}
        Can you answer it?""",
        "stream": False,
    }

    # Send request to the local LLM API running in Docker
    print("Start prompt to llama3...")
    response = requests.post(url, json=data)
    # print(response.json())
    return response.json().get("response", "No answer found.")


def on_press(key):
    try:
        # if key == keyboard.KeyCode.from_char('\x9c') and keyboard.Controller().ctrl_pressed:
        if key.char.lower() == "p":
            # Capture the screen (Chrome window)
            screen = capture_chrome_window()

            # Save the image for verification (optional)
            cv2.imwrite("captured_screen.png", screen)

            # Get the answer from the LLM
            answer = query_llama3(screen)
            print("Answer:", answer)
    except Exception as e:
        print(f"Error: {e}")


def on_release(key):
    try:
        if key.char.lower() == "q":
            # Handle Ctrl+C for exiting
            print("Exiting...")
            return False  # Stop listener
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt: Exiting...")
        return False


def main():
    try:
        # Set up key listener
        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()
    except Exception as e:
        print(f"Unhandled exception in listener callback: {e}")


if __name__ == "__main__":
    main()
