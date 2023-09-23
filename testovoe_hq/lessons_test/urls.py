from django.urls import path
from . import views

urlpatterns = [
    path('lessons/', views.get_lessons_by_user, name='lessons-by-user'),
    path('lessons/product/<int:product_id>/', views.get_lessons_by_product, name='lessons-by-product'),
    path('product/statistics/', views.get_product_statistics, name='product-statistics'),
]