from __future__ import unicode_literals
import re
from django.db import models

# Create your models here.
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
NAME_REGEX = re.compile(r'^[^A-Za-z0-9_]$')
class UserManager(models.Manager):
    def validate(self, post_data):
        errors = {}

        # check all fields for emptyness
        for field, value in post_data.iteritems():
            if len(value) < 1 :
                errors[field] = "{} field is reqired".format(field.replace('_', ' '))

            # check name fields for min length
            if field == "first_name" or field == "last_name":
                if not field in errors and len(value) < 2:
                    errors[field] = "{} field must bet at least 2 characters".format(field.replace('_', ' '))
                if not field in errors and re.match(NAME_REGEX, field):
                    errors[field] = "{} field must bet only letters".format(field.replace('_', ' '))
            if field == "email":
                if not field in errors and len(value) < 8:
                    errors[field] = "{} field must bet at least 8 characters".format(field.replace('_', ' '))
                    
        # check email field for valid email
        if not "email" in errors and not re.match(EMAIL_REGEX, post_data['email']):
            errors['email'] = "invalid email"
        
        # if email is valid check db for existing email
        else:
            if len(self.filter(email=post_data['email'])) > 1:
                errors['email'] = "email already in use"

        return errors


class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.EmailField(max_length = 254)
    password = models.CharField(max_length = 255)    
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
    def __str__(self):
        return self.email

