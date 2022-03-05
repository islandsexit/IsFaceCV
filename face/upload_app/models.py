from django.db import models


# Create your models here.

class Face(models.Model):
    face_id = models.CharField('idFace', help_text='Code',max_length=30)
    face_name = models.CharField('faceName', max_length=30, help_text='Name')
    face_img = models.ImageField('faceImg', upload_to='images/')

    def __str__(self):
        return self.face_name
