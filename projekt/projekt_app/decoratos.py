from .models import Korisnik
from django.shortcuts import redirect

def mentor_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.role.role == Korisnik.MENTOR:#ako ulogirani korisnik ima odgovarajuću rolu pozove se funkcija koja je dekorirana
            return function(request, *args, **kwargs)
        else:
            return redirect('courses')
    return wrap
