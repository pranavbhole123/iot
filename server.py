import os
import base64
import random
import string
from flask import Flask, request, jsonify
from deepface import DeepFace

app = Flask(__name__)

# Create directories if they don't exist
USER_FOLDER = "users"
THIEF_FOLDER = "thief"

os.makedirs(USER_FOLDER, exist_ok=True)
os.makedirs(THIEF_FOLDER, exist_ok=True)

def save_image(base64_image, folder):
    """Save a Base64 image to the specified folder with a random filename."""
    try:
        # Generate a random filename
        filename = ''.join(random.choices(string.ascii_letters + string.digits, k=10)) + ".jpg"
        file_path = os.path.join(folder, filename)

        # Decode and save the image
        with open(file_path, "wb") as img_file:
            img_file.write(base64.b64decode(base64_image))

        return file_path
    except Exception as e:
        print(f"Error saving image: {e}")
        return None

@app.route('/add_user_image', methods=['POST'])
def add_user_image():
    """Endpoint to add a user image."""
    data = request.json
    base64_image = data.get("image")

    if not base64_image:
        return jsonify({"error": "No image provided"}), 400

    file_path = save_image(base64_image, USER_FOLDER)
    if not file_path:
        return jsonify({"error": "Failed to save image"}), 500

    return jsonify({"message": "User image added successfully", "file_path": file_path})

@app.route('/check_thief', methods=['POST'])
def check_thief():
    """Endpoint to check if an image matches a user and save if it's a thief."""
    data = request.json
    base64_image = data.get("image")

    if not base64_image:
        return jsonify({"error": "No image provided"}), 400

    file_path = save_image(base64_image, THIEF_FOLDER)
    if not file_path:
        return jsonify({"error": "Failed to save image"}), 500

    # Use the check2 function to verify
    is_thief = check2(file_path, USER_FOLDER)

    if is_thief:
        return jsonify({"message": "Image does not match any user. Saved as a thief.", "file_path": file_path})
    else:
        os.remove(file_path)  # Remove from thief folder if it's a user
        return jsonify({"message": "Image matches an existing user. Not a thief."})

def check2(image_name, folder_path=USER_FOLDER):
    """Verify if an image matches any in the user folder."""
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist.")
        return True  # Assume thief if no user images are present

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        try:
            result = DeepFace.verify(img1_path=image_name, img2_path=file_path)
            similarity = result['verified']
            print(f"Compared with {file_name}: Match: {similarity}")
            if similarity:
                return False  # Match found, not a thief
        except Exception as e:
            print(f"Error processing {file_name}: {e}")
    return True  # No match found, assume thief

if __name__ == '__main__':
    app.run(debug=True)
