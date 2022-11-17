from django.db import models


# Create your models here.
class stu(models.Model):
    stu_id = models.CharField(max_length=30)
    stu_password = models.CharField(max_length=255)
    stu_name = models.CharField(max_length=255)
    depart = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(max_length=127, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    message = models.CharField(max_length=50, blank=True, null=True)


class teacher(models.Model):
    teacher_id = models.CharField(max_length=50)
    teacher_password = models.CharField(max_length=255)
    teacher_name = models.CharField(max_length=255)
    depart = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(max_length=127, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    message = models.CharField(max_length=50, blank=True, null=True)


class adm(models.Model):
    adm_id = models.CharField(max_length=60)
    adm_password = models.CharField(max_length=255)
    adm_name = models.CharField(max_length=255)
    depart = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(max_length=127, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    message = models.CharField(max_length=50, blank=True, null=True)


class course(models.Model):
    course_id = models.CharField(max_length=25)
    course_name = models.CharField(max_length=255)
    course_intro = models.CharField(max_length=520, blank=True, null=True)
    course_rate = models.IntegerField(blank=True, null=True, default=0)
    course_total = models.IntegerField(blank=True, null=True, default=0)
    course_capacity = models.IntegerField(default=0)


class material(models.Model):
    material_id = models.CharField(max_length=25)
    material_name = models.CharField(max_length=255)
    material_intro = models.CharField(max_length=255, blank=True, null=True)


class stu_course(models.Model):
    stu_id = models.CharField(max_length=255)
    course_id = models.CharField(max_length=25)


class teacher_course(models.Model):
    teacher_id = models.CharField(max_length=255)
    course_id = models.CharField(max_length=25)


class teacher_material(models.Model):
    teacher_id = models.CharField(max_length=50)
    material_id = models.CharField(max_length=25)


class course_material(models.Model):
    course_id = models.CharField(max_length=25)
    material_id = models.CharField(max_length=25)

