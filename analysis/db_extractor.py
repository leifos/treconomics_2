import os
import sys
from utils import setup_django_env

# Run me in the treconomics directory, with the database set to the one you wish to parse.

def get_include_ids(include_ids_path):
    """
    Returns a list of strings, each string representing the ID of a AMT worker to include.
    """
    ret_list = []
    f = open(include_ids_path, 'r')
    
    for line in f:
        if line.startswith('#'):
            continue
        
        line = line.strip()
        ret_list.append(line)
    
    f.close()
    return ret_list


def get_user_accounts(users_to_include):
    from django.contrib.auth.models import User
    from treconomics.models import UserProfile

    accounts = []

    count = 0
    users = User.objects.all()
    print("number of users", len(users))
    for user in users:
        try:
            treconomics_user = UserProfile.objects.get(user=user)
            if treconomics_user.steps_completed > 0 and treconomics_user.user.username in users_to_include:
                count = count + 1
                accounts.append({'userid': treconomics_user.user.id,
                     'username': treconomics_user.user.username,
                     'condition': treconomics_user.condition,
                     'rotation': treconomics_user.rotation})
        except:
            pass
    
    print("number of users with step:", count)
    return accounts

def get_user_key():
    return 'userid,username,condition,rotation'

def get_user_details(treconomics_user):
    keys = get_user_key().split(',')
    return_str = ""

    for key in keys:
        return_str = '{0}{1},'.format(return_str, treconomics_user[key])

    return return_str[:-1]

def get_key(model, exclude_fields):
    return_str = ''
    fields = model._meta.get_fields()
    field_names = []

    for field in fields:
        field_names.append(field.name)

    for field in field_names:
        if field not in exclude_fields:
            return_str = '{0}{1},'.format(return_str, field)

    return return_str[:-1]






def get_demographics(users):
    from survey.models import DemographicsSurvey
    exclude = ['id', 'user']  # Exclude the following fields from output
    fields = get_key(DemographicsSurvey, exclude)
    output = '{0},{1}{2}'.format(get_user_key(), fields, os.linesep)

    fields = fields.split(',')

    for treconomics_user in users:
        try:
            survey = DemographicsSurvey.objects.get(user=treconomics_user['userid'])

            output_line = get_user_details(treconomics_user) + ','

            for field in fields:
                output_line = '{0}{1},'.format(output_line, survey.__dict__[field])

            output = output + output_line[:-1]
            output = output + os.linesep
        except:
            # user does not have a record
            print("user didnt complete demographics", treconomics_user)
            pass

    output = output[:-1]
    return output


def get_task_survey(users, model, exclude=['id', 'user', 'user_id']):
    fields = get_key(model, exclude)
    output = '{0},{1}{2}'.format(get_user_key(), fields, os.linesep)

    fields = fields.split(',')

    for treconomics_user in users:
        surveys = model.objects.filter(user=treconomics_user['userid'])

        for survey in surveys:
            output_line = get_user_details(treconomics_user) + ','

            for field in fields:
                val = survey.__dict__[field]
                
                if type(val) == unicode:
                    val = val.replace(',', '')
                    val = val.replace('\r\n', ' ')
                
                output_line = '{0}{1},'.format(output_line, val)

            output = output + output_line[:-1]
            output = output + os.linesep

    output = output[:-1]
    return output

def write(filename, contents):
    f = open(filename, 'w')
    f.write(contents)
    f.close()

if __name__ == '__main__':
    if len(sys.argv) < 3 or len(sys.argv) > 3:
        print("Place the database you wish to parse in the treconomics_project directory.")
        print('Usage: {0} <user_list> <path_to_treconomics_project>'.format(sys.argv[0]))
        exit(2)
    
    setup_django_env(sys.argv[2])

    users_to_include = get_include_ids(sys.argv[1])
    users = get_user_accounts(users_to_include)
    demographics = get_demographics(users)
    
    # from snippets.models import BehaveDiversityPostTaskSurvey
    # from snippets.models import SystemDiversityPostTaskSurvey
    # from snippets.models import DiversityExitSurvey
    # from snippets.models import SnippetPreTaskTopicKnowledgeSurvey
    
    # pre_task_knowledge = get_task_survey(users, SnippetPreTaskTopicKnowledgeSurvey)
    # post_task_behavioural = get_task_survey(users, BehaveDiversityPostTaskSurvey)
    # post_task_system = get_task_survey(users, SystemDiversityPostTaskSurvey)
    # exit_survey = get_task_survey(users, DiversityExitSurvey)
    
    write('demographics.csv', demographics)
    # write('pre_task_knowledge.csv', pre_task_knowledge)
    # write('post_task_behavioural.csv', post_task_behavioural)
    # write('post_task_system.csv', post_task_system)
    # write('exit_survey.csv', exit_survey)