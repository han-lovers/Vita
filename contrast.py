import cv2
from PIL import Image
from deepface import DeepFace

class contrast():
    def __init__(self):
        self.backends = ["opencv", "ssd", "dlib", "mtcnn", "retinaface", "mediapipe"]

    def detect_and_crop_face(self, image_path, output_path):
        # Load the image
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Load the Haar cascade for face detection
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        # Detect faces in the image
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        if len(faces) == 0:
            print("No faces detected.")
            return

        # Get the coordinates of the first detected face (x, y, width, height)
        x, y, w, h = faces[0]

        # Draw a bounding box around the detected face
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Crop the image to the bounding box
        cropped_image = Image.fromarray(image[y:y + h, x:x + w])

        # Save the cropped image
        cropped_image.save(output_path)

        print(f"Face detected and cropped. Image saved to {output_path}")
        return

    def contrast_faces(self, img1, img2):
        for backend in self.backends:

                # Attempt face verification with the current backend
                result = DeepFace.verify(img1_path=img1, img2_path=img2, detector_backend=backend)

                # Check if the verification was successful
                if result['verified']:
                    return True

        return False
