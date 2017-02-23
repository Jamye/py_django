from __future__ import unicode_literals
from django.db import models
from django.contrib import messages
import re
import bcrypt

# Create your models here.

email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
name_regex = re.compile(r'^[a-zA-Z]{2,}$')

class UserManager(models.Manager):
    def validate(self, postData):
        count = 0
        errors = []
        if not name_regex.match(postData['f_name']):
            errors.append("First name must be at least 2 characters and only letters")
            count += 1
        if not name_regex.match(postData['l_name']):
            errors.append("Last name must be at least 2 characters and only letters")
            count += 1
        if not email_regex.match(postData['email']):
            errors.append("Email not valid. Please use name@host.com format")
            count += 1
        if len(User.objects.filter(email = postData['email'])) > 0:
            errors.append("Email in use. Please choose another")
            count += 1
        if postData['pass1'] != postData['pass2']:
            errors.append("Passwords do not match")
            count += 1
        if len(postData['pass1']) | len(postData['pass2']) < 7:
            errors.append("Password must be at least 8 characters")
            count += 1
        if count > 0:
            return {'errors': errors}
        else:
            password = postData['pass1']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            User.objects.create(f_name = postData['f_name'], l_name = postData['l_name'], email = postData['email'], pw_hash = pw_hash)
            return {'validate': True }

    def login(self, postData):
        count = 0
        errors = []
        user = User.objects.filter(email = postData['l_email'])
        if len(user) < 1:
            errors.append("Not a registered Email")
            count +=1
        if count > 0:
            return {'errors': errors}

        else:
            if bcrypt.hashpw(postData['l_password'].encode(), user[0].pw_hash.encode()) == user[0].pw_hash:
                print "it matches***************"
                return {'login': True}
            else:
                print "nopes****************"
                errors.append('Password does not match')
                return {'errors': errors}



class User(models.Model):
    f_name = models.CharField(max_length = 100)
    l_name = models.CharField(max_length = 100)
    email = models.CharField(max_length = 100)
    pw_hash = models.CharField(max_length = 250)
    created_at = models.DateTimeField(auto_now_add =True)
    updated_at = models.DateTimeField(auto_now =True)
    objects = UserManager()
