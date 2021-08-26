from django.contrib import admin

from photologue.admin import GalleryAdmin as GalleryAdminDefault, PhotoAdmin, PhotoAdminForm
from photologue.models import Gallery, Photo
from .models import GalleryExtended, PhotoExtended2


class GalleryExtendedInline(admin.StackedInline):
    model = GalleryExtended
    can_delete = False


class GalleryAdmin(GalleryAdminDefault):

    """Define our new one-to-one model as an inline of Photologue's Gallery model."""

    inlines = [GalleryExtendedInline, ]

admin.site.unregister(Gallery)
admin.site.register(Gallery, GalleryAdmin)




class PhotoExtendedInline(admin.StackedInline):
    model = PhotoExtended2
    can_delete = False


class PhotoAdmin2(PhotoAdmin):

    """Define our new one-to-one model as an inline of Photologue's Gallery model."""

    inlines = [PhotoExtendedInline, ]

admin.site.unregister(Photo)
admin.site.register(Photo, PhotoAdmin2)
