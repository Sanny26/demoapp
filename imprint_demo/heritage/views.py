from django.shortcuts import render

import os
# Create your views here.

def index(request, pid, patch_id):
	page_template = "hr_index.html"
	context = {}
	context['iname'] = 'docs/heritage/patch_input/images/{}/{}.jpg'.format(pid, patch_id)
	context['rname'] = 'docs/heritage/patch_output/images/{}/{}.jpg'.format(pid, patch_id)
	context['files'] = os.listdir('static/docs/resolution/TestImage/')
	context['pid']  = pid
	context['patch_id'] = patch_id
	context['patch_iname'] = 'docs/heritage/patch_input/patches/{}/{}.jpg'.format(pid, patch_id)
	context['patch_rname'] = 'docs/heritage/patch_output/patches/{}/{}.jpg'.format(pid, patch_id)
	
	# context['patch_iname'] = 'docs/heritage/patch_input/2_patch.gif'
	# context['patch_rname'] = 'docs/heritage/patch_output/2_patch.gif'
	# context['iname'] = 'docs/heritage/patch_input/2.gif'
	# context['rname'] = 'docs/heritage/patch_output/2.gif'
	
	return render(request, page_template, context)



# def index(request, pid, patch_id):
# 	page_template = "hr_index2.html"
# 	context = {}
# 	context['iname'] = 'docs/heritage/input/{}.jpg'.format(pid, patch_id)
# 	context['rname'] = 'docs/heritage/output/{}_output.png'.format(pid, patch_id)
# 	context['files'] = os.listdir('static/docs/resolution/TestImage/')
# 	context['pid']  = pid
# 	context['patch_id'] = patch_id
# 	return render(request, page_template, context)
