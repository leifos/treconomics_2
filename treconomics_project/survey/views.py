from django.template.context import RequestContext
from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from treconomics.experiment_functions import get_experiment_context
from treconomics.experiment_functions import log_event
from .forms import *
from treconomics.models import TaskDescription
from survey.models import PSTCharSearch


APP_NAME = '/treconomics/'

def handle_survey(request, SurveyForm, survey_name, action, template):
    context = RequestContext(request)
    ec = get_experiment_context(request)
    uname = ec["username"]
    condition = ec["condition"]
    u = User.objects.get(username=uname)
    # handle post within this element. save data to survey table,
    if request.method == 'POST':
        form = SurveyForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = u
            obj.save()
            log_event(event=survey_name.upper() + "_SURVEY_COMPLETED", request=request)
            return HttpResponseRedirect('/treconomics/next/')
        else:
            print(form.errors)
            survey = SurveyForm(request.POST)
    else:
        log_event(event=survey_name.upper() + "_SURVEY_STARTED", request=request)
        survey = SurveyForm()

    context_dict = {'participant': uname, 'condition': condition, 'formset': survey, 'action': action}
    return render(request, template, context_dict)

@login_required
def view_demographics_survey(request):
    return handle_survey(request, DemographicsSurveyForm, 'DEMOGRAPHICS', '/treconomics/demographicssurvey/',
                         'survey/demographics_survey.html')


@login_required
def view_final_personality_survey(request):
    return handle_survey(request, FinalPersonalitySurveyForm, 'PERSONALITY', '/treconomics/personalitysurvey/',
                         'survey/final_personality_survey.html')


@login_required
def view_concept_listing_survey(request, taskid, when):
     context = RequestContext(request)
     # Set the tasks id manually from request
     request.session['taskid'] = taskid
     ec = get_experiment_context(request)
     uname = ec["username"]
     condition = ec["condition"]
     topicnum = ec["topicnum"]
     t = TaskDescription.objects.get(topic_num=topicnum)
     errors = ""

     uname = request.user.username
     u = User.objects.get(username=uname)

     # handle post within this element. save data to survey table,
     if request.method == 'POST':
         form = ConceptListingSurveyForm(request.POST)
         if form.is_valid():
             obj = form.save(commit=False)
             obj.user = u
             obj.task_id = ec["taskid"]
             obj.topic_num = ec["topicnum"]
             obj.when = when
             obj.save()
             log_event(event="CONCEPT_LISTING_COMPLETED", request=request)
             return HttpResponseRedirect('/treconomics/next/')
         else:
             print(form.errors)
             errors = form.errors
             survey = ConceptListingSurveyForm(request.POST)
     else:
         survey = ConceptListingSurveyForm()

     action = '/treconomics/conceptlistingsurvey/' + taskid + '/' + when + '/'

    # provide link to search interface / next system
     context_dict = {'participant': uname,
                     'condition': condition,
                     'task': taskid,
                     'topic': t.topic_num,
                     'tasktitle': t.title,
                     'taskdescription': t.description,
                     'concepts' :t.concepts,
                     'formset': survey,
                     'action': action,
                     'errors': errors}

     return render(request, 'survey/concept_listing_survey.html', context_dict)



@login_required
def view_pst_findas(request):

    action = '/treconomics/pst-findas/'

    context = RequestContext(request)
    ec = get_experiment_context(request)
    uname = ec["username"]
    condition = ec["condition"]

    u = User.objects.get(username=uname)
    # handle post within this element. save data to survey table,
    if request.method == 'POST':
            correct = request.POST.get('correct')
            incorrect = request.POST.get('incorrect')
            psta = PSTCharSearch.objects.get_or_create(user=u, correct=correct, incorrect=incorrect)[0]
            log_event(event="PST_A_COMPLETED {} {}".format(correct, incorrect), request=request)
            return HttpResponseRedirect('/treconomics/next/')

    else:
        log_event(event="PST_A_STARTED", request=request)

    context_dict = {'participant':uname, 'condition':condition, 'action':action}
    return render(request, 'survey/perceptual_speed_test_findas.html', context_dict)


@login_required
def view_pst_numbers(request):
    context = RequestContext(request)
    ec = get_experiment_context(request)
    uname = ec["username"]
    condition = ec["condition"]
    #u = User.objects.get(username=uname)

    # provide link to search interface / next system
    context_dict = {'participant': uname,
                    'condition': condition }

    return render(request, 'survey/perceptual_speed_test_number_compare.html', context_dict)




@login_required
def view_nasa_survey(request):
    return handle_survey(request, NasaSurveyForm, 'NASA_LOAD', '/treconomics/nasasurvey/',
                         'survey/nasa_survey.html')

@login_required
def view_post_perception_survey(request, taskid):
    return handle_post_task_survey(request, taskid, PostPerceptionSurveyForm, 'PERCEPTION', '/treconomics/perceptionsurvey/',
                         'survey/post_perception_survey.html')

@login_required
def view_post_system_survey(request, taskid):
    return handle_post_task_survey(request, taskid, PostSystemSurveyForm, 'SYSTEM', '/treconomics/systemsurvey/',
                         'survey/post_system_survey.html')

def handle_post_task_survey(request, taskid, survey_form, survey_name, survey_link, survey_template):

    #survey_form = PostPerceptionSurveyForm
    #survey_name = "POST_PERCEPTION"
    #survey_link = '/treconomics/perceptionsurvey/'
    #survey_template = 'survey/post_perception_survey.html'

    # Set the tasks id manually from request
    request.session['taskid'] = taskid
    ec = get_experiment_context(request)
    condition = ec["condition"]
    topicnum = ec["topicnum"]
    t = TaskDescription.objects.get(topic_num=topicnum)
    errors = ""
    uname = request.user.username
    u = User.objects.get(username=uname)

    # handle post within this element. save data to survey table,
    if request.method == 'POST':
        form = survey_form(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = u
            obj.task_id = ec["taskid"]
            obj.topic_num = ec["topicnum"]
            obj.save()
            log_event(event="{}_SURVEY_COMPLETED".format(survey_name), request=request)
            return redirect('treconomics:next')
        else:
            print(form.errors)
            errors = form.errors
            survey = survey_form(request.POST)

    else:
        log_event(event="{}_SURVEY_STARTED".format(survey_name), request=request)
        survey = survey_form()

    # if we had a survey questions we could ask them here
    # else we can provide a link to a hosted questionnaire

    action =  survey_link + taskid + '/'
    print(action)

    # provide link to search interface / next system

    context_dict = {'participant': uname,
                    'condition': condition,
                    'task': taskid,
                    'topic': t.topic_num,
                    'tasktitle': t.title,
                    'taskdescription': t.description,
                    'formset': survey,
                    'action': action, 'errors': errors}

    return render(request, survey_template, context_dict)
