import datetime
from django.db import models

class Poll(models.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date_published')
    poops = models.CharField(max_length=255)

    def was_published_today(self):
        return self.pub_date.date() == datetime.date.today
    was_published_today.short_description = "Published today?"

    def __unicode__(self):
        return self.question

class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __unicode__(self):
        return self.choice
