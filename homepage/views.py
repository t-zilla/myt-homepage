from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from .models import Player, Rank, Game, Server, News, Setting, Country


def index(request):
	'''

		TODO: Fetch data
		
	'''

	return render(request, 'homepage/index.html', {
		'featured_servers': {},
		'latest_news': {},
		'social_media': '',
		'support': '',
		'jumbo_header': '',
		'jumbo_subheader': '',
		'greeting': '',
		'new_members': {},
		'links': '',
	})


def members(request):
	'''

		TODO: Fetch data
		
	'''

	return render(request, 'homepage/members.html', {
		'members': {},
		'latest_news': {},
		'new_members': {},
		'links': '',
	})

	
def member(request, pk):
	'''

		TODO: Fetch data
		
	'''

	return render(request, 'homepage/member.html', {
		'member': {},
		'latest_news': {},
		'new_members': {},
		'links': '',
	})

	
def servers(request):
	'''

		TODO: Redirect to single server view
		
	'''
	pass

	
def server(request, pk):
	'''

		TODO: Fetch data, implement server status
		
	'''

	return render(request, 'homepage/servers.html', {
		'servers': {},
		'viewed_server': {},
		'latest_news': {},
		'new_members': {},
		'links': '',
	})
	

def news(request, pk):
	'''

		TODO: Fetch data
		
	'''

	return render(request, 'homepage/news.html', {
		'news': {},
		'latest_news': {},
		'new_members': {},
		'links': '',
	})
	

def redirect(request, destination):
	'''
	
		TODO: Redirect to destination
	
	'''
	pass
