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
    age = models.IntegerField(default=0, help_text="Please provide your age (in years).")
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, help_text="Please indicate your gender.")
    education = models.CharField(max_length=1, choices=ED_CHOICES, help_text="Please indicate your highest level of education.")
    language = models.CharField(max_length=1, choices=LANGUAGE_CHOICES, help_text="Please indicate your English language ability", default="")
    search_freq = models.CharField(max_length=1, choices=EXPERTISE_CHOICES, help_text="Please indicate how often you search for news online", default="")
    browse_freq = models.CharField(max_length=1, choices=EXPERTISE_CHOICES, help_text="Please indicate how often you read news online", default="")

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


############## PRE TOPIC SURVEY ############### --- needed?

class PreTaskTopicKnowledgeSurvey(models.Model):
     user = models.ForeignKey(User, on_delete=models.CASCADE)
     task_id = models.IntegerField()
     topic_num = models.IntegerField()
     topic_knowledge = models.IntegerField()
     topic_relevance = models.IntegerField()
     topic_interest = models.IntegerField()
     topic_searched = models.IntegerField()
     topic_difficulty = models.IntegerField()

     def __unicode__(self):
         return self.user.username



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
    perception_difficulty = models.IntegerField(default=0)
    perception_tiredness = models.IntegerField(default=0)
    perception_alert = models.IntegerField(default=0)

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

    def __unicode__(self):
        return self.user.username

    def __str__(self):
        return "{}".format(self.user.username)



class ConceptListingSurvey(models.Model):
     user = models.ForeignKey(User, on_delete=models.CASCADE)
     task_id = models.IntegerField(default=0)
     topic_num = models.IntegerField(default=0)
     concepts = models.TextField(default=0)
     when=models.IntegerField(default=0)

     def __unicode__(self):
         return self.user.username


####### FINAL SURVEYS #################

class PersonalitySurvey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    personality_distract = models.IntegerField(default=0)
    personality_absorbed = models.IntegerField(default=0)
    personality_immersed = models.IntegerField(default=0)
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




################# NOT USED ##################
class NasaSurvey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task_id = models.IntegerField()
    topic_num = models.IntegerField()
    nasa_mental = models.IntegerField(default=0)
    nasa_physical = models.IntegerField(default=0)
    nasa_temporal = models.IntegerField(default=0)
    nasa_performance = models.IntegerField(default=0)
    nasa_effort = models.IntegerField(default=0)
    nasa_frustration = models.IntegerField(default=0)

    def __unicode__(self):
        return self.user.username

    def __str__(self):
        return "{}-{}".format(self.user.username, self.task_id)



class NasaFactorCompare(models.Model):
    nasa_mental_physical = forms.CharField(max_length=1)
    nasa_mental_temporal = forms.CharField(max_length=1)
    nasa_mental_performance = forms.CharField(max_length=1)
    nasa_mental_effort = forms.CharField(max_length=1)
    nasa_mental_frustration = forms.CharField(max_length=1)
    nasa_physical_temporal = forms.CharField(max_length=1)
    nasa_physical_performance = forms.CharField(max_length=1)
    nasa_physical_effort = forms.CharField(max_length=1)
    nasa_physical_frustration = forms.CharField(max_length=1)
    nasa_temporal_performance = forms.CharField(max_length=1)
    nasa_temporal_effort = forms.CharField(max_length=1)
    nasa_temporal_frustration = forms.CharField(max_length=1)
    nasa_performance_effort = forms.CharField(max_length=1)
    nasa_performance_frustration = forms.CharField(max_length=1)
    nasa_effort_frustration = forms.CharField(max_length=1)


class PostTaskTopicRatingSurvey(models.Model):
     user = models.ForeignKey(User, on_delete=models.CASCADE)
     task_id = models.IntegerField(default=0)
     topic_num = models.IntegerField(default=0)
     relevance_difficulty = models.IntegerField(default=0)
     relevance_skill = models.IntegerField(default=0)
     relevance_system = models.IntegerField(default=0)
     relevance_success = models.IntegerField(default=0)
     relevance_number = models.IntegerField(default=0)

     def __unicode__(self):
         return self.user.username


# class PostConceptListingSurvey(ConceptListingSurvey):
#     def __unicode__(self):
#         return self.user.username


# class ModifiedStressSurvey(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     stress_confident = models.IntegerField(default=0)
#     stress_alert = models.IntegerField(default=0)
#     stress_irritated = models.IntegerField(default=0)
#     stress_others = models.IntegerField(default=0)
#     stress_angry = models.IntegerField(default=0)
#     stress_proficient = models.IntegerField(default=0)
#     stress_grouchy = models.IntegerField(default=0)
#     stress_concerned = models.IntegerField(default=0)
#     stress_committed = models.IntegerField(default=0)
#     stress_annoyed = models.IntegerField(default=0)
#     stress_impatient = models.IntegerField(default=0)
#     stress_self_conscious = models.IntegerField(default=0)
#     stress_control = models.IntegerField(default=0)
#     stress_sad = models.IntegerField(default=0)
#     stress_active = models.IntegerField(default=0)
#     stress_motivated = models.IntegerField(default=0)
#     stress_dissatisfied = models.IntegerField(default=0)
#     stress_performance = models.IntegerField(default=0)
#
#     def __unicode__(self):
#         return self.user.username

# class ShortStressSurvey(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     stress_confident = models.IntegerField(default=0)
#     stress_alert = models.IntegerField(default=0)
#     stress_others = models.IntegerField(default=0)
#     stress_figure = models.IntegerField(default=0)
#     stress_angry = models.IntegerField(default=0)
#     stress_proficient = models.IntegerField(default=0)
#     stress_irritated = models.IntegerField(default=0)
#     stress_grouchy = models.IntegerField(default=0)
#     stress_reflecting = models.IntegerField(default=0)
#     stress_concerned = models.IntegerField(default=0)
#     stress_committed = models.IntegerField(default=0)
#     stress_annoyed = models.IntegerField(default=0)
#     stress_impatient = models.IntegerField(default=0)
#     stress_self_conscious = models.IntegerField(default=0)
#     stress_daydreaming = models.IntegerField(default=0)
#     stress_control = models.IntegerField(default=0)
#     stress_sad = models.IntegerField(default=0)
#     stress_active = models.IntegerField(default=0)
#     stress_motivated = models.IntegerField(default=0)
#     stress_dissatisfied = models.IntegerField(default=0)
#     stress_performance = models.IntegerField(default=0)
#
#     def __unicode__(self):
#         return self.user.username



# class SearchEfficacy(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     efficacy_identify_requirements = models.IntegerField(default=0)
#     efficacy_develop_queries = models.IntegerField(default=0)
#     efficacy_special_syntax = models.IntegerField(default=0)
#     efficacy_evaluate_list = models.IntegerField(default=0)
#     efficacy_many_relevant = models.IntegerField(default=0)
#     efficacy_enough_results = models.IntegerField(default=0)
#     efficacy_like_a_pro = models.IntegerField(default=0)
#     efficacy_few_irrelevant = models.IntegerField(default=0)
#     efficacy_structure_time = models.IntegerField(default=0)
#     efficacy_focus_query = models.IntegerField(default=0)
#     efficacy_distinguish_relevant = models.IntegerField(default=0)
#     efficacy_competent_effective = models.IntegerField(default=0)
#     efficacy_little_difficulty = models.IntegerField(default=0)
#     efficacy_allocated_time = models.IntegerField(default=0)
#
#     def __unicode__(self):
#         return self.user.username
