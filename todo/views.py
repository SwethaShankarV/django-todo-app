from django.shortcuts import render, redirect # render-returns a HTML template with context, redirect-returns HTTP redirect to another URL 
from django.contrib.auth.models import User #Django’s built-in user model
from todo import models
from todo.models import TODOO
# login_required- decorator that blocks unauthenticated users from accessing views
from django.contrib.auth import authenticate, login as auth_login, logout #auth-checks username/password, login&logout-logs the user in by creating a session and out by clearing the session
from django.contrib.auth.decorators import login_required

def signup(request): #handles user registration

    # POST req: processes the submitted signup form
    if request.method=='POST':
        fnm= request.POST.get('fnm')
        emailid= request.POST.get('email')
        pwd=request.POST.get('pwd')
        print(fnm, emailid,pwd)
        myuser= User.objects.create_user(fnm, emailid, pwd)
        myuser.save() #save user to the database
        return redirect('login')
    
    # GET req: shows the signup form
    return render(request, 'signup.html')

def login(request): #handles user login + error messaging
    
    if request.method=='POST':
        fnm= request.POST.get('fnm')
        pwd=request.POST.get('pwd')
        print(fnm, pwd)
        # If credentials are correct, userr gets a 'User' instance, None otheriwse
        userr= authenticate(request, username=fnm, password=pwd)
        if userr is not None:
            auth_login(request, userr) # logs the user in
            return redirect('todo')
        else: # re-renders login page along with the error message
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    
    # GET req: renders empty form
    return render(request, 'login.html')

@login_required(login_url='login') #If the user is not logged in, Django redirects them to the login URL
def todo(request): #dashboard: add tasks and list existing ones
    
    if request.method=='POST':
        title= request.POST.get('title') #Reads the title from the form
        print(title)
        TODOO.objects.create(title=title, user=request.user) #creates a TODOO linked to that specific user (user=request.user)
        # redirect to todo again- avoids re-submitting on refresh
        return redirect('todo')
    
    # else GET: fetches all todos for the current logged-in user(most recent task at top)
    res=TODOO.objects.filter(user=request.user).order_by('-date')
    return render(request, 'todo.html', {'res':res})

@login_required(login_url='login')
def edit_todo(request, srno): # edit one todo item

    if request.method == 'POST':
        title = request.POST.get('title') #gets the updated title(editted task content) from the form
        print(title)
        obj = models.TODOO.objects.get(srno=srno) #looks up that specific todo using srno
        obj.title = title # Update its title and saves it
        obj.save()
        return redirect('todo')

    obj = models.TODOO.objects.get(srno=srno) # Fetch the todo(obj) being edited
    res=models.TODOO.objects.filter(user=request.user).order_by('-date') # Fetch all the todos for that user in order of creation
    return render(request, 'edit_todo.html', {'obj': obj, 'res': res})

@login_required(login_url='login')
def delete_todo(request,srno): #delete task endpoint
    print(srno) #gets srno from URL
    obj=models.TODOO.objects.get(srno=srno)
    obj.delete() #finds that todo and deletes it
    return redirect('todo')

def signout(request): #logout function
    logout(request) # Django's logout(req) clears the session and the {{user}} variable becomes AnonymousUser
    return redirect('login')