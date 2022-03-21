from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Connection_Spec(models.Model):

    MODE_CHOICES = (
        ('EXISTS', 'exists'),
        ('NOT_EQUAL', 'not_equal')
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    
    name = models.CharField(max_length=60)
    url = models.CharField(max_length=150)
    seq = models.CharField(max_length=60)
    interval_seconds = models.IntegerField(default=600, validators=[
            MaxValueValidator(100000),
            MinValueValidator(15)
        ])
    title = models.CharField(max_length=100, default="It's already there!")
    msg = models.CharField(max_length=100, default="Element found.")
    eta = models.CharField(max_length=100, default=None, null=True, blank=True)
    rand = models.FloatField(default=0, validators=[
            MaxValueValidator(0.8),
            MinValueValidator(0)
        ])
    mode = models.CharField(max_length=100, choices=MODE_CHOICES, default='EXISTS')
    username = models.CharField(max_length=100, default=None, null=True, blank=True)
    password = models.CharField(max_length=100, default=None, null=True, blank=True)
    max_cycles = models.IntegerField(default=10, validators=[
            MaxValueValidator(300),
            MinValueValidator(1)
        ])


    def __str__(self):
        return self.name
    

    def get_absolute_url(self):
        # redirect user to specific url whenever an item is created
        # ImproperlyConfigured at /add/
        # No URL to redirect to.  Either provide a url or define a get_absolute_url method on the Model.
        return reverse('core:home')
    

    @property
    def short_url(self):
        return '/'.join(self.url.split('/')[2:5])