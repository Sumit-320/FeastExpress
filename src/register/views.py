from django.shortcuts import render,HttpResponse
# Create your views here.
def registerUser(request):
    return render(request,'register/registerUser.html')