from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.core.validators import URLValidator
from myt_homepage.utils import merge_dicts
from .models import Player, Rank, Game, Server, News, Setting, Country


common_context = {
	'latest_news': News.objects.latest(),
	'new_members': Player.objects.new_members(),
	'links': Setting.fetch_setting('links', '[links]'),
	'footer': Setting.fetch_setting('footer', '[footer]'),
}


def index(request):
	return render(request, 'homepage/index.html', merge_dicts(common_context, {
		'featured_servers': Server.objects.featured(),
		'social_media': Setting.fetch_setting('social_media', '[social_media]'),
		'support': Setting.fetch_setting('support', '[support]'),
		'jumbo_header': Setting.fetch_setting('jumbo_header', '[jumbo_header]'),
		'jumbo_subheader': Setting.fetch_setting('jumbo_subheader', '[jumbo_subheader]'),
		'greeting': Setting.fetch_setting('greeting', '[greeting]'),
	}))


def members(request):
	return render(request, 'homepage/members.html', merge_dicts(common_context, {
		'members': Player.objects.members(),	
	}))

	
def member(request, pk):
	try:
		player = Player.objects.get(pk=pk)
	except Player.DoesNotExist:
		raise Http404

	return render(request, 'homepage/member.html', merge_dicts(common_context, {
		'player': player,
	}))

	
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
	
	if not request.user.is_authenticated and not viewed_server.is_active:
		viewed_server = {}
		
	'''

		TODO: Implement server status
		
	'''

	return render(request, 'homepage/servers.html', merge_dicts(common_context, {
		'servers': servers,
		'viewed_server': viewed_server,
	}))
	

def news(request, pk):
	try:
		news = News.objects.get(pk=pk)
	except News.DoesNotExist:
		raise Http404
		
	if not request.user.is_authenticated and news.is_draft:
		raise Http404
		
	return render(request, 'homepage/news.html', merge_dicts(common_context, {
		'news': news,
	}))
	
	
def flat_page(request, page_key, page_title):
	page_content = Setting.fetch_setting(page_key)
	if not page_content:
		raise Http404
	
	return render(request, 'homepage/flat_page.html', merge_dicts(common_context, {
		'page_title': page_title,
		'page_content': page_content,
	}))

	
def redirect(request, destination):
	address = Setting.fetch_setting(destination)
	try:
		url = URLValidator()
		url(address)
	except:
		raise Http404
	return HttpResponseRedirect(address)
