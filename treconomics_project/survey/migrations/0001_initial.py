# Generated by Django 2.2.3 on 2019-12-12 11:00

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
            name='SystemSurvey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.IntegerField()),
                ('topic_num', models.IntegerField()),
                ('system_aesthetics', models.IntegerField(default=0)),
                ('system_boring', models.IntegerField(default=0)),
                ('system_annoying', models.IntegerField(default=0)),
                ('system_ease', models.IntegerField(default=0)),
                ('system_confusing', models.IntegerField(default=0)),
                ('system_focus', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PSTNumberSearch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('correct', models.IntegerField(default=0)),
                ('incorrect', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PSTCharSearch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('correct', models.IntegerField(default=0)),
                ('incorrect', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PreTaskTopicKnowledgeSurvey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.IntegerField()),
                ('topic_num', models.IntegerField()),
                ('topic_knowledge', models.IntegerField(default=0)),
                ('topic_relevance', models.IntegerField(default=0)),
                ('topic_interest', models.IntegerField(default=0)),
                ('topic_searched', models.IntegerField(default=0)),
                ('topic_difficulty', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PostTaskTopicRatingSurvey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.IntegerField(default=0)),
                ('topic_num', models.IntegerField(default=0)),
                ('topic_learn', models.IntegerField(default=0)),
                ('topic_difficulty', models.IntegerField(default=0)),
                ('topic_examples', models.IntegerField(default=0)),
                ('topic_documents', models.IntegerField(default=0)),
                ('topic_interest', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PostPerceptionSurvey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.IntegerField()),
                ('topic_num', models.IntegerField()),
                ('perception_frustration', models.IntegerField(default=0)),
                ('perception_confidence', models.IntegerField(default=0)),
                ('perception_enjoyment', models.IntegerField(default=0)),
                ('perception_satisfaction', models.IntegerField(default=0)),
                ('perception_checking', models.IntegerField(default=0)),
                ('perception_tiredness', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PersonalitySurvey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('personality_distract', models.IntegerField(default=0)),
                ('personality_absorbed', models.IntegerField(default=0)),
                ('personality_immersed', models.IntegerField(default=0)),
                ('personality_attention', models.IntegerField(default=0)),
                ('personality_reserved', models.IntegerField(default=0)),
                ('personality_trusting', models.IntegerField(default=0)),
                ('personality_lazy', models.IntegerField(default=0)),
                ('personality_relaxed', models.IntegerField(default=0)),
                ('personality_artistic', models.IntegerField(default=0)),
                ('personality_social', models.IntegerField(default=0)),
                ('personality_fault', models.IntegerField(default=0)),
                ('personality_thorough', models.IntegerField(default=0)),
                ('personality_nervous', models.IntegerField(default=0)),
                ('personality_imagine', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OverallInterview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('overall_distracting', models.TextField(default='')),
                ('overall_preference', models.TextField(default='')),
                ('overall_ad_effect', models.TextField(default='')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DemographicsSurvey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.IntegerField(default=0, help_text='Please provide your age (in years)')),
                ('sex', models.CharField(choices=[(' ', 'Please Select'), ('F', 'Female'), ('M', 'Male'), ('N', 'Not Indicated'), ('O', 'Other'), ('P', 'Prefer not to say')], help_text='Please indicate your gender', max_length=1)),
                ('education', models.CharField(choices=[(' ', 'Please Select'), ('H', 'High School'), ('C', 'College / Diploma'), ('U', 'Undergraduate / Bachelors'), ('M', 'Masters'), ('P', 'PhD'), ('N', 'Prefer not to say')], help_text='Please indicate your highest level of education', max_length=1)),
                ('language', models.CharField(choices=[('', 'Please select'), ('N', 'Native'), ('B', 'Bilingual'), ('P', 'Professional Working'), ('L', 'Limited Working')], default='', help_text='Please indicate your English language ability', max_length=1)),
                ('search_freq', models.CharField(choices=[('', 'Please select'), ('N', 'Never'), ('R', 'Rarely'), ('S', 'Sometimes'), ('F', 'A few times a week'), ('M', 'Many times a week'), ('2', '1-2 times a day'), ('3', 'Several times a day')], default='', help_text='Please indicate how often you SEARCH FOR news online', max_length=1)),
                ('browse_freq', models.CharField(choices=[('', 'Please select'), ('N', 'Never'), ('R', 'Rarely'), ('S', 'Sometimes'), ('F', 'A few times a week'), ('M', 'Many times a week'), ('2', '1-2 times a day'), ('3', 'Several times a day')], default='', help_text='Please indicate how often you READ news online', max_length=1)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ConceptListingSurvey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.IntegerField(default=0)),
                ('topic_num', models.IntegerField(default=0)),
                ('concepts', models.TextField(default=0)),
                ('when', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
