from django.db.models import Q
from .models import Project, Tag
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def paginateProjects(request, projects, results):
    #Pagination
    page = request.GET.get('page')  #Will store the page indice as clicked by the user from projects template
    results = 6  #Setting variable to show 3 projects per page
    paginator = Paginator(projects, results)
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:  
        page = 1
        projects = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages   #Will set value of page to last page
        projects = paginator.page(page)
    
    # Creating Custom ranges and indexes to limit large no. of buttons on the projects template (Rolling Window for pages)
    leftIndex = (int(page) - 3)
    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page) + 3)
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1
    
    custom_range = range(leftIndex, rightIndex)
    return custom_range, projects


def searchProjects(request):
    search = ''
    if request.GET.get('search'):
        search = request.GET.get('search')
    tags = Tag.objects.filter(name__icontains=search)
    projects = Project.objects.distinct().filter(
        Q(title__icontains=search) |
        Q(description__icontains=search) |
        Q(owner__name__icontains=search) |
        Q(tags__in = tags)
    )   #.objects.all() to get all the data contents of the project table
    return projects, search
