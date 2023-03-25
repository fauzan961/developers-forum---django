from django.contrib import admin

# Register your models here.
from .models import Project, Review, Tag

admin.site.register(Project)  #Adding our created project table in the models.py to the admin panel
admin.site.register(Review)
admin.site.register(Tag)

