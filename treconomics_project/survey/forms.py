__author__ = 'olivia'
from django.forms import ModelForm
from django import forms

from django.forms.widgets import RadioSelect, Textarea
from survey.models import *
from survey.models import DemographicsSurvey, SEX_CHOICES, LANGUAGE_CHOICES, EXPERTISE_CHOICES, ED_CHOICES


def clean_to_zero(self):
    cleaned_data = self.cleaned_data
    for item in cleaned_data:
        if not cleaned_data[item]:
            cleaned_data[item] = 0
    return cleaned_data


#### Starting Survey Forms ######

class DemographicsSurveyForm(ModelForm):
    age = forms.IntegerField(label="Please provide your age (in years)",
                             max_value=100,
                             min_value=0,
                             required=True)

    sex = forms.CharField(max_length=1,
                          widget=forms.Select(choices=SEX_CHOICES),
                          label="Please indicate your sex",
                          required=True)

    education = forms.CharField(max_length=1, widget=forms.Select(choices=ED_CHOICES),
                                label="Please indicate your highest level of education", required=True)

    language = forms.CharField(max_length=1,
                               widget=forms.Select(choices=LANGUAGE_CHOICES),
                               label="Please indicate your English language proficiency",
                               required=True)

    search_freq = forms.CharField(max_length=1, widget=forms.Select(choices=EXPERTISE_CHOICES),
                                  label="Please indicate how often you search for news online", required=True)
    browse_freq = forms.CharField(max_length=1, widget=forms.Select(choices=EXPERTISE_CHOICES),
                                  label="Please indicate how often you read news online", required=True)


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
                                                 required=True)
    perception_confidence = forms.ChoiceField(widget=RadioSelect, choices=PERCEPTION_CHOICES,
                                                label="I was confident in my decisions.",
                                                required=True)
    perception_enjoyment = forms.ChoiceField(widget=RadioSelect, choices=PERCEPTION_CHOICES,
                                               label="I enjoyed completing this task.",
                                               required=True)
    perception_satisfaction = forms.ChoiceField(widget=RadioSelect, choices=PERCEPTION_CHOICES,
                                               label="I was satisfied with my search performance.",
                                               required=True)
    perception_checking = forms.ChoiceField(widget=RadioSelect, choices=PERCEPTION_CHOICES,
                                               label="I checked each document carefully before saving.",
                                               required=True)

    perception_tiredness = forms.ChoiceField(widget=RadioSelect, choices=PERCEPTION_CHOICES,
                                              label="I felt tired when completing this task.",
                                              required=True)
    perception_ads = forms.ChoiceField(widget=RadioSelect, choices=PERCEPTION_CHOICES,
                                               label="If present, I understood why the advertisements were being shown.",
                                               required=False)
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
                                             required=True)
    system_boring = forms.ChoiceField(widget=RadioSelect, choices=SYSTEM_CHOICES,
                                label="The system was boring.",
                                required=True)
    system_annoying = forms.ChoiceField(widget=RadioSelect, choices=SYSTEM_CHOICES,
                                label="The system was annoying.",
                                required=True)
    system_ease = forms.ChoiceField(widget=RadioSelect, choices=SYSTEM_CHOICES,
                                label="The system was easy to use.",
                                required=True)
    system_confusing = forms.ChoiceField(widget=RadioSelect, choices=SYSTEM_CHOICES,
                                label="The system was confusing.",
                                required=True)
    system_focus = forms.ChoiceField(widget=RadioSelect, choices=SYSTEM_CHOICES,
                                label="The system was engaging.",
                                required=True)
    system_congruence = forms.ChoiceField(widget=RadioSelect, choices=SYSTEM_CHOICES,
                                label="If present, the system showed related advertising.",
                                required=False)

    def clean(self):
        return clean_to_zero(self)

    class Meta:
        model = SystemSurvey
        exclude = ('user', 'task_id', 'topic_num')


class ConceptListingSurveyForm(ModelForm):
     concepts = forms.CharField(widget=forms.Textarea(attrs={"rows":16, "cols":80}),
                                label="For the given topic, please list the relevant entities or descriptions, one per line.",
                                required=True)

     def clean(self):
         return clean_to_zero(self)

     class Meta:
         model = ConceptListingSurvey
         exclude = ('user', 'task_id', 'topic_num', 'when', 'interface')




#### FINAL SURVEY ######


