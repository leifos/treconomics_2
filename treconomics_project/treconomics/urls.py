from django.urls import path
from treconomics import views

app_name = 'treconomics'

urlpatterns = [
             path('', views.view_amt_login, name='home'),
             path('login/', views.view_amt_login, name='login'),
             path('register/', views.view_register_amt_user, name='register-amt-user'),
             path('logout/', views.view_logout, name='logout'),
             path('next/', views.view_next, name='next'),
             path('startexperiment/', views.start_amt_experiment, name='start-experiment'),
             path('preexperiment/<version>/', views.PreExperimentView.as_view(), name='pre-experiment'),
             path('pretask/<taskid>/', views.pre_task, name='pre-task'),
             path('prepracticetask/<taskid>/', views.pre_practice_task, name='pre-task-questions'),
             path('pretaskquestions/<taskid>/', views.pre_task_with_questions),
             path('postpracticetask/<taskid>/', views.post_practice_task),
             path('posttaskquestions/<taskid>/', views.post_task_with_questions),
             path('posttask/<taskid>/', views.post_task, name='post-task'),

             path('showtask/', views.show_task),
             path('sessioncommence/', views.commence_session),
             path('taskspacer/', views.TaskSpacerView.as_view()),
             path('taskspacerwithdetails/<taskid>/', views.task_spacer_with_details),
             path('taskspacer2/<msg_id>/', views.task_spacer_msg),

             path('sessioncompleted/', views.SessionCompletedView.as_view(), name='session-completed'),
             path('postexperiment/', views.PostExperimentView.as_view()),
             path('endexperiment/', views.EndExperimentView.as_view()),

#            path('(?P<whoosh_docid>\d+)/$', search_views.show_document),
#            path('saved/$', search_views.show_saved_documents, name='saved'),
#            path('search/$', search_views.search, name='search'),
#            path('search/(?P<taskid>\d+)/$', search_views.search, name='search-task'),


]
