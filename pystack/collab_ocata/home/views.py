''' 
1)	All the API calls (external iteraction) is in the openstack module.

2)	To the Application Template we are primarily returning 3 values:
	response_data, this is string object which gives user friendly information informing him about the result of the action he just performed
	instance_meta, this is a dictionary object which has the details of the instance end user spinned up.
	image_list, this is a list object which has all the images available at end user's disposal on the openstack server.

	url, when the instance is present and in RUNNING state the url string is passed so that the user can view the console.
'''





from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from modules.openstack import *
import re

login="""<li class="nav-item"><a class="nav-link" href="#myModal" data-toggle="modal">Login</a></li>"""
logout=''

def ocata_home(request):
	print('******Debug: IN ocata_home_func_in_views.py:  ')
	if request.method=='get' or request.method=='GET':	
		return render(request,'home/home.html',{'login_logout':login}) 
	else:
		user=request.POST['user']
		password=request.POST['password']
		code = authenticate(user,password)
		print(code)
		if re.match('2[0][012]',str(code))!= None:
			image_list=list_images()
			instance_meta=check_tenant()
			if instance_meta!= None and instance_meta['powerstate'] == 'RUNNING':
				url=get_console()
			else:
				url=None
			global logout
			logout="""<li class="nav-item"><a class="nav-link" title="Log out" href="/logout">Logged in as {0} <i class="fa fa-sign-out"></i></a></li>""".format(user)
			return render(request,'home/app.html',{'image_list':image_list,'instance_meta':instance_meta,'login_logout':logout,'instance_url':url})
		else:
			alert="""<div class="alert alert-warning text-center" style="background=transpartent !important"><strong>Wrong Credentials</strong>, Try Again!</div>"""
			return render(request,'home/home.html',{'alert':alert,'login_logout':login})

def ocata_signup(request):
	print("****** Debug: IN ocate_signup function in filename views.py")
	if request.method == 'get' or request.method == 'GET':
		return render(request,'home/signup.html',{'login_logout':login})
	else:
		username = request.POST['usernametextbox']
		password = request.POST['userpassword']
		confirm_password = request.POST['confirmpassword']
		email_id = request.POST['EmailID']
		email_res = validate_email(email_id)
		if password == confirm_password and email_res:
			alert = create_user(username,password,email_id)
			return render(request,'home/signup.html',{'alert':alert,'login_logout':login})
		else:
			if email_res==False:
				alert = '''<div class="alert alert-warning text-center">Not a Valid Email Address ! Please enter a valid Email Address</div>'''
				return render(request, 'home/signup.html', {'alert': alert,'login_logout':login})
			else:
				alert ='''<div class="alert alert-warning text-center">Password doesn't match, Please try again!</div>'''
				return render(request,'home/signup.html',{'alert':alert,'login_logout':login})

				
				
def ocata_aboutus(request):
	print("****** Debug: in aboutus function in filename views.py")
	if request.method=='get' or request.method=='GET':
		return render(request,'home/about.html',{'login_logout':login})
	else:
		user = request.POST['user']
		password = request.POST['password']
		code = authenticate(user, password)
		print(code)
		if re.match('2[0][012]', str(code)) != None:
			image_list = list_images()
			return render(request, 'home/app.html', {'image_list': image_list,'login_logout':logout})
		else:
			alert = """<div class="alert alert-warning text-center" style="background=transpartent !important"><strong>Wrong Credentials</strong>, Try Again!</div>"""
			return render(request, 'home/documentation.html', {'alert': alert,'login_logout':login})				
				

def ocata_app(request):
	print('******Debug: IN ocata_app_func_in_views.py:  ')
	if request.method=='POST' or request.method =='post':
		args={}
		args['instance_name']=request.POST['instance_name']
		args['instance_image']=request.POST['instance_image']
		args['flavour']=request.POST['flavour']
		response_data=create_instance(**args)
		image_list=list_images()
		instance_meta=check_tenant()
		return render(request,'home/app.html',{'image_list':image_list,'response_data':response_data,'instance_meta':instance_meta,'login_logout':logout})



def ocata_delete(request):
	print('******Debug: IN ocata_delete_func_in_views.py:  ')
	response_data=delete_instance()
	image_list=list_images()
	instance_meta=check_tenant()
	return render(request,'home/app.html',{'image_list':image_list,'response_data':response_data,'instance_meta':instance_meta,'login_logout':logout})


def ocata_status(request):
	print('******Debug: IN ocata_status_func_in_views.py:  ')
	image_list=list_images()
	instance_meta=check_tenant()
	if instance_meta!= None and instance_meta['powerstate'] == 'RUNNING':
		url=get_console()
	else:
		url=None
	response_data=["""<div class="alert alert-success">Info: Instance Status Updated</div>"""]
	return render(request,'home/app.html',{'image_list':image_list,'response_data':response_data,'instance_meta':instance_meta,'login_logout':logout,'instance_url':url})


def ocata_console(request):
	print('******Debug: IN ocata_console_func_in_views.py:  ')
	url=get_console()
	image_list=list_images()
	instance_meta=check_tenant()
	response_data= None
	return render(request,'home/app.html',{'image_list':image_list,'response_data':response_data,'instance_meta':instance_meta,'instance_url':url,'login_logout':logout})


def ocata_poweron(request):
	print('******Debug: IN ocata_poweron_func_in_views.py:  ')
	response_data=instance_on()
	return render(request,'home/app.html',{'response_data':response_data,'login_logout':logout})

def ocata_poweroff(request):
	print('******Debug: IN ocata_poweroff_func_in_views.py:  ')
	response_data=instance_off()
	return render(request,'home/app.html',{'response_data':response_data,'login_logout':logout})


def ocata_documentation(request):
	print('******Debug: IN ocata_documentation_func_in_views.py:  ')
	if request.method=='get' or request.method=='GET':
		return render(request,'home/documentation.html',{'login_logout':login})	
	else:
		user=request.POST['user']
		password=request.POST['password']
		code = authenticate(user,password)
		print(code)
		if re.match('2[0][012]',str(code))!= None:
			instance_meta=check_tenant()
			image_list=list_images()
			return render(request,'home/app.html',{'image_list':image_list,'instance_meta':instance_meta,'login_logout':logout})
		else:
			alert="""<div class="alert alert-warning text-center" style="background=transpartent !important"><strong>Wrong Credentials</strong>, Try Again!</div>"""
			return render(request,'home/documentation.html',{'alert':alert,'login_logout':login})
		
