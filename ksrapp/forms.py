#%%
import ast
import logging

import pandas as pd
from tqdm import tqdm as tqdm
from django import forms
from django.contrib.sites.models import Site
from django.core.files.base import ContentFile
from django.template.defaultfilters import slugify
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _
from photologue.models import Gallery, Photo
from django.db.models import prefetch_related_objects
from ksrapp.models import GalleryExtended, PhotoExtended2

logger = logging.getLogger('photologue.forms')

current_site = Site.objects.get_current()

#exec(open('ksrapp/forms.py').read())
class UploadZipForm():

    def write_one_file(self, filename, gallery, image_data):
        image = open(filename, 'rb')
        data = image.read()

        photo_title = image_data['title']
        slug = slugify(photo_title)
        photo = Photo(title=photo_title,
                      slug=slug,
                      caption=image_data['caption'],
                      is_public=image_data['is_public'])

        # Basic check that we have a valid image.
        contentfile = ContentFile(data)
        photo.image.save(filename, contentfile)
        photo.save()
        photo.sites.add(current_site)
        gallery.photos.add(photo)
        #photo.refresh_from_db()
        photo_extended = PhotoExtended2()
        photo_extended.photo = photo
        photo_extended.captiona = str(image_data['caption1'])
        photo_extended.captionb = str(image_data['caption2'])
        photo_extended.save()
        photo_extended.photo_tags.add(*image_data['tags'])
        photo_extended.save()
        
        

    def verify_title(title):
        if title and Gallery.objects.filter(title=title).exists():
            raise forms.ValidationError(
                _('A gallery with that title already exists.'))

    def create_gallery_write_files(self, df, gallery_data):
        #gallery_data['title']
        #gallery_data['description']
        #gallery_data['is_public']
        gallery = self.create_gallery(self,gallery_data)
    

        #TODO
        image_data = {}
        df = df.drop_duplicates(['title'])
        for index, row in tqdm(df.iterrows()):
            image_data['title'] = str(row['title'])
            captions = ast.literal_eval(row['captions'])
            captions = '.<br>'.join(captions)
            image_data['caption'] = captions
            image_data['is_public'] = True
            image_data['tags'] = ast.literal_eval(row['combined_predicates'])
            image_data['caption1']="Cap1"
            image_data['caption2']= "Cap2"
            filename = row['path']
            self.write_one_file(filename, gallery, image_data)
        print('Done')

    def create_gallery(self,gallery_data):
        gallery_title= gallery_data['title']
        slug = slugify(gallery_title)
        count=0
        
        if Gallery.objects.filter(slug=slug).exists():
            
            while True:
                                
                    gallery_title = str(gallery_title)+'_', str(count)
                    slug = slugify(gallery_title)
                    gallery_title = slug
                    if Gallery.objects.filter(slug=slug).exists():
                        count += 1
                        continue
                    break
        
       
        gallery = Gallery.objects.create(title=gallery_data['title'],
                                         slug=slug,
                                         description=gallery_data['description'],
                                         is_public=gallery_data['is_public'])
        gallery.sites.add(current_site)
        return gallery
    
    def add_photo_to_gallery(self,title,gallery):
        photo = Photo.objects.get(title=title)
        gallery.photos.add(photo)
        
  
     
#%%

# %%
kp = UploadZipForm()
import pickle
print('here')
with open('ksrapp/static/gallery_file_association.pkl','rb' ) as file:
    gallery_to_file = pickle.load(file)
print('here2')
k = 0
photos = Photo.objects.all()
prefetch_related_objects(photos)
for key ,val in tqdm(gallery_to_file.items()):
    if key == r"player's" :
        #key = 'kites_2'        
        k=1
         
    if k==1:
        gallery_data = {}
        gallery_data['title'] = key
        gallery_data['description'] = f'Contains images with {key}'
        gallery_data['is_public'] = True
        gallery = kp.create_gallery(gallery_data)
        for phot in photos.filter(title__in=val):
            gallery.photos.add(phot)
        # for image in val:
        #     gallery.photos.add(photos.filter(title=image).get())
        #     gallery.photos.add(photos.filter(title__in=val).get())
        


'''

df = pd.read_csv('ksrapp/static/gallery_test.csv')
kp=UploadZipForm()
gallery_data = {}
gallery_data['title'] = 'All images'
gallery_data['description'] = 'Testing with all images '
gallery_data['is_public'] = True
kp.create_gallery_write_files(df,gallery_data)






gallery = Gallery.objects.create(title=gallery_data['title'],
                                 slug=slugify(gallery_data['title']),
                                 description=gallery_data['description'],
                                 is_public=gallery_data['is_public'])
gallery.sites.add(current_site)
image_data = {}
image_data['title'] = 'wrassawewewew'
image_data['caption'] = 'image_captions'
image_data['is_public'] = True
image_data['tags'] = ['mouse', 'dog', 'cat']
print('here')
file = 'ksrapp/static/resizedImages/2.jpg'
kp = UploadZipForm()
kp.write_one_file(file, gallery, image_data)

print('Done')
'''

# %%
