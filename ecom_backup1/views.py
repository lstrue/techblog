from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def index(resquest):
	return HttpResponse("<h2>Hey</h2>")
