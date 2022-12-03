from django.db import models


# Create your models here.
class stu(models.Model):
    stu_id = models.CharField(max_length=25, primary_key=True, unique=True)
    stu_password = models.CharField(max_length=255)
    stu_name = models.CharField(max_length=255)
    depart = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(max_length=127, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    message = models.CharField(max_length=50, blank=True, null=True)


class teacher(models.Model):
    teacher_id = models.CharField(max_length=25, primary_key=True, unique=True)
    teacher_password = models.CharField(max_length=255)
    teacher_name = models.CharField(max_length=255)
    depart = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(max_length=127, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    message = models.CharField(max_length=50, blank=True, null=True)


class adm(models.Model):
    adm_id = models.CharField(max_length=25, primary_key=True, unique=True)
    adm_password = models.CharField(max_length=255)
    adm_name = models.CharField(max_length=255)
    depart = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(max_length=127, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    message = models.CharField(max_length=50, blank=True, null=True)


class course(models.Model):
    course_id = models.CharField(max_length=25, primary_key=True, unique=True)
    course_name = models.CharField(max_length=255)
    course_intro = models.CharField(max_length=520, blank=True, null=True)
    course_rate = models.DecimalField(blank=True, null=True, default=0)
    course_total = models.IntegerField(blank=True, null=True, default=0)
    course_capacity = models.IntegerField(default=0)


class material(models.Model):
    material_id = models.CharField(max_length=25, primary_key=True, unique=True)
    material_name = models.CharField(max_length=255)
    material_intro = models.CharField(max_length=255, blank=True, null=True)


class comment(models.Model):
    comment_id = models.CharField(max_length=25, primary_key=True, unique=True)
    comment_content = models.CharField(max_length=255)
    comment_time = models.TimeField(auto_now_add=True, blank=True, null=True)


class themepost(models.Model):
    tp_id = models.CharField(primary_key=True, unique=True, max_length=25)
    tp_title = models.CharField(max_length=127)
    tp_content = models.CharField(max_length=512, blank=True, null=True)
    tp_time = models.TimeField(auto_now_add=True, blank=True, null=True)
    tp_isTeacher = models.BooleanField()


class followpost(models.Model):
    fp_id = models.CharField(primary_key=True, unique=True, max_length=25)
    fp_content = models.CharField(max_length=127)
    fp_time = models.TimeField(auto_now_add=True, blank=True, null=True)
    fp_isTeacher = models.BooleanField()


class stu_course(models.Model):
    stu_id = models.ForeignKey(stu, on_delete=models.CASCADE)
    course_id = models.ForeignKey(course, on_delete=models.CASCADE)


class teacher_course(models.Model):
    teacher_id = models.ForeignKey(teacher, on_delete=models.CASCADE)
    course_id = models.ForeignKey(course, on_delete=models.CASCADE)


class teacher_material(models.Model):
    teacher_id = models.ForeignKey(teacher, on_delete=models.CASCADE)
    material_id = models.ForeignKey(material, on_delete=models.CASCADE)


class course_material(models.Model):
    course_id = models.ForeignKey(course, on_delete=models.CASCADE)
    material_id = models.ForeignKey(material, on_delete=models.CASCADE)


class stu_comment(models.Model):
    stu_id = models.ForeignKey(stu, on_delete=models.CASCADE)
    comment_id = models.ForeignKey(comment, on_delete=models.CASCADE)


class course_comment(models.Model):
    course_id = models.ForeignKey(course, on_delete=models.CASCADE)
    comment_id = models.ForeignKey(comment, on_delete=models.CASCADE)


class tp_fp(models.Model):
    tp_id = models.ForeignKey(themepost, on_delete=models.CASCADE)
    fp_id = models.ForeignKey(followpost, on_delete=models.CASCADE)


class stu_tp(models.Model):
    stu_id = models.ForeignKey(stu, on_delete=models.CASCADE)
    tp_id = models.ForeignKey(themepost, on_delete=models.CASCADE)


class teacher_tp(models.Model):
    teacher_id = models.ForeignKey(teacher, on_delete=models.CASCADE)
    tp_id = models.ForeignKey(themepost, on_delete=models.CASCADE)


class adm_tp(models.Model):
    adm_id = models.ForeignKey(adm, on_delete=models.CASCADE)
    tp_id = models.ForeignKey(themepost, on_delete=models.CASCADE)


class stu_fp(models.Model):
    stu_id = models.ForeignKey(stu, on_delete=models.CASCADE)
    fp_id = models.ForeignKey(followpost, on_delete=models.CASCADE)


class teacher_fp(models.Model):
    teacher_id = models.ForeignKey(teacher, on_delete=models.CASCADE)
    fp_id = models.ForeignKey(followpost, on_delete=models.CASCADE)


class adm_fp(models.Model):
    adm_id = models.ForeignKey(adm, on_delete=models.CASCADE)
    fp_id = models.ForeignKey(followpost, on_delete=models.CASCADE)
