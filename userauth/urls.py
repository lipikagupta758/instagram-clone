from django.urls import path
from userauth import views

urlpatterns=[
    path('<username>/', views.userProfile, name= 'profile'),
    path('<username>/saved/', views.userProfile, name= 'saved'),
    path('<username>/follow/', views.follow, name= 'follow'),
    path('<username>/editprofile', views.editProfile, name= 'editProfile'),
] 