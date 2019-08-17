from django.urls import path
from survey import views

app_name = 'survey'

urlpatterns = [
    path('demographicssurvey/', views.view_demographics_survey),
    path('searchefficacysurvey/', views.view_search_efficacy_survey),
    path('nasaloadsurvey/', views.view_nasa_load_survey),
    path('conceptlistingsurvey/<taskid>/<when>/', views.view_concept_listing_survey),
    path('shortstresssurvey/', views.view_short_stress_survey),
    path('modifiedstresssurvey/', views.view_modified_stress_survey),
    path('pst-findas/', views.view_pst_findas, name='pst-findas'),
    path('pst-numbers/', views.view_pst_numbers, name='pst-numbers'),
]
