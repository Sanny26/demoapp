from django.shortcuts import render
import os
# Create your views here.
	
def index(request, factor, pid):
	page_template = "hr_index.html"
	context = {}
	folder = 'Results_im_{}x'.format(factor)
	iname = 'final{}.png'.format(pid)
	context['iname'] = 'docs/resolution/TestImage/{}'.format(iname)
	context['rname'] = 'docs/resolution/{}/{}'.format(folder, iname)
	context['files'] = os.listdir('static/docs/resolution/TestImage/')
	context['pid']  = pid
	return render(request, page_template, context)
