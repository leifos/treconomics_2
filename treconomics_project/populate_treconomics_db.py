import os
import django



def populate():
    print('Adding Task Descriptions')
    add_task(topic_num='341',
             title='Airport Security',
             description='<p>For this task, '
                         'your job is to find articles '
                         'that discuss procedures taken by international '
                         'airports, to better screen passengers '
                         'and their carry-on luggage.</p>'
                         '<p>A RELEVANT document would discuss how effective government orders to '
                         'better scrutinize passengers and luggage on international flights and to step '
                         'up screening of all carry-on baggage has been.</p> ',
             diversify='<p> A RELEVANT AND DIFFERENT document should mention NEW airports.</p>',
             concepts ='<p> Try to recall and list the airports that were taking measures that you found.</p>'
             )
    add_task(topic_num='347',
             title='Wildlife Extinction',
             description='<p>For this task, your job is '
                         'to find articles that discuss efforts '
                         'made by countries other than the United States '
                         'to prevent the extinction of wildlife species '
                         'native to their countries. </p>'
                         '<p>A RELEVANT document will specify the country, the involved species, and steps taken to save the species.</p>'
                         '<p>A document that discusses such efforts in the United States is NOT RELEVANT.</p>',
             diversify='<p> A RELEVANT AND DIFFERENT document should be RELEVANT and also mention NEW species.</p>',
             concepts ='<p> Try to recall and list the different species which were being protected that you found.</p>'
             )
    add_task(topic_num='354',
             title='Journalist Risks',
             description='<p>For this task, your job is to find '
                         'articles that discuss instances where journalists '
                         'have been put at risk '
                         '(e.g., killed, arrested or taken hostage) '
                         'in the performance of their work.</p>'
                         '<p>A RELEVANT document must identify an instance where a journalist or'
                         ' correspondent has been killed, arrested or taken hostage in the performance of their work.</p>',
             diversify='<p> A RELEVANT AND DIFFERENT document should be RELEVANT and also mention NEW journalists.</p>',
             concepts ='<p> Try to recall and list the journalists involved .</p>'
             )
    add_task(topic_num='435',
             title='Curbing Population Growth',
             description='<p>For this task, your job '
                         'is to find articles that discuss countries '
                         'that have been successful in curbing population '
                         'growth and the measures they have taken to do so.</p>'
                         '<p>A RELEVANT document must describe an actual case in which population measures have been taken and their results are known.</p> '
                         '<p>The reduction measures must have been actively pursued; '
                         'that is, passive events such as disease or famine involuntarily reducing the population are NOT RELEVANT.</p>',
             diversify='<p> A RELEVANT AND DIFFERENT document should be RELEVANT and also mention NEW countries.</p>',
             concepts ='<p> Try to recall and list the different countries try to control population growth that you found.</p>'
             )
    add_task(topic_num='367',
             title='Piracy',
             description='<p>For this task, your job is to find '
                         'articles that discuss instances of piracy, '
                         'or the illegal boarding or taking control of a boat.</p>'
                         '<p>A RELEVANT document must describe  piracy on any body of water.</p>'
                         '<p>Documents discussing the legal taking of ships or their contents by a national authority are NOT RELEVANT.</p>  '
                         '<p>Clashes between fishing vessels over fishing are NOT RELEVANT, unless one vessel is boarded.</p>',
             diversify='<p> A RELEVANT AND DIFFERENT document should be RELEVANT and also mention NEW ships that were boarded.',
             concepts ='<p> Try to recall and list the different ships involved in the incidences that you found.</p>')

    add_task(topic_num='408',
             title='Tropical Storms',
             description='<p>For this task, your job is to find articles '
                        'about tropical storms (hurricanes and typhoons) that have caused significant property damage and loss of life.</p> '
                         '<p> A RELEVANT document must name the storm, the area and describe the extent of the damage/casulaties.'
                         '<p>Documents that describe the damage caused by a tropical storm as  '
                         ' "slight", "limited", or "small" are NOT RELEVANT.</p>',
             diversify='<p> A RELEVANT AND DIFFERENT document should be RELEVANT and also mention NEW tropical storms.</p>',
             concepts ='<p> Try to recall and list the tropical storms which caused damage that you found.</p>'
             )


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


def add_task(topic_num, title, description, diversify, concepts):
    t = TaskDescription.objects.get_or_create(topic_num=topic_num)[0]
    t.title = title
    t.description = description
    t.diversify = diversify
    t.concepts = concepts
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
