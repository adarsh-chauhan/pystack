"""ocata URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from home import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^delete',views.ocata_delete),
    url(r'^status',views.ocata_status),
    url(r'^console',views.ocata_console),
    url(r'^poweron',views.ocata_poweron),
    url(r'^poweroff',views.ocata_poweroff),
    url(r'^app',views.ocata_app),
    url(r'^signup',views.ocata_signup),
    url(r'about',views.ocata_aboutus),
    url(r'^documentation', views.ocata_documentation),	
    url(r'^',views.ocata_home)
]
