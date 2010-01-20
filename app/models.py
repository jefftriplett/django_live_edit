from django.contrib.auth.models import User
from django.db import models


class Entry(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    public = models.BooleanField(default=True)

    def __unicode__(self):
        return u'%s' % self.body

    class Meta:
        verbose_name_plural = 'Entries'
