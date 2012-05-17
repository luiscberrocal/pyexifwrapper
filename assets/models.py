from django.db import models

# Create your models here.
class AssetFolder(models.Model):
    path = models.CharField(max_length = 512, unique = True)
    asset_count = models.IntegerField()
    last_scanned = models.DateTimeField()
    
class Asset(models.Model):
    filename = models.CharField(max_length=128)
    folder = models.ForeignKey(AssetFolder)
    file_date = models.DateTimeField()
    file_size = models.DecimalField(max_digits=8, decimal_places=2)