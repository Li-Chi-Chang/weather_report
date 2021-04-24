from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
]

from . import models
for city in models.get_locations():
    urlpatterns += [
        path(city, views.location, name=city),
    ]

from django.urls import re_path
urlpatterns += [
    re_path('history/.*', views.history, name='history'),
]

urlpatterns += [
    path('search', views.search, name='search'),
    path('search_post', views.search_post, name='search_post'),
]
