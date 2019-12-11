import os
import django

def populate():
    print('Adding PST Users')
    for i in range(0,12):
        uname = 'pst'+str(i)
        add_user(uname,uname,0,2,i)


    print('Adding AD Users')

    for i in range(0,12):
        uname = 'ad'+str(i)+'a'
        add_user(uname,uname,1,1,i)

    for i in range(0,12):
        uname = 'ad'+str(i)+'b'
        add_user(uname,uname,1,2,i)

    for i in range(0,12):
        uname = 'ad'+str(i)+'c'
        add_user(uname,uname,1,3,i)

    for i in range(0,12):
        uname = 'ad'+str(i)+'d'
        add_user(uname,uname,1,4,i)


    for i in range(0,12):
        uname = 'test'+str(i)
        add_user(uname,uname,2,5,i)



def add_user(username, password, experiment, condition, rotation, data=None):
    u = User.objects.get_or_create(username=username)[0]
    u.set_password(password)
    u.save()
    up = \
        UserProfile.objects.get_or_create(user=u,
                                          condition=condition,
                                          experiment=experiment,
                                          rotation=rotation,
                                          data=data)[0]
    print('%s, %s, %d, %d  ' % (username, password, experiment, rotation))


def add_task(topic_num, title, description):
    t = TaskDescription.objects.get_or_create(topic_num=topic_num,
                                              title=title,
                                              description=description)[0]
    print("\t %s" % t)
    return t


if __name__ == '__main__':

    print("Starting Treconomics population script...")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'treconomics_project.settings')

    django.setup()
    from treconomics.models import TaskDescription
    from treconomics.models import UserProfile
    from django.contrib.auth.models import User
    populate()
