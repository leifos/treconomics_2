from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.views.generic.base import ContextMixin

from treconomics.models import DocumentsExamined
from treconomics.models import TaskDescription
from treconomics.models import UserProfile
from treconomics.experiment_functions import get_experiment_context, print_experiment_context
from treconomics.experiment_functions import log_event, populate_context_dict, get_performance
from treconomics.experiment_functions import log_performance
from treconomics.experiment_configuration import experiment_setups, user_conditions


from survey.models import DemographicsSurvey
from survey.models import PreTaskTopicKnowledgeSurvey
from survey.models import PostTaskTopicRatingSurvey

from survey.forms import PreTaskTopicKnowledgeSurveyForm
from survey.forms import PostTaskTopicRatingSurveyForm

"""
from search.views import set_descriptions
from search.views import set_status
"""
import logging


logging.basicConfig(level=logging.WARNING)

APP_NAME = '/treconomics/'

def reset_test_users(request):
    usernames = ['t1', 't2', 't3', 't4', 'a1', 'a2', 'a3', 'a4', 'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8']

    for un in usernames:
        print(un)
        temp_user = User.objects.get(username=un)
        profile = temp_user.profile
        profile.steps_completed = 0
        profile.tasks_completed = 0
        profile.save()
        DocumentsExamined.objects.filter(user=temp_user).delete()
        """
        PreTaskTopicKnowledgeSurvey.objects.filter(user=temp_user).delete()
        PostTaskTopicRatingSurvey.objects.filter(user=temp_user).delete()
        DemographicsSurvey.objects.filter(user=temp_user).delete()
        NasaSystemLoad.objects.filter(user=temp_user).delete()
        NasaQueryLoad.objects.filter(user=temp_user).delete()
        NasaNavigationLoad.objects.filter(user=temp_user).delete()
        NasaAssessmentLoad.objects.filter(user=temp_user).delete()
        SearchEfficacy.objects.filter(user=temp_user).delete()
        ShortStressSurvey.objects.filter(user=temp_user).delete()
        ConceptListingSurvey.objects.filter(user=temp_user).delete()
        """
        request.session['current_step'] = '0'
    return HttpResponse(
        "<script type='text/javascript'>"
        "setTimeout(function(){window.location='/treconomics/'}, 1500);"
        "</script>"
        "Test users reset, redirecting to login...")


def view_login(request):
    return render(request, 'base/login.html')

def view_amt_login(request):
    return render(request, 'base/amt_login.html')


def do_login(request,user):
    if user.is_active:
        login(request, user)
        # Redirect to a success page.
        # set cookies for experiment
        ec = get_experiment_context(request)
        print_experiment_context(ec)
        log_event(event='EXPERIMENT_LOGIN', request=request)

        context_dict = {
            'popup_width': 1024,
            'popup_height': 1024,
            'test': 1022,
            }

        # Instead of redirecting to next/, give back a popup launching script instead!
        return render(request=request,  template_name='base/popup_launcher.html', context=context_dict)
    else:
        # Return a 'disabled account' error message
        return HttpResponse("Your account is disabled.")





def view_register_amt_user(request):
    if request.method == 'POST':
        username = request.POST['username'].strip()
        password = request.POST['username'].strip()

        up = UserProfile.objects.filter(experiment=9)
        lup = len(up)

        user_list = User.objects.filter(username=username)
        if len(user_list) == 0:
            user = User.objects.get_or_create(username=username)[0]
            user.set_password(password)
            user.save()
            print(user)

            (a,b) = divmod(lup, len(user_conditions))
            t_rotation = user_conditions[b][0]
            i_rotation = user_conditions[b][1]

            up = UserProfile.objects.get_or_create(user=user, condition=t_rotation,experiment=9,rotation=i_rotation, data='')[0]
            print("UserProfile: {} {} {} {}".format(lup, user.id, t_rotation, i_rotation))

            up.save()
            print(up)
            #log_event(event="USER_CREATED {} {}".format(t_rotation, i_rotation), request=request)
            return render(request, 'base/amt_login.html', {'registered': True})
        else:
            return render(request, 'base/amt_login.html', {'already': True})
    else:
        return render(request, 'base/register.html')


def start_amt_experiment(request):

    if request.method == 'POST':
        username = request.POST['username'].strip()
        password = request.POST['username'].strip()
        print(username)
        try:
            user = authenticate(username=username, password=password)

        except:
            user = None

        if user is not None:
            return do_login(request,user)
        else:
            return render(request, 'base/amt_login.html', {'invalid': True})
    else:
        return render(request, 'base/amt_login.html')


