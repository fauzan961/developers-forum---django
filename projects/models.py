from django.db import models
import uuid
from django.db.models.base import Model
from users.models import Profile

from django.db.models.fields import CharField #Imported uuid for unique id creation below

# Create your models here

class Project(models.Model): #Compulsarily the class name should be models.Model
    owner = models.ForeignKey(Profile,null=True,blank=True,on_delete=models.CASCADE)
    title = models.CharField(max_length = 200)
    description = models.TextField(null=True, blank=True )
    featured_image = models.ImageField(null=True, blank=True, default="default.jpg")
    demo_link = models.CharField(max_length = 2000, null=True, blank=True)
    source_link = models.CharField(max_length=2000, null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True) #Tag is inside the quotes because the Tag class is created below this class
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):   #To return title name in the projects section of admin page
        return self.title 

    class Meta:
        ordering = ['-vote_ratio','-vote_total','title']   #Will sort projects wrt vote_ratio then vote_total and title
                                                            # - sign for descending order
    @property
    def imageURL(self):
        try:
            url = self.featured_image.url
        except:
            url = ''
        return url

                                                            
     #Creating a function to create a list to store only owner id's of the users who have submitted their reviews
    @property
    def reviewers(self):
        queryset = self.review_set.all().values_list('owner__id', flat=True)
        return queryset

    #Creating a function to update vote count after any user submits review to any project
    @property
    def getVoteCount(self):
        reviews = self.review_set.all()
        upVotes = reviews.filter(value='up').count()
        totalVotes = reviews.count()

        ratio = (upVotes/totalVotes) * 100 
        self.vote_total = totalVotes
        self.vote_ratio = ratio 
        self.save()  

class Review(models.Model):
    VOTE_TYPE = (
        ('up','Up Vote'),
        ('down','Down Vote'),
    )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    class Meta:
        unique_together = [['owner', 'project']] #Same owner cannot review on the same project. 1 review by 1 owner on 1 project

    def __str__(self):
        return self.value

class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name

    


