from django.shortcuts import render
import simplejson as json

from .forms import PhotoForm
import os

# Create your views here.

# https://simpleisbetterthancomplex.com/tutorial/2017/03/02/how-to-crop-images-in-a-django-application.html
# http://blog.appliedinformaticsinc.com/how-to-add-image-cropping-features-using-django-image-cropping-app-jcrop/

def index(request, pid):
	page_template = "wr_index2.html"
	context = {}
	if request.method == 'POST':
		form = PhotoForm(request.POST, request.FILES)
		if form.is_valid():
			return redirect('index')
	else:
		form = PhotoForm()
		context['path'] = 'docs/wr_pages/notes-34.jpg'
		context['files'] = os.listdir('static/docs/wr_pages')
		context['pid']  = pid
		context['word_dict'] = json.dumps({"90#78":"गुजरात", "265#72":"सौर"})
	return render(request, page_template, context)
