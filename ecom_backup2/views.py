from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

# def index(resquest):
# 	return HttpResponse("<h2>Hey</h2>")

def index(request):
	return render(request, 'ecom/home.html')

def contact(request):
	return render(request, 'ecom/basic.html', {"content": ["email address", "david@gmail.com"]})
