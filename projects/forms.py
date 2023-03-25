from django.forms import ModelForm
from django import forms
from .models import Project, Review

class ProjectForm(ModelForm): #Creating a Model Form 
    class Meta:
        model = Project      #Applying Model Form on Project Table Created
        fields = ['title', 'featured_image', 'description', 'demo_link', 'source_link']    #Will take all attributes of Project Table for input field in the form
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }

    #Below function is created to style input boxes wrt input class used in css 
    def __init__(self,*args,**kwargs):       #Function created to add styling to the input boxes of the form page 
        super(ProjectForm, self).__init__(*args,**kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


        #self.fields['title'].widget.attrs.update({'class':'input'})  Updating manually one by one 

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value', 'body']
        labels = {
            'value': 'Place your vote',
            'body': 'Add a comment'
        }

    def __init__(self,*args,**kwargs):       
        super(ReviewForm, self).__init__(*args,**kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


        


