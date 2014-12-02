from django.db import models

class Event(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    summary = models.CharField(max_length=200)
    start_date = models.DateTimeField('date start')
    end_date = models.DateTimeField('date end')

    def __unicode__(self):
        return "%s - %s | %s" % (self.id, self.summary, self.start_date)
