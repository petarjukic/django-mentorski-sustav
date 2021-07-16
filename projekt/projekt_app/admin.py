from django.contrib import admin
from .models import Korisnik, Predmet, Upisi

# Register your models here.

admin.site.register(Korisnik)
admin.site.register(Predmet)
admin.site.register(Upisi)
