from django.shortcuts import render, redirect

from .forms import ImUpForm, DetailsForm
from hw_ann_tool.settings import MEDIA_URL,MEDIA_ROOT

import random
import os
import io
import PIL.Image as Image

def upload(request):
	page_template = "upload.html"
	context = {}
	lang = request.session['lang']
	dirpath = f'media/{lang}_paras/'
	files = os.listdir(dirpath)
	upload_prefix = f'{MEDIA_ROOT}/uploads/{lang}_paras/'

	# print(request.session.items(), request.method)
	if request.method == 'POST':
		form = ImUpForm(request.POST, request.FILES)
		if form.is_valid():
			fobj = request.FILES['hwform']
			jpeg_array = bytearray(fobj.read())
			image = Image.open(io.BytesIO(jpeg_array))
			image = image.convert('RGB')
			para_id = request.session['para_id'] 
			savepath = f'{upload_prefix}{para_id}.jpg'
			# need to create db model to link filename, email, paragraph id(rid)
			image.save(savepath)
			print('After form validation', request.session.items(), request.method)
			return redirect('review', para_id=para_id)
		else:
			print(form.errors)
	else:
		para_id = random.choice(files)[:-4]
		nfile = f'{dirpath}{para_id}.txt'
		text = open(nfile).read()
		context['text'] = text
		request.session['para_id'] = para_id
		# if 'para_id' in request.session:		
		# 	del request.session['para_id']
		# print(f'upload get request{para_id}')
		form = ImUpForm()

	context['form'] = form
	return render(request, page_template, context) 


def review(request, para_id):
	page_template = "review.html"
	context = {}
	lang = request.session['lang']
	dirpath = f'media/{lang}_paras/'
	files = os.listdir(dirpath)
	upload_prefix = f'{MEDIA_ROOT}/uploads/{lang}_paras/'
	display_prefix = f'{MEDIA_URL}/uploads/{lang}_paras/'
	print(request.session.items(), request.method)
	# para_id = request.session['para_id']
	nfile = f'{dirpath}{para_id}.txt'
	print(f'upload {para_id}')
	text = open(nfile).read()
	context['text'] = text	
	
	if request.method == 'POST':
		form = ImUpForm(request.POST, request.FILES)
		if form.is_valid():
			fobj = request.FILES['hwform']
			jpeg_array = bytearray(fobj.read())
			image = Image.open(io.BytesIO(jpeg_array))
			image = image.convert('RGB')
			savepath = f'{upload_prefix}{para_id}.jpg'
			# need to create db model to link filename, email, paragraph id(rid)
			image.save(savepath)
			return redirect('review', para_id=para_id)
	else:
		context['im_path'] =  f'{display_prefix}{para_id}.jpg'
		form = ImUpForm()

	context['form'] = form
	return render(request, page_template, context) 


def home(request):
	page_template = "home.html"
	context = {}
	if request.method == 'POST':
		form = DetailsForm(request.POST)
		print('asdas')
		if form.is_valid():
			lang = form.cleaned_data.get("lang")
			print('CHosen lang', lang)
			request.session['lang'] = lang
			request.session['email'] = form.cleaned_data.get("email")
			return redirect('upload')


	else:
		form = DetailsForm()

	context['form'] = form
	return render(request, page_template, context) 