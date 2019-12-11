from django.urls import path
from survey import views

app_name = 'survey'

urlpatterns = [
    path('demographicssurvey/', views.view_demographics_survey),
    path('pst-findas/', views.view_pst_findas, name='pst-findas'),
    path('pst-numbers/', views.view_pst_numbers, name='pst-numbers'),
    path('perceptionsurvey/<taskid>/', views.view_post_perception_survey),
    path('systemsurvey/<taskid>/', views.view_post_system_survey),
    path('conceptlistingsurvey/<taskid>/<when>/', views.view_concept_listing_survey),
    path('personalitysurvey/', views.view_final_personality_survey),
    path('nasasurvey/', views.view_nasa_survey),

]
