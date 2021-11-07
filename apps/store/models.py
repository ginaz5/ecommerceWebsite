from django.db import models

# database model
class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255) # use id in urls
    ordering = models.IntegerField(default=0)

    # Customized 'Categorys' -> 'Categories'
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ('ordering',)
    
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
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_added',)

    def __str__(self):
        return self.title