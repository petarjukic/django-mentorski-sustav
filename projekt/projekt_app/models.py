from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Korisnik(AbstractUser):
    MENTOR = 'MENTOR'
    STUDENT = 'STUDENT'
    ROLES = (
        (MENTOR,'Mentor'), 
        (STUDENT,'Student'),
    )

    NONE = 'NONE'
    REDOVNI = 'REDOVNI'
    IZVANREDNI = 'IZVANREDNI'
    STATUS = (
        (NONE,'None'),
        (REDOVNI, 'Redovni'),
        (IZVANREDNI, 'Izvanredni'),
    )
    role = models.CharField(max_length=16, choices=ROLES, default=STUDENT)
    status = models.CharField(max_length=20, choices=STATUS, default=NONE)

    def __str__(self):
        return ('%s %s') % (self.role, self.status)


class Predmet(models.Model):
    ime = models.CharField(max_length=255)
    kod = models.CharField(max_length=16)
    program = models.TextField(null=False)
    bodovi = models.PositiveIntegerField(null=False)
    sem_redovni = models.PositiveIntegerField(null=False)
    sem_izvanredni = models.PositiveIntegerField(null=False)
    izborni_enum = (('da','da'), ('ne','ne'))
    izborni = models.CharField(max_length=50, choices=izborni_enum)

    def __str__(self):
        return self.ime


class Upisi(models.Model):
    student_id = models.ForeignKey(Korisnik, on_delete=models.CASCADE)
    predmet_id = models.ForeignKey(Predmet, on_delete=models.CASCADE)
    status = models.CharField(max_length=64)

    def __str__(self):
        return self.status

