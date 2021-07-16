"""projekt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.contrib.auth.views import LoginView
from projekt_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home_page, name='home'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    
    path('logout/', views.logout_view, name='logout'),
    path('courses/', views.courses, name='courses'),
    path('all_students/', views.all_students, name='all_students'),
    
    path('register/', views.register, name='register'),
    path('insert_course/', views.insert_course, name='insert_course'),
    path('detail_course/<str:course_id>', views.course_detail, name='detail_course'),
    
    path('edit_course/<str:course_id>', views.edit_course, name='edit_course'),
    path('upisni_list/<int:student_id>', views.upisni_list, name='upisni_list'),
    path('ispis_predmeta/<int:predmet_id>/<int:student_id>', views.ispis_predmeta, name='ispis_predmeta'),

    path('upis_predmeta/<int:predmet_id>/<int:student_id>', views.upis_predmeta, name='upis_predmeta'),
    path('polozio_predmet/<int:predmet_id>/<int:student_id>', views.polozio_predmet, name='polozio_predmet'),
    path('delete_course/<int:course_id>', views.delete_course, name='delete_course'),
]
