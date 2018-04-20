from django.contrib import admin
from .models import Player, Rank, Game, Server, News, Setting, Country


class ServerAdmin(admin.ModelAdmin):
	list_display = ('name', 'ip', 'game_port', 'game', 'is_active', 'is_public', 'is_featured')
	
admin.site.register(Server, ServerAdmin)

class RankAdmin(admin.ModelAdmin):
	list_display = ('name', 'suffix')
	
admin.site.register(Rank, RankAdmin)

class PlayerAdmin(admin.ModelAdmin):
	list_display = ('username', 'is_member', 'rank', 'country',)
	
admin.site.register(Player, PlayerAdmin)

class NewsAdmin(admin.ModelAdmin):
	list_display = ('title', 'date_modified', 'is_draft', 'is_sticky', )
	
admin.site.register(News, NewsAdmin)

class GameAdmin(admin.ModelAdmin):
	list_display = ('title', 'is_supported', )
	
admin.site.register(Game, GameAdmin)

class SettingAdmin(admin.ModelAdmin):
	list_display = ('verbose_key', 'value_trimmed',)

	fields = ('verbose_key', 'hints', 'key', 'value')
	readonly_fields = ()
	readonly_edit_fields = ('key', 'verbose_key', 'hints')
	
	def get_readonly_fields(self, request, obj=None):
		if obj: # editing an existing object
			return self.readonly_fields + self.readonly_edit_fields
		return self.readonly_fields
		
	def value_trimmed(self, obj):
		return "{}".format(obj.value)[:100]
	value_trimmed.short_description = 'Value'
	
admin.site.register(Setting, SettingAdmin)

admin.site.register(Country)