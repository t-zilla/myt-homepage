from django.conf.urls import url
from . import views


urlpatterns = [
	url(r'^$', views.index, name="index"),
	url(r'^members/$', views.members, name="members"),
	url(r'^members/(?P<pk>\d+)$', views.member, name="member"),
	url(r'^servers/$', views.servers, name="servers"),
	url(r'^servers/(?P<pk>\d+)$', views.server, name="server"),
	url(r'^news/(?P<pk>\d+)$', views.news, name="news"),
	url(r'^forum/$', views.redirect, {"destination": "forum_address"}, name="forum"),
	url(r'^discord/$', views.redirect, {"destination": "discord_address"}, name="discord"),
]