
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('projects/',include('projects.urls')),  #Includes the url's present in the url file of projects folder
    path('',include('users.urls')),  #Any url starting with users will get connected to users.urls py file
    path('api/',include('api.urls')),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="reset_password.html"), name="reset_password" ),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="reset_password_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/,<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="reset.html"), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="reset_password_complete.html"), name="password_reset_complete")
    # Template_name = 'reset_password.html' to render our manually created template instead of django's admin template on forget passwrd
    #Done same for all 4 paths 
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)  #Connecting url path of images of project
urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)