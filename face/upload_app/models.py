from django.db import models


# Create your models here.

class Face(models.Model):
    face_id = models.IntegerField()
    face_img = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.face_id
