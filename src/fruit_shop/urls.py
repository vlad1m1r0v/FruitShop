from django.urls import path

from src.fruit_shop import views

app_name = 'app'

urlpatterns = [
        path('', views.PageView.as_view(), name='page'),
]