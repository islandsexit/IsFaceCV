from django.db import models



# Create your models here.

# class FaceToken(models.Model):
#     # face_id_ch = models.CharField('idFace', help_text='Code', max_length=6, blank=False, default=None)
#     # face_name_ch = models.CharField('faceName', max_length=30, help_text='Name', blank=False, default=None)
#     # face_img = models.ImageField('faceImg', upload_to='images/',help_text='Загрузите фото')
#     face_token_ch = models.CharField('faceToken', max_length=6, help_text='Токен', blank=False,
#                                      default=None)
#     # face_token_valid_bol = models.BooleanField('face_valid', help_text='Токен действующий?', blank=False, default=None)
#     # face_group_ch = models.CharField('face_group', help_text='Организация', max_length=50, blank=False, default=None)
#     # face_worker_bol = models.BooleanField('face_worker', help_text='Постоянный работник?', blank=False, default=None)
#
#     def __str__(self):
#         return self.face_token_ch
#
#     # class Meta:
#     #     constraints = [
#     #         models.CheckConstraint(
#     #             check=models.Q(face_token_int__length__gte=6),
#     #             name="%(app_label)s_%(class)s_title_length",
#     #         )
#     #     ]


