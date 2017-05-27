from django.db import models
from django.contrib.auth.models import User


class Nomination(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=1000, null=True, blank=True)
    results_declared = models.BooleanField(default=False)
    nomi_form=models.ForeignKey('forms.Questionnaire',null=True,blank=True)


    def __str__(self):
        return self.name


class NominationInstance(models.Model):
    STATUS = (
        ('a', 'Accepted'),
        ('r', 'Rejected'),
    )

    nomination = models.ForeignKey('Nomination', on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=1, choices=STATUS,  null=True, blank=True, default=None)

    def __str__(self):
        return str(self.user) + ' ' + str(self.id)


class UserProfile(models.Model):
    PROGRAMME = (
        ('B.Tech', 'B.Tech'),
        ('B.S', 'B.S'),
    )

    DEPT = (
        ('Aerospace Engineering', 'AE'),
        ('Biological Sciences & Engineering', 'BSBE'),
        ('Chemical Engineering', 'CHE'),
        ('Civil Engineering', 'CE'),
        ('Computer Science & Engineering', 'CSE'),
        ('Electrical Engineering', 'EE'),
        ('Materials Science & Engineering', 'MSE'),
        ('Mechanical Engineering', 'ME'),
        ('Industrial & Management Engineering', 'IME'),
        ('Chemistry', 'CHM'),
        ('Mathematics & Scientific Computing', 'MTH'),
        ('Physics', 'PHY'),
        ('Earth Sciences', 'ES')
    )

    YEAR = (
        ('Y16', 'Y16'),
        ('Y15', 'Y15'),
        ('Y14', 'Y14'),
        ('Y13', 'Y13'),
        ('Y12', 'Y12'),
        ('Y11', 'Y11'),
    )

    HALL = (
        (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'),
        (7, '7'), (8, '8'), (9, '9'), (10, '10'), (11, '11'), (12, '12'),
    )

    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=40, default=user)
    roll_no = models.IntegerField(null=True)
    year = models.CharField(max_length=4, choices=YEAR, default='Y16')
    programme = models.CharField(max_length=7, choices=PROGRAMME, default='B.Tech')
    department = models.CharField(max_length=200, choices=DEPT, default=None)
    hall = models.IntegerField(choices=HALL, default=1)
    room_no = models.CharField(max_length=10, null=True)

    def __str__(self):
        return str(self.name)


class Post(models.Model):
    post_name=models.CharField(max_length=500,null=True)
    parent=models.ForeignKey('self' ,on_delete=models.CASCADE)
    persons=models.ManyToManyField(User,blank=True)
    nomination=models.OneToOneField(Nomination,null=True,blank=True)



