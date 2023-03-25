from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm
from django.contrib import messages
from django.contrib.auth.models import User
from .utils import searchProfiles, paginateProfiles
from .models import Profile, Skill, Message

# Create your views here.

def loginUser(request):
    page = 'login'
    if request.user.is_authenticated:   #To prevent logged in user to go to login page by typing /login url
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST['username'].lower() 
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)  #To check whether typed username exists or not 
        except:
            messages.error(request,'Username doesnot exist')  #Display flash message on the page
        
        user = authenticate(request, username=username, password=password) #Will check password credentials of user

        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'account') 

        else:
            messages.error(request,'Username or password incorrect')

    return render(request, 'users/login_register.html')

def logoutUser(request):  #Funcion to logout the logged in user
    logout(request)
    messages.info(request,'User was logged out!')
    return redirect('login')

def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()  #Creating object of our created class in forms.py

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  #Commit=False will not directly save the form
            user.username = user.username.lower()  #Will convert any capitalized username into lowercase username
            user.save()

            messages.success(request, 'User account was created!')

            login(request, user)
            return redirect('edit-account')
        else:
            messages.error(request, "Error Occurred during registeration!")

    context = {'page':page,'form':form}
    return render(request, 'users/login_register.html', context)

def profiles(request):
    profiles, search = searchProfiles(request)
    custom_range, profiles = paginateProfiles(request, profiles, 6) #Allow 1 result per page

    context = {'profiles':profiles,'search':search, 'custom_range':custom_range}
    return render(request, 'users/profiles.html',context)

def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    topSkills = profile.skill_set.exclude(description__exact="") #Exclude all skill tags without any description assciated to it
    otherSkills = profile.skill_set.filter(description="")    #Include all skill tags without any description associated to it
    context = {'profile':profile, 'topSkills':topSkills, 'otherSkills':otherSkills}
    return render(request, 'users/user-profile.html', context)

@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile
    skills = profile.skill_set.all()
    projects = profile.project_set.all()

    context = {'profile':profile, 'skills':skills, 'projects':projects}
    return render(request, 'users/account.html', context)

@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)  #Instance is defined to prefill the data of user in the form input boxes
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect('account')
        
    context = {'form':form}
    return render(request, 'users/profile_form.html', context)

@login_required(login_url='login')
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid:
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, 'Skill was added successfully!')
            return redirect('account')
    context={'form':form}
    return render(request, 'users/skill_form.html', context)

@login_required(login_url='login')
def updateSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill) #instance = skill to gather previous data of skills in the form labels
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid:
            form.save()
            messages.success(request, 'Skill was updated successfully!')
            return redirect('account')
    context={'form':form}
    return render(request, 'users/skill_form.html', context)

@login_required(login_url='login')
def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill was deleted succesfully!')
        return redirect('account')
    context={'object':skill}
    return render(request, 'delete_template.html', context)

@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    messageRequests = profile.messages.all()
    unreadCount = messageRequests.filter(is_read=False).count()
    context = {'messageRequests':messageRequests, 'unreadCount':unreadCount}
    return render(request, 'users/inbox.html', context)

@login_required(login_url='login')
def viewMessage(request,pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()    #.save() will add the True value to the database
    context={'message':message}
    return render(request, 'users/message.html', context)

def createMessage(request,pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()
    try:
        sender = request.user.profile
    except:
        sender = None
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient
            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()
            messages.success(request,'Your message was sent successfully!')
            return redirect('user-profile',pk=recipient.id)

    context = {'recipient':recipient,'form':form}
    return render(request, 'users/message_form.html', context)
    
