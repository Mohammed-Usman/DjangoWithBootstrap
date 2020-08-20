"""django_realtime URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView


from .views import home_page, upload, dbAction, view_tables, database_to_select


urlpatterns = [
    
    path('upload/', upload),
    path('admin/', admin.site.urls),
    path('', home_page, name='home'),
    
    path('fileCalculations/', dbAction),
    path('view-db/', database_to_select),
    # path('view-db/', view_tables),
    
    path('accounts/', include('django.contrib.auth.urls')),
    # path('accounts/login/', auth_views.LoginView.as_view()),
    # path('accounts/logout/', auth_views.LogoutView.as_view()),
    

    # path('', include('django.contrib.auth.urls')),
    #path('', TemplateView.as_view(template_name='hello_world.html'), name='home'),
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)