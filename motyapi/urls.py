from django.conf.urls import url
from motyapi import views


urlpatterns = [
    url(r'^$', views.HomePageView.as_view()),
]
