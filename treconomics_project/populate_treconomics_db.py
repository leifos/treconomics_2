import os
import django



def populate():
    print('Adding Task Descriptions')
    add_task(topic_num='341',
             title='Airport Security',
             description='<p>For this task, '
                         'your job is to find a number of articles '
                         'that discuss procedures taken by international '
                         'AIRPORTS, to better screen passengers '
                         'and their carry-on luggage.</p>'
                         '<p>Bookmark news articles which discuss specific AIRPORTS that describe security measures '
                         'that they have taken to better scrutinize passengers '
                         'and/or luggage on international flights.</p>',
             remember = '<p> You will be asked to recall these AIRPORTS, after you have finish searching.</p>',
             diversify='<p> A RELEVANT AND DIFFERENT document should mention NEW airports.</p>',
             concepts ='<p> Try to recall and list the AIRPORTS that were taking additional'
                       ' security measures, that you found.</p>'
             )
    add_task(topic_num='347',
             title='Wildlife Extinction',
             description='<p>For this task, your job is '
                         'to find a number of articles that discuss efforts '
                         'made by countries '
                         'to prevent the extinction of WILDLIFE SPECIES '
                         'native to their countries. </p>'
                         '<p>Bookmark news articles which discuss specific WILDLIFE '
                         'SPECIES where steps and efforts have been take to save and protect them.</p>',
             remember = '<p>You will be asked to recall these WILDLIFE SPECIES, after you have finish searching.</p>',
             diversify='<p> A RELEVANT AND DIFFERENT document should be RELEVANT and also mention NEW species.</p>',
             concepts ='<p> Try to recall and list the different WILDLIFE SPECIES which are being protected, that you found.</p>'
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
             remember = '',
             diversify='<p> A RELEVANT AND DIFFERENT document should be RELEVANT and also mention NEW journalists.</p>',
             concepts ='<p> Try to recall and list the journalists involved .</p>'
             )
    add_task(topic_num='435',
             title='Curbing Population Growth',
             description='<p>For this task, your job '
                         'is to find a number of articles that discuss COUNTRIES '
                         'that have been successful in curbing population '
                         'growth and the measures they have taken to do so.</p>',
             remember='<p> You will be asked to recall these COUNTRIES, after you have finish searching.</p>',
             diversify='<p> A RELEVANT AND DIFFERENT document should be RELEVANT and also mention NEW countries.</p>',
             concepts ='<p> Try to recall and list the different COUNTRIES trying to control population growth, that you found.</p>'
             )
    add_task(topic_num='367',
             title='Piracy',
             description='<p>For this task, your job is to find a number of '
                         'articles that discuss instances of piracy, '
                         'or the illegal boarding or taking control of a BOAT or SHIP.</p>'
                         '<p>Bookmark news articles that describe BOATS or SHIPS'
                         ' that have been subjected to piracy.</p>',
             remember = '<p>You will be asked to recall these BOATS and SHIPS, after you finish searching.</p>',
             diversify='<p> A RELEVANT AND DIFFERENT document should be RELEVANT and also mention NEW ships that were boarded.',
             concepts ='<p> Try to recall and list the different BOATS and SHIPS involved in these incidences, that you found.</p>')

    add_task(topic_num='408',
             title='Tropical Storms',
             description='<p>For this task, your job is to find a number of articles '
                        'about TROPICAL STORM (hurricanes and typhoons) that have caused significant property damage and loss of life.</p> '
                         '<p> Bookmark news articles that describe the TROPICAL STORM and the extent of the damage/casualties caused by it.</p>',
             remember='<p>You will be asked to recall these TROPICAL STORMS, after you finish searching</p> ',
             diversify='<p> A RELEVANT AND DIFFERENT document should be RELEVANT and also mention NEW tropical storms.</p>',
             concepts ='<p> Try to recall and list the TROPICAL STORMS which caused damage/casualties, that you found.</p>'
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


def add_task(topic_num, title, description, remember, diversify, concepts):
    t = TaskDescription.objects.get_or_create(topic_num=topic_num)[0]
    t.title = title
    t.description = description
    t.diversify = diversify
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
