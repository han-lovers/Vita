from django.shortcuts import render, redirect
from django.conf import settings
from .forms import ReceiveImageForm, UserForm
from .models import CustomUser
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from vita import settings
from django.http import HttpResponse
from PIL import Image
from img_recon.vision_ine import vision_ine
from img_recon.contrast import contrast
import os
import csv
import pandas as pd

# Create your views here.
def home(request):
    return render(request, 'home.html')

# Ask for INE photo
def signup(request):
    if(request.method == 'GET'):
        return render(request, 'signup.html', {
            'form': ReceiveImageForm(), 
        })
    if(request.method == 'POST'):
        form = ReceiveImageForm(request.POST, request.FILES)
        if(form.is_valid()):
            # Store image in img
            img = form.cleaned_data['image']
            
            # Set into a directory the loaded image
            upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
            os.makedirs(upload_dir, exist_ok=True)  # Create the directory if it doesn't exist
            image_path = os.path.join(upload_dir, img.name)

            # Save the image file
            with open(image_path, 'wb+') as destination:
                for chunk in img.chunks():
                    destination.write(chunk)

            # Create INE checker
            checker = vision_ine()
            
           

            try:
                 # Load data onto the checker
                checker.load_data(image_path)
                checker.save_data()

            except ValueError:    
                return render(request, 'signup.html', {
                    'form': ReceiveImageForm(),
                    'error': "Something went wrong. Please try again!",
                })
            # Construye la ruta completa al archivo output.csv
            csv_path = os.path.join(settings.BASE_DIR, 'output.csv')

            # Define the directory where `views.py` is located
            current_directory = os.path.dirname(os.path.abspath(__file__))

            # Write image_path to a file
            image_path_file = os.path.join(current_directory, 'image_path.txt')
            with open(image_path_file, 'w') as file:
                file.write(image_path)

            # Convert df to JSON or string format before writing
            df_file = os.path.join(current_directory, 'csv_path.txt')
            with open(df_file, 'w') as file:
                file.write(csv_path)

            return redirect('face_upload')

        return render(request, 'signup.html', {
            'form': ReceiveImageForm(),
            'error': "Something went wrong. Please try again!",
        })


# Ask for face photo
def face_upload(request):
    if request.method == 'GET':
        return render(request, 'faceUpload.html', {
            'form': ReceiveImageForm(),
        })
    if request.method == 'POST':
        form = ReceiveImageForm(request.POST, request.FILES)
        if(form.is_valid()):
            # Store image in img
            img = form.cleaned_data['image']
            
            # Set into a directory the loaded image
            upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
            os.makedirs(upload_dir, exist_ok=True)  # Create the directory if it doesn't exist
            image_path = os.path.join(upload_dir, img.name)

            # Save the image file
            with open(image_path, 'wb+') as destination:
                for chunk in img.chunks():
                    destination.write(chunk)
            
            # Determine the current directory where views.py is located
            current_directory = os.path.dirname(os.path.abspath(__file__))
    
            # Construct the full path to image_path.txt
            ine_path_file = os.path.join(current_directory, 'image_path.txt')

            # Open the file and read the content
            with open(ine_path_file, 'r') as file:
                ine_path = file.read().strip()  # Read the content and remove any extra whitespace
            
            # Create checker
            checker = contrast()
            
            # Crop ine
            print(ine_path)
            checker.crop_imgs(ine_path, f'{current_directory}/photo_rect.png')

            # Compare both images
            checker.detect_and_crop_face(image_path, f'{current_directory}/output_photo.png') # outputs photo_rect.png
            succesfull = checker.contrast_faces(f'{current_directory}/output_photo.png', f'{current_directory}/photo_rect.png')
            
            if(succesfull):
                return redirect('signup_user')

            return render(request, 'faceUpload.html', {
                'form': ReceiveImageForm(),
                'error': "Something went wrong. Please try again!",
            })
            # contraster.crop_imgs()
        return render(request, 'faceUpload.html', {
            'form': ReceiveImageForm(),
            'error': "Something went wrong. Please try again!",
        })


# User Creation Form
def signup_user(request):
    if(request.method == 'GET'):
        csv_data = []
        

        current_directory = os.path.dirname(os.path.abspath(__file__))

        with open(f'{current_directory}/csv_path.txt', 'r') as file:
            csv_path = file.read().strip()

        with open(str(csv_path), newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                csv_data.append(row)  # Each row is a dictionary

        # Assuming you want to use the first row to prefill the inputs
        prefill_data = csv_data[0] if csv_data else {}  # Get the first row
        
        return render(request, 'signupUser.html', {
           'form': UserForm,
           'prefill_data': prefill_data,
        })
    if(request.method == 'POST'):
        # Validate if both passwords are correct
        if(request.POST['password1'] != request.POST['password2']):
            return render(request, 'signupUser.html', {
                'error': 'Passwords do not match!',
            })
        # Validate password security
        try:
            validate_password(request.POST['password1'])
        except ValidationError as e:
            return render(request, 'signup.html',  {
                'form': UserForm,
                'invalid_password': True,
                'error': e,
            })

        #password = make_password(request.POST['password1'])

        # Validate if user already exists
        try:
            user_form = UserForm(request.POST)
            user = user_form.save()
            
            return redirect('home')
        except :
            return render(request, 'signupUser.html', {
                'form': UserForm,
                'error': 'Username already exists',
            })        
        return redirect('signup-user')        
