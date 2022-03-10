# Generated by Django 4.0.3 on 2022-03-05 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload_app', '0003_face_face_name_alter_face_face_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='face',
            name='face_id',
            field=models.IntegerField(help_text='Code', verbose_name='idFace'),
        ),
        migrations.AlterField(
            model_name='face',
            name='face_img',
            field=models.ImageField(upload_to='images/', verbose_name='faceImg'),
        ),
        migrations.AlterField(
            model_name='face',
            name='face_name',
            field=models.CharField(help_text='Name', max_length=30, verbose_name='faceName'),
        ),
    ]