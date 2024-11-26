import base64
import requests

# Encode the image to Base64
with open("thief/captured_image.jpg", "rb") as image_file:
    base64_image = base64.b64encode(image_file.read()).decode('utf-8')

# Prepare the request payload
url = "http://127.0.0.1:5000/add_user_image"
payload = {"image": base64_image}

# Send POST request
response = requests.post(url, json=payload)

# Print the response
print(response.json())
