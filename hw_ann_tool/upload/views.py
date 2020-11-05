from django.shortcuts import render, redirect

from .forms import ImUpForm, DetailsForm

import random
import os

def upload(request):
	page_template = "upload.html"
	context = {}
	lang = request.session['lang']
	dirpath = f'media/{lang}_paras/'
	files = os.listdir(dirpath)

	# text = "Lorem ipsum, or lipsum as it is sometimes known, is dummy text used in laying out print, graphic or web designs. The passage is attributed to an unknown typesetter in the 15th century who is thought to have scrambled parts of Cicero's De Finibus Bonorum et Malorum for use in a type specimen book. It usually begins with:\
	# 		Lorem ipsum, or lipsum as it is sometimes known, is dummy text used in laying out print, graphic or web designs. The passage is attributed to an unknown typesetter in the 15th century who is thought to have scrambled parts of Cicero's De Finibus Bonorum et Malorum for use in a type specimen book. It usually begins with:"
	nfile = f'{dirpath}{random.choice(files)}'
	text = open(nfile).read()
	context['text'] = text	
	
	if request.method == 'POST':
		form = ImUpForm(request.POST, request.FILES)
		if form.is_valid():
			fobj = request.FILES['hwform']
			return redirect('home')
	else:
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
			return redirect('upload')


	else:
		form = DetailsForm()

	context['form'] = form
	return render(request, page_template, context) 