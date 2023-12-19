import cv2
import face_recognition

def capture_and_append_encoding(name, camera_index=0, encoding_file='face_encodings.txt'):
    # Open the camera
    cap = cv2.VideoCapture(camera_index)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    # Capture a single frame
    ret, frame = cap.read()

    # Detect faces in the captured frame
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    if face_encodings:
        # Append the new face encodings with associated name to the existing file
        with open(encoding_file, 'a') as file:
            for encoding in face_encodings:
                # Convert the encoding to a string for storage
                encoding_str = ','.join(map(str, encoding))
                file.write(f"{name},{encoding_str}\n")

        print(f"Face encodings for {name} appended to {encoding_file}")
    else:
        print("No faces detected.")

    # Release the camera
    cap.release()

if __name__ == "__main__":
    # Get input name from the user
    name = input("Enter the name for the face encoding: ")

    # Capture an image and append face encodings with the associated name
    capture_and_append_encoding(name, camera_index=0, encoding_file='face_encodings.txt')
