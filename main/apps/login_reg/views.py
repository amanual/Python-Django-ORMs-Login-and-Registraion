from django.shortcuts import render, redirect, HttpResponse
from django.contrib.messages import error
from django.contrib import messages
from .models import *


# Create your views here.
def index(request):
    print "hello"    
    
    return render(request, 'login_reg/index.html',{"user_data": User.objects.all()})
def create(request):
    # Creats a new user
    errors = User.objects.validate(request.POST)
    if len(errors):
        for field, message in errors.iteritems():
            error(request, message, extra_tags=field)
        return redirect('/')
    # if request.POST['password'] != request.POST['confirmation']:
    #     new_message = 'Your password and confirmation password need to be the same'
    #     error(request,message,extra_tags = new_message)
    
    User.objects.create(
        first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        email = request.POST['email'],
        password = request.POST['password']
        
        )    
    # return render(request,'login_reg/index.html')
    # return render(request, 'login_reg/display_reg.html')
    return redirect('/show')
def show(request):
    context = {
        "user_data": User.objects.all()
        }
    # return redirect('/')
    return render(request,'login_reg/index.html',context)

def login(request):    
    # Displays a page that show success login
    errors = User.objects.validate(request.POST)
    if len(errors):
        for field, message in errors.iteritems():
            error(request, message, extra_tags=field)
        
        return redirect('/')
    

    check_email = request.POST['email']
    user_email = User.objects.filter(email = check_email)
    print check_email

    check_pass = request.POST['password']
    user_pass = User.objects.filter(password = check_pass)
    print check_pass

    if check_email == user_email[0].email and check_pass == user_pass[0].password:
        request.session['email'] = check_email
        request.session['password'] = check_pass
        print request.session['email']
        print request.session['password']
        return render(request, 'login_reg/display_log.html')
    
        
    return redirect('/')
def remove(request,id):
    User.objects.get(id = id).delete()
    return redirect('/show')
