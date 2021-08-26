from django.db import models

from taggit.managers import TaggableManager
from django.utils.translation import gettext_lazy as _
from photologue.models import Gallery
from photologue.models import Photo



class GalleryExtended(models.Model):

    # Link back to Photologue's Gallery model.
    gallery = models.OneToOneField(Gallery, related_name='extended',on_delete =models.CASCADE)


    # This is the important bit - where we add in the tags.
    tags = TaggableManager(blank=True)

    # Boilerplate code to make a prettier display in the admin interface.
    class Meta:
        verbose_name = u'Extra fields'
        verbose_name_plural = u'Extra fields'

    def __str__(self):
        return self.gallery.title

class PhotoExtended2(models.Model):

    # Link back to Photologue's Gallery model.
    photo = models.OneToOneField(Photo, related_name='extended',on_delete =models.CASCADE)
    # This is the important bit - where we add in the tags.
    photo_tags = TaggableManager(blank=True)
    # Extra field for captions
    captiona = models.TextField(_('Caption1'),blank=True,null=True)
    captionb = models.TextField(_('Caption2'),blank=True,null=True)


    # Boilerplate code to make a prettier display in the admin interface.
    class Meta:
        verbose_name = u'Extra fields'
        verbose_name_plural = u'Captions and Tags'

    def __str__(self):
        return self.photo.title