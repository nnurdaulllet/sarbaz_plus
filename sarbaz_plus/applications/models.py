from django.db import models
from django.db.models import CASCADE
from registration.models import Person


class CatalogEmployment(models.Model):
    employment = models.CharField()

class NewsImg(models.Model):
    files = models.CharField()

class ApplicationDeferment(models.Model):
    file = models.FileField(upload_to='deferments/files/')
    application = models.ForeignKey('Applications', on_delete=models.CASCADE, related_name='application_deferment')

class ApplicationFiles(models.Model):
    file = models.FileField(upload_to='applications/files/')
    application = models.ForeignKey('Applications', on_delete=models.CASCADE, related_name='application_files')

class Applications(models.Model):
    user = models.ForeignKey('registration.Person', on_delete=models.CASCADE)
    catalog = models.ForeignKey('CatalogEmployment', on_delete=models.CASCADE)
    education_type = models.CharField(max_length=100)
    is_work_exp = models.BooleanField()
    work_describe = models.CharField(max_length=255, null=True)
    is_deferment = models.BooleanField()
    deferment = models.ManyToManyField('ApplicationDeferment', related_name='application_deferment')
    date_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, default='1')
    files = models.ManyToManyField('ApplicationFiles', related_name='applications_files', null=True)

    REQUIRED_FIELDS = ["user", "catalog", "education_type", 'is_work_exp', 'work_describe',
                       'deferment', 'date_time', 'status', "files"]

class News(models.Model):
    title = models.CharField(max_length=100)
    content = models.CharField()
    date_time = models.DateTimeField(auto_now_add=True)
    img = models.ForeignKey(NewsImg, on_delete=models.CASCADE)


class Questions(models.Model):
    title = models.CharField()
    content = models.CharField()
    user = models.ForeignKey(Person, on_delete=models.CASCADE)
    answer =  models.CharField()
    date_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField()