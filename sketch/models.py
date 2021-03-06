from django.db import models
import datetime
import random

class RandomIDField(models.CharField):
    def __init__(self, verbose_name=None, name=None, auto=False, **kwargs):
        self.auto = auto
        kwargs['max_length'] = 10
        if auto:
            kwargs['editable'] = False
            kwargs['blank'] = False
        models.CharField.__init__(self, verbose_name, name, **kwargs)

    #def get_internal_type(self):
    #  return models.CharField.__name__

    def _get_random_key(self):
        alphabet = "abcdefghijklmnopqrstuvwxyz123456789"
        rndstr = "".join([x for x in random.sample(alphabet, 5)])
        while Sketch.objects.filter(pk=rndstr):
            rndstr = "".join([x for x in random.sample(alphabet, 5)])

        return rndstr

    def pre_save(self, model_instance, add):
        value = super(RandomIDField, self).pre_save(model_instance, add)
        if (not value) and self.auto:
            value = self._get_random_key()
            setattr(model_instance, self.attname, value)
        return value


class Sketch(models.Model):

    key = RandomIDField(primary_key=True, auto=True)
    image = models.ImageField(upload_to="drawings/")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Creation time")

    def __unicode__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return "/%s/" % self.pk

    def thumbnail(self):
        ratio = 0.2
        if self.image:
            return '<img src="%s" width="%s" height="%s" />' % (self.image.url, ratio * self.image.width, ratio * self.image.height)
        else:
            return ""
    thumbnail.allow_tags = True

    class Meta:
        verbose_name_plural = "sketches"

    def delete(self, *args, **kwargs):
        if self.image:
            self.image.delete()
        super(Sketch, self).delete(*args, **kwargs)

    def humanize_timediff(self):
        delta = datetime.datetime.now() - self.created

        if delta.days > 6:
            human_date = self.created.strftime("%e.%m.%Y %R")
        elif delta.days >= 2:
            human_date = self.created.strftime("last %A at %R").lower()
        elif delta.days == 1:
            human_date = self.created.strftime("yesterday at %R")
        elif delta.seconds > 7200:
            human_date = str(delta.seconds / 3600) + " hours ago"
        elif delta.seconds > 120:
            human_date = str(delta.seconds / 60) + " minutes ago"
        else:
            human_date = "a few seconds ago"

        return human_date
