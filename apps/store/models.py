from io import BytesIO # built-in packages
from django.core.files import File # to deal with files
from PIL import Image
from django.db import models


# database model
class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255) # use id in urls
    ordering = models.IntegerField(default=0)

    # Customized 'Categorys' -> 'Categories'
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ('ordering',) # it must be a tuple or list, so comma is necessary
    
    # to show title instead of object num in admin
    def __str__(self):
        return self.title

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE) 
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255) # use id in urls
    description = models.TextField(blank=True, null=True) # it could be empty
    price = models.FloatField()
    is_featured = models.BooleanField(default=False)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/',blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_added',)

    def __str__(self):
        return self.title
    
    # overwirte default save function
    # when upload image and run save in admin, this function will be called
    # set thumnail of Product that generated from function make_thumbnail
    def save(self, *args, **kwargs):
        print('Save', self.image.path)
        self.thumbnail = self.make_thumnail(self.image)
        super().save(*args, **kwargs)

    def make_thumnail(self, image, size=(200, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size, Image.ANTIALIAS) # add filter

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)
        
        thumbnail = File(thumb_io, name=image.name)

        return thumbnail