class FinalPersonalitySurveyForm(ModelForm):
    PERSONALITY_CHOICES = (
    (1, 'Strongly Disagree'), (2, ''), (3, ''), (4, ''), (5, 'Strongly Agree')
    )

    personality_distract = forms.ChoiceField(widget=RadioSelect, choices=PERSONALITY_CHOICES,
                                     label="... is able to block out distractions.",
                                     required=True)
    personality_reserved = forms.ChoiceField(widget=RadioSelect, choices=PERSONALITY_CHOICES,
                                     label="... is reserved.",
                                     required=True)
    personality_trusting = forms.ChoiceField(widget=RadioSelect, choices=PERSONALITY_CHOICES,
                                     label="... is generally trusting.",
                                     required=True)
    personality_lazy = forms.ChoiceField(widget=RadioSelect, choices=PERSONALITY_CHOICES,
                                     label="... tends to be lazy.",
                                     required=True)
    personality_relaxed = forms.ChoiceField(widget=RadioSelect, choices=PERSONALITY_CHOICES,
                                     label="... is relaxed, handles stress well.",
                                     required=True)
    personality_artistic = forms.ChoiceField(widget=RadioSelect, choices=PERSONALITY_CHOICES,
                                     label="... has few artistic interests.",
                                     required=True)
    personality_social = forms.ChoiceField(widget=RadioSelect, choices=PERSONALITY_CHOICES,
                                     label="... is outgoing, sociable.",
                                     required=True)
    personality_absorbed = forms.ChoiceField(widget=RadioSelect, choices=PERSONALITY_CHOICES,
                                     label="... gets absorbed in what I am doing.",
                                     required=True)
    personality_fault = forms.ChoiceField(widget=RadioSelect, choices=PERSONALITY_CHOICES,
                                     label="... tends to find fault with others.",
                                     required=True)
    personality_thorough = forms.ChoiceField(widget=RadioSelect, choices=PERSONALITY_CHOICES,
                                     label="... does a thorough job.",
                                     required=True)
    personality_nervous = forms.ChoiceField(widget=RadioSelect, choices=PERSONALITY_CHOICES,
                                     label="... gets nervous easily.",
                                     required=True)
    personality_imagine = forms.ChoiceField(widget=RadioSelect, choices=PERSONALITY_CHOICES,
                                     label="... has an active imagination.",
                                     required=True)
    personality_attention = forms.ChoiceField(widget=RadioSelect, choices=PERSONALITY_CHOICES,
                                     label="... is generally attentive.",
                                     required=True)


    def clean(self):
        return clean_to_zero(self)

    class Meta:
        model = PersonalitySurvey
        exclude = ('user',)


class OverallInterviewForm(ModelForm):
    #overall_distracting = forms.CharField(label='Did you find anything distracting when you were searching for relevant documents?', required=True)
    #overall_preference = forms.CharField(label='What system did you find most preferable overall and why? '
    #                                           'When advertisements were present, absent, either, or you’re unsure ', required=True)
    #overall_ad_effect = forms.CharField(label='Did the presence of advertisements affect your search positively or negatively? '
    #                                          'For example, were they enjoyable or helped you to complete the search task? '
    #                                          'Or were they distracting?', required=True)
    overall_comments = forms.CharField(widget=forms.Textarea(attrs={"rows":16, "cols":80}),label='Please list any comments / feedback / suggestions you have about the experiment here', required=False)

    def clean(self):
        return clean_to_zero(self)

    class Meta:
        model = OverallInterview
        exclude = ('user','overall_ad_effect','overall_preference','overall_distracting' )


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
    topic_learn = forms.ChoiceField(widget=RadioSelect, choices=TOPIC_NOTHING_CHOICES ,
                                        label="How much did you learn about this topic?",
                                        required=True)
    topic_examples = forms.ChoiceField(widget=RadioSelect, choices=TOPIC_EASY_CHOICES,
                                         label="How easy was it to find different examples for this topic?",
                                         required=True)
    topic_documents = forms.ChoiceField(widget=RadioSelect, choices=TOPIC_EASY_CHOICES,
                                          label="How difficult was it to find relevant documents for this topic?", required=True)
    topic_interest = forms.ChoiceField(widget=RadioSelect, choices=TOPIC_NOTATALL_CHOICES,
                                         label="How interesting was this topic?",
                                         required=True)
    topic_difficulty = forms.ChoiceField(widget=RadioSelect, choices=TOPIC_EASY_CHOICES,
                                             label="How difficult was this task to complete?", required=True)

    def clean(self):
        return clean_to_zero(self)

    class Meta:
        model = PostTaskTopicRatingSurvey
        exclude = ('user', 'task_id', 'topic_num')
