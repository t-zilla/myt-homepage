from django.contrib import admin
from .models import Player, Rank, Game, Server, News, Setting, Country


admin.site.register(Player)
admin.site.register(Rank)
admin.site.register(Game)
admin.site.register(Server)
admin.site.register(News)
admin.site.register(Setting)
admin.site.register(Country)