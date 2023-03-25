from .models import Profile, Skill
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def paginateProfiles(request, profiles, results):
    #Pagination
    page = request.GET.get('page')  #Will store the page indice as clicked by the user from profiles template
    paginator = Paginator(profiles, results)
    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:  
        page = 1
        profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages   #Will set value of page to last page
        profiles = paginator.page(page)
    
    # Creating Custom ranges and indexes to limit large no. of buttons on the profiles template (Rolling Window for pages)
    leftIndex = (int(page) - 3)
    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page) + 3)
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1
    
    custom_range = range(leftIndex, rightIndex)
    return custom_range, profiles


def searchProfiles(request):
    search = ''
    if request.GET.get('search'): #Will check if any search input is typed by the user in the search box 
        search = request.GET.get('search')
    skills = Skill.objects.filter(name__icontains=search) #creating variable to enable search by skills also
    profiles = Profile.objects.distinct().filter(Q(name__icontains=search) | Q(short_intro__icontains=search) | Q(skill__in=skills))

    return profiles, search