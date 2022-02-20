from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('bag', views.BagView.as_view(), name='summary'),
    path('', views.ProductListView.as_view(), name='products'),
    path('<slug>/', views.ProductDetailView.as_view(), name='product-detail')
]