import cv2
from PIL import Image
from deepface import DeepFace
import os

class contrast():
    def __init__(self):
        self.backends = ["opencv", "ssd", "dlib", "mtcnn", "retinaface", "mediapipe"]

    def crop_imgs(self, img_name, output_path):
        image = cv2.imread(img_name)

        # Dimensions of the image
        height, width, _ = image.shape

        # Define the coordinates of the three red rectangles (based on the given image)
        # These coordinates are approximations, adjust them if necessary
        rectangles = [
            {"name": "photo_rect",
             "coords": (int(0.05 * width), int(0.22 * height), int(0.32 * width), int(0.67 * height))},

        ]

        # Loop through the rectangles, crop and save each one
        for rect in rectangles:
            x1, y1, x2, y2 = rect["coords"]
            cropped_image = image[y1:y2, x1:x2]
            gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)

            # Save the cropped image
            cv2.imwrite(output_path, gray)

        return

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


#a = contrast()
#a.crop_imgs('cropped_id_front2.jpeg')
