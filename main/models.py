from django.db import models
from django.urls import reverse_lazy


class Category(models.Model):
    slug = models.SlugField(max_length=80, primary_key=True)
    name = models.CharField(max_length=80, unique=True)

    def __str__(self):
        return self.name


class Destination(models.Model):
    name = models.CharField(max_length=40)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT, related_name='destinations')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('destination-details', args=(self.id, ))


class DestinationImage(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='destinations')


