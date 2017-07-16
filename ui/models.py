from django.db import models

# Create your models here.
class Network(models.Model):
    """Just a network with name and IPv4 network address."""
    
    name = models.CharField(max_length=128)
    address = models.CharField(max_length=17)

    def __str__(self):
        return '{} ({})'.format(self.name, self.address)
