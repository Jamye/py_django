from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
# Create your views here.

def index(request):
    # User.objects.all().delete() #delete login database
    if "id" not in request.session:
        request.session['id'] = ""

    if "success" not in request.session:
        request.session['success'] = ""
    return render(request, 'main/index.html')



def register(request):
    if request.method == "GET":
        return redirect('/')

    user = User.objects.validate(request.POST)
    if 'errors' in user:
        show = user['errors']
        for i in show:
            messages.error(request, i)
        return redirect('/')
    if user['validate'] == True:
        user = User.objects.filter(email = request.POST['email'])
        request.session['id'] = user[0].id
        request.session['success'] = 'registered'
    return redirect('/success')


def login(request):
    if request.method == "GET":
        return redirect('/')

    user = User.objects.login(request.POST)
    if 'errors' in user:
        show = user['errors']
        for i in show:
            messages.error(request, i)
        return redirect('/')

    if user['login'] == True:
        user = User.objects.filter(email = request.POST['l_email'])
        request.session['id'] = user[0].id
        request.session['success'] = 'logged_in'
    return redirect('/success')


def success(request):
    if "id" not in request.session:
        return redirect('/')
    context = {
    "people" : User.objects.all(),
    "person" : User.objects.filter(id = request.session['id'])[0]
    }
    return render(request, 'main/success.html', context)

def reroute(request):
    messages.add_message(request, messages.INFO, 'Invalid Page.')
    return redirect('/')

def logout(request):
    request.session.clear()
    messages.success(request, "You are now logged out!")
    return redirect('/')
