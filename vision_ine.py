import cv2
import pytesseract
import pandas as pd
from openai import OpenAI
from datetime import datetime

class vision_ine:
    def __init__(self):
        self.client = OpenAI()
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update this path
        columns = ['primer_nombre', 'segundo_nombre', 'apellido_materno', 'apellido_paterno', 'calle', 'numero_exterior', 'numero_interior', 'colonia', 'codigo_postal', 'delegacion', 'ciudad', 'CURP', 'gender', 'edad', 'year', 'month', 'day']
        columns2 = ['CIC', 'ID']
        self.df2 = pd.DataFrame(columns=columns2)
        self.df = pd.DataFrame(columns=columns)

    # Function to parse the input text and append data to the DataFrame using pd.concat
    def parse_and_append_to_dataframe(self, input_text, dataframe):
        # Split the input text into lines
        lines = input_text.strip().split('\n')

        # Create a dictionary to hold the key-value pairs
        data = {}

        # Iterate over each line to extract key-value pairs
        for line in lines:
            key, value = line.split(': ', 1)
            data[key.strip()] = value.strip()

        # Convert the dictionary to a DataFrame
        row_df = pd.DataFrame([data])

        # Use pd.concat to append the new row to the existing DataFrame
        dataframe = pd.concat([dataframe, row_df], ignore_index=True)

        return dataframe

    def parse_and_append_to_dataframe_back(self, input_text, dataframe):
        # Split the input text into lines
        lines = input_text.strip().split('\n')

        # Create a dictionary to hold the key-value pairs
        data = {}

        # Iterate over each line to extract key-value pairs
        for line in lines:
            key, value = line.split(': ', 1)
            data[key.strip()] = value.strip()

        # Convert the dictionary to a DataFrame
        row_df = pd.DataFrame([data])

        # Use pd.concat to append the new row to the existing DataFrame
        dataframe = pd.concat([dataframe, row_df], ignore_index=True)

        return dataframe
    def clean_data_with_llm(self, raw_data, type):
        if type == 'name':
            completion = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {
                        "role": "user",
                        "content": f"Clean and format the following name by correcting any typos and making it readable:\n\n{raw_data}\n\nEnsure the output is clear and properly formatted as a name, meaning first name, middle name, and both last names. Remove any text that clearly isn't part of a person's name, such as numbers, special characters, or unrelated words."
                    }
                ]
            )

            formatted_name = completion.choices[0].message.content.strip()
            return formatted_name

        elif type == 'curp':
            completion = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {
                        "role": "user",
                        "content": f"In this text: '{raw_data}', there is a mexican curp, which is comprised of 4 letters, 6 numbers, 7 letters and 1 number, this means that if from the 5th to the 10th position you see a letter, it is a number, so a O is a 0, an S is a 5, etc. I want you to return only the curp, no other text or explanation."
                    }
                ]
            )

            # Extract the formatted or corrected CURP from the response
            formatted_curp = completion.choices[0].message.content.strip()
            return formatted_curp

        elif type == 'address':
            completion = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {
                        "role": "user",
                        "content": f"Clean and format the following address by correcting any typos and making it readable:\n\n{raw_data}\n\nEnsure the output is clear and properly formatted as an address. Additionaly, remove any text that isnt part of the adress."
                    }
                ]
            )

            # Extract the cleaned address content from the response
            cleaned_address = completion.choices[0].message.content.strip()
            return cleaned_address
    def extract_with_llm(self, data, type):

        if type == 'name':
            completion = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {
                        "role": "user",
                        # "content": "say hi!"
                        "content": f"Solo extrae la información solicitada: Extrae el primer nombre, segundo nombre, apellido materno y apellido paterno del siguente nombre:\n\n{data}\n\nEl formato de salida debe ser:\nprimer_nombre: <primer_nombre>\nsegundo_nombre: <segundo_nombre>\napellido_materno: <apellido_materno>\napellido_paterno: <apellido_paterno>. Si alguno no existe, completa con un guión."
                    }
                ]
            )

            return completion.choices[0].message.content

        elif type == 'curp':
            # Year
            year = int(data[4:6])
            if year >= 24:
                year = 1900 + year
            else:
                year = 2000 + year

            # Month
            month = int(data[6:8])

            # Day
            day = int(data[8:10])

            #Gender
            if data[10] == 'H':
                gender = 'Hombre'
            elif data[10] == 'M':
                gender = 'Mujer'
            else:
                gender = 'No binario'

            date1 = datetime(year, month, day)
            date2 = datetime.now()

            edad = date2.year - date1.year - ((date2.month, date2.day) < (date1.month, date1.day))

            data2 = f"CURP: {data}\nyear: {year}\nmonth: {month}\nday: {day}\nedad: {edad}\ngender: {gender}"

            return data2

        elif type == 'address':
            completion = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {
                        "role": "user",
                        #"content": "say hi!"
                        "content": f"Solo extrae la información solicitada: Extrae el nombre de la calle, número exterior, número interior, colonia, código postal, delegación y ciudad de la siguiente dirección:\n\n{data}\n\nEl formato de salida debe ser:\ncalle: <nombre_de_la_calle>\nnumero_exterior: <numero_exterior>\nnumero_interior: <numero_interior>\ncolonia: <nombre_de_la_colonia>\ncodigo_postal: <codigo_postal>\ndelegacion: <nombre_de_la_delegacion>\nciudad: <nombre_de_la_ciudad>"
                    }
                ]
            )

            return completion.choices[0].message.content

        elif type == 'back':
            completion = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {
                        "role": "user",
                        "content": f"In the following paragraph: {data}, it should start with the word IDMEX, and the 6th character until the 15th, and the 18th to the 31st characters should be all numbers, so a O should be a 0, an S is a 5, and so on. I need you to get the CIC which is the 6th to the 14th character and the ID which is the 22th to the 31th character. For example, in the case of 'IDMEX1262783693<<4507132458169', the CIC is 126278369 and the ID is 132458169. You should return it in the form CIC: <CIC>\n ID: <ID>, no other text or explanation."
                    }
                ]
            )

            return completion.choices[0].message.content
    def load_image_and_crop(self, image_name):
        # Load the image from which to extract text
        image = cv2.imread(image_name)

        # Dimensions of the image
        height, width, _ = image.shape

        # Define the coordinates of the three red rectangles (based on the given image)
        # These coordinates are approximations, adjust them if necessary
        rectangles = [
            {"name": "adress_rect", "coords": (int(0.30 * width), int(0.48 * height), int(0.84 * width), int(0.74 * height))},
            {"name": "name_rect", "coords": (int(0.30 * width), int(0.26 * height), int(0.72 * width), int(0.51 * height))},
            {"name": "curp_rect", "coords": (int(0.30 * width), int(0.72 * height), int(0.60 * width), int(0.88 * height))}
        ]

        # Loop through the rectangles, crop and save each one
        for rect in rectangles:
            x1, y1, x2, y2 = rect["coords"]
            cropped_image = image[y1:y2, x1:x2]
            gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)


            # Save the cropped image
            output_path = f'{rect["name"]}.png'
            cv2.imwrite(output_path, gray)

        return
    def data_to_text(self, type):
        if type == 'name':
            image = cv2.imread('name_rect.png')
            text = pytesseract.image_to_string(image, config='--psm 6')

            clean_name = self.clean_data_with_llm(text, "name")
            output = self.extract_with_llm(clean_name, "name")

            return output

        elif type == 'curp':
            image = cv2.imread('curp_rect.png')
            text = pytesseract.image_to_string(image, config='--psm 6')
            clean_curp = self.clean_data_with_llm(text, "curp")
            output = self.extract_with_llm(clean_curp, "curp")
            return output

        elif type == 'address':
            image = cv2.imread('adress_rect.png')
            # Use Tesseract to extract text
            text = pytesseract.image_to_string(image, config='--psm 6')

            clean_address = self.clean_data_with_llm(text, "address")
            output = self.extract_with_llm(clean_address, "address")
            return output

        elif type == 'back':
            image = cv2.imread('back_rect.png')
            # Use Tesseract to extract text
            text = pytesseract.image_to_string(image, config='--psm 6')
            output = self.extract_with_llm(text, "back")
            return output

    def load_data(self, image):

        self.load_image_and_crop(image)

        output1 = self.data_to_text("name")

        output2 = self.data_to_text("curp")

        output3 = self.data_to_text("address")

        output = output1 + "\n" + output2 + "\n" + output3

        self.df = self.parse_and_append_to_dataframe(output, self.df)


    def save_data(self):
        self.df.to_csv('output.csv', index=False)


    def read_back(self, image_name):
        import cv2

        # Load the image
        image = cv2.imread(image_name)

        # Check if the image is loaded correctly
        if image is None:
            print(f"Failed to load image: {image_name}")
            exit()

        # Dimensions of the image
        height, width, _ = image.shape

        # Define the coordinates of the rectangle (based on the given image)
        # These coordinates are approximations, adjust them if necessary
        rectangles = [
            {"name": "back_rect",  # Fixed the name for consistency
             "coords": (int(0.0 * width), int(0.65 * height), int(1 * width), int(1 * height))}
            # Changed 'back' to 'coords'
        ]

        # Loop through the rectangles, crop and save each one
        for rect in rectangles:
            x1, y1, x2, y2 = rect["coords"]  # Use 'coords' key correctly
            cropped_image = image[y1:y2, x1:x2]

            # Check if the cropping resulted in an empty image
            if cropped_image.size == 0:
                print(f"Cropping resulted in an empty image for {rect['name']}. Check coordinates.")
                continue

            # Convert to grayscale
            gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)

            # Save the cropped image
            output_path = f'{rect["name"]}.png'
            cv2.imwrite(output_path, gray)
            return

    def load_back(self, image):
        self.read_back(image)
        output = self.data_to_text("back")
        self.df2 = self.parse_and_append_to_dataframe_back(output, self.df2)
        return

    def join_dataframes(self):
        self.df = pd.concat([self.df, self.df2], axis=1)
        return
