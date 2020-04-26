from django.shortcuts import render

def home(requests):
    return render(requests, 'home/welcome.html')
