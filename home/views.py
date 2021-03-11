from django.shortcuts import render , HttpResponse ,redirect
from home.models import Contact
from django.contrib  import messages
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate ,login , logout
from blog.models import Post

# Create your views here.

#HTML PAGES
def home(request):
    return render(request,'home/home.html')
    # return HttpResponse("This is home inside home")

def contact(request):

    if request.method=='POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        print(name,email,phone,content)
        if len(name)<3 or len(email)<4 or len(phone)<10 or len(content)<4:
            messages.error(request,'Please fill the form correctly')
        else:

            contact = Contact(name=name , email=email ,phone=phone , content=content)
            contact.save()
            messages.success(request,'Your form has been sent Successfully')
    return render(request,'home/contact.html')
    # return HttpResponse("This is contact inside home")

def about(request):
    return render(request,'home/about.html')
    # return HttpResponse("This is about inside home")

def search(request):
    query =request.GET['query']
    if len(query) > 50:
        allPosts = Post.objects.none()
    else:
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsContent = Post.objects.filter(content__icontains=query)
        allPosts = allPostsTitle.union(allPostsContent)
    if allPosts.count()==0:
        messages.warning(request,'No search Results found.........')
    params = {'allPosts':allPosts,'query':query}
    return render(request,'home/search.html',params)
    
#AUTHENTICATION APISs
def handleSignup(request):
    if request.method=='POST':
        # Get the Post Parameters
        username = request.POST['username'] 
        fname = request.POST['fname'] 
        lname = request.POST['lname'] 
        email= request.POST['email'] 
        pass1 = request.POST['pass1'] 
        pass2 = request.POST['pass2']
        print('Post') 

        # Checks for Validition of SignUp
        if len(username)>30:
            messages.error(request,'Message length should under 10 Characters')
            return render(request,'home/home.html')

        # if not username.isalnum():
        #     messages.error(request,'Username should only contain Letters and Numbers')
        #     return render(request,'home/home.html')
        if pass1!=pass2:
            messages.error(request,'Password does not match')
            return render(request,'home/home.html')


        #Create The User
        myuser = User.objects.create_user(username,email,pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request,'Your account has been created successfully')
        return redirect('home')
        # return render(request,'home/home.html')

    else:
        return HttpResponse('404 -Not Found')

def handleLogIn(request):

    if request.method=='POST':
        loginusername = request.POST['loginUsername'] 
        loginpassword = request.POST['loginPass']

        user = authenticate(username=loginusername,password=loginpassword)
        if User is not None:
            login(request,user)
            messages.success(request,'Successfully Logged In')
            return redirect('home')
            # return render(request,'home/home.html')

        else:
            messages.error(request,"Invalid Credentials,Please Try again")
            return redirect('home')
            # return render(request,'home.html')
    else:
        return HttpResponse("404-Not Found")

def handleLogOut(request):
    
    logout(request)
    messages.success(request,"Successfully Logged Out")
    return redirect('home')

def aboutlogin(request):
    return HttpResponse('Please Go to Home Page to Login')

def contactlogin(request):
    return HttpResponse('Please Go to Home Page to Login')