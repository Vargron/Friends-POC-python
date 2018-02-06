# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from ..login_app.models import user


def loginvalidation(sessiondata, adminlvl):

    if adminlvl>0:
        if "admin" not in sessiondata:
            return False
        if sessiondata["admin"]==True:
            return True
        return False
    if adminlvl==0:
        if 'first_name' not in sessiondata:
            return False
        else:
            return True
# Create your views here.
def index(request):

    if loginvalidation(request.session,0)!=True:
        return redirect("/")
    users=user.objects.all()
    friends=user.objects.get(email=request.session['email']).friends.all()
    if len(friends)<1:
        friends_on=False
    else:
        friends_on= True

    requestor=user.objects.get(email=request.session["email"])

    not_friends=users.exclude(friends=requestor).exclude(email=request.session["email"])



    context={
    "first_name":request.session["first_name"],
    "admin":request.session["admin"],
    'not_friends':not_friends,
    'friends_on':friends_on,
    'friends':friends,
    }
    return render(request, "friend_app/index.html", context=context)




def add_friend(request,num):
    if loginvalidation(request.session,0)!=True:
        return redirect("/")

    print "hitting route"
    requestor= user.objects.get(email=request.session['email'])
    target= user.objects.get(id=num)
    requestor.friends.add(target)
    requestor.save()
    target.friends.add(requestor)
    target.save()
    print user.objects.get(email=request.session['email']).friends.all(), "requestor"

    print user.objects.get(id=num).friends.all(), "target"

    return redirect('/friends/')

def remove_friend(request, num):
    if loginvalidation(request.session,0)!=True:
        return redirect("/")
    requestor= user.objects.get(email=request.session['email'])
    target= user.objects.get(id=num)
    requestor.friends.remove(target)
    target.friends.remove(requestor)
    requestor.save()
    target.save()

    return redirect('/friends/')

def view_friend(request, num):

    if loginvalidation(request.session,0)!=True:
        return redirect("/")
    print "hitting view friend route", num
    target= user.objects.get(id=num)

    context={
    "alias":target.alias,
    "first_name":target.first_name,
    "last_name":target.last_name,
    "email":target.email,

    }
    return render(request, 'friend_app/user_profile.html', context=context)


#used for random queries during development
def test(request):
    # print user.objects.last().friends
    return redirect('/friends/')
