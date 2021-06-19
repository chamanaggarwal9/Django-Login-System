from django.urls import path
from . import views

urlpatterns = [
    path('reg/', views.Registration),
    path('activate/<token>', views.Confirm_Activation),
    path('login/', views.Login),
]