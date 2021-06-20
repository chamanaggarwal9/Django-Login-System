from django.urls import path
from . import views

urlpatterns = [
    path('reg/', views.User_Registration),
    path('activate/<token>', views.Confirm_Activation),
    path('login/', views.Login),
    path('forgot_password/', views.Forget_Password),
    path('reset_complete/<token>', views.Reset_Password),
]