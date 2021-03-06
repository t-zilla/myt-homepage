# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-10 13:01
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('flag', models.FilePathField(blank=True, null=True, path='F:\\webdev\\myt/media/flags/')),
            ],
            options={
                'verbose_name_plural': 'countries',
            },
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Game title including its version', max_length=20)),
                ('icon', models.ImageField(blank=True, help_text='Allowed types: jpg/png/gif, recommended dimensions: 64x64 pixels', max_length=300, null=True, upload_to='game_icons/')),
                ('is_supported', models.BooleanField(default=True, help_text='Is this game supported by the clan')),
            ],
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('body', models.TextField()),
                ('date_written', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('is_sticky', models.BooleanField(default=False, verbose_name='pin at the top')),
                ('is_draft', models.BooleanField(default=False, verbose_name='save as draft')),
            ],
            options={
                'verbose_name_plural': 'news',
            },
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='associated account')),
                ('is_member', models.BooleanField(default=True)),
                ('date_joined', models.DateField(auto_now_add=True, verbose_name='joined the clan on')),
                ('date_left', models.DateField(blank=True, help_text='Leave blank if currently is a member', null=True, verbose_name='left the clan on')),
                ('first_name', models.CharField(blank=True, max_length=20, null=True)),
                ('birthday', models.DateField(blank=True, null=True)),
                ('gender', models.PositiveIntegerField(blank=True, choices=[(1, 'Male'), (2, 'Female')], null=True)),
                ('discord_profile', models.CharField(blank=True, help_text='Discord name and discriminator in format: Example#1234', max_length=20, null=True)),
                ('steam_profile', models.CharField(blank=True, help_text='Full URL to steam profile', max_length=150, null=True)),
                ('forum_profile', models.PositiveIntegerField(blank=True, help_text='User ID on phpBB forum', null=True)),
                ('db_profile', models.PositiveIntegerField(blank=True, help_text='Profile ID in players database', null=True, verbose_name='DB profile')),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='homepage.Country')),
                ('games', models.ManyToManyField(related_name='players', to='homepage.Game')),
            ],
        ),
        migrations.CreateModel(
            name='Rank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('suffix', models.CharField(blank=True, help_text="Suffix added to member's name, for example: >SrM<", max_length=10, null=True)),
                ('value', models.IntegerField(help_text='Used for sorting; greater value -> rank displayed higher')),
            ],
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('ip', models.GenericIPAddressField(verbose_name='IP address')),
                ('game_port', models.PositiveIntegerField()),
                ('is_active', models.BooleanField(default=True, help_text="Inactive servers aren't displayed")),
                ('is_public', models.BooleanField(default=True)),
                ('value', models.IntegerField(default=0, help_text='Used for sorting; greater value -> higher on the list')),
                ('is_featured', models.BooleanField(default=False, help_text="If there are too many or too few servers marked as featured, 'value' will be the deciding factor", verbose_name='feature on front page')),
                ('gamemode', models.CharField(help_text='Dominant gamemode or a brief description of the server', max_length=20)),
                ('query_enabled', models.BooleanField(default=False, verbose_name='show server status')),
                ('query_type', models.CharField(blank=True, max_length=100, null=True)),
                ('query_port', models.PositiveIntegerField(blank=True, null=True)),
                ('query_username', models.CharField(blank=True, max_length=100, null=True)),
                ('query_password', models.CharField(blank=True, max_length=100, null=True)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='homepage.Game')),
            ],
        ),
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('key', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('verbose_key', models.CharField(blank=True, max_length=50, null=True, verbose_name='setting')),
                ('hints', models.TextField(blank=True, null=True)),
                ('value', models.TextField(blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='player',
            name='rank',
            field=models.ForeignKey(blank=True, help_text='Every member must have a rank', null=True, on_delete=django.db.models.deletion.SET_NULL, to='homepage.Rank'),
        ),
    ]
