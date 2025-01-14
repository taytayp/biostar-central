# Generated by Django 2.2 on 2019-05-28 22:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
        ('taggit', '0002_auto_20150616_2121'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Badge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('desc', models.CharField(default='', max_length=200)),
                ('type', models.IntegerField(choices=[(0, 'Bronze'), (1, 'Silver'), (2, 'Gold')], default=0)),
                ('icon', models.CharField(default='', max_length=250)),
                ('uid', models.CharField(max_length=32, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(0, 'Pending'), (1, 'Open'), (2, 'Closed'), (3, 'Deleted')], db_index=True, default=1)),
                ('type', models.IntegerField(choices=[(0, 'Question'), (1, 'Answer'), (6, 'Comment'), (2, 'Job'), (3, 'Forum'), (8, 'Tutorial'), (7, 'Data'), (4, 'Page'), (10, 'Tool'), (11, 'News'), (5, 'Blog'), (9, 'Bulletin Board')], db_index=True)),
                ('title', models.CharField(db_index=True, max_length=200)),
                ('anon', models.BooleanField(default=False)),
                ('rank', models.FloatField(blank=True, db_index=True, default=0)),
                ('answer_count', models.IntegerField(blank=True, db_index=True, default=0)),
                ('accept_count', models.IntegerField(blank=True, default=0)),
                ('reply_count', models.IntegerField(blank=True, db_index=True, default=0)),
                ('comment_count', models.IntegerField(blank=True, default=0)),
                ('vote_count', models.IntegerField(blank=True, db_index=True, default=0)),
                ('thread_votecount', models.IntegerField(db_index=True, default=0)),
                ('view_count', models.IntegerField(blank=True, db_index=True, default=0)),
                ('book_count', models.IntegerField(default=0)),
                ('subs_count', models.IntegerField(default=0)),
                ('creation_date', models.DateTimeField(db_index=True)),
                ('lastedit_date', models.DateTimeField(db_index=True)),
                ('sticky', models.BooleanField(default=False)),
                ('content', models.TextField(default='')),
                ('html', models.TextField(default='')),
                ('tag_val', models.CharField(blank=True, default='', max_length=100)),
                ('uid', models.CharField(db_index=True, max_length=32, unique=True)),
                ('spam', models.IntegerField(choices=[(0, 'Spam'), (1, 'Not spam'), (2, 'Default')], default=2)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('last_contributor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contributor', to=settings.AUTH_USER_MODEL)),
                ('lastedit_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='editor', to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='forum.Post')),
                ('root', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='descendants', to='forum.Post')),
                ('site', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sites.Site')),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
                ('thread_users', models.ManyToManyField(related_name='thread_users', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(choices=[(0, 'Upvote'), (4, 'Empty'), (1, 'DownVote'), (2, 'Bookmark'), (3, 'Accept')], db_index=True, default=4)),
                ('date', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('uid', models.CharField(max_length=32, unique=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='forum.Post')),
            ],
        ),
        migrations.CreateModel(
            name='PostView',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.GenericIPAddressField(blank=True, default='', null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_views', to='forum.Post')),
            ],
        ),
        migrations.CreateModel(
            name='Award',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('uid', models.CharField(max_length=32, unique=True)),
                ('badge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forum.Badge')),
                ('post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='forum.Post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(max_length=32, unique=True)),
                ('type', models.IntegerField(choices=[(2, 'no messages'), (3, 'default'), (0, 'local messages'), (1, 'email'), (4, 'email for every new thread (mailing list mode)')], default=0)),
                ('date', models.DateTimeField()),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subs', to='forum.Post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'post')},
            },
        ),
    ]
