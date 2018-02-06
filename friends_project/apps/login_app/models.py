# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime
import bcrypt

def usefultimenow():
    now = datetime.now()

    nowstr=now.strftime('%Y%m%d %H:%M:%S.%f')

    nowstr=nowstr[:-16]
    nowstr=int(nowstr)
    return nowstr



# Create your models here.

class userhelper(models.Manager):
    def new_user_validator(self, postdata):
        print" in user validator"
        errors=[]
        print postdata['first_name'], postdata['last_name']
        # first_name checker length at least 2
        if len(postdata['first_name'])<2:
            errors.append("your first name is too short please enter a valid first name")
        if len(postdata['alias'])<2:
            errors.append("your alias is too short please enter a valid alias")
        # last_name checker length at least 2
        if len(postdata['last_name'])<2:
            errors.append("your last name is too short please enter a valid last name")
        # email checker has at least one at and one dot after an at to prove email address valid does not include
        # first or last character to make sure email address is at least one letter and extension is at least one letter

        if len(postdata['email'])<5:
            errors.append("your email is invalid please enter a valid email adddress")
        else:
            dot=0
            at=0
            order=0
            for i in range(1, len(postdata['email'])-1):

                if postdata['email'][i]== ".":
                    dot+=1
                    if at==1:
                        order+=1
                if postdata['email'][i]=="@":
                    at+=1
            if at!=1 or dot<1 or order<1:
                errors.append("your email is invalid please enter a valid email adddress")

        # this checks that the email is unique:
        users=user.objects.all()
        l= len(users)
        for i in range(0, l):
            print i, users[i], users[i].email
            if users[i].email==postdata['email']:
                 errors.append('this email is already in use')


        # this checks the date against before today

        usefulbirthday=""

        for i in range(0, len(postdata['birth_date'])):
            if postdata['birth_date'][i]!="-":
                usefulbirthday=usefulbirthday+postdata['birth_date'][i]
        usefulbirthday=int(usefulbirthday)
        currenttime=usefultimenow()

        if usefulbirthday > currenttime:
            errors.append("your birth_day has to be after today")

        # this validates passwordhash
        if postdata['password']!= postdata['passwordconfirm']:
            errors.append("your passwords must match")
        if len(postdata['password'])<8:
            errors.append("your password is not long enough it must be 8 characters")

        return errors
    def enter_new_user(self,postdata):
        # this code automates add new user
        hashedpass=bcrypt.hashpw(postdata["password"].encode(),bcrypt.gensalt())
        print hashedpass

        print postdata['first_name'], postdata['last_name'],postdata['birth_date']
        user.objects.create(first_name=postdata['first_name'], last_name= postdata['last_name'],alias= postdata['alias'],email=postdata['email'], passwordhash=hashedpass,birth_date=postdata['birth_date'], admin=False)



    def login(self, postdata):
        users=user.objects.all()
        print users, postdata
        for i in range(0, len(users)):
            print users[i].email, postdata['email']
            if users[i].email==postdata['email']:
                print "match"
                if bcrypt.checkpw(postdata["password"].encode(), users[i].passwordhash.encode()):

                    mydict={
                    "first_name":users[i].first_name,
                    "last_name":users[i].last_name,
                    "email":users[i].email,
                    "birth_date":users[i].birth_date,
                    "admin":users[i].admin,
                    }

                    return mydict
        return False

class user(models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    alias=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    passwordhash=models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    admin=models.BooleanField(default=False)
    birth_date= models.DateTimeField()
    friends=models.ManyToManyField("self", related_name="friends")
    objects=userhelper()
