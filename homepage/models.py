import datetime
from PIL import Image
import re
import os
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone
from myt_homepage import settings


class PlayerManager(models.Manager):
	def get_queryset(self, *args, **kwargs):
		return super(PlayerManager, self).get_queryset().order_by("user__username")
	
	def members(self):
		return self.get_queryset().filter(is_member=True)
		
	def ex_members(self):
		return self.get_queryset().filter(is_member=False, date_left__isnull=False)
		
	def new_members(self, period=30):
		return self.members().filter(date_joined__gte=timezone.now()-datetime.timedelta(days=period))
	
	
class Player(models.Model):
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
	db_profile = models.PositiveIntegerField("DB profile", null=True, blank=True, help_text="Profile ID in players database")
	
	objects = PlayerManager()
	
	def username(self):
		return self.user.username
		
	def member_name(self):
		if not self.is_member:
			return self.user.username
		else:
			return "|MYT|" + self.user.username
	
	def full_member_name(self):
		if not self.is_member or not self.rank:
			return self.user.username
		elif self.rank.suffix:
			return "|MYT|" + self.user.username + self.rank.suffix
		else:
			return "|MYT|" + self.user.username
		
	def email(self):
		return self.user.email
		
	def age(self):
		today = datetime.date.today()
		if self.birthday:
			return today.year - self.birthday.year - ((today.month, today.day) < (self.birthday.month, self.birthday.day))
		return None
	
	def __str__(self):
		return self.full_member_name()
		
	def clean(self):
		if self.is_member:
			if not self.rank:
				raise ValidationError("Clan member must have a rank.")
			if self.date_left:
				raise ValidationError("Clan member cannot have a date of leave.")
		else:
			if self.rank:
				raise ValidationError("Only clan members can have ranks.")
		if self.date_left:
			if self.date_joined > self.date_left:
				raise ValidationError("Date of leave must be later than join date.")
		if self.birthday and self.age() < 0:
			raise ValidationError("Age must be greater than 0.")
		if self.discord_profile and not re.match(r'.+#\d+', str(self.discord_profile)):
			raise ValidationError("Discord profile must follow the format: Example#1234")
		if self.steam_profile and not re.match(r'https://steamcommunity.com/.*', str(self.steam_profile)):
			raise ValidationError("Steam profile must be the full URL starting with: https://steamcommunity.com/")


class RankManager(models.Manager):
	def get_queryset(self, *args, **kwargs):
		return super(RankManager, self).get_queryset().order_by("-value", "name")
		

class Rank(models.Model):
	name = models.CharField(max_length=30)
	suffix = models.CharField(max_length=10, null=True, blank=True, help_text="Suffix added to member's name, for example: >SrM<")
	value = models.IntegerField(help_text="Used for sorting; greater value -> rank displayed higher")
	
	objects = RankManager()
	
	def __str__(self):
		return self.name
		
	def clean(self):
		if self.suffix and not re.match(r'>.+<', self.suffix):
			raise ValidationError("Suffix must follow the format: >Example<")


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
		image = Image.open(flag.path)
		if image.width != 64 or image.height != 64:
			image = image.resize((22, 16))
			image.save(flag.path)
		

post_save.connect(Game.post_save, Game)
		

class ServerManager(models.Manager):
	def get_queryset(self, *args, **kwargs):
		return super(ServerManager, self).get_queryset().order_by("-value", "game", "name")
		
	def active(self):
		return self.get_queryset().filter(is_active=True)
		
	def featured(self):
		return self.active().order_by("-is_featured", "-value", "game", "name")
	
	
class Server(models.Model):
	name = models.CharField(max_length=50)
	ip = models.GenericIPAddressField("IP address")
	game_port = models.PositiveIntegerField()
	is_active = models.BooleanField(default=True, help_text="Inactive servers aren't displayed")
	is_public = models.BooleanField(default=True)
	game = models.ForeignKey("homepage.Game", on_delete=models.PROTECT)
	value = models.IntegerField(default=0, help_text="Used for sorting; greater value -> higher on the list")
	is_featured = models.BooleanField("feature on front page", default=False, help_text="If there are too many or too few servers marked as featured, 'value' will be the deciding factor")
	gamemode = models.CharField(max_length=20, help_text="Dominant gamemode or a brief description of the server")
	query_enabled = models.BooleanField("show server status", default=False)
	query_type = models.CharField(max_length=100, null=True, blank=True)
	query_port = models.PositiveIntegerField(null=True, blank=True)
	query_username = models.CharField(max_length=100, null=True, blank=True)
	query_password = models.CharField(max_length=100, null=True, blank=True)
	
	objects = ServerManager()
	
	def __str__(self):
		return self.name + " @ " + self.ip + ":" + str(self.game_port)
		
	def clean(self):
		if not 1 <= self.game_port <= 65535:
			raise ValidationError("Port must be between 1 and 65535.")
		'''
		
			TODO: Validate query settings
			
		'''
		

class NewsManager(models.Manager):
	def get_queryset(self, *args, **kwargs):
		return super(NewsManager, self).get_queryset().order_by("-is_sticky", "-date_written")
		
	def public(self):
		return self.get_queryset().filter(is_draft=False)
		
	def latest(self, count=5):
		return self.public()[:count]

		
class News(models.Model):
	title = models.CharField(max_length=150)
	body = models.TextField()
	date_written = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now=True)
	is_sticky = models.BooleanField("pin at the top", default=False)
	is_draft = models.BooleanField("save as draft", default=False)
	
	objects = NewsManager()
	
	def __str__(self):
		return self.title if not self.is_draft else "[Draft] " + self.title
		
	class Meta:
		verbose_name_plural = "news"

		
class Setting(models.Model):
	key = models.CharField(primary_key=True, max_length=50)
	verbose_key = models.CharField("setting", max_length=50, blank=True, null=True)
	hints = models.TextField(blank=True, null=True)
	value = models.TextField(blank=True)
	
	def __str__(self):
		return self.key
	
	
	'''
		Fetches value for the specified key
		Returns default if either key doesn't exist or has empty value
	'''
	@staticmethod
	def fetch_setting(key, default=""):
		try:
			setting = Setting.objects.get(key=key)
		except Setting.DoesNotExist:
			return default
		if setting.value:
			return setting.value
		else:
			return default
		

class Country(models.Model):
	name = models.CharField(max_length=20)
	flag = models.FilePathField(path=settings.MEDIA_ROOT+"flags/", allow_files=True, blank=True, null=True)
	
	def flag_url(self):
		return settings.MEDIA_URL+"flags/"+os.path.basename(self.flag)
	
	def __str__(self):
		return self.name
		
	class Meta:
		verbose_name_plural = "countries"
