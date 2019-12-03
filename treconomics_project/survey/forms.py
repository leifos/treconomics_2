__author__ = 'olivia'
from django.forms import ModelForm
from django import forms

from django.forms.widgets import RadioSelect, Textarea
from survey.models import *
from survey.models import DemographicsSurvey, SEX_CHOICES, LANGUAGE_CHOICES, EXPERTISE_CHOICES, ED_CHOICES


#### Starting Survey Forms ######

class DemographicsSurveyForm(ModelForm):
    age = forms.IntegerField(label="Please provide your age (in years).",
                             max_value=100,
                             min_value=0,
                             required=False)

    sex = forms.CharField(max_length=1,
                          widget=forms.Select(choices=SEX_CHOICES),
                          label="Please indicate your sex.",
                          required=False)

    education = forms.CharField(max_length=1, widget=forms.Select(choices=ED_CHOICES),
                                label="Please indicate your highest level of education.", required=False)

    language = forms.CharField(max_length=1,
                               widget=forms.Select(choices=LANGUAGE_CHOICES),
                               label="Please indicate your English language proficiency.",
                               required=False)

    search_freq = forms.CharField(max_length=1, widget=forms.Select(choices=EXPERTISE_CHOICES),
                                  label="Please indicate how often you search for news online", required=False)
    browse_freq = forms.CharField(max_length=1, widget=forms.Select(choices=EXPERTISE_CHOICES),
                                  label="Please indicate how often you read news online", required=False)


    def clean(self):
        cleaned_data = self.cleaned_data
        if not cleaned_data.get("age"):
            cleaned_data["age"] = 0
        return cleaned_data

    class Meta:
        model = DemographicsSurvey
        exclude = ('user',)


### Pre task form ####


#### Post task forms #####
### perception, systems, concepts


class PostPerceptionSurveyForm(ModelForm):
    PERCEPTION_CHOICES = (
        (1, 'Strongly Disagree'), (2, ''), (3, ''), (4, ''), (5, 'Strongly Agree')
    )

    perception_frustration = forms.ChoiceField(widget=RadioSelect, choices=PERCEPTION_CHOICES,
                                                 label="I felt frustrated while doing the task.",
                                                 required=False)
    perception_confidence = forms.ChoiceField(widget=RadioSelect, choices=PERCEPTION_CHOICES,
                                                label="I was confident in my decisions.",
                                                required=False)
    perception_enjoyment = forms.ChoiceField(widget=RadioSelect, choices=PERCEPTION_CHOICES,
                                               label="I enjoyed completing this task.",
                                               required=False)
    perception_satisfaction = forms.ChoiceField(widget=RadioSelect, choices=PERCEPTION_CHOICES,
                                               label="I was satisfied with my search performance.",
                                               required=False)
    perception_checking = forms.ChoiceField(widget=RadioSelect, choices=PERCEPTION_CHOICES,
                                               label="I checked each document carefully before saving.",
                                               required=False)
    perception_difficulty = forms.ChoiceField(widget=RadioSelect, choices=PERCEPTION_CHOICES,
                                             label="I found it difficult to find relevant documents.",
                                              required=False)
    perception_tiredness = forms.ChoiceField(widget=RadioSelect, choices=PERCEPTION_CHOICES,
                                              label="I felt tired when completing this task.",
                                              required=False)
    perception_alert = forms.ChoiceField(widget=RadioSelect, choices=PERCEPTION_CHOICES,
                                     label="I felt alert while I was completing these tasks.", required=False)

    def clean(self):
        return clean_to_zero(self)

    class Meta:
        model = PostPerceptionSurvey
        exclude = ('user', 'task_id', 'topic_num')


