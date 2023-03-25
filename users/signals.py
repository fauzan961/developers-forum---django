from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile
from django.core.mail import send_mail
from django.conf import settings


#@receiver(post_save, sender=Profile)    Either use this method or .connect method below
def createProfile(sender,instance,created,**kwargs):  #Creating a function to use signals amd create profile after creating a user
    if created:
        user = instance
        profile = Profile.objects.create(
            user = user,
            username = user.username ,
            email = user.email,
            name = user.first_name,
        )
        #Creating a send_mail to send a welcome from gmail account to the newly created user 
        subject = 'Welcome to DevSearch'
        message = 'Thanks for joining our forum!'

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False
        )

def updateUser(sender,instance,created,**kwargs):
    profile = instance
    user = profile.user
    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()


def deleteUser(sender,instance,**kwargs):   #Creating function to delete the user after the profile is deleted
    try:
        user = instance.user
        user.delete()
    except:
        pass


post_save.connect(createProfile, sender=User)   #connects the post save method with any user created
post_save.connect(updateUser, sender=Profile)
post_delete.connect(deleteUser, sender=Profile)