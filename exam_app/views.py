from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from django.core.exceptions import PermissionDenied


def index(request):
    if "user_id" in request.session:
        return redirect('/dashboard')
    return render(request, "index.html")

def login(request):
    if request.method == "GET":
        return redirect('/')
    if not User.objects.authenticate(request.POST['username'], request.POST['password']):
        messages.error(request,"Invalid username/password")
        return redirect('/')
    user = User.objects.get(username=request.POST['username'])
    request.session['user_id'] = user.id
    messages.success(request, "You have successfully logged in!")
    return redirect('/dashboard')

def register(request):
    if request.method == "GET":
        return redirect('/')
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for e in errors.values():
            messages.error(request, e)
        return redirect('/')
    else:
        user = User.objects.register(request.POST)
        request.session['user_id'] = user.id
        return redirect('/dashboard')

def logout(request):
    request.session.flush()
    return redirect('/')

def dashboard(request):
    if "user_id" not in request.session:
        return redirect('/')
    user= User.objects.get(id=request.session['user_id'])
    ids = []
    for i in user.wishlists.all():
        ids.append(i.id)
    wishlist = Wishlist.objects.exclude(id__in=ids)
    context = {
        'user' : user,
        'wishlists' : wishlist
    }
    return render(request, "dashboard.html", context)

def create(request):
    if "user_id" not in request.session:
        return redirect('/')
    return render(request, "create.html")

def add(request):
    errors = Wishlist.objects.validate(request.POST)
    if len(errors)>0:
        for e in errors.values():
            messages.error(request, e)
        return redirect('/wish_items/create')
    else:
        user = User.objects.get(id=request.session['user_id'])
        wishlist = Wishlist.objects.create(
            item=request.POST['item'],
            user=user
        )
        user.wishlists.add(wishlist)
        return redirect('/dashboard')

def item(request, id):
    if "user_id" not in request.session:
        return redirect('/')
    wishlist = Wishlist.objects.get(id=id)
    context = {
        'wishlist' : wishlist
    }
    return render(request, "item.html", context)

def getItem(request, id):
    user = User.objects.get(id=request.session['user_id'])
    wishlist = Wishlist.objects.get(id=id)
    user.wishlists.add(wishlist)
    return redirect('/dashboard')

def remove(request, id):
    user = User.objects.get(id=request.session['user_id'])
    wishlist = Wishlist.objects.get(id=id)
    user.wishlists.remove(wishlist)
    return redirect('/dashboard')

def delete(request, id):
    wishlist_delete = Wishlist.objects.get(id=id)
    wishlist_delete.delete()
    return redirect('/dashboard')
