from django.contrib import admin

# Register your models here.
from survey.models import PSTCharSearch, PersonalitySurvey, SystemSurvey, PostPerceptionSurvey, DemographicsSurvey, ConceptListingSurvey

admin.site.register(PSTCharSearch)
admin.site.register(PersonalitySurvey)
admin.site.register(SystemSurvey)
admin.site.register(PostPerceptionSurvey)
admin.site.register(DemographicsSurvey)
admin.site.register(ConceptListingSurvey)
