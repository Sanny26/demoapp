from django.shortcuts import render
import os
# Create your views here.
	
def index(request):
	page_template = "an_index2.html"
	context = {}
	return render(request, page_template, context)
