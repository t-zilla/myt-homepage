from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.core.validators import URLValidator
from .models import Player, Rank, Game, Server, News, Setting, Country


def index(request):
	return render(request, 'homepage/index.html', {
		'featured_servers': Server.objects.featured(),
		'latest_news': News.objects.public()[:5],
		'social_media': Setting.fetch_setting('social_media'),
		'support': Setting.fetch_setting('support'),
		'jumbo_header': Setting.fetch_setting('jumbo_header'),
		'jumbo_subheader': Setting.fetch_setting('jumbo_subheader'),
		'greeting': Setting.fetch_setting('greeting'),
		'new_members': Player.objects.new_members(),
		'links': Setting.fetch_setting('links'),
	})


def members(request):
	return render(request, 'homepage/members.html', {
		'members': Player.objects.members(),
		'latest_news': News.objects.public()[:5],
		'new_members': Player.objects.new_members(),
		'links': Setting.fetch_setting('links'),
	})

	
def member(request, pk):
	try:
		player = Player.objects.get(pk=pk)
	except Player.DoesNotExist:
		raise Http404

	return render(request, 'homepage/member.html', {
		'player': player,
		'latest_news': News.objects.public()[:5],
		'new_members': Player.objects.new_members(),
		'links': Setting.fetch_setting('links'),
	})

	
def servers(request):
	servers = Server.objects.active()
	if servers.count() > 0:
		return server(request,servers[0].pk)
	else:
		return server(request, -1)

	
def server(request, pk):
	servers = Server.objects.active()
	try:
		viewed_server = Server.objects.get(pk=pk)
	except Server.DoesNotExist:
		viewed_server = {}
	
	'''

		TODO: Implement server status
		
	'''

	return render(request, 'homepage/servers.html', {
		'servers': servers,
		'viewed_server': viewed_server,
		'latest_news': News.objects.public()[:5],
		'new_members': Player.objects.new_members(),
		'links': Setting.fetch_setting('links'),
	})
	

def news(request, pk):
	try:
		news = News.objects.get(pk=pk)
	except News.DoesNotExist:
		raise Http404
	
	return render(request, 'homepage/news.html', {
		'news': news,
		'latest_news': News.objects.public()[:5],
		'new_members': Player.objects.new_members(),
		'links': Setting.fetch_setting('links'),
	})
	
	
def flat_page(request, page_key, page_title):
	page_content = Setting.fetch_setting(page_key)
	if not page_content:
		raise Http404
	
	return render(request, 'homepage/flat_page.html', {
		'page_title': page_title,
		'page_content': page_content,
		'latest_news': News.objects.public()[:5],
		'new_members': Player.objects.new_members(),
		'links': Setting.fetch_setting('links'),
	})

	
def redirect(request, destination):
	address = Setting.fetch_setting(destination)
	try:
		url = URLValidator()
		url(address)
	except:
		raise Http404
	return HttpResponseRedirect(address)
