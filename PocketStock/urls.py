"""PocketStock URL Configuration

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
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views, duo_auth

urlpatterns = [
    url(r'^getDashBoardData/$', views.getDashBoardData, name='getDashboardData'),
    url(r'^publicforum/$', views.publicForum, name='publicForum'),
    url(r'^$', views.home, name='home'),
    url(r'insert/', views.insertData, name='ins'),
    url(r'getCompanies/', views.getCompanies, name='getCompanies'),
    url(r'searchResults/', views.searchResults, name='searchresults'),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^accounts/signup', views.signup, name="signup"),

    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),

    url(r'^settings/$', views.settings, name='settings'),
    url(r'^settings/password/$', views.password, name='password'),

    url(r'^accounts/duo_login', duo_auth.login),
    url(r'^accounts/duo_logout/$', duo_auth.logout),
    url(r'^home/$', views.home, name='homepage'),

    url(r'^dashboard/$', views.registered_home, name='dashboard'),
    url(r'^prediction/$', views.predict, name='prediction'),
    url(r'^create_transaction/$', views.create_transaction, name='create_transaction'),
    url(r'^stockProfile/$', views.stockProfile, name='stockProfile'),
    url(r'^forum/', views.forumPage, name="forum"),

    url(r'^chat/$', views.chat_room_direct, name='chat'),
    #url(r'^chat/new/$', views.new_room, name='new_room'),
    url(r'^chat/(?P<label>[\w-]{,50})/$', views.chat_room, name='chat_room'),
]


channel_routing = {}
