from django.urls import path
from .views import RegisterView,LoginView,ShortenedUrlsCreating, GetUserData,GetallUserurls,Redirect,Logout


urlpatterns = [
    path('auth/registerUser/',RegisterView.as_view()),
    path('auth/loginUser/',LoginView.as_view()),
    path('auth/refresh/',GetUserData.as_view()),
    path('auth/logout',Logout.as_view()),


    path('url/creaturl/',ShortenedUrlsCreating.as_view()), 
    path('url/geturl/',GetallUserurls.as_view()),
    path('url/red/<str:pk>',Redirect.as_view())
]
