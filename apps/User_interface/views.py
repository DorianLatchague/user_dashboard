from django.shortcuts import render, redirect
from .models import Users, Messages, Comments
from django.contrib import messages
import bcrypt
import re
def welcome(request):
    return render(request, 'User_interface/welcome.html')
def signin(request):
    return render(request, 'User_interface/signin.html')
def register(request):
    return render(request, 'User_interface/register.html')
def dashboard(request):
    if 'id' in request.session:
        context={
            "users" : Users.objects.all(),
            "my_user" : Users.objects.get(id=request.session['id']),
        }
        return render(request, 'User_interface/dashboard.html', context)
    else:
        return redirect('/')
def new(request):
    if 'id' in request.session:
        if Users.objects.get(id=request.session['id']).user_level == 9:
            return render(request, 'User_interface/new.html')
        else:
            return redirect('/dashboard')
    else:
        return redirect('/')
def edit_self(request):
    if 'id' in request.session:
        context = {
            "user" : Users.objects.get(id=request.session['id'])
        }
        return render(request, 'User_interface/edit_self.html', context)
    else:
        return redirect('/')
def show(request, id):
    if 'id' in request.session:
        context={
            "user" : Users.objects.get(id=id),
            "all_messages": Users.objects.get(id=id).messages_received.all().order_by("-created_at")
        }
        return render(request, 'User_interface/show.html', context)
    else:
        return redirect('/')
def admin_edit(request, id):
    if 'id' in request.session:
        if Users.objects.get(id=request.session['id']).user_level == 9:
            if int(id) == request.session['id']:
                return redirect('/users/edit')
            else:
                context={
                    "user" : Users.objects.get(id=id),
                }
                return render(request, 'User_interface/admin_edit.html', context)
        else:
            return redirect('/dashboard')
    else:
        return redirect('/')
def login(request):
    if request.method=="POST":
        if Users.objects.filter(email=request.POST['email']):
            identify = Users.objects.get(email=request.POST['email'])
            if bcrypt.checkpw(request.POST['password'].encode(), identify.password.encode())==True:
                request.session['id'] = identify.id
                return redirect('/dashboard')
            else:
                messages.error(request, "Your password did not match this email address.")
                return redirect('/signin')
        else:
            messages.error(request, "Your email did not match any in our records.")
            return redirect('/signin')
    else:
        return redirect('/signin')
def add_user(request):
    if request.method=="POST":
        errors = Users.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/users/new')
        else:
            pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            Users.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=pw_hash, user_level = 1)
            return redirect('/dashboard')
    else: 
        return redirect('/dashboard')
def registering(request):
    if request.method=="POST":
        errors = Users.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/register')
        else:
            pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            if Users.objects.filter(user_level=9).count() == 0:
                info = Users.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=pw_hash, user_level = 9)
            else:
                info = Users.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=pw_hash, user_level = 1)
            request.session['id'] = info.id
            return redirect('/dashboard')
    else: 
        return redirect('/register')
def edit_info(request):
    if request.method=="POST":
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        edit = {}
        if Users.objects.filter(email=request.POST['email']): 
            messages.error(request, 'This email is already in use')
        elif EMAIL_REGEX.match(request.POST["email"]):
            edit['email'] = request.POST['email']
        elif len(request.POST["email"]) > 0:
            messages.error(request,'Your email is invalid')
        if len(request.POST['first_name']) > 1:
            edit['first_name'] = request.POST['first_name']
        elif len(request.POST['first_name']) == 1:
            messages.error(request,'Your first name needs to be at least 2 characters long.')
        if len(request.POST['last_name']) > 1:
            edit['last_name'] = request.POST['last_name']
        elif len(request.POST['last_name']) == 1:
            messages.error(request, 'Your last name needs to be at least 2 characters long.')
        info = Users.objects.get(id=request.session['id'])
        if 'email' in edit:
            info.email = edit['email']
        if 'first_name' in edit:
            info.first_name = edit['first_name']
        if 'last_name' in edit:
            info.last_name = edit['last_name']
        info.save()
        if len(edit) != 0:
            messages.success(request, 'Changes saved')
    return redirect('/users/edit')
