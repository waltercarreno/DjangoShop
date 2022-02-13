from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='products'),
    path('<slug>/', views.ProductDetailView.as_view(), name='product-detail')
]