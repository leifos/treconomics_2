__author__ = 'olivia'
from django.forms import ModelForm
from django import forms

from django.forms.widgets import RadioSelect, Textarea
from survey.models import *


class DemographicsSurveyForm(ModelForm):
    age = forms.IntegerField(label="Please provide your age (in years).",
                             max_value=100,
                             min_value=0,
                             required=False)

    sex = forms.CharField(max_length=1,
                          widget=forms.Select(choices=SEX_CHOICES),
                          label="Please indicate your sex.",
                          required=False)

    language = forms.CharField(max_length=1,
                               widget=forms.Select(choices=LANGUAGE_CHOICES),
                               label="Please indicate your English language proficiency.",
                               required=False)

    expertise = forms.CharField(max_length=1,
                               widget=forms.Select(choices=EXPERTISE_CHOICES),
                               label="How often do you search for or read news online?",
                               required=False)

    def clean(self):
        cleaned_data = self.cleaned_data
        if not cleaned_data.get("age"):
            cleaned_data["age"] = 0
        return cleaned_data

    class Meta:
        model = DemographicsSurvey
        exclude = ('user',)


class PostPerceptionSurveyForm(ModelForm):
    PERCEPTION_CHOICES = (
        (1, 'Strongly disagree'), (2, ''), (3, ''), (4, ''), (5, ''), (6, ''), (7, 'Strongly agree')
    )

    perception_frustration = forms.ChoiceField(widget=RadioSelect, choices=PERCEPTION_CHOICES,
                                                 label="I felt frustrated while doing the task",
                                                 required=False)
    perception_confidence = forms.ChoiceField(widget=RadioSelect, choices=PERCEPTION_CHOICES,
                                                label="I felt confident in my decisions",
                                                required=False)
    perception_enjoyment = forms.ChoiceField(widget=RadioSelect, choices=PERCEPTION_CHOICES,
                                               label="I enjoyed completing this task",
                                               required=False)
    perception_satisfaction = forms.ChoiceField(widget=RadioSelect, choices=PERCEPTION_CHOICES,
                                               label="I was satisfied with my search performance",
                                               required=False)
    perception_checking = forms.ChoiceField(widget=RadioSelect, choices=PERCEPTION_CHOICES,
                                               label="I checked each document carefully before saving",
                                               required=False)
    perception_difficulty = forms.ChoiceField(widget=RadioSelect, choices=PERCEPTION_CHOICES,
                                             label="It was difficult to find relevant documents for the task",
                                              required=False)
    perception_tiredness = forms.ChoiceField(widget=RadioSelect, choices=PERCEPTION_CHOICES,
                                              label="I felt tired when completing this task",
                                              required=False)
    perception_alert = forms.ChoiceField(widget=RadioSelect, choices=PERCEPTION_CHOICES,
                                     label="I felt alert while I was completing these tasks.", required=False)

    def clean(self):
        return clean_to_zero(self)

    class Meta:
        model = PostPerceptionSurvey
        exclude = ('user',)


NASA_LOW_CHOICES = ((1, 'Very Low'), (2, ''), (3, ''), (4, ''), (5, ''), (6, ''), (7, 'Very High'))
NASA_PERFECT_CHOICES = ((1, 'Perfect'), (2, ''), (3, ''), (4, ''), (5, ''), (6, ''), (7, 'Failure'))


def clean_nasa_data(self):
    cleaned_data = self.cleaned_data
    if not cleaned_data.get("nasa_mental"):
        cleaned_data["nasa_mental"] = 0
    if not cleaned_data.get("nasa_temporal"):
        cleaned_data["nasa_temporal"] = 0
    if not cleaned_data.get("nasa_physical"):
        cleaned_data["nasa_physical"] = 0
    if not cleaned_data.get("nasa_performance"):
        cleaned_data["nasa_performance"] = 0
    if not cleaned_data.get("nasa_effort"):
        cleaned_data["nasa_effort"] = 0
    if not cleaned_data.get("nasa_frustration"):
        cleaned_data["nasa_frustration"] = 0
    return cleaned_data


def clean_to_zero(self):
    cleaned_data = self.cleaned_data
    for item in cleaned_data:
        if not cleaned_data[item]:
            cleaned_data[item] = 0
    return cleaned_data


