from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return render(request, 'home.html')

def signup(request):
    return render(request, 'signup.html')
def faceUpload(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('photo')
    return render(request, 'faceUpload.html')