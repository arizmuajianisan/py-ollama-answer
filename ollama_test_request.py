import requests
import base64

images_path = "D:\\playground\\py-ollama-answer\\captured_screen.png"

# Open the image file and read it as binary
with open(images_path, "rb") as image_file:
    images_tobyte = image_file.read()

# Encode the binary data to base64
encoded_image = base64.b64encode(images_tobyte).decode('utf-8')

url = "http://localhost:11434/api/generate"
data = {
    "model": "llama3",
    "prompt": "Explain this image",
    "stream": False,
    "images": [{"image_data": encoded_image}]  # base64 encoded image within a dictionary
}

response = requests.post(url, json=data)

print(response.json().get('response', 'No answer found.'))
