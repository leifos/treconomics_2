from django.contrib import admin
from django import forms
from treconomics.models import DocumentsExamined, UserProfile
from treconomics.models import TaskDescription, TopicQuerySuggestion, TopicAds


class UserProfileAdmin(admin.ModelAdmin):
    fields = ['user', 'data', 'experiment', 'condition', 'rotation', 'tasks_completed', 'steps_completed']
    list_display = ('user', 'data', 'experiment', 'condition', 'rotation', 'tasks_completed', 'steps_completed')


class TaskDescriptionForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = TaskDescription
        fields = ('description', )


class TaskDescriptionAdmin(admin.ModelAdmin):
    list_display = ('topic_num', 'title')
    form = TaskDescriptionForm

class TopicQuerySuggestionForm(forms.ModelForm):
    class Meta:
        model = TopicQuerySuggestion
        fields = ('title', )


class TopicQuerySuggestionAdmin(admin.ModelAdmin):
    list_display = ('topic_num', 'title')
    form = TopicQuerySuggestionForm


class PreTaskTopicKnowledgeSurveyAdmin(admin.ModelAdmin):
    # fields = ['user','task_id','topic_num']
    list_display = ['user', 'task_id', 'topic_num']


class PostTaskTopicRatingSurveyAdmin(admin.ModelAdmin):
    # fields = ['user','task_id','topic_num']
    list_display = ['user', 'task_id', 'topic_num']


class NasaLoadAdmin(admin.ModelAdmin):
    list_display = ['user', 'nasa_mental_demand', 'nasa_physical_demand', 'nasa_temporal', 'nasa_performance',
                    'nasa_effort', 'nasa_frustration']


class UserSurveyAdmin(admin.ModelAdmin):
    list_display = ['user']


class TaskQuestionSurveyAdmin(admin.ModelAdmin):
    # fields = ['user','task_id','topic_num']
    list_display = ['user', 'task_id', 'topic_num']


class TopicAdsAdmin(admin.ModelAdmin):
    # fields = ['user','task_id','topic_num']
    ist_display = ('topic_num', 'title')


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(TaskDescription, TaskDescriptionAdmin)
admin.site.register(DocumentsExamined)
admin.site.register(TopicAds, TopicAdsAdmin)


