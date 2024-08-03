from django.urls import path
from chatapp import views

urlpatterns=[
    path('inbox/',views.inbox, name='inbox'),
    path('<username>/', views.directs, name= 'directs'),
] 