from django.db import models

# Create your models here.
class choiceData(models.Model):
    username = models.CharField(max_length=128)
    compType = models.CharField(max_length=128)
    matchupNames = models.CharField(max_length=5000)
    choices = models.CharField(max_length=5000)
    TTChoose = models.CharField(max_length=5000)
    CTime = models.CharField(max_length=1000)
    ip = models.CharField(max_length=128, default=0)
    familiarity = models.BooleanField()
    # userInfo = models.CharField(max_length=300, default=0)

    class Meta:
      verbose_name_plural = "Choice Data"
      
class userInfo(models.Model):
  username = models.CharField(max_length=128)
  number_test = models.BooleanField()
  secret_code = models.CharField(max_length=128, default=None)
  
  class Meta:
      verbose_name_plural = "User Info"