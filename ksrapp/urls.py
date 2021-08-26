from ksrapp.views import GalleryListViewByKSR
from django.urls import path

appname = 'ksrapp'
urlpatterns = [
    path('gallerylist/', GalleryListViewByKSR.as_view(template_name="ksrapp/gallery_list.html"))]
    #path('gallerylist/', GalleryListViewByKSR.as_view(), name='gallery-list')]