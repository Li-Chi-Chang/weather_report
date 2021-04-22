from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='video_view'),
]

from . import models
for city in models.locations:
    urlpatterns += [
        path(city, views.location, name=city),
    ]