from django.conf.urls import url
from motyapi import views


urlpatterns = [
    url(r'^$', views.HomePageView.as_view()),
    url(r'^get_bot_responses/$', views.BotResponseView.get_bot_response_list),
    url(r'^translate_to_chinese/$', views.BotResponseView.translate),
    url(r'^process_bot_request/$', views.BotResponseView.process_bot_request),
    url(r'^send_tweet/$', views.BotResponseView.send_tweet),
]
