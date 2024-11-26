import os
import base64
import requests
from picamera import PiCamera
from time import sleep
import RPi.GPIO as GPIO

# Configuration
BUTTON_PIN = 18  # GPIO pin where the button is connected
ENDPOINT_URL = "http://127.0.0.1:5000/check_thief"
CAPTURED_IMAGE_PATH = "captured.jpg"

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Pull-up resistor for button

# Initialize Camera
camera = PiCamera()

def capture_image(file_path):
    """Capture an image using the PiCamera."""
    camera.start_preview()
    sleep(2)  # Allow camera to adjust
    camera.capture(file_path)
    camera.stop_preview()
    print(f"Image captured: {file_path}")

def image_to_base64(file_path):
    """Convert an image to a Base64-encoded string."""
    with open(file_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

def send_to_server(base64_image):
    """Send the Base64 image to the check_thief endpoint."""
    payload = {"image": base64_image}
    try:
        response = requests.post(ENDPOINT_URL, json=payload)
        if response.status_code == 200:
            print("Server Response:", response.json())
        else:
            print(f"Error: Server returned status code {response.status_code}")
    except Exception as e:
        print(f"Error connecting to server: {e}")

def button_pressed(channel):
    """Callback function for button press."""
    print("Button pressed! Capturing photo...")
    capture_image(CAPTURED_IMAGE_PATH)
    base64_image = image_to_base64(CAPTURED_IMAGE_PATH)
    print("Sending image to server...")
    send_to_server(base64_image)

# Set up event detection for button press
GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=button_pressed, bouncetime=300)

try:
    print("Waiting for button press...")
    while True:
        sleep(1)  # Keep the script running

except KeyboardInterrupt:
    print("Exiting program.")

finally:
    GPIO.cleanup()
    print("GPIO cleaned up.")
