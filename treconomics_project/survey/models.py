__author__ = 'leif'

from django.db import models
from django import forms
from django.contrib.auth.models import User

SEX_CHOICES = (
                (' ', 'Please Select'),
                ('F', 'Female'),
                ('M', 'Male'),
                ('N', 'Not Indicated'),
                ('O', 'Other'),
                ('P', 'Prefer not to say')
               )

LANGUAGE_CHOICES = (
    ('', 'Please select'), ('N', 'Native'), ('B', 'Bilingual'), ('P', 'Professional Working'), ('L', 'Limited Working')
)

EXPERTISE_CHOICES = (
    ('', 'Please select'), ('N', 'Never'), ('R', 'Rarely'), ('S', 'Sometimes'), ('F', 'A few times a week'),
    ('M', 'Many times a week'), ('2', '1-2 times a day'), ('3', 'Several times a day')
)


ED_CHOICES = (
                (' ','Please Select'),
                ('H', 'High School'),
                ('C', 'College / Diploma'),
                ('U', 'Undergraduate / Bachelors'),
                ('M', 'Masters'),
                ('P', 'PhD'),
                ('N', 'Prefer not to say')
               )



########## STARTING SURVEYS  ##########################

class DemographicsSurvey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    age = models.IntegerField(default=0, help_text="Please provide your age (in years)")
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, help_text="Please indicate your gender")
    education = models.CharField(max_length=1, choices=ED_CHOICES, help_text="Please indicate your highest level of education")
    language = models.CharField(max_length=1, choices=LANGUAGE_CHOICES, help_text="Please indicate your English language ability", default="")
    search_freq = models.CharField(max_length=1, choices=EXPERTISE_CHOICES, help_text="Please indicate how often you SEARCH FOR news online", default="")
    browse_freq = models.CharField(max_length=1, choices=EXPERTISE_CHOICES, help_text="Please indicate how often you READ news online", default="")

    def __unicode__(self):
        return self.user.username

    def __str__(self):
        return "{}".format(self.user.username)


class PSTCharSearch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    correct = models.IntegerField(default=0)
    incorrect = models.IntegerField(default=0)

    def __unicode__(self):
        return self.user.username

    def __str__(self):
        return "{}".format(self.user.username)


class PSTNumberSearch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    correct = models.IntegerField(default=0)
    incorrect = models.IntegerField(default=0)

    def __unicode__(self):
        return self.user.username

    def __str__(self):
        return "{}".format(self.user.username)


############## PRE TOPIC SURVEY ############### --- needed?

class PreTaskTopicKnowledgeSurvey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task_id = models.IntegerField()
    topic_num = models.IntegerField()
    topic_knowledge = models.IntegerField(default=0)
    topic_relevance = models.IntegerField(default=0)
    topic_interest = models.IntegerField(default=0)
    topic_searched = models.IntegerField(default=0)
    topic_difficulty = models.IntegerField(default=0)

    def __unicode__(self):
        return self.user.username

    def __str__(self):
        return "{}-{}".format(self.user.username, self.task_id)


class PostTaskTopicRatingSurvey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task_id = models.IntegerField(default=0)
    topic_num = models.IntegerField(default=0)
    topic_learn = models.IntegerField(default=0)
    topic_difficulty = models.IntegerField(default=0)
    topic_examples = models.IntegerField(default=0)
    topic_documents = models.IntegerField(default=0)
    topic_interest = models.IntegerField(default=0)

    def __unicode__(self):
        return self.user.username

    def __str__(self):
        return "{}-{}".format(self.user.username, self.task_id)


########## POST TASK SURVEYS #####################

class PostPerceptionSurvey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task_id = models.IntegerField()
    topic_num = models.IntegerField()
    perception_frustration = models.IntegerField(default=0)
    perception_confidence = models.IntegerField(default=0)
    perception_enjoyment = models.IntegerField(default=0)
    perception_satisfaction = models.IntegerField(default=0)
    perception_checking = models.IntegerField(default=0)
    perception_ads = models.IntegerField(default=0)
    perception_tiredness = models.IntegerField(default=0)

    def __unicode__(self):
        return self.user.username

    def __str__(self):
        return "{}-{}".format(self.user.username, self.task_id)



class SystemSurvey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task_id = models.IntegerField()
    topic_num = models.IntegerField()
    system_aesthetics = models.IntegerField(default=0)
    system_boring = models.IntegerField(default=0)
    system_annoying = models.IntegerField(default=0)
    system_ease = models.IntegerField(default=0)
    system_confusing = models.IntegerField(default=0)
    system_focus = models.IntegerField(default=0)
    system_congruence = models.IntegerField(default=0)

    def __unicode__(self):
        return self.user.username

    def __str__(self):
        return "{}".format(self.user.username)



class ConceptListingSurvey(models.Model):
     user = models.ForeignKey(User, on_delete=models.CASCADE)
     task_id = models.IntegerField(default=0)
     topic_num = models.IntegerField(default=0)
     interface = models.IntegerField(default=0)
     concepts = models.TextField(default=0)
     when=models.IntegerField(default=0)

     def __unicode__(self):
         return self.user.username


####### FINAL SURVEYS #################

class PersonalitySurvey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    personality_distract = models.IntegerField(default=0)
    personality_absorbed = models.IntegerField(default=0)
    personality_attention = models.IntegerField(default=0)
    personality_reserved = models.IntegerField(default=0)
    personality_trusting = models.IntegerField(default=0)
    personality_lazy = models.IntegerField(default=0)
    personality_relaxed = models.IntegerField(default=0)
    personality_artistic = models.IntegerField(default=0)
    personality_social = models.IntegerField(default=0)
    personality_fault = models.IntegerField(default=0)
    personality_thorough = models.IntegerField(default=0)
    personality_nervous = models.IntegerField(default=0)
    personality_imagine = models.IntegerField(default=0)

    def __unicode__(self):
        return self.user.username

    def __str__(self):
        return "{}".format(self.user.username)


class OverallInterview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #overall_distracting = models.TextField(default="")
    #overall_preference = models.TextField(default="")
    #overall_ad_effect = models.TextField(default="")
    overall_comments = models.TextField(default="")

    def __unicode__(self):
        return self.user.username

    def __str__(self):
        return "{}".format(self.user.username)





