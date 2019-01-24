from django.shortcuts import render
# import simplejson as json
import json
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



def index2(request, pid):
	page_template = "wr_index.html"
	context = {}
	
	context['path'] = 'docs/wr_pages/page1.jpg'
	context['pid']  = pid
	# word_dict = {"90#78":"गुजरात", "265#72":"सौर"}
	rects = []
	word_dict = {}
	words = ['दिवस', 'शब्द', 'मार्च', 'विश्व', 'अधिकार ']
	with open('static/docs/wr_pages/doc1_positions.txt') as f:
		for i, line in enumerate(f):
			line = line.strip().split(',')
			key = '{}#{}'.format(int(line[0]), int(line[1]))
			value = words[i%5]
			word_dict[key] = value
			rects.append({'x': int(line[0]), 'y': int(line[1]), 'w': int(line[2])-int(line[0]), 'h':int(line[3])-int(line[1]) })
	context['word_dict'] = json.dumps(word_dict)
	context['rects'] = json.dumps(rects)
	context['files'] = os.listdir('static/docs/wr_pages/')
	return render(request, page_template, context)


def index(request, pid):
	page_template = "wr_index2.html"
	context = {}
	context['pid']  = pid
	context['iname'] = 'docs/wr_pages/page1.jpg'.format(pid)
	context['rname'] = 'docs/wr_pages/test_out.jpg'.format(pid)
	return render(request, page_template, context)
