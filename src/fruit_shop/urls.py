from django.urls import path

from src.fruit_shop import views

app_name = 'app'

urlpatterns = [
    path('', views.PageView.as_view(), name='page'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]
