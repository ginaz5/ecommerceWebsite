from django.db import models

# database model
class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255) # use id in urls

    # Customized 'Categorys' -> 'Categories'
    class Meta:
        verbose_name_plural = 'Categories'
    
    # to show title instead of object num in admin
    def __str__(self):
        return self.title

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE) 
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255) # use id in urls
    description = models.TextField(blank=True, null=True) # it could be empty
    price = models.FloatField()

    def __str__(self):
        return self.title