from django.db import models
from django.contrib.auth.models import User


class DocumentsExamined(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    docid = models.CharField(max_length=30)
    doc_num = models.CharField(max_length=30)
    judgement = models.IntegerField()
    judgement_date = models.DateTimeField('Date Examined')
    url = models.CharField(max_length=200)
    task = models.IntegerField(default=0)
    topic_num = models.IntegerField(default=0)

    def __unicode__(self):
        return self.docid

    def __str__(self):
        return "{} {}".format(self.docid, self.title)


class TaskDescription(models.Model):
    topic_num = models.IntegerField(default=0)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1500)
    diversify = models.CharField(max_length=1500, default="")
    concepts = models.CharField(max_length=700)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return "{} {}".format(self.topic_num,  self.title)


class TopicQuerySuggestion(models.Model):
    topic_num = models.IntegerField(default=0)
    title = models.CharField(max_length=40)
    link = models.CharField(max_length=150)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title


class TopicAds(models.Model):
    topic_num = models.IntegerField(default=0)
    title = models.CharField(max_length=40)
    url = models.CharField(max_length=150)
    shape = models.CharField(max_length=20)
    adimage = models.ImageField(blank=True, upload_to='ads/')
    on_topic = models.BooleanField(default=True)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    # This field is required.
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    # Other fields here
    data = models.CharField(max_length=200, null=True, blank=True)
    experiment = models.IntegerField(default=0)
    condition = models.IntegerField(default=0)
    rotation = models.IntegerField(default=0)
    tasks_completed = models.IntegerField(default=0)
    steps_completed = models.IntegerField(default=0)

    def __unicode__(self):
        return self.user.username

        # def create_user_profile(sender, instance, created, **kwargs):
        # if created:
        #        UserProfile.objects.create(user=instance)

        #post_save.connect(create_user_profile, sender=User)

    def __str__(self):
        return self.user.username

