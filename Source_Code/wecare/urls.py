"""falcon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from module import views

urlpatterns = [

    url(r'^$', views.login_view, name="login"),
    url(r'^admin/', admin.site.urls, name="admin"),
    url(r'^app_end', views.app_end, name="app_end"),
    url(r'^login/', views.login_view, name="login"),
    url(r'^logout/', views.logout_view, name="logout"),
    url(r'^doctors/(?P<id>\d+)', views.patient_file, name="OpenApp"),
    url(r'^xx', views.xx, name="xx"),
    url(r'^doctors/', views.doctors, name="doctors"),
    url(r'^receptionist/', views.receptionist, name=""),
    url(r'^receptionist_dev/', views.receptionist_dev, name="receptionist"),
    url(r'^receptionist_his/', views.receptionist_appointment_history, name="receptionist_his"),
    url(r'^receptionist_arc/', views.receptionist_appointment_history_archive, name="receptionist_arc"),
    url(r'^cancle_appointment/', views.cancle_appointment, name="cancle_appointment"),
    # url(r'^1/', views.manufacturer_detail_view, name="1"),
    url(r'^pharmacy/search', views.search_medicine, name="spharmacy"),
    url(r'^pharmacy/', views.pharmacy, name="pharmacy"),
    url(r'^reset', views.PasswordReset, name="reset"),
    url(r'^rw', views.endapp, name="rw"),
    url(r'^search', views.search_patient, name="register"),
    url(r'^register_patient', views.register_patient, name="register_patient"),
    url(r'^register', views.test2, name="register"),
    url(r'^que', views.doctor_dashboard_que, name="que"),
    url(r'^bookapp', views.book_appointment, name="bookapp"),
    url(r'^slots', views.search_slot, name="slots"),
    url(r'^finalbook', views.final_book, name="finalbook"),
    url(r'^xpharma/', include('pharmacy.urls'), name="xpharma"),
    url(r'^patient/', include('patient.urls'), name="patient"),

    url(r'^(?P<id>\d+)/edit', views.edit_appointment, name=""),
    url(r'^(?P<id>\d+)/cancel', views.cancle_appointment, name=""),
    url(r'^(?P<id>\d+)', views.View_appointment, name="s"),

]
