from django.shortcuts import render

import os
# Create your views here.

# def index(request, pid, patch_id):
# 	page_template = "hr_index.html"
# 	context = {}	
# 	context['patch_iname'] = 'docs/heritage/patch_input/2_patch.gif'
# 	context['patch_rname'] = 'docs/heritage/patch_output/2_patch.gif'
# 	context['iname'] = 'docs/heritage/patch_input/2.gif'
# 	context['rname'] = 'docs/heritage/patch_output/2.gif'
	
# 	return render(request, page_template, context)

def index(request, pid):
	page_template = "hr_index.html"
	context = {}
	context['pid']  = pid
	context['iname'] = 'docs/heritage/input/{}.jpg'.format(pid)
	context['rname'] = 'docs/heritage/output/{}_output.png'.format(pid)
	context['files'] = [str(i) for i in range(2, 9)]
	# context['patch_iname'] = 'docs/heritage/patch_input/patches/{}/{}.jpg'.format(pid, patch_id)
	# context['iname'] = 'docs/heritage/patch_input/images/{}/{}.jpg'.format(pid, patch_id)
	# context['rname'] = 'docs/heritage/patch_output/images/{}/{}.jpg'.format(pid, patch_id)
	# context['patch_rname'] = 'docs/heritage/patch_output/patches/{}/{}.jpg'.format(pid, patch_id)

	return render(request, page_template, context)




