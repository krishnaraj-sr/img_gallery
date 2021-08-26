from django.shortcuts import render

# Create your views here.
from django.views.generic.dates import ArchiveIndexView, DateDetailView, DayArchiveView, MonthArchiveView, \
    YearArchiveView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from photologue.models import Photo, Gallery


# Gallery views.


class GalleryListViewByKSR(ListView):
    queryset = Gallery.objects.only('id')
    paginate_by = 50