class NasaSurveyForm(ModelForm):
    nasa_mental = forms.ChoiceField(widget=RadioSelect, choices=NASA_LOW_CHOICES,
                                           label="MENTAL DEMAND: How mentally demanding was the task?",
                                           required=False)
    nasa_physical = forms.ChoiceField(widget=RadioSelect, choices=NASA_LOW_CHOICES,
                                             label="PHYSICAL DEMAND: How physically demanding was the task?",
                                             required=False)
    nasa_temporal = forms.ChoiceField(widget=RadioSelect, choices=NASA_LOW_CHOICES,
                                      label="TEMPORAL DEMAND: How hurried or rushed was the pace of the task?",
                                      required=False)
    nasa_performance = forms.ChoiceField(widget=RadioSelect, choices=NASA_PERFECT_CHOICES,
                                         label="PERFORMANCE: How successful were you in accomplishing what you were asked to do?",
                                         required=False)
    nasa_effort = forms.ChoiceField(widget=RadioSelect, choices=NASA_LOW_CHOICES,
                                    label="EFFORT: How hard did you have to work to accomplish your level of performance?",
                                    required=False)
    nasa_frustration = forms.ChoiceField(widget=RadioSelect, choices=NASA_LOW_CHOICES,
                                         label="FRUSTRATION: How insecure, discouraged, irritated, stressed, and annoyed were you?",
                                         required=False)

    def clean(self):
        return clean_nasa_data(self)

    class Meta:
        model = NasaSurvey
        exclude = ('user',)


class PostSystemSurveyForm(ModelForm):
    SYSTEM_CHOICES = (
        (1, 'Yes'), (2, ''), (3, ''), (4, ''), (5, ''), (6, ''), (7, 'No')
    )

    system_aesthetics = forms.ChoiceField(widget=RadioSelect, choices=SYSTEM_CHOICES,
                                             label="Aesthetically appealing",
                                             required=False)
    system_boring = forms.ChoiceField(widget=RadioSelect, choices=SYSTEM_CHOICES,
                                label="Boring",
                                required=False)
    system_annoying = forms.ChoiceField(widget=RadioSelect, choices=SYSTEM_CHOICES,
                                label="Annoying",
                                required=False)
    system_ease = forms.ChoiceField(widget=RadioSelect, choices=SYSTEM_CHOICES,
                                label="Easy to use",
                                required=False)
    system_confusing = forms.ChoiceField(widget=RadioSelect, choices=SYSTEM_CHOICES,
                                label="Confusing",
                                required=False)
    system_focus = forms.ChoiceField(widget=RadioSelect, choices=SYSTEM_CHOICES,
                                label="Enabled me to focus",
                                required=False)

    def clean(self):
        return clean_to_zero(self)

    class Meta:
        model = PostSystemSurvey
        exclude = ('user',)


class FinalPersonalitySurveyForm(ModelForm):
    PERSONALITY_CHOICES = (
    (1, 'Strongly disagree'), (2, ''), (3, ''), (4, ''), (5, ''), (6, ''), (7, 'Strongly agree')
    )

    personality_distract = forms.ChoiceField(widget=RadioSelect, choices=PERSONALITY_CHOICES,
                                     label="While using the Web I am able to block out most other distractions",
                                     required=False)
    personality_absorbed = forms.ChoiceField(widget=RadioSelect, choices=PERSONALITY_CHOICES,
                                     label="While using the Web, I am absorbed in what I am doing",
                                     required=False)
    personality_immersed = forms.ChoiceField(widget=RadioSelect, choices=PERSONALITY_CHOICES,
                                     label="While using the Web, I am immersed in the task I am performing",
                                     required=False)
    personality_attention = forms.ChoiceField(widget=RadioSelect, choices=PERSONALITY_CHOICES,
                                     label="While on the Web, my attention does not get diverted very easily",
                                     required=False)

    def clean(self):
        return clean_to_zero(self)

    class Meta:
        model = FinalPersonalitySurvey
        exclude = ('user',)


# I don't know what the below bit is.....-->

