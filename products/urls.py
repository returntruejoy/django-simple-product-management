from django.urls import path

from . import views

app_name = 'products'

urlpatterns = [
    path('', views.draft_upload, name='draft_upload'),
    path('approved/', views.approved_products, name='approved_products'),
    path('approve/<int:product_id>/', views.approve_product, name='approve_product'),
]
