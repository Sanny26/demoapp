from django.shortcuts import render

from .forms import PhotoForm
# Create your views here.

# https://simpleisbetterthancomplex.com/tutorial/2017/03/02/how-to-crop-images-in-a-django-application.html
# http://blog.appliedinformaticsinc.com/how-to-add-image-cropping-features-using-django-image-cropping-app-jcrop/

def index(request):
	page_template = "wr_index.html"
	context = {}
	if request.method == 'POST':
		form = PhotoForm(request.POST, request.FILES)
		if form.is_valid():
			return redirect('index')
	else:
		form = PhotoForm()
		context['path'] = 'wr_pages/notes-34.jpg'
	return render(request, page_template, context)
