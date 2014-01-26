# Create your views here. 
''' This will be the Controller of the Application. Examples below. '''

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# from django.core.urlresolvers import reverse
# from django.shortcuts import render, redirect
# 
def index(request):
	return render(request, 'yalladevelop/index.html')
	
	# return render(request, 'WebGallery/login.html')


# def get_session(request):
# 	response = request.session['session_id']
# 	return HttpResponse('Done')
