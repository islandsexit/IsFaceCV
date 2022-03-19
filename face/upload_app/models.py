# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Requests(models.Model):
    id = models.BigAutoField(primary_key=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    active = models.BooleanField(blank=True, null=True)
    active_from = models.DateField(blank=True, null=True)
    active_to = models.DateField(blank=True, null=True)
    checked = models.BooleanField(blank=True, null=True)
    deleted = models.BooleanField(blank=True, null=True)
    invite_code = models.IntegerField(blank=True, null=True)
    check_in = models.BooleanField(blank=True, null=True)
    photo_url = models.TextField(blank=True, null=True)
    sms_phone = models.CharField(max_length=50, blank=True, null=True)
    sms_sent = models.BooleanField(blank=True, null=True)
    sms_status = models.IntegerField(blank=True, null=True)
    sms_id = models.CharField(max_length=50, blank=True, null=True)
    is_sms = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'requests'


