# Generated by Django 2.2.3 on 2019-07-31 19:18

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
            name='TaskDescription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic_num', models.IntegerField(default=0)),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=1500)),
                ('diversify', models.CharField(default='', max_length=1500)),
            ],
        ),
        migrations.CreateModel(
            name='TopicQuerySuggestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic_num', models.IntegerField(default=0)),
                ('title', models.CharField(max_length=40)),
                ('link', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.CharField(blank=True, max_length=200, null=True)),
                ('experiment', models.IntegerField(default=0)),
                ('condition', models.IntegerField(default=0)),
                ('rotation', models.IntegerField(default=0)),
                ('tasks_completed', models.IntegerField(default=0)),
                ('steps_completed', models.IntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DocumentsExamined',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('docid', models.CharField(max_length=30)),
                ('doc_num', models.CharField(max_length=30)),
                ('judgement', models.IntegerField()),
                ('judgement_date', models.DateTimeField(verbose_name='Date Examined')),
                ('url', models.CharField(max_length=200)),
                ('task', models.IntegerField(default=0)),
                ('topic_num', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]