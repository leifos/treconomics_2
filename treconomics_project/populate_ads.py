import os
import django



def populate():
    afile = open('data/imgs/ad_list.csv','r')
    while afile:
        line = afile.readline()
        if not line.strip():
            break

        (img_file, topic, shape, title, url) = line.split(',')
        print(topic, title)
        add_ad(topic, title, shape, url, img_file)



def add_ad(topic_num, title, shape, url, filename):
    ad = TopicAds.objects.get_or_create(topic_num=topic_num,
                                              title=title)[0]

    ad.url = url
    ad.shape = shape
    img_path = os.path.join(os.getcwd(), 'data/imgs/', filename)
    f = File(open(img_path,'rb'))
    ad.adimage.save(filename, f)
    ad.save()
    print("\t %s" % ad)
    return ad


#    adimage



if __name__ == '__main__':
    print("Starting Treconomics population script...")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'treconomics_project.settings')
    django.setup()
    from treconomics.models import TopicAds
    from treconomics.models import UserProfile
    from django.contrib.auth.models import User
    from django.core.files import File

    populate()
