from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from .views import ProductsViewSet, OrderItemViewSet, OrderViewSet

router = DefaultRouter()
router.register(r'dishes', ProductsViewSet)
router.register(r'order-items', OrderItemViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('<int:pk>/', views.order_detail, name='order_detail'),
    path('profit', views.get_profit, name='profit'),
    path('new/', views.order_create, name='order_create'),
    path('<int:pk>/edit/', views.order_update, name='order_update'),
    path('<int:pk>/delete/', views.order_delete, name='order_delete'),
    path('<int:pk>/add-item/', views.add_order_item, name='add_order_item'),
    path('/delete-item/<int:pk>', views.delete_order_item, name='delete_order_item'),
    path('api/', include(router.urls)),
]