MVP = ( ('M', 'Mental Demand'), ('P', 'Physical Demand') )
MVT = ( ('M', 'Mental Demand'), ('T', 'Temporal Demand') )
MVS = ( ('M', 'Mental Demand'), ('S', 'Performance') )
MVE = ( ('M', 'Mental Demand'), ('E', 'Effort') )
MVF = ( ('M', 'Mental Demand'), ('F', 'Frustration') )
PVT = ( ('P', 'Physical Demand'), ('T', 'Temporal Demand') )
PVS = ( ('P', 'Physical Demand'), ('S', 'Performance') )
PVE = ( ('P', 'Physical Demand'), ('E', 'Effort')  )
PVF = ( ('P', 'Physical Demand'), ('F', 'Frustration') )
TVS = ( ('T', 'Temporal Demand'), ('S', 'Performance') )
TVE = ( ('T', 'Temporal Demand'), ('E', 'Effort') )
TVF = ( ('T', 'Temporal Demand'), ('F', 'Frustration') )
SVE = ( ('S', 'Performance'), ('E', 'Effort') )
SVF = ( ('S', 'Performance'), ('E', 'Frustration') )
EVF = ( ('E', 'Effort'), ('E', 'Frustration') )


class NasaFactorCompareForm(ModelForm):
    nasa_mental_physical = forms.ChoiceField(widget=RadioSelect, choices=MVP, label="", required=False)
    nasa_performance_frustration = forms.ChoiceField(widget=RadioSelect, choices=SVF, label="", required=False)
    nasa_mental_temporal = forms.ChoiceField(widget=RadioSelect, choices=MVT, label="", required=False)
    nasa_physical_effort = forms.ChoiceField(widget=RadioSelect, choices=PVE, label="", required=False)
    nasa_temporal_performance = forms.ChoiceField(widget=RadioSelect, choices=TVS, label="", required=False)
    nasa_mental_effort = forms.ChoiceField(widget=RadioSelect, choices=MVE, label="", required=False)
    nasa_physical_frustration = forms.ChoiceField(widget=RadioSelect, choices=PVF, label="", required=False)
    nasa_performance_effort = forms.ChoiceField(widget=RadioSelect, choices=SVE, label="", required=False)
    nasa_temporal_effort = forms.ChoiceField(widget=RadioSelect, choices=TVE, label="", required=False)
    nasa_mental_frustration = forms.ChoiceField(widget=RadioSelect, choices=MVF, label="", required=False)
    nasa_physical_performance = forms.ChoiceField(widget=RadioSelect, choices=PVS, label="", required=False)
    nasa_physical_temporal = forms.ChoiceField(widget=RadioSelect, choices=PVT, label="", required=False)
    nasa_temporal_frustration = forms.ChoiceField(widget=RadioSelect, choices=TVF, label="", required=False)
    nasa_mental_performance = forms.ChoiceField(widget=RadioSelect, choices=MVS, label="", required=False)
    nasa_effort_frustration = forms.ChoiceField(widget=RadioSelect, choices=EVF, label="", required=False)

    def clean(self):
        cleaned_data = self.cleaned_data
        for item in cleaned_data:
            if not cleaned_data[item]:
                cleaned_data[item] = 'VVV'
                return cleaned_data

    class Meta:
        model = NasaFactorCompare
        exclude = ('user',)


# <----Up until this point.


    # def clean(self):
    #     return clean_to_zero(self)
    #
    # class Meta:
    #     model = PreTaskTopicKnowledgeSurvey
    #     exclude = ('user', 'task_id', 'topic_num')


# class ConceptListingSurveyForm(ModelForm):
#     concepts = forms.CharField(widget=Textarea,
#                                label="Please list any concepts that come to mind for this topic. You can list any concepts "
#                                      "that you feel are relevant or important.",
#                                required=False)
#     paragraph = forms.CharField(widget=Textarea,
#                                 label="Imagine you would like to tell someone you know about what you have learned about this topic."
#                                       " Please compose a paragraph describing the topic and what you learnt about the topic. ",
#                                 required=False)
#
#     def clean(self):
#         return clean_to_zero(self)
#
#     class Meta:
#         model = ConceptListingSurvey
#         exclude = ('user', 'task_id', 'topic_num', 'when')


# class PostConceptListingSurveyForm(ConceptListingSurveyForm):
#     class Meta:
#         model = PostConceptListingSurvey
#         exclude = ('user', 'task_id', 'topic_num')