def start_experiment(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            return do_login(request,user)
        else:
            # Return an 'invalid login' error message.
            print("invalid login details " + username + " " + password)
            return render(request, 'base/login.html', {'invalid': True})
    else:
        return render(request, 'base/login.html')


@login_required
def view_logout(request):
    log_event(event='EXPERIMENT_COMPLETED', request=request)
    # pid = request.user.username
    logout(request)
    # Redirect to a success page.
    return render(request, 'base/logout.html')


@login_required
def view_next(request):
    # define experiment flow here
    ec = get_experiment_context(request)
    print_experiment_context(ec)
    step = int(ec["current_step"])

    # Record the completed step
    uname = request.user.username
    u = User.objects.get(username=uname)
    profile = u.profile
    profile.steps_completed = step
    profile.save()

    # TODO KNOWN ISSUE HERE - Clicking the back button will mean this can get out of sync.
    workflow = ec["workflow"]
    num_of_steps = len(workflow)

    # current_url = ec["current_url"]
    # find the position of the current_url in the workflow,
    # increment that position and move subject to the next step...
    # this does not solve the back button issue entirely

    if step < num_of_steps:
        next_step = step + 1
        request.session['current_step'] = str(next_step)
    else:
        next_step = step

    # Does this work correctly?
    try:
        url_to_visit_next = APP_NAME + workflow[next_step]
    except IndexError:
        url_to_visit_next = APP_NAME + workflow[next_step-1]

    print("WORKFLOW is {}".format(workflow[next_step]))
    print('view_next - step : ' + str(next_step))
    print('url to visit next: ' + str(url_to_visit_next))
    return HttpResponseRedirect(url_to_visit_next)


@login_required
def show_task(request):
    ec = get_experiment_context(request)
    uname = ec["username"]
    condition = ec["condition"]
    topicnum = ec["topicnum"]
    taskid = ec["taskid"]
    t = TaskDescription.objects.get(topic_num=topicnum)

    log_event(event="VIEW_TASK", request=request)

    context_dict = {'participant': uname,
                    'condition': condition,
                    'task': taskid,
                    'topic': t.topic_num,
                    'tasktitle': t.title,
                    'taskdescription': t.description,
                    'remember': t.remember}
    populate_context_dict(ec, context_dict)


    return render(request, 'base/show_task.html', context_dict)


@login_required
def pre_task(request, taskid):
    # TODO Could benefit from a generic view
    # Set the tasks id
    request.session['taskid'] = taskid

    ec = get_experiment_context(request)
    uname = ec["username"]
    condition = ec["condition"]

    topicnum = ec["topicnum"]
    t = TaskDescription.objects.get(topic_num=topicnum)
    # if we had a survey questions we could ask them here
    # else we can provide a link to a hosted questionnaire
    # provide link to search interface / next system

    context_dict = {'participant': uname,
                    'condition': condition,
                    'task': taskid,
                    'topic': t.topic_num,
                    'tasktitle': t.title,
                    'taskdescription': t.description,
                    'remember': t.remember}

    populate_context_dict(ec, context_dict)

    return render(request, 'base/pre_task.html', context_dict)


@login_required
def pre_practice_task(request, taskid):
    # Set the tasks id
    request.session['taskid'] = taskid

    ec = get_experiment_context(request)
    #uname = ec["username"]
    #condition = ec["condition"]

    topicnum = ec["topicnum"]
    t = TaskDescription.objects.get(topic_num=topicnum)

    # provide link to search interface / next system
    context_dict = {'topic': t.topic_num,
                    'tasktitle': t.title,
                    'taskdescription': t.description,
                    'remember': t.remember}

    populate_context_dict(ec, context_dict)
    print(context_dict)

    return render(request, 'base/pre_practice_task.html', context_dict)


@login_required
def post_practice_task(request, taskid):
    ec = get_experiment_context(request)
    uname = ec["username"]
    condition = ec["condition"]

    topicnum = ec["topicnum"]

    # Save out to profile what task has just been completed
    # This is probably not necessary ---- as the step  and taskid coming defines this.
    u = User.objects.get(username=uname)
    profile = u.profile
    profile.tasks_completed = int(taskid)
    profile.save()

    # if participant has completed all the tasks, go to the post experiment view
    # else direct the participant to the pre task view

    perf = get_performance(uname, topicnum)

    denom = perf["rels"]+perf["nons"]
    if denom != 0:
        perf["estimated_rels"] = (perf["rels"]/denom) * perf["total_marked"]
    else:
        perf["estimated_rels"] = 0.0

    perf["estimated_acc"] = 0.0
    if (perf["total_marked"]>0):
        perf["estimated_acc"] = perf["estimated_rels"] / perf["total_marked"] if perf["total_marked"] != 0 else 0.0

    if perf["estimated_acc"] > 0.5:
        perf["status_message"] = "Passed"
    else:
        perf["status_message"] = "Failed"


    context_dict = {'participant': uname, 'condition': condition, 'performance': perf}

    populate_context_dict(ec, context_dict)
    #print(context_dict)
    log_performance(request, perf)


    return render(request, 'base/post_practice_task.html', context_dict)


@login_required
def pre_task_with_questions(request, taskid):
    # Set the tasks id manually from request
    request.session['taskid'] = taskid
    ec = get_experiment_context(request)
    # uname = ec["username"]
    condition = ec["condition"]
    topicnum = ec["topicnum"]
    t = TaskDescription.objects.get(topic_num=topicnum)
    errors = ""

    uname = request.user.username
    u = User.objects.get(username=uname)

    # handle post within this element. save data to survey table,
    if request.method == 'POST':
        form = PreTaskTopicKnowledgeSurveyForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = u
            obj.task_id = ec["taskid"]
            obj.topic_num = ec["topicnum"]
            obj.save()
            log_event(event="PRE_TASK_SURVEY_COMPLETED", request=request)
            return redirect('treconomics:next')
        else:
            print(form.errors)
            errors = form.errors
            survey = PreTaskTopicKnowledgeSurveyForm(request.POST)

    else:
        log_event(event="PRE_TASK_SURVEY_STARTED", request=request)
        survey = PreTaskTopicKnowledgeSurveyForm()

    # if we had a survey questions we could ask them here
    # else we can provide a link to a hosted questionnaire

    action = APP_NAME + 'pretaskquestions/' + taskid + '/'
    print(action)

    # provide link to search interface / next system

    context_dict = {'participant': uname,
                    'condition': condition,
                    'task': taskid,
                    'topic': t.topic_num,
                    'tasktitle': t.title,
                    'taskdescription': t.description,
                    'remember': t.remember,
                    'formset': survey,
                    'action': action, 'errors': errors}

    return render(request, 'base/pre_task_with_questions.html', context_dict)



@login_required
def post_task(request, taskid):
    ec = get_experiment_context(request)
    uname = ec["username"]
    condition = ec["condition"]

    # Save out to profile what task has just been completed
    # This is probably not necessary ---- as the step  and taskid coming defines this.
    u = User.objects.get(username=uname)
    profile = u.profile
    profile.tasks_completed = int(taskid)
    profile.save()

    # write_to_log
    print ("SEARCH TASK COMPLETED")
    log_event(event="SEARCH_TASK_COMPLETED", request=request)
    # if we had post task survey we could ask them here
    # else we can provide a link to a hosted questionnaire

    # if participant has completed all the tasks, go to the post experiment view
    # else direct the participant to the pre task view

    context_dict = {'participant': uname, 'condition': condition, 'task': taskid}

    return render(request, 'base/post_task.html', context_dict)


@login_required
def post_task_with_questions(request, taskid):
    ec = get_experiment_context(request)
    uname = ec["username"]
    condition = ec["condition"]
    # Save out to profile what task has just been completed
    # This is probably not necessary ---- as the step  and taskid coming defines this.
    u = User.objects.get(username=uname)
    profile = u.profile
    errors = ""

    # #################
    # handle post within this element. save data to survey table,
    if request.method == 'POST':
        form = PostTaskTopicRatingSurveyForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = u
            obj.task_id = ec["taskid"]
            obj.topic_num = ec["topicnum"]
            obj.save()
            log_event(event="POST_TASK_SURVEY_COMPLETED", request=request)
            return redirect('treconomics:next')
        else:
            print (form.errors)
            errors = form.errors
            survey = PostTaskTopicRatingSurveyForm(request.POST)
    else:
        survey = PostTaskTopicRatingSurveyForm()
        profile.tasks_completed = int(taskid)
        profile.save()
        log_event(event="POST_TASK_SURVEY_STARTED", request=request)

    # if we had a survey questions we could ask them here
    # else we can provide a link to a hosted questionnaire

    action = APP_NAME + 'posttaskquestions/' + taskid + '/'

    # if participant has completed all the tasks, go to the post experiment view
    # else direct the participant to the pre task view

    context_dict = {'participant': uname,
                    'condition': condition,
                    'task': taskid,
                    'formset': survey,
                    'action': action,
                    'errors': errors}

    return render(request, 'base/post_task_with_questions.html', context_dict)


@login_required
def commence_session(request):
    ec = get_experiment_context(request)
    uname = ec["username"]
    condition = ec["condition"]
    logging.debug('SESSION COMMENCED')
    log_event(event="SESSION_COMMENCED", request=request)

    context_dict = {'participant': uname, 'condition': condition}
    return render(request, 'base/session_commenced.html', context_dict)


@login_required
def show_timeout_message(request):
    """
    Used to display a simple page indicating the user to the fact that their time for a task has expired.
    After a 5 second delay, the page automatically redirects to /treconomics/next/.
    """
    log_event(event="SESSION_COMPLETED", request=request)
    log_event(event="EXPERIMENT_TIMEOUT", request=request)

    return render(request, 'base/timeout.html')


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class ExperimentContextMixin(LoginRequiredMixin, ContextMixin):
    """
    ExperiemntContextMixin requires LoginRequiredMixin conceptually:
    You have to be logged in for get_experiment_context to be defined!
    """
    def get_context_data(self, **kwargs):
        context = super(ExperimentContextMixin, self).get_context_data(**kwargs)

        # I'd just do this and change the templates:
        # context['experiment'] = get_experiment_context(self.request)

        # But you seem to currently want:
        ec = get_experiment_context(self.request)
        context['participant'] = ec['username']
        context['condition'] = ec['condition']
        context['target'] = ec['target']

        return context


class PreExperimentView(ExperimentContextMixin, TemplateView):
    template_name = 'base/pre_experiment.html'


class PostExperimentView(ExperimentContextMixin, TemplateView):
    template_name = 'base/post_experiment.html'


class TaskSpacerView(ExperimentContextMixin, TemplateView):
    template_name = 'base/task_spacer.html'


@login_required
def task_spacer_with_details(request, taskid):
    request.session['taskid'] = taskid
    ec = get_experiment_context(request)

    topicnum = ec["topicnum"]
    t = TaskDescription.objects.get(topic_num=topicnum)

    log_event(event="VIEW_TASK_SPACER_DETAILS", request=request)

    context_dict = {'topic': t.topic_num,
                    'tasktitle': t.title,
                    'taskdescription': t.description,
                    'remember': t.remember,
                    'task': taskid}

    populate_context_dict(ec, context_dict)

    return render(request, 'base/task_spacer_with_details.html', context_dict)


@login_required
def task_spacer_msg(request, msg_id):
    ec = get_experiment_context(request)


    head_msg = {'0': 'Practice Task Completed',
                '1': 'Task 1 of 4 Completed',
                '2': 'Task 2 of 4 Completed',
                '3': 'Task 3 of 4 Completed',
                '4': 'Task 4 of 4 Completed',
                'pst': 'Perceptual Speed Test Completed',
                }


    body_msg = {'0': 'Before undertaking the four search tasks, we would like you to first complete a perceptual speed test.',
                '1': '',
                '2': '',
                '3': '',
                '4': 'You have now completed all tasks. In the last few remaining screens, we would like'
                     'you to complete another perceptual speed test, and then answer a few more questions.',
                'pst':'Now you have completed the perceptual speed test, we would like you to undertake the search tasks.'
    }

    if msg_id in head_msg:
        heading = head_msg[msg_id]
    else:
        heading = 'No msg found'

    if msg_id in body_msg:
        body = body_msg[msg_id]
    else:
        body = ''



    context_dict = {'heading': heading, 'body':body}

    populate_context_dict(ec, context_dict)
    return render(request, 'base/task_spacer2.html', context_dict)





class EndExperimentView(ExperimentContextMixin, TemplateView):
    template_name = 'base/end_experiment.html'


class SessionCompletedView(ExperimentContextMixin, TemplateView):
    template_name = 'base/session_completed.html'
    # TODO print "SESSION COMPLETED"

    def dispatch(self, request, *args, **kwargs):
        log_event(event="SESSION_COMPLETED", request=self.request)
        pass


class TimeoutView(ExperimentContextMixin, TemplateView):
    """
    Used to display a simple page indicating the user to the fact that their time for a task has expired.
    After a 5 second delay, the page automatically redirects to /treconomics/next/.
    """
    template_name = 'base/timeout.html'

    def dispatch(self, request, *args, **kwargs):
        log_event(event="SESSION_COMPLETED", request=request)
        log_event(event="EXPERIMENT_TIMEOUT", request=request)


def show_users(request):
    users = User.objects.all()

    context_dict = {'users':users}
    return render(request, 'base/show_users.html', context_dict)

def show_user_performance(request, userid):

    u = User.objects.get(id=userid)
    up = UserProfile.objects.get(user=u)
    uname = u.username
    condition = up.condition
    rotation = up.rotation
    setup = experiment_setups[condition]
    target = setup.target

    performances = []

    for i in range(1, 5):
        topic_num = setup.get_rotation_topic(rotation, i)

        topic_desc = TaskDescription.objects.get(topic_num=topic_num).title

        perf = {}
        perf['num'] = topic_num
        perf['title'] = topic_desc

    context_dict = {'user':u,
                    'performances': performances,}
    return render(request, 'base/show_user_performance.html', context_dict)
