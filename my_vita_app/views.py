from django.shortcuts import render, redirect
from .forms import ReceiveImageForm, UserForm
from vita import settings
from django.http import HttpResponse
from PIL import Image
from img_recon.vision_ine import vision_ine
import os

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
                # Save data onto a df
                df = checker.save_data()
            except ValueError:
                return render(request, 'signup.html', {
                    'form': ReceiveImageForm(),
                    'error': "Something went wrong. Please try again!",
                })

            response = HttpResponse("")
            response.set_cookie('image_data', df, max_age=3600)

            return redirect('signup_user')
        return render(request, 'signup.html', {
            'form': ReceiveImageForm(),
            'error': "Something went wrong. Please try again!",
        })

# User Creation Form
def signup_user(request):
    if(request.method == 'GET'):
        return render(request, 'signupUser.html', {
            'form': UserForm,
        })

# Ask for face photo
def face_upload(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('photo')
    return render(request, 'faceUpload.html')
