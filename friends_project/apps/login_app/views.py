# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import messages

from django.shortcuts import render, redirect
from models import user, userhelper, usefultimenow


# htis function will check session to if user is regular or admin and give a bool for each view funciton to use
def loginvalidation(sessiondata, adminlvl):

    if adminlvl>0:
        if "admin" not in sessiondata:
            return False
        if sessiondata["admin"]==True:
            return True
        return False
    if adminlvl==0:
        if 'first_name' in sessiondata:
            return True

def index(request):
    return render(request, "login_app/index.html")

def register(request, method="POST"):
    # this validates all user data in the post request and returns an array of all errors
    errors=user.objects.new_user_validator(request.POST)
    #this creates a new user entry in database if no errors are found
    if len(errors)==0:
        user.objects.enter_new_user(request.POST)
        return render(request, "login_app/userlanding.html")
    #this returns a validation errors page providing the user with what they need to fix to log in
    else:
        for i in range( 0 ,len(errors)):
            messages.add_message(request,messages.INFO,errors[i])
        return render(request,"login_app/validation_errors.html")

def login(request, methods="GET"):
    data= user.objects.login(request.GET)
    if user.objects.login(request.GET)!=False:
        for k in data:
            if k!="birth_date" and k!="created_at":

                request.session[k]=data[k]
                print k, request.session[k]
        # print request.session, "session for ts"
        return redirect("/friends/")

        # return render(request, "login_app/loginlanding.html", context=data)
    else:
        messages.add_message(request, messages.INFO, "email and password did not match")
        return render(request,"login_app/validation_errors.html")

def main_menu(request):
    if loginvalidation(request,0):
        context={
        'first_name':request.session['first_name'],
        'last_name':request.session['last_name'],
        'admin':request.session['admin'],
        }
        return render(request, "login_app/loginlanding.html", context=context)
    else:
        return redirect("/")

def logout(request):
    print "logging out"
    for i in ("first_name", "last_name", "admin","email", "birth_date"):
        try:
            del request.session[i]
        except KeyError:
            pass

    return redirect("/")



def view_users(request):
    data=request.session

    if loginvalidation(request.session, 1):
        users= user.objects.all()
        context={"users":users}
        return render(request,"login_app/userlist.html", context=context)
    else:
        return redirect("/")


def user_by_id(request, num):
    if loginvalidation(request.session, 1):
        target=user.objects.get(id=num)
        context={
        "id":target.id,
        "first_name":target.first_name,
        "last_name":target.last_name,
        'email':target.email,
        'birth_date':target.birth_date,
        'admin': target.admin,
        }
        return render(request,"login_app/user_info.html", context=context)
    else:
        return redirect("/")

def edit_user(request,num, methods="POST"):


    if loginvalidation(request.session, 1):
        target= user.objects.get(id=num)
        target.first_name=request.POST['first_name']
        target.last_name=request.POST['last_name']
        target.email=request.POST['email']
        if len(request.POST['birth_date'])==10:
            target.birth_date=request.POST['birth_date']

        target.admin=request.POST['admin']

        target.save()



        return redirect("/users/"+str(num)+"/")
    else:

        return redirect("/")

def delete_user(request, num):
    if loginvalidation(request.session, 1):

        target=user.objects.get(id=num)
        if request.session['email']==target.email:
            messages.add_message(request, messages.INFO, "you cant delete yourself")
            return render(request,"login_app/validation_errors.html")
        target.delete()

        return redirect("/users/")

    else:
        return redirect("/")






## below are for troubleshooting only leave them commented out unless you either need
## the default admin or to clear the db

# troubleshooting database delete leave everythin up till the redirect commented out
# route is /clear/
def clear(request):

    # print "clearing"
    # user.objects.all().delete()
    return redirect("/")
# unlocks thor, password thundergod leave commented out unless setting up database for the first time
# route is /Thor,theThundergod/
def create_default_admin(request):
    # hashedpass=bcrypt.hashpw("thundergod".encode(),bcrypt.gensalt())
    # user.objects.create(first_name="Thor", last_name="Odinson",email="thor", passwordhash=hashedpass,birth_date="0001-01-01", admin=True )

    return redirect("/")
