from django.db import models

class ClassList(models.Model):
    class_name = models.CharField(max_length=25)
    instructor = models.CharField(max_length=25)
    total_slots = models.IntegerField()
    available_slots = models.IntegerField()
    date = models.DateTimeField()

    def __str__(self):
        return self.class_name
        

class Client(models.Model):
    client = models.CharField(max_length=25)
    email = models.EmailField(unique=True)
    enrolled_classes = models.ManyToManyField(ClassList,related_name='clients')

    def __str__(self):
        return self.client