class PostSystemSurveyForm(ModelForm):
    SYSTEM_CHOICES = (
        (1, 'Strongly Disagree'), (2, ''), (3, ''), (4, ''),  (5, 'Strongly Agree')
    )

    system_aesthetics = forms.ChoiceField(widget=RadioSelect, choices=SYSTEM_CHOICES,
                                             label="The system was aesthetically appealing.",
                                             required=False)
    system_boring = forms.ChoiceField(widget=RadioSelect, choices=SYSTEM_CHOICES,
                                label="The system was boring.",
                                required=False)
    system_annoying = forms.ChoiceField(widget=RadioSelect, choices=SYSTEM_CHOICES,
                                label="The system was annoying.",
                                required=False)
    system_ease = forms.ChoiceField(widget=RadioSelect, choices=SYSTEM_CHOICES,
                                label="The system was easy to use.",
                                required=False)
    system_confusing = forms.ChoiceField(widget=RadioSelect, choices=SYSTEM_CHOICES,
                                label="The system was confusing.",
                                required=False)
    system_focus = forms.ChoiceField(widget=RadioSelect, choices=SYSTEM_CHOICES,
                                label="The system was engaging.",
                                required=False)

    def clean(self):
        return clean_to_zero(self)

    class Meta:
        model = SystemSurvey
        exclude = ('user', 'task_id', 'topic_num')


class ConceptListingSurveyForm(ModelForm):
     concepts = forms.CharField(widget=forms.Textarea(attrs={"rows":16, "cols":80}),
                                label="For the given topic, please list the relevant entities or descriptions, one per line.",
                                required=False)

     def clean(self):
         return clean_to_zero(self)

     class Meta:
         model = ConceptListingSurvey
         exclude = ('user', 'task_id', 'topic_num', 'when')





#### FINAL SURVEY ######


class FinalPersonalitySurveyForm(ModelForm):
    PERSONALITY_CHOICES = (
    (1, 'Strongly Disagree'), (2, ''), (3, ''), (4, ''), (5, 'Strongly Agree')
    )

    personality_distract = forms.ChoiceField(widget=RadioSelect, choices=PERSONALITY_CHOICES,
                                     label="... tends to block out distractions",
                                     required=False)
    personality_reserved = forms.ChoiceField(widget=RadioSelect, choices=PERSONALITY_CHOICES,
                                     label="... is reserved",
                                     required=False)
    personality_trusting = forms.ChoiceField(widget=RadioSelect, choices=PERSONALITY_CHOICES,
                                     label="... is generally trusting",
                                     required=False)
    personality_lazy = forms.ChoiceField(widget=RadioSelect, choices=PERSONALITY_CHOICES,
                                     label="... tends to be lazy",
                                     required=False)
    personality_relaxed = forms.ChoiceField(widget=RadioSelect, choices=PERSONALITY_CHOICES,
                                     label="... is relaxed, handles stress well",
                                     required=False)
    personality_immersed = forms.ChoiceField(widget=RadioSelect, choices=PERSONALITY_CHOICES,
                                     label="... tends to be immersed in the task at hand ",
                                     required=False)
    personality_artistic = forms.ChoiceField(widget=RadioSelect, choices=PERSONALITY_CHOICES,
                                     label="... has few artistic interests",
                                     required=False)
    personality_social = forms.ChoiceField(widget=RadioSelect, choices=PERSONALITY_CHOICES,
                                     label="... is outgoing, sociable",
                                     required=False)
    personality_absorbed = forms.ChoiceField(widget=RadioSelect, choices=PERSONALITY_CHOICES,
                                     label="... gets absorbed in what I am doing",
                                     required=False)
    personality_fault = forms.ChoiceField(widget=RadioSelect, choices=PERSONALITY_CHOICES,
                                     label="... tends to find fault with others",
                                     required=False)
    personality_thorough = forms.ChoiceField(widget=RadioSelect, choices=PERSONALITY_CHOICES,
                                     label="... does a thorough job",
                                     required=False)
    personality_nervous = forms.ChoiceField(widget=RadioSelect, choices=PERSONALITY_CHOICES,
                                     label="... gets nervous easily",
                                     required=False)
    personality_imagine = forms.ChoiceField(widget=RadioSelect, choices=PERSONALITY_CHOICES,
                                     label="... has an active imagination",
                                     required=False)
    personality_attention = forms.ChoiceField(widget=RadioSelect, choices=PERSONALITY_CHOICES,
                                     label="... is generally attentive",
                                     required=False)


    def clean(self):
        return clean_to_zero(self)

    class Meta:
        model = PersonalitySurvey
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






# class PostConceptListingSurveyForm(ConceptListingSurveyForm):
#     class Meta:
#         model = PostConceptListingSurvey
#         exclude = ('user', 'task_id', 'topic_num')


TOPIC_NOTHING_CHOICES = ( (1, 'Nothing'), (2, ''), (3, ''), (4, ''), (5, 'I Know Details')  )
TOPIC_NOTATALL_CHOICES = ( (1, 'Not at all'), (2, ''), (3, ''), (4, ''), (5, 'Very Much')  )
TOPIC_NEVER_CHOICES = ( (1, 'Never'), (2, ''), (3, ''), (4, ''), (5, 'Very Often')  )
TOPIC_EASY_CHOICES = ( (1, 'Very Easy'), (2, ''), (3, ''), (4, ''), (5, 'Very Difficult')  )
TOPIC_NOTGOOD_CHOICES = ( (1, 'Not Good'), (2, ''), (3, ''), (4, ''), (5, 'Very Good')  )
TOPIC_UNSUCCESSFUL_CHOICES = ( (1, 'Unsuccessful'), (2, ''), (3, ''), (4, ''), (5, 'Successful')  )
TOPIC_FEW_CHOICES = ( (1, 'A few of them'), (2, ''), (3, ''), (4, ''), (5, 'All of them')  )



class PreTaskTopicKnowledgeSurveyForm(ModelForm):

    topic_knowledge = forms.ChoiceField(widget=RadioSelect,
                                        choices=TOPIC_NOTHING_CHOICES,
                                        label="How much do you know about this topic?",
                                        required=True)
    topic_relevance = forms.ChoiceField(widget=RadioSelect,
                                        choices=TOPIC_NOTATALL_CHOICES,
                                        label="How relevant is this topic to your life?",
                                        required=True)
    topic_interest = forms.ChoiceField(widget=RadioSelect,
                                       choices=TOPIC_NOTATALL_CHOICES,
                                       label="How interested are you to learn more about this topic?",
                                       required=True)
    topic_searched = forms.ChoiceField(widget=RadioSelect, choices=TOPIC_NEVER_CHOICES,
                                       label="Have you ever searched for information related to this topic?",
                                       required=True)
    topic_difficulty = forms.ChoiceField(widget=RadioSelect, choices=TOPIC_EASY_CHOICES,
                                         label="How difficult do you think it will be to search for information about this topic?",
                                         required=True)

    def clean(self):
        return clean_to_zero(self)

    class Meta:
        model = PreTaskTopicKnowledgeSurvey
        exclude = ('user', 'task_id', 'topic_num')


class PostTaskTopicRatingSurveyForm(ModelForm):
    relevance_skill = forms.ChoiceField(widget=RadioSelect, choices=TOPIC_NOTGOOD_CHOICES,
                                        label="How would you rate your skill and ability at finding relevant examples?",
                                        required=False)
    relevance_difficulty = forms.ChoiceField(widget=RadioSelect, choices=TOPIC_EASY_CHOICES,
                                             label="How difficult was it to find relevant and different examples?", required=False)
    relevance_system = forms.ChoiceField(widget=RadioSelect, choices=TOPIC_NOTGOOD_CHOICES,
                                         label="How would you rate the system's ability at retrieving relevant examples?",
                                         required=False)
    relevance_success = forms.ChoiceField(widget=RadioSelect, choices=TOPIC_UNSUCCESSFUL_CHOICES,
                                          label="How successful was your search?", required=False)
    relevance_number = forms.ChoiceField(widget=RadioSelect, choices=TOPIC_FEW_CHOICES,
                                         label="How many relevant and different example do you think you found?",
                                         required=False)

    def clean(self):
        return clean_to_zero(self)

    class Meta:
        model = PostTaskTopicRatingSurvey
        exclude = ('user', 'task_id', 'topic_num')



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

