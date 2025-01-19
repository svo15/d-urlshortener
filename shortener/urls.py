from django.urls import path
from . import views

urlpatterns=[
    path('create/',views.posturls),
    path('red/<str:shorted>',views.Urlredirect,name='url-redirect'),
    path('getall/',views.getall)
]