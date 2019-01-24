from django.shortcuts import render
import os
# Create your views here.
	
def index(request, pid):
	page_template = "pp_index2.html"
	context = {}
	context['iname'] = 'docs/resolution/IP/final{}.png'.format(pid)
	context['rname'] = 'docs/resolution/Res/final{}.png'.format(pid)
	context['files'] = os.listdir('static/docs/resolution/IP/')
	context['pid']  = pid
	return render(request, page_template, context)
