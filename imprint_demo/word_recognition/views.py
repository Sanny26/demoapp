from django.shortcuts import render
# import simplejson as json

from .forms import PhotoForm
import os

# Create your views here.

# https://simpleisbetterthancomplex.com/tutorial/2017/03/02/how-to-crop-images-in-a-django-application.html
# http://blog.appliedinformaticsinc.com/how-to-add-image-cropping-features-using-django-image-cropping-app-jcrop/

def home(request):
	page_template = "home.html"
	context = {}
	return render(request, page_template, context)

def pub(request):
	page_template = "publications.html"
	context = {}
	return render(request, page_template, context)

def partners(request):
	page_template = "partners.html"
	context = {}
	return render(request, page_template, context)

def imgann(request):
	page_template = "techdetail_imgann.html"
	context = {}
	return render(request, page_template, context)

def imgenh(request):
	page_template = "techdetail_imgenh.html"
	context = {}
	return render(request, page_template, context)

def imgsr(request):
	page_template = "techdetail_imgsr.html"
	context = {}
	return render(request, page_template, context)

def imgws(request):
	page_template = "techdetail_ws.html"
	context = {}
	return render(request, page_template, context)

def postprocess(request):
	page_template = "techdetail_postprocess.html"
	context = {}
	return render(request, page_template, context)



# def index(request, pid):
# 	page_template = "wr_index.html"
# 	context = {}
# 	if request.method == 'POST':
# 		form = PhotoForm(request.POST, request.FILES)
# 		if form.is_valid():
# 			return redirect('index')
# 	else:
# 		form = PhotoForm()
# 		context['path'] = 'docs/wr_pages/notes-34.jpg'
# 		context['files'] = os.listdir('static/docs/wr_pages')
# 		context['pid']  = pid
# 		context['word_dict'] = json.dumps({"90#78":"गुजरात", "265#72":"सौर"})
# 	return render(request, page_template, context)


def index(request, pid):
	page_template = "wr_index2.html"
	context = {}
	context['pid']  = pid
	context['iname'] = 'docs/wr_pages/input/{}.jpg'.format(pid)
	context['rname'] = 'docs/wr_pages/output/{}_output.png'.format(pid)
	return render(request, page_template, context)
