from django.conf.urls import url
from motyapi import views


urlpatterns = [
    url(r'^$', views.HomePageView.as_view()),
    url(r'^get_bot_responses/$', views.BotResponseView.get_bot_responses),
    url(r'^translate_to_chinese/$', views.BotResponseView.translate_to_chinese),
]
