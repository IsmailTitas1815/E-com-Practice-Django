from django.urls import path
from App_Login import views

app_name = "App_Login"

urlpatterns = [
    path('login/', views.user_login, name="login"),
    path('signup/', views.user_signup, name="signup"),
    path('logout/', views.user_logout, name="logout"),
    path('profile/', views.user_profile, name="profile"),
]