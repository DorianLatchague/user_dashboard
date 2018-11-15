from __future__ import unicode_literals
from django.db import models
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class Usermanager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if not EMAIL_REGEX.match(postData["email"]):
            errors['email'] = "Your email is invalid."
        else:
            if Users.objects.filter(email=postData["email"]):
                errors['email'] = "This email is already in use."
        if len(postData["first_name"]) < 2:
            errors['first_name'] = "Your first name must be at least 2 characters long."
        if len(postData["last_name"]) < 2:
            errors['last_name'] = "Your last name must be at least 2 characters long."
        if len(postData["password"]) < 8:
            errors['password'] = "Your password must be at least 8 characters."
        elif postData["confirm_password"] != postData["password"]:
            errors['confirm_password'] = "The confirm password field must be the same as password."
        return errors

class Users(models.Model):
    email = models.CharField(max_length=55)
    first_name = models.CharField(max_length=55)
    last_name = models.CharField(max_length=55)
    password = models.CharField(max_length=255)
    user_level = models.IntegerField()
    desc = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True) 
    objects = Usermanager()
    
class MessageManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData["message"]) < 5:
            errors['message']= "Your messages must be at least 5 characters long."
        return errors

class Messages(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    user_to = models.ForeignKey(Users, related_name="messages_received")
    user_from = models.ForeignKey(Users, related_name="messages_sent")
    objects = MessageManager()

class CommentManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData["comment"]) < 5:
            errors['comment']= "Your comments must be at least 5 characters long."
        return errors

class Comments(models.Model):
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    message = models.ForeignKey(Messages, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(Users, related_name="comments")
    objects = CommentManager()