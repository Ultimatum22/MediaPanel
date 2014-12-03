from django.db import models


class BackgroundImage(models.Model):
    path = models.CharField(max_length=255, primary_key=True)
    taken_by = models.CharField(max_length=255, blank=True, null=True)
    album = models.CharField(max_length=255)
    date_taken = models.DateTimeField()

    def __unicode__(self):
        return "%s" % self.path
