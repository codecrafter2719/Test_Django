from django.shortcuts import render,redirect

def home(request):
    return render(request, 'user_auth/home.html')

def symptom_checker(request):
    return render(request, 'guest_access/symtoms.html')
