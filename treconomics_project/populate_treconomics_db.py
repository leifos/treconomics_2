import os
import django

#Testing out new instructions

def populate():
    print('Adding Task Descriptions')
    add_task(topic_num='341',
             title='Airport Security',
             description='<p>Find and bookmark articles '
                         'that discuss how DIFFERENT AIRPORTS '
                         'use SECURITY MEASURES to better screen passengers '
                         'and their carry-on luggage.</p>',
             remember = '<p> Afterwards, you will be asked to recall these '
                        'DIFFERENT AIRPORTS and their SECURITY MEASURES </p>',
             concepts ='<p> Recall as many AIRPORTS and SECURITY MEASURES that were taking additional security measures, '
                       'that you  found.</p>'
             )
    #airport and measures to improve security
    add_task(topic_num='347',
             title='Wildlife Extinction',
             description='<p>Find and bookmark articles '
                         'that discuss EXTINCTION PREVENTION MEASURES made by countries '
                         'to protect DIFFERENT WILDLIFE SPECIES </p>',
             remember = '<p> Afterwards, you will be asked to recall these '
                        'DIFFERENT WILDLIFE SPECIES and their EXTINCTION PREVENTION MEASURES.</p>', #or countries
             concepts ='<p> Recall as many WILDLIFE SPECIES and their EXTINCTION PREVENTION MEASURES, '
                       'that you found.</p>'
             )

    add_task(topic_num='435',
             title='Curbing Population Growth',
             description='<p>Find and bookmark articles that discuss '
                         'DIFFERENT COUNTRIES that have been successful in '
                         'CURBING POPULATION GROWTH MEASURES. '
                         'growth and the measures they have taken to do so.</p>',
             remember='<p> Afterwards, you will be asked to recall these '
                      'DIFFERENT COUNTRIES and their MEASURES to reduce population growth.</p>',
             concepts ='<p> Recall as many COUNTRIES and the MEASURES they use to control population growth, '
                       'that you found.</p>'
             )
    #country and measure
        #Q) so am i right in thinking if i list 3 different ways of curbing population growth but
        # they're all in vietnam, then i would only get a score of '1'?

    add_task(topic_num='367',
             title='Piracy',
             description='<p>Find and bookmark articles that discuss instances of piracy, '
                         'where DIFFERENT BOATS/SHIPS have been illegally taken control of or boarded '
                         'and in what SEA/OCEAN the piracy took place.',
             remember = '<p>Afterwards, you will be asked to recall these BOATS/SHIPS.</p>',
             concepts ='<p> Recall as many BOATS/SHIPS involved in piracy and the SEA/OCEAN that it occurred, '
                       'that you found.</p>')

    add_task(topic_num='408',
             title='Tropical Storms',
             description='<p>Find and bookmark articles that discuss  '
                         'COUNTRIES that have had DIFFERENT TROPICAL STORMS (hurricanes and typhoons) '
                         'which caused significant property damage and loss of life.</p> ',
             remember='<p>Afterwards, you will be asked to recall these '
                      'COUNTRIES and the different names of their TROPICAL STORMS that caused fatal damage</p> ',
             concepts ='<p> Recall as many TROPICAL STORMS which caused fatal damage and their COUNTRY LOCATION, '
                       'that you found.</p>'
             )

#storm and location
#Q) Does it count as relevant if someone lists a storm that caused property damage but not FATALITIES?


def add_user(username, password, condition, experiment, rotation, data=None):
    u = User.objects.get_or_create(username=username)[0]
    u.set_password(password)
    u.save()
    up = \
        UserProfile.objects.get_or_create(user=u,
                                          condition=condition,
                                          experiment=experiment,
                                          rotation=rotation,
                                          data=data)[0]
    print('%s, %s, %d, %d  ' % (username, password, condition, rotation))


def add_task(topic_num, title, description, remember, concepts):
    t = TaskDescription.objects.get_or_create(topic_num=topic_num)[0]
    t.title = title
    t.description = description
    t.diversify = ''
    t.concepts = concepts
    t.remember = remember
    t.save()
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
