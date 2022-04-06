# Generated by Django 2.2 on 2022-04-06 10:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id_chat', models.SmallIntegerField(default=-1, primary_key=True, serialize=False, verbose_name='id_chat')),
            ],
        ),
        migrations.CreateModel(
            name='GroupChannel',
            fields=[
                ('chat_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='chat.Chat')),
                ('channel_name', models.CharField(default=-1, max_length=255, verbose_name='channel_name')),
            ],
            bases=('chat.chat',),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.SmallIntegerField(default=-1, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('text', models.CharField(default='text', max_length=255, verbose_name='text')),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.Chat')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PrivateChat',
            fields=[
                ('chat_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='chat.Chat')),
                ('participant1', models.ForeignKey(default='admin', on_delete=django.db.models.deletion.CASCADE, related_name='participant1', to=settings.AUTH_USER_MODEL)),
                ('participant2', models.ForeignKey(default='admin', on_delete=django.db.models.deletion.CASCADE, related_name='participant2', to=settings.AUTH_USER_MODEL)),
            ],
            bases=('chat.chat',),
        ),
        migrations.CreateModel(
            name='Partecipa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('participant', models.ForeignKey(default='admin', on_delete=django.db.models.deletion.CASCADE, related_name='participant', to=settings.AUTH_USER_MODEL)),
                ('group_channel', models.ForeignKey(default='channel', on_delete=django.db.models.deletion.CASCADE, related_name='group_channel', to='chat.GroupChannel')),
            ],
        ),
    ]
