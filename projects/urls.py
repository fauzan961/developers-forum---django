from django.urls import path
from . import views


urlpatterns = [
   # path('projects/',views.projects,name="projects"), #The existing projects url path is modified into homepage below.
    path('',views.projects,name='projects'),
    path('project/<str:pk>/',views.project,name="project"),  #Two url's created with two different names, with functions assigned in the
    #View file of project folder

    path('create-project/', views.createProject, name="create-project"),

    path('update-project/<str:pk>/', views.updateProject, name="update-project",),

    path('delete-project/<str:pk>/', views.deleteProject, name="delete-project"),


]