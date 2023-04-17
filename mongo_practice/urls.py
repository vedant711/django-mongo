from django.urls import path

from . import views

urlpatterns = [
    path('',views.index),
    path('dashboard',views.dashboard),
    path('create',views.create),
    path('logout',views.logout_usr),
    path('credit',views.credit),
    path('debit',views.debit),



    

]