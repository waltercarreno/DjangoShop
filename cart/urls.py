from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('bag', views.BagView.as_view(), name='bag'),
    path('', views.ProductListView.as_view(), name='products'),
    path('<slug>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('increase/<pk>/',
         views.IncreaseProductView.as_view(), name='increase-product'),
    path('decrease/<pk>/',
         views.DecreaseProductView.as_view(), name='decrease-product'),
    path('remove/<pk>/',
         views.RemoveProductView.as_view(), name='remove-product'),
]