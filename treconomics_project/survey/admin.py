from django.contrib import admin

# Register your models here.
from survey.models import PSTCharSearch, PSTNumberSearch, PersonalitySurvey, SystemSurvey
from survey.models import PostPerceptionSurvey, DemographicsSurvey, ConceptListingSurvey
from survey.models import PreTaskTopicKnowledgeSurvey, PostTaskTopicRatingSurvey

admin.site.register(PSTCharSearch)
admin.site.register(PSTNumberSearch)
admin.site.register(PersonalitySurvey)
admin.site.register(SystemSurvey)
admin.site.register(PostPerceptionSurvey)
admin.site.register(DemographicsSurvey)
admin.site.register(ConceptListingSurvey)
admin.site.register(PreTaskTopicKnowledgeSurvey)
admin.site.register(PostTaskTopicRatingSurvey)
