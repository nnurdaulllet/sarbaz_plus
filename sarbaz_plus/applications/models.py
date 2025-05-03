from django.db import models
from django.db.models import CASCADE
from registration.models import Person



class CatalogEmployment(models.Model):
    employment = models.CharField()


class ApplicationFiles(models.Model):
    files = models.CharField()

class ApplicationDeferment():
    files = models.CharField

class NewsImg(models.Model):
    files = models.CharField()

class Applications(models.Model):
    user = models.ForeignKey(Person, on_delete=models.CASCADE())
    catalog = models.ForeignKey(CatalogEmployment, on_delete=models.CASCADE())
    education_type = models.CharField()
    is_work_exp = models.BooleanField()
    work_describe = models.CharField()
    is_deferment = models.BooleanField()
    deferment = models.ForeignKey(ApplicationDeferment, on_delete=models.CASCADE())
    date_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10)
    files = models.ForeignKey(ApplicationFiles, on_delete=models.CASCADE())


class News(models.Model):
    title = models.CharField(max_length=100)
    content = models.CharField()
    date_time = models.DateTimeField(auto_now_add=True)
    img = models.ForeignKey(NewsImg, on_delete=models.CASCADE())


class Questions(models.Model):
    title = models.CharField()
    content = models.CharField()
    user = models.ForeignKey(Person, on_delete=models.CASCADE())
    answer =  models.CharField()
    date_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField()