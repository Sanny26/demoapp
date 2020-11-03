from django.shortcuts import render, redirect

from .forms import ImUpForm

def upload(request):
	page_template = "upload.html"
	context = {}

	if request.method == 'POST':
		form1 = ImUpForm(request.POST, request.FILES)
		if form1.is_valid():
			fobj = request.FILES['hwform']
			return redirect('home')
	else:
		form1 = ImUpForm()

	context['form1'] = form1
	return render(request, page_template, context) 


def home(request):
	page_template = "home.html"
	context = {}

	text = "Lorem ipsum, or lipsum as it is sometimes known, is dummy text used in laying out print, graphic or web designs. The passage is attributed to an unknown typesetter in the 15th century who is thought to have scrambled parts of Cicero's De Finibus Bonorum et Malorum for use in a type specimen book. It usually begins with:\
			Lorem ipsum, or lipsum as it is sometimes known, is dummy text used in laying out print, graphic or web designs. The passage is attributed to an unknown typesetter in the 15th century who is thought to have scrambled parts of Cicero's De Finibus Bonorum et Malorum for use in a type specimen book. It usually begins with:"
	context['text'] = text	
	
	return render(request, page_template, context) 