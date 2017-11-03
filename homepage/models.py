from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone
from myt_homepage import settings
from myt_homepage.utils import resize_image


class PlayerManager(models.Manager):
	def get_queryset(self, *args, **kwargs):
		return super(PlayerManager, self).get_queryset().order_by("user__username")
	
	def members(self):
		return self.get_queryset().filter(is_member=True)
		
	def ex_members(self):
		return self.get_queryset().filter(is_member=False, date_left__isnull=False)
	
	
class Player(models.Model):
	# Constants
	MALE = 1
	FEMALE = 2
	GENDER_CHOICES = (
		(MALE, 'Male'),
		(FEMALE, 'Female'),
	)

	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, verbose_name="associated account")
	rank = models.ForeignKey("homepage.Rank", on_delete=models.SET_NULL, blank=True, null=True, help_text="Every member must have a rank")
	games = models.ManyToManyField("homepage.Game", related_name="players")
	country = models.ForeignKey("homepage.Country", on_delete=models.SET_NULL, null=True, blank=True)
	is_member = models.BooleanField(default=True)
	date_joined = models.DateField("joined the clan on", auto_now_add=True)
	date_left = models.DateField("left the clan on", null=True, blank=True, help_text="Leave blank if currently is a member")
	first_name = models.CharField(max_length=20, null=True, blank=True)
	birthday = models.DateField(null=True, blank=True)
	gender = models.PositiveIntegerField(choices=GENDER_CHOICES, blank=True, null=True)
	discord_profile = models.CharField(max_length=20, null=True, blank=True, help_text="Discord name and discriminator in format: Example#1234")
	steam_profile = models.CharField(max_length=150, null=True, blank=True, help_text="Full URL to steam profile")
	forum_profile = models.PositiveIntegerField(null=True, blank=True, help_text="User ID on phpBB forum")
	db_profile = models.PositiveIntegerField("DB profile", null=True, blank=True, help_text="Profile ID on players db")
	
	objects = PlayerManager()
	
	def username(self):
		return user.username
		
	def email(self):
		return user.email
	
	def __str__(self):
		return self.user.username
		
	def clean(self):
		'''
		
			TODO: Add model validation
			
		'''
		pass

		
class RankManager(models.Manager):
	def get_queryset(self, *args, **kwargs):
		return super(RankManager, self).get_queryset().order_by("-value", "name")
		

class Rank(models.Model):
	name = models.CharField(max_length=30)
	suffix = models.CharField(max_length=6, null=True, blank=True, help_text="Suffix added to member's name, for example: >SrM<")
	value = models.IntegerField(help_text="Used for sorting; greater value => more significant rank")
	
	objects = RankManager()
	
	def __str__(self):
		return self.name
		
	def clean(self):
		'''
		
			TODO: Add model validation
			
		'''
		pass


class GameManager(models.Manager):
	def get_queryset(self, *args, **kwargs):
		return super(GameManager, self).get_queryset().order_by("title")
		
	def supported(self):
		return self.get_queryset().filter(is_supported=True)
	
		
class Game(models.Model):
	title = models.CharField(max_length=20, help_text="Game title including its version")
	icon = models.ImageField(upload_to="game_icons/", blank=True, null=True, help_text="Allowed types: jpg/png/gif, recommended dimensions: 64x64 pixels", max_length=300)
	is_supported = models.BooleanField(default=True, help_text="Is this game supported by the clan")
	
	objects = GameManager()
	
	def __str__(self):
		return self.title
		
	@staticmethod
	def post_save(sender, instance, *args, **kwargs):
		'''
		
			TODO: Validate and resize icon
		
		'''
		pass
		

post_save.connect(Game.post_save, Game)
		

class ServerManager(models.Manager):
	def get_queryset(self, *args, **kwargs):
		return super(ServerManger, self).get_queryset().order_by("-value", "game", "name")
		
	def active(self):
		return self.get_queryset().filter(is_active=True)
		
	def featured(self):
		return self.active.order_by("-is_featured", "-value", "game", "name")
	
	
class Server(models.Model):
	name = models.CharField(max_length=40)
	ip = models.GenericIPAddressField()
	game_port = models.PositiveIntegerField()
	is_active = models.BooleanField(default=True, help_text="Inactive servers aren't display on the page")
	is_public = models.BooleanField(default=True)
	game = models.ForeignKey("homepage.Game", on_delete=models.PROTECT)
	value = models.IntegerField(default=0, help_text="Used for sorting; greater value => higher on the list")
	is_featured = models.BooleanField("feature on front page", default=False, help_text="If there are too many or too few featured servers, value will be the deciding factor")
	gamemode = models.CharField(max_length=20, help_text="Dominant gamemode or a brief description of the server")
	query_enabled = models.BooleanField("show server status", default=False)
	query_type = models.CharField(max_length=100, null=True, blank=True)
	query_port = models.PositiveIntegerField(null=True, blank=True)
	query_username = models.CharField(max_length=100, null=True, blank=True)
	query_password = models.CharField(max_length=100, null=True, blank=True)
	
	objects = ServerManager()
	
	def __str__(self):
		return self.name + " @ " + self.ip + ":" + self.game_port
		
	def clean(self):
		'''
		
			TODO: Add model validation
			
		'''
		pass
		

class NewsManager(models.Manager):
	def get_queryset(self, *args, **kwargs):
		return super(NewsManager, self).get_queryset().order_by("-is_sticky", "-date_written")
		
	def public():
		return self.get_queryset().filter(is_draft=False)

		
class News(models.Model):
	title = models.CharField(max_length=150)
	body = models.TextField()
	author = models.ForeignKey(User, on_delete=models.PROTECT, related_name="news_written")
	date_written = models.DateTimeField()
	edited_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="news_edited")
	date_edited = models.DateTimeField()
	is_sticky = models.BooleanField(default=False, help_text="Always display at the top")
	is_draft = models.BooleanField("save as draft", default=True)
	
	objects = NewsManager()
	
	def __str__(self):
		return self.title + " by " + self.author.username

	@staticmethod
	def post_save(sender, instance, *args, **kwargs):
		'''
		
			TODO: Populate author, date_written, edited_by and date_edited
		
		'''
		pass
		
	class Meta:
		verbose_name_plural = "news"

post_save.connect(News.post_save, News)
		
		
class Setting(models.Model):
	key = models.CharField(primary_key=True, max_length=50)
	value = models.TextField()
	
	def __str__(self):
		return self.key
		

class Country(models.Model):
	name = models.CharField(max_length=20)
	flag = models.ImageField(upload_to="flags/", blank=True, null=True, help_text="Allowed types: jpg/png/gif, recommended dimensions: 22x16 pixels", max_length=300)
	
	def __str__(self):
		return self.name
		
	@staticmethod
	def post_save(sender, instance, *args, **kwargs):
		'''
		
			TODO: Validate and resize flag
		
		'''
		pass
		
	class Meta:
		verbose_name_plural = "countries"

		
post_save.connect(Country.post_save, Country)
