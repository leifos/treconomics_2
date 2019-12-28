from django.contrib import admin

# Register your models here.
from survey.models import PSTCharSearch, PSTNumberSearch, PersonalitySurvey, SystemSurvey, OverallInterview
from survey.models import PostPerceptionSurvey, DemographicsSurvey, ConceptListingSurvey
from survey.models import PreTaskTopicKnowledgeSurvey, PostTaskTopicRatingSurvey

class PSTAdmin(admin.ModelAdmin):
    fields = ['user', 'correct', 'incorrect']
    list_display = ('user', 'correct', 'incorrect')


class GenericUserAdmin(admin.ModelAdmin):
    list_display = ['user']

class GenericUserTopicAdmin(admin.ModelAdmin):
    list_display = ['user', 'task_id', 'topic_num']


admin.site.register(PSTCharSearch, PSTAdmin)
admin.site.register(PSTNumberSearch, PSTAdmin)
admin.site.register(PersonalitySurvey,GenericUserAdmin)
admin.site.register(SystemSurvey, GenericUserTopicAdmin)
admin.site.register(PostPerceptionSurvey, GenericUserTopicAdmin)
admin.site.register(DemographicsSurvey, GenericUserAdmin)
admin.site.register(OverallInterview, GenericUserAdmin)
admin.site.register(ConceptListingSurvey, GenericUserTopicAdmin)
admin.site.register(PreTaskTopicKnowledgeSurvey, GenericUserTopicAdmin)
admin.site.register(PostTaskTopicRatingSurvey, GenericUserTopicAdmin)
