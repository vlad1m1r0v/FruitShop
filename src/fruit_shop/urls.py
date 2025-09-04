from django.urls import path

from src.fruit_shop import views

app_name = 'app'

urlpatterns = [
    path('', views.PageView.as_view(), name='page'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('audit/', views.AuditView.as_view(), name='audit'),
    path('declaration/', views.DeclarationView.as_view(), name='declaration'),
    path('warehouse/', views.WarehouseView.as_view(), name='warehouse'),
    path('trade/', views.TradeView.as_view(), name='trade'),
    path('balance/', views.BalanceView.as_view(), name='balance'),
]
