from deepface import DeepFace
import os

def check2(image_name, folder_path="users/"):
    # Check if the folder exists
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist.")
        return

    # Loop through all files in the folder
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        # Verify the image with each file in the folder
        try:
            result = DeepFace.verify(img1_path=image_name, img2_path=file_path)
            similarity = result['verified']
            print(f"Compared with {file_name}: Match: {similarity}")
            if similarity :
                return False
        except Exception as e:
            print(f"Error processing {file_name}: {e}")
    return True