def admin_edit_info(request, id):
    if request.method=="POST":
        if Users.objects.get(id=request.session['id']).user_level == 9:
            EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
            edit = {}
            if Users.objects.filter(email=request.POST['email']): 
                messages.error(request, 'This email is already in use')
            elif EMAIL_REGEX.match(request.POST["email"]):
                edit['email'] = request.POST['email']
            elif len(request.POST["email"]) > 0:
                messages.error(request,'Your email is invalid')
            if len(request.POST['first_name']) > 1:
                edit['first_name'] = request.POST['first_name']
            elif len(request.POST['first_name']) == 1:
                messages.error(request,'Your first name needs to be at least 2 characters long.')
            if len(request.POST['last_name']) > 1:
                edit['last_name'] = request.POST['last_name']
            elif len(request.POST['last_name']) == 1:
                messages.error(request, 'Your last name needs to be at least 2 characters long.')
            info = Users.objects.get(id=id)
            if 'email' in edit:
                info.email = edit['email']
            if 'first_name' in edit:
                info.first_name = edit['first_name']
            if 'last_name' in edit:
                info.last_name = edit['last_name']
            info.user_level = int(request.POST['user_level'])
            info.save()
            if len(edit) != 0:
                messages.success(request, 'Changes saved')
            return redirect('/users/edit/'+str(id))
        else:
            return redirect('/users/edit/'+str(id))
    else:
        return redirect('/users/edit/'+str(id))
def edit_password(request):
    if request.method=="POST":
        if len(request.POST["password"]) < 8:
            messages.error(request,"Your password must be at least 8 characters.")
            return redirect('/users/edit')
        elif request.POST["confirm_password"] != request.POST["password"]:
            messages.error(request,"The confirm password field must be the same as password.")
            return redirect('/users/edit')
        else:
            pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            info = Users.objects.get(id=request.session['id'])
            info.password = pw_hash
            info.save()
            messages.success(request, 'Changes saved')
            return redirect('/users/edit')
    else:
        return redirect('/users/edit')
def admin_edit_password(request, id):
    if request.method == "POST":
        if len(request.POST["password"]) < 8:
            messages.error(request,"Your password must be at least 8 characters.")
            return redirect('/users/edit/'+str(id))
        elif request.POST["confirm_password"] != request.POST["password"]:
            messages.error(request,"The confirm password field must be the same as password.")
            return redirect('/users/edit/'+str(id))
        else:
            pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            save = Users.objects.get(id=id)
            info = Users.objects.get(id=id)
            info.password = pw_hash
            info.save()
            messages.success(request, 'Changes saved')
            return redirect('/users/edit'+str(id))
    else:
        return redirect('/users/edit/'+str(id))
def edit_desc(request):
    if request.method=="POST":
        if request.POST['desc'] == 0:
            messages.error(request, "Please enter a description before pressing enter.")
            return redirect('/users/edit')
        else:
            info = Users.objects.get(id=request.session['id'])
            info.desc = request.POST['desc']
            info.save()
            messages.success(request, 'Changes saved')
            return redirect('/users/edit')
    else:
        return redirect('/users/edit')
def add_message(request, id):
    if request.method=="POST":
        errors = Messages.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
        else:
            user_to = Users.objects.get(id=id)
            user_from = Users.objects.get(id=request.session['id'])
            Messages.objects.create(message=request.POST['message'], user_from=user_from, user_to=user_to)
    return redirect('/users/show/'+str(id))
def add_comment(request, id):
    if request.method=="POST":
        errors = Comments.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
        else:
            user = Users.objects.get(id=request.session['id'])
            message = Messages.objects.get(id=request.POST['message'])
            Comments.objects.create(message=message, comment=request.POST['comment'], user=user)
    return redirect('/users/show/'+str(id))
def delete(request, id):
    if Users.objects.get(id=request.session['id']).user_level == 9:
        Users.objects.get(id=int(id)).delete()
    return redirect('/dashboard')
def logoff(request):
    request.session.clear()
    return redirect('/')