from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Project, Review, Tag
from django.contrib import messages
from .utils import searchProjects, paginateProjects
from .forms import ProjectForm, ReviewForm

def projects(request):
    #Applying search filter
    projects, search = searchProjects(request)
    custom_range, projects = paginateProjects(request, projects, 6)


    
    context = {'projects': projects,'search':search,  'custom_range':custom_range}
    return render(request,'projects/projects.html',context)            #Function for projects path url 

def project(request,pk):
    projectObj = Project.objects.get(id=pk)  #Variable will store the contents of Project table of specified id
    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = projectObj
        review.owner = request.user.profile
        review.save()
        
        projectObj.getVoteCount #Call the decorator function in the models.py review table
        messages.success(request, 'Your review was submitted succesfully!')
        return redirect(project, pk=projectObj.id)
    return render(request,'projects/single-project.html',{'project':projectObj, 'form':form})    

@login_required(login_url="login")    #To stop the unlogged user to access add/delete/update projects page
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()

    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',', " ").split()
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():   #Checks whether form is properly filled 
            project = form.save(commit=False)     #Adds the data typed by user in the form to the database table
            project.owner = profile
            project.save()
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag) #get_or_create method to avoid duplicate entries of tags
                project.tags.add(tag)
            return redirect('account')   #After submitting the form it will redirect the user to projects page 

    context = {'form':form}
    return render(request, "projects/project_form.html", context )

@login_required(login_url="login")
def updateProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',', " ").split()  #Will get the tags typed in the tag box and split the tags into individual elements of list by using split function
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save()
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag) #get_or_create method to avoid duplicate entries of tags
                project.tags.add(tag)
            return redirect('account')
    context = {'form':form,'project':project}
    return render(request, "projects/project_form.html", context )

@login_required(login_url="login")
def deleteProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('projects')
    context = {'object':project}
    return render(request, 'delete_template.html